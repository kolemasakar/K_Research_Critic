import json,os,socket,threading
from krc_research.uds_stage121 import UDSHTTPServer
from krc_research.research_boundary120 import ResearchBoundary
from krc_research.request_ledger119 import RequestLedger
from krc_research.artifact_exchange import ArtifactExchange

def call(path,body=b"",method="POST",content_type="application/json"):
 s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);s.connect(str(path))
 with s:
  h=(method+" "+("/healthz" if method=="GET" else "/v1/execute")+" HTTP/1.1\r\nHost: localhost\r\nContent-Type: "+content_type+"\r\nContent-Length: "+str(len(body))+"\r\nConnection: close\r\n\r\n").encode()
  s.sendall(h+body)
  blocks=[]
  while True:
   chunk=s.recv(65536)
   if not chunk:break
   blocks.append(chunk)
 return b"".join(blocks)

def make(tmp_path,uids):
 b=ResearchBoundary(ledger=RequestLedger(tmp_path/"ledger.db"),exchange=ArtifactExchange(tmp_path/"store"),dispatch=lambda op,p,who:{"scientific_approval":False,"who":who})
 path=tmp_path/"stage121.sock"
 srv=UDSHTTPServer(str(path),boundary=b,allowed_uids=uids)
 t=threading.Thread(target=srv.serve_forever,daemon=True);t.start()
 return srv,t,path

def test_allowed_identity(tmp_path):
 srv,t,p=make(tmp_path,{os.getuid()})
 try:
  req={"version":"krc-transport/2","request_id":"r1","operation":"research.profile.validate","payload":{"x":1},"identity":{"principal":"forged"}}
  res=call(p,json.dumps(req).encode())
  assert b"200 OK" in res and ("uid:"+str(os.getuid())).encode() in res
  assert b"forged" not in res
 finally:srv.shutdown();srv.server_close();t.join()

def test_disallowed_peer(tmp_path):
 srv,t,p=make(tmp_path,{os.getuid()+10000})
 try:
  assert b"403 Forbidden" in call(p,b"{}")
  assert b"403 Forbidden" in call(p,method="GET")
 finally:srv.shutdown();srv.server_close();t.join()

def test_invalid_operation(tmp_path):
 srv,t,p=make(tmp_path,{os.getuid()})
 try:
  req={"version":"krc-transport/2","request_id":"r2","operation":"research.unsupported","payload":{}}
  assert b"403 Forbidden" in call(p,json.dumps(req).encode())
 finally:srv.shutdown();srv.server_close();t.join()

def test_health(tmp_path):
 srv,t,p=make(tmp_path,{os.getuid()})
 try:assert b"200 OK" in call(p,method="GET")
 finally:srv.shutdown();srv.server_close();t.join()
