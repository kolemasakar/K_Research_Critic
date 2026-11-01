"""Isolated disabled-by-default UDS HTTP server for signed Artifact GET. Never auto-start."""
import json, os, socket, socketserver, struct, threading
from http.server import BaseHTTPRequestHandler

class SignedArtifactUDSServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads=True
    block_on_close=False
    request_queue_size=16
    max_active_workers=4
    request_deadline_seconds=20
    def process_request(self, request, client_address):
        # Acquire before creating a worker thread: slow clients cannot exhaust threads.
        if not self._worker_slots.acquire(blocking=False):
            try:
                request.sendall(
                    b"HTTP/1.1 503 Service Unavailable\r\n"
                    b"Content-Length: 0\r\nConnection: close\r\n\r\n"
                )
            except OSError:
                pass
            finally:
                self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except BaseException:
            self._worker_slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._worker_slots.release()
    def __init__(self,path,*,boundary):
        self.boundary=boundary
        self._worker_slots=threading.BoundedSemaphore(self.max_active_workers)
        super().__init__(str(path),SignedArtifactUDSHandler)

class SignedArtifactUDSHandler(BaseHTTPRequestHandler):
    protocol_version="HTTP/1.1"
    def log_message(self,*args):pass
    def setup(self):
        super().setup()
        self.connection.settimeout(5)
        # Absolute cap, independent of byte-by-byte socket activity.
        # Timer is cancelled when the handler finishes, including error paths.
        self._deadline_timer=threading.Timer(
            self.server.request_deadline_seconds, self._expire_connection
        )
        self._deadline_timer.daemon=True
        self._deadline_timer.start()

    def _expire_connection(self):
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

    def finish(self):
        try:
            super().finish()
        finally:
            timer=getattr(self,"_deadline_timer",None)
            if timer is not None:
                timer.cancel()
    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (TimeoutError, socket.timeout, ConnectionError, OSError):
            self.close_connection=True
    def respond(self,status,body):
        data=json.dumps(body,separators=(",",":"),ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(data)))
        self.send_header("Cache-Control","no-store")
        self.send_header("Connection","close")
        self.end_headers()
        self.wfile.write(data)
        self.close_connection=True
    def do_POST(self):
        if self.path!="/v1/artifacts/read":return self.respond(404,{"error":"NOT_FOUND"})
        if self.headers.get("Content-Type")!="application/json":return self.respond(415,{"error":"UNSUPPORTED_MEDIA_TYPE"})
        lengths=self.headers.get_all("Content-Length",[])
        if self.headers.get_all("Transfer-Encoding",[]) or len(lengths)!=1:
            return self.respond(400,{"error":"INVALID_REQUEST"})
        raw_length=lengths[0]
        if not raw_length.isascii() or not raw_length.isdecimal():
            return self.respond(400,{"error":"INVALID_REQUEST"})
        try:n=int(raw_length)
        except ValueError:n=-1
        if n<1 or n>262144:return self.respond(413,{"error":"REQUEST_TOO_LARGE"})
        try:
            body=self.rfile.read(n)
            if len(body)!=n:
                return self.respond(400,{"error":"INVALID_REQUEST"})
            message=json.loads(body)
            if not isinstance(message,dict):
                return self.respond(400,{"error":"INVALID_REQUEST"})
            # Source-only UDS retrieval requires a write-half-close from the peer.
            # Never dispatch until EOF is observed after the declared body:
            # late/undeclared bytes fail closed, not merely bytes already buffered.
            # The absolute connection deadline closes peers withholding EOF.
            if self.rfile.read(1) != b"":
                return self.respond(400,{"error":"INVALID_REQUEST"})
        except (ValueError, UnicodeDecodeError, OSError):
            return self.respond(400,{"error":"INVALID_REQUEST"})
        try: uid=struct.unpack("3i",self.connection.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))[1]
        except (OSError,struct.error):return self.respond(403,{"error":"FORBIDDEN"})
        try:
            outcome=self.server.boundary.execute(message,peer_uid=uid)
        except Exception:
            return self.respond(503,{"error":"BACKEND_UNAVAILABLE"})
        if outcome["http_status"]!=200:
            return self.respond(outcome["http_status"],outcome["body"])
        f=outcome.get("body_file")
        try:
            self.send_response(200)
            self.send_header("Content-Type","application/octet-stream")
            self.send_header("Content-Length",str(outcome["size_bytes"]))
            self.send_header("X-Content-SHA256",outcome["sha256"])
            self.send_header("Cache-Control","no-store")
            self.send_header("Connection","close")
            self.end_headers()
            if f is None:self.wfile.write(outcome["body_bytes"])
            else:
                while True:
                    chunk=f.read(256*1024)
                    if not chunk:break
                    self.wfile.write(chunk)
        except (BrokenPipeError,ConnectionResetError,OSError):
            pass
        finally:
            if f is not None:f.close()
            self.close_connection=True
    def do_GET(self):
        return self.respond(404,{"error":"NOT_FOUND"})
