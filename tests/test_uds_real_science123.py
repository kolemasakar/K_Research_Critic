import json,os,socket,threading
from datetime import datetime, timezone
from krc_research.uds_stage123 import Stage123Server
from krc_research.research_boundary120 import ResearchBoundary
from krc_research.request_ledger119 import RequestLedger
from krc_research.artifact_stage117 import HardenedExchange
from krc_research.science_adapter122 import ScienceAdapter122
from krc_research.interproject_contract import envelope,sign_envelope

def send(path,req):
 raw=json.dumps(req).encode()
 s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
 s.connect(str(path))
 with s:
  s.sendall(b"POST /v1/execute HTTP/1.1\r\nHost: local\r\nContent-Type: application/json\r\nContent-Length: "+str(len(raw)).encode()+b"\r\nConnection: close\r\n\r\n"+raw)
  chunks=[]
  while True:
   b=s.recv(65536)
   if not b:break
   chunks.append(b)
 data=b"".join(chunks)
 return data.split(b"\r\n\r\n",1)[0],json.loads(data.split(b"\r\n\r\n",1)[1])

def test_real_signed_profile_over_uds(tmp_path):
 key=b"s"*32
 principal="K_Science"
 backend=ScienceAdapter122(secret=key,allowed_principals={principal})
 b=ResearchBoundary(ledger=RequestLedger(tmp_path/"ledger.sqlite"),exchange=HardenedExchange(tmp_path/"store",free_bytes_min=0),dispatch=backend)
 path=tmp_path/"r.sock"
 server=Stage123Server(path,boundary=b,peer_principals={os.getuid():principal})
 th=threading.Thread(target=server.serve_forever,daemon=True);th.start()
 try:
  inner=envelope(task_id="stage123-test-000001",operation="research.profile.validate",payload={"critic_profile":{"profile_id":"s","version":"v1","protocol":"KRC Core","topic":"synthetic"}},created_at=datetime.now(timezone.utc).isoformat())
  req={"version":"krc-transport/2","request_id":"req123real","operation":"research.profile.validate","payload":{"science_envelope":inner,"science_signature":sign_envelope(inner,key)}}
  status,answer=send(path,req)
  assert b"200 OK" in status
  assert answer["result"]["operation"]=="research.profile.validate"
  assert answer["result"]["scientific_approval"] is False
  status2,answer2=send(path,req)
  assert answer2==answer
 finally:
  server.shutdown();server.server_close();th.join()
