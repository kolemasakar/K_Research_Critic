"""Stage123-A UDS staging bridge: peer-scoped real science and private artifacts.
Not a production service. Requires trusted peer UID mapping configured by owner.
"""
import json,os,socket, socketserver,struct
from http.server import BaseHTTPRequestHandler
from .staging_backend114 import OPS
from .artifact_exchange import MIB,ExchangeError

class Stage123Server(socketserver.UnixStreamServer):
    def __init__(self,path,*,boundary,peer_principals):
        self.boundary=boundary
        self.peer_principals=dict(peer_principals)
        if not self.peer_principals:raise ValueError("No trusted peers")
        super().__init__(str(path),Stage123Handler)

class Stage123Handler(BaseHTTPRequestHandler):
    protocol_version="HTTP/1.1"
    def log_message(self,*args):pass
    def principal(self):
        uid=struct.unpack("3i",self.connection.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))[1]
        return self.server.peer_principals.get(uid)
    def send_json(self,status,obj):
        data=json.dumps(obj,ensure_ascii=False,allow_nan=False,separators=(",",":")).encode("utf-8")
        if len(data)>MIB:
            status=507
            data=b'{"status":"error","error":{"code":"RESPONSE_TOO_LARGE"}}'
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(data)))
        self.send_header("Connection","close")
        self.end_headers()
        self.wfile.write(data)
        self.close_connection=True
    def do_POST(self):
        principal=self.principal()
        if principal is None:return self.send_json(403,{"error":"UNAUTHORIZED"})
        if self.path!="/v1/execute":return self.send_json(404,{"error":"NOT_FOUND"})
        if self.headers.get("Content-Type")!="application/json":
            return self.send_json(415,{"error":"UNSUPPORTED_MEDIA_TYPE"})
        try:n=int(self.headers.get("Content-Length","-1"))
        except ValueError:n=-1
        if n<0 or n>262144:return self.send_json(413,{"error":"REQUEST_TOO_LARGE"})
        try:req=json.loads(self.rfile.read(n))
        except (ValueError,UnicodeDecodeError):return self.send_json(400,{"error":"INVALID_REQUEST"})
        if not isinstance(req,dict) or req.get("operation") not in OPS:
            return self.send_json(403,{"error":"OPERATION_DENIED"})
        out=self.server.boundary.execute(req,trusted_principal=principal)
        return self.send_json(200 if out.get("status")=="completed" else 409,out)
    def do_GET(self):
        principal=self.principal()
        if principal is None:return self.send_json(403,{"error":"UNAUTHORIZED"})
        if self.path=="/healthz":return self.send_json(200,{"status":"staging","production":False})
        prefix="/v1/artifacts/"
        if not self.path.startswith(prefix):return self.send_json(404,{"error":"NOT_FOUND"})
        artifact_id=self.path[len(prefix):]
        request_id=self.headers.get("X-KRC-Request-ID","")
        # This header is only a *selector*, never an identity credential.
        try:
            chunks=self.server.boundary.exchange.read_stream(
                artifact_id,principal=principal,request_id=request_id)
            # Preflight iterator validation and hash verification before response headers.
            # tempfile-free staged output: stream generator starts on first next().
            iterator=iter(chunks)
            first=next(iterator,b"")
            with self.server.boundary.exchange._connect() as db:
                row=db.execute("SELECT size,sha256 FROM objects WHERE id=? AND principal=? AND request_id=?",
                    (artifact_id,principal,request_id)).fetchone()
            if row is None:raise ExchangeError("NOT_FOUND")
        except ExchangeError as exc:return self.send_json(404,{"error":exc.code})
        self.send_response(200)
        self.send_header("Content-Type","application/octet-stream")
        self.send_header("Content-Length",str(row[0]))
        self.send_header("X-Content-SHA256",row[1])
        self.send_header("Connection","close")
        self.end_headers()
        try:
            self.wfile.write(first)
            for piece in iterator:self.wfile.write(piece)
        finally:self.close_connection=True
