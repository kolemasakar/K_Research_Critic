import hashlib, http.client, json, os, socket, tempfile, threading
from pathlib import Path
from krc_research.stage131_signed_artifact_uds import SignedArtifactUDSServer
from krc_research.stage131_signed_artifact_boundary import SignedArtifactReadBoundary
from krc_research.stage131_signed_artifact_read import sign_fixture
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
from krc_research.request_ledger119 import RequestLedger
KEY=b"synthetic-retrieval-secret-key-only"
IDENTITY={"principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}
class Exchange:
 def read_stream(self,*a,**k):
  yield b"x"*(1024*1024)
  yield b"end"
def test_actual_uds_signed_headers_and_bytes():
 with tempfile.TemporaryDirectory() as d:
  ledger=RequestLedger(Path(d)/"ledger.db");q="KS-"+"a"*32;p={"task_id":"t"}
  ledger.admit(principal="K_Science",request_id=q,operation="research.profile.validate",payload=p)
  ledger.complete(principal="K_Science",request_id=q,operation="research.profile.validate",payload=p,result={"status":"completed"})
  boundary=SignedArtifactReadBoundary(exchange=Exchange(),ledger=ledger,nonce_registry=ArtifactNonceRegistry(Path(d)/"nonce.db"),keyring={"k":KEY},trusted_peer_identities={os.getuid():IDENTITY},enabled=True)
  sock=Path(d)/"server.sock";server=SignedArtifactUDSServer(sock,boundary=boundary)
  thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  try:
   msg={"version":"krc-artifact-get/1","operation":"artifact.read","request_id":q,"artifact_id":"b"*48,"identity":IDENTITY,"auth":{"key_id":"k","issued_at_epoch":int(__import__("time").time()),"nonce":"nonce-1234567890123456","mac_sha256":"0"*64}}
   msg=sign_fixture(msg,KEY);raw=json.dumps(msg).encode()
   def request():
    s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);s.connect(str(sock))
    s.sendall(b"POST /v1/artifacts/read HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nContent-Length: "+str(len(raw)).encode()+b"\r\nConnection: close\r\n\r\n"+raw)
    s.shutdown(socket.SHUT_WR)
    data=b""
    while True:
     chunk=s.recv(256*1024)
     if not chunk:break
     data+=chunk
    s.close()
    return data
   response=request();head,body=response.split(b"\r\n\r\n",1)
   assert b"200 OK" in head
   assert b"X-Content-SHA256: "+hashlib.sha256(body).hexdigest().encode() in head
   assert len(body)==1024*1024+3
   assert b"403 Forbidden" in request()
  finally:server.shutdown();server.server_close();thread.join(timeout=5)
