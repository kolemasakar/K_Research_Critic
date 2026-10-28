import copy,hashlib,hmac,json,os,socket,threading
from datetime import datetime,timezone,timedelta
import pytest
from krc_research.transport_auth123b import verify,TransportAuthError,canonical
from krc_research.uds_verified123b import VerifiedStage123Server
from krc_research.request_ledger119 import RequestLedger
from krc_research.research_boundary120 import ResearchBoundary
from krc_research.artifact_stage117 import HardenedExchange
KEY=b"Q"*32
IDENTITY={"client":"K_Science","principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}
ALLOW={tuple(IDENTITY[k] for k in ("client","principal","repository","workflow_ref"))}
def signed(body=None,stamp=None):
 body=body or {"version":"krc-transport/2","request_id":"stage123b001","operation":"research.profile.validate","identity":dict(IDENTITY),"payload":{"v":1}}
 stamp=stamp or datetime.now(timezone.utc).isoformat()
 binding={"domain":"KRC-TRANSPORT-IDENTITY/2","key_id":"staging-1","issued_at":stamp,"envelope":body}
 return {**body,"transport_auth":{"alg":"HMAC-SHA256","key_id":"staging-1","issued_at":stamp,"mac":hmac.new(KEY,canonical(binding),hashlib.sha256).hexdigest()}}
def checked(msg):
 return verify(msg,peer_uid=os.getuid(),uid_keys={os.getuid():{"staging-1":KEY}},claim_allowlist=ALLOW)
def test_valid():assert checked(signed())["identity"]==IDENTITY
@pytest.mark.parametrize("field",["identity","operation","request_id","payload"])
def test_mutation(field):
 msg=signed()
 msg[field]=({"client":"forged","principal":"forged","repository":"forged","workflow_ref":"forged"} if field=="identity" else ("research.bibliography.audit" if field=="operation" else "different" if field=="request_id" else {"v":2}))
 with pytest.raises(TransportAuthError):checked(msg)
def test_expired():
 with pytest.raises(TransportAuthError,match="EXPIRED_ASSERTION"):
  checked(signed(stamp=(datetime.now(timezone.utc)-timedelta(minutes=8)).isoformat()))
def test_bad_uid():
 with pytest.raises(TransportAuthError,match="UNAUTHORIZED"):
  verify(signed(),peer_uid=os.getuid()+1000,uid_keys={os.getuid():{"staging-1":KEY}},claim_allowlist=ALLOW)
def test_wrong_allowlist():
 with pytest.raises(TransportAuthError,match="UNAUTHORIZED"):
  verify(signed(),peer_uid=os.getuid(),uid_keys={os.getuid():{"staging-1":KEY}},claim_allowlist=set())
def _post(path,body):
 raw=json.dumps(body).encode();s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);s.connect(str(path))
 with s:
  s.sendall(b"POST /v1/execute HTTP/1.1\r\nHost: local\r\nContent-Type: application/json\r\nContent-Length: "+str(len(raw)).encode()+b"\r\nConnection: close\r\n\r\n"+raw)
  data=b""
  while True:
   c=s.recv(65536)
   if not c:break
   data+=c
 return data
def test_uds_verified_before_dispatch(tmp_path):
 count=[]
 b=ResearchBoundary(ledger=RequestLedger(tmp_path/"ledger.sqlite"),exchange=HardenedExchange(tmp_path/"objects",free_bytes_min=0),dispatch=lambda op,p,who:(count.append(who) or {"ok":True}))
 sock=tmp_path/"backend.sock"
 srv=VerifiedStage123Server(sock,boundary=b,peer_principals={os.getuid():"K_Science"},uid_keys={os.getuid():{"staging-1":KEY}},claim_allowlist=ALLOW)
 t=threading.Thread(target=srv.serve_forever,daemon=True);t.start()
 try:
  assert b"200 OK" in _post(sock,signed())
  invalid=signed();invalid["payload"]={"forged":True}
  assert b"403 Forbidden" in _post(sock,invalid)
  assert count==["K_Science"]
 finally:srv.shutdown();srv.server_close();t.join()
