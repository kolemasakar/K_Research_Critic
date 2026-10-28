import hashlib,hmac,json,os,socket,threading
from datetime import datetime,timezone
from krc_research.staging_service123c import make_staging_server
from krc_research.transport_auth123b import canonical
from krc_research.interproject_contract import envelope,sign_envelope

IDENTITY={"client":"K_Science","principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}
KEY=b"X"*32
SECRET=b"Y"*32

def request(task="stage123c-real-001",rid="stage123c-request-001"):
 inner=envelope(task_id=task,operation="research.profile.validate",payload={"critic_profile":{"profile_id":"s","version":"v1","protocol":"KRC Core","topic":"synthetic"}},created_at=datetime.now(timezone.utc).isoformat())
 body={"version":"krc-transport/2","request_id":rid,"operation":"research.profile.validate","identity":IDENTITY,"payload":{"science_envelope":inner,"science_signature":sign_envelope(inner,SECRET)}}
 stamp=datetime.now(timezone.utc).isoformat()
 binding={"domain":"KRC-TRANSPORT-IDENTITY/2","key_id":"stage","issued_at":stamp,"envelope":body}
 body["transport_auth"]={"alg":"HMAC-SHA256","key_id":"stage","issued_at":stamp,"mac":hmac.new(KEY,canonical(binding),hashlib.sha256).hexdigest()}
 return body

def post(path,data):
 raw=json.dumps(data).encode();s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);s.connect(str(path))
 with s:
  s.sendall(b"POST /v1/execute HTTP/1.1\r\nHost: local\r\nContent-Type: application/json\r\nContent-Length: "+str(len(raw)).encode()+b"\r\nConnection: close\r\n\r\n"+raw)
  all=b""
  while True:
   block=s.recv(65536)
   if not block:break
   all+=block
 return all

def test_signed_verified_real_science_and_restart(tmp_path):
 root=tmp_path/"state"
 opts={"peer_principals":{os.getuid():"K_Science"},"uid_keys":{os.getuid():{"stage":KEY}},
       "claim_allowlist":{tuple(IDENTITY.values())},"science_secret":SECRET}
 msg=request()
 def once():
  sock=tmp_path/"backend.sock"
  server=make_staging_server(sock,root,**opts)
  thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  try:return post(sock,msg)
  finally:
   server.shutdown();server.server_close();thread.join();sock.unlink()
 first=once()
 assert b"200 OK" in first
 assert b'research.profile.validate' in first
 assert b'"scientific_approval":false' in first
 second=once()
 assert json.loads(first.partition(b"\r\n\r\n")[2])==json.loads(second.partition(b"\r\n\r\n")[2])
 # Brand-new request id does not bypass the durable signed task replay registry.
 replay=request(task="stage123c-real-001",rid="stage123c-request-002")
 sock=tmp_path/"backend2.sock";server=make_staging_server(sock,root,**opts)
 thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 try:
  res=post(sock,replay)
  assert b"409 Conflict" in res
 finally:server.shutdown();server.server_close();thread.join()
