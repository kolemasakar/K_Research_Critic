"""Stage121 staging-only UDS HTTP bridge; peer UID is authoritative."""
import json, socket, socketserver, struct
from http.server import BaseHTTPRequestHandler
from .staging_backend114 import OPS

class UDSHTTPServer(socketserver.UnixStreamServer):
    def __init__(self,path,*,boundary,allowed_uids):
        self.boundary=boundary
        self.allowed_uids=frozenset(allowed_uids)
        if not self.allowed_uids: raise ValueError("Empty peer allowlist")
        super().__init__(path,UDSHandler)

class UDSHandler(BaseHTTPRequestHandler):
    protocol_version="HTTP/1.1"
    def log_message(self,*args): pass
    def _peer(self):
        return struct.unpack("3i",self.connection.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))[1]
    def _send(self,status,obj):
        raw=json.dumps(obj,ensure_ascii=False,separators=(",",":"),allow_nan=False).encode("utf8")
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(raw)))
        self.send_header("Connection","close")
        self.end_headers()
        self.wfile.write(raw)
        self.close_connection=True
    def do_POST(self):
        if self.path!="/v1/execute":return self._send(404,{"error":"NOT_FOUND"})
        uid=self._peer()
        if uid not in self.server.allowed_uids:return self._send(403,{"error":"UNAUTHORIZED"})
        if self.headers.get("Content-Type")!="application/json":
            return self._send(415,{"error":"UNSUPPORTED_MEDIA_TYPE"})
        try:n=int(self.headers.get("Content-Length","-1"))
        except ValueError:n=-1
        if n<0 or n>262144:return self._send(413,{"error":"REQUEST_TOO_LARGE"})
        try:req=json.loads(self.rfile.read(n))
        except (ValueError,UnicodeDecodeError):return self._send(400,{"error":"INVALID_REQUEST"})
        if not isinstance(req,dict) or req.get("operation") not in OPS:
            return self._send(403,{"error":"OPERATION_DENIED"})
        result=self.server.boundary.execute(req,trusted_principal="uid:"+str(uid))
        return self._send(200 if result.get("status")=="completed" else 409,result)
    def do_GET(self):
        if self.path!="/healthz":return self._send(404,{"error":"NOT_FOUND"})
        if self._peer() not in self.server.allowed_uids:return self._send(403,{"error":"UNAUTHORIZED"})
        return self._send(200,{"status":"staging","production":False})
