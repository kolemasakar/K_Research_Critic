"""Isolated disabled-by-default UDS HTTP server for signed Artifact GET. Never auto-start."""
import json, os, socket, socketserver, struct
from http.server import BaseHTTPRequestHandler

class SignedArtifactUDSServer(socketserver.UnixStreamServer):
    def __init__(self,path,*,boundary):
        self.boundary=boundary
        super().__init__(str(path),SignedArtifactUDSHandler)

class SignedArtifactUDSHandler(BaseHTTPRequestHandler):
    protocol_version="HTTP/1.1"
    def log_message(self,*args):pass
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
        try:n=int(self.headers.get("Content-Length","-1"))
        except ValueError:n=-1
        if n<1 or n>262144:return self.respond(413,{"error":"REQUEST_TOO_LARGE"})
        try: message=json.loads(self.rfile.read(n))
        except (ValueError,UnicodeDecodeError):return self.respond(400,{"error":"INVALID_REQUEST"})
        try: uid=struct.unpack("3i",self.connection.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))[1]
        except (OSError,struct.error):return self.respond(403,{"error":"FORBIDDEN"})
        outcome=self.server.boundary.execute(message,peer_uid=uid)
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
