import json,os,socket,threading
from krc_research.uds_stage123 import Stage123Server
from krc_research.research_boundary120 import ResearchBoundary
from krc_research.request_ledger119 import RequestLedger
from krc_research.artifact_stage117 import HardenedExchange

def query(path,method,target,body=b"",request_id=""):
 s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
 s.connect(str(path))
 with s:
  s.sendall((f"{method} {target} HTTP/1.1\r\nHost: local\r\nContent-Type: application/json\r\nContent-Length: {len(body)}\r\nX-KRC-Request-ID: {request_id}\r\nConnection: close\r\n\r\n").encode()+body)
  data=b""
  while True:
   b=s.recv(65536)
   if not b:break
   data+=b
  return data

def fixture(tmp_path,peers):
 exchange=HardenedExchange(tmp_path/"objects",free_bytes_min=0)
 boundary=ResearchBoundary(ledger=RequestLedger(tmp_path/"ledger.sqlite"),exchange=exchange,dispatch=lambda op,p,who:{"text":"x"*p.get("length",4),"principal":who})
 path=tmp_path/"stage123.sock"
 server=Stage123Server(path,boundary=boundary,peer_principals=peers)
 thread=threading.Thread(target=server.serve_forever,daemon=True)
 thread.start()
 return server,thread,path,exchange

def test_authorized_inline_and_artifact(tmp_path):
 server,thread,path,exchange=fixture(tmp_path,{os.getuid():"K_Science"})
 try:
  small={"version":"krc-transport/2","request_id":"r12345","operation":"research.profile.validate","payload":{"length":4}}
  resp=query(path,"POST","/v1/execute",json.dumps(small).encode())
  assert b"200 OK" in resp and b'"delivery":"inline"' in resp
  large={**small,"request_id":"r12346","payload":{"length":1100000}}
  resp=query(path,"POST","/v1/execute",json.dumps(large).encode())
  assert b'"delivery":"artifact"' in resp
  obj=json.loads(resp.split(b"\r\n\r\n",1)[1])
  aid=obj["artifact"]["artifact_id"]
  fetch=query(path,"GET","/v1/artifacts/"+aid,request_id="r12346")
  assert b"200 OK" in fetch and len(fetch.split(b"\r\n\r\n",1)[1])>1000000
  denied=query(path,"GET","/v1/artifacts/"+aid,request_id="wrong")
  assert b"404 Not Found" in denied
 finally:
  server.shutdown();server.server_close();thread.join()

def test_denied_uid(tmp_path):
 server,thread,path,_=fixture(tmp_path,{os.getuid()+1000:"K_Science"})
 try:
  assert b"403 Forbidden" in query(path,"GET","/healthz")
 finally:server.shutdown();server.server_close();thread.join()

def test_large_response_guard(tmp_path):
 server,thread,path,_=fixture(tmp_path,{os.getuid():"K_Science"})
 try:
  obj={"version":"krc-transport/2","request_id":"r12347","operation":"research.profile.validate","payload":{"length":1048576}}
  response=query(path,"POST","/v1/execute",json.dumps(obj).encode())
  assert b"200 OK" in response and b'"delivery":"artifact"' in response
 finally:server.shutdown();server.server_close();thread.join()
