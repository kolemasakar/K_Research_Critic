"""Explicitly constructed synthetic/staging adapter; no automatic startup."""
import json
import socket
import struct
from .stage135_prepared_read import Denied, digest
from .stage131_signed_artifact_uds import SignedArtifactUDSServer, SignedArtifactUDSHandler

PATH = "/v1/requests/prepared/read"

class Handler(SignedArtifactUDSHandler):
    def do_POST(self):
        if not self.server.reader.enabled or self.path != PATH:
            return self.respond(404,{"error":"NOT_FOUND"})
        if self.headers.get_all("Content-Type",[]) != ["application/json"]:
            return self.respond(415,{"error":"UNSUPPORTED_MEDIA_TYPE"})
        lengths = self.headers.get_all("Content-Length",[])
        if self.headers.get_all("Transfer-Encoding",[]) or len(lengths)!=1 or not lengths[0].isascii() or not lengths[0].isdecimal():
            return self.respond(400,{"error":"INVALID_REQUEST"})
        try:
            n = int(lengths[0])
        except ValueError:
            return self.respond(400,{"error":"INVALID_REQUEST"})
        if not 0<n<=4096:
            return self.respond(413,{"error":"REQUEST_TOO_LARGE"})
        try:
            raw = self.rfile.read(n)
            if len(raw)!=n or self.rfile.read(1)!=b"":
                return self.respond(400,{"error":"INVALID_REQUEST"})
            if self._deadline_expired.is_set():
                return self.respond(408,{"error":"REQUEST_TIMEOUT"})
        except (TimeoutError,OSError):
            return self.respond(408,{"error":"REQUEST_TIMEOUT"})
        try:
            uid = struct.unpack("3i",self.connection.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))[1]
        except (OSError,struct.error):
            return self.respond(403,{"error":"FORBIDDEN"})
        try:
            body = self.server.reader.read(raw,peer_uid=uid)
        except Denied as e:
            return self.respond(e.status,{"error":e.code})
        except Exception:
            return self.respond(503,{"error":"BACKEND_UNAVAILABLE"})
        if self._deadline_expired.is_set():
            return self.respond(408,{"error":"REQUEST_TIMEOUT"})
        self.send_response(200)
        for k,v in (("Content-Type","application/octet-stream"),("Content-Length",str(len(body))),("X-Content-SHA256",digest(body)),("Cache-Control","no-store"),("X-Content-Type-Options","nosniff"),("Connection","close")):
            self.send_header(k,v)
        self.end_headers()
        self.close_connection=True
        self.wfile.write(body)

    def do_GET(self):
        return self.respond(405,{"error":"METHOD_NOT_ALLOWED"})

class PreparedServer(SignedArtifactUDSServer):
    def __init__(self,path,*,reader):
        import socketserver
        import threading
        self.reader=reader
        self._worker_slots=threading.BoundedSemaphore(self.max_active_workers)
        socketserver.UnixStreamServer.__init__(self,str(path),Handler)
