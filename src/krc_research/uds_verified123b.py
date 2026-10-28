"""Stage123-B independent pre-dispatch assertion gate for staging UDS."""
from .uds_stage123 import Stage123Server,Stage123Handler
from .transport_auth123b import verify,TransportAuthError
from .staging_backend114 import OPS
import json,struct,socket

class VerifiedStage123Server(Stage123Server):
    def __init__(self,path,*,boundary,peer_principals,uid_keys,claim_allowlist):
        self.uid_keys=uid_keys
        self.claim_allowlist=frozenset(claim_allowlist)
        super().__init__(path,boundary=boundary,peer_principals=peer_principals)
        self.RequestHandlerClass=VerifiedStage123Handler

class VerifiedStage123Handler(Stage123Handler):
    def do_POST(self):
        peer_uid=struct.unpack("3i",self.connection.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))[1]
        if peer_uid not in self.server.peer_principals:
            return self.send_json(403,{"error":"UNAUTHORIZED"})
        if self.path!="/v1/execute":return self.send_json(404,{"error":"NOT_FOUND"})
        if self.headers.get("Content-Type")!="application/json":return self.send_json(415,{"error":"UNSUPPORTED_MEDIA_TYPE"})
        try:n=int(self.headers.get("Content-Length","-1"))
        except ValueError:n=-1
        if n<0 or n>262144:return self.send_json(413,{"error":"REQUEST_TOO_LARGE"})
        try:message=json.loads(self.rfile.read(n))
        except (UnicodeDecodeError,ValueError):return self.send_json(400,{"error":"INVALID_REQUEST"})
        try:
            envelope=verify(message,peer_uid=peer_uid,uid_keys=self.server.uid_keys,claim_allowlist=self.server.claim_allowlist)
        except TransportAuthError as exc:
            return self.send_json(403 if exc.args[0]!="REQUEST_TOO_LARGE" else 413,{"error":exc.args[0]})
        if envelope["operation"] not in OPS:return self.send_json(403,{"error":"OPERATION_DENIED"})
        principal=envelope["identity"]["principal"]
        if principal!=self.server.peer_principals[peer_uid]:
            return self.send_json(403,{"error":"UNAUTHORIZED"})
        output=self.server.boundary.execute(envelope,trusted_principal=principal)
        return self.send_json(200 if output.get("status")=="completed" else 409,output)
