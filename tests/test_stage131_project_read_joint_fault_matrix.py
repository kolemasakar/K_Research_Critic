"""Real isolated ProjectResearchRoute + signed UDS matrix; no live state.
Run with optional KRC_N39_FIXTURE_OUTPUT to capture synthetic response evidence.
"""
import hashlib,json,os,socket,sqlite3,threading,time
from pathlib import Path
from contextlib import contextmanager
import pytest
from krc_research.stage131_project_research_route import ProjectResearchRoute
from krc_research.stage131_project_signed_read import ProjectArtifactAuthority,ProjectSignedArtifactBoundary,IDENTITY,KEY_ID
from krc_research.stage131_signed_artifact_read import sign_fixture
from krc_research.stage131_signed_artifact_uds import SignedArtifactUDSServer
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
from krc_research.stage131_project_descriptor_client import fetch_descriptor,DescriptorDenied,describe_envelope

KEY=b"n39-synthetic-key-32bytes-only!!"
assert len(KEY)==32
PROFILE={"purpose":"N39 synthetic fault fixture","operation":"research.profile.validate","policy":"FREE_ONLY_OFFLINE",
 "payload":{"critic_profile":{"profile_id":"fault-fixture","version":"1","protocol":"KRC Core","topic":"Synthetic only"},"user_profile_approved":True}}
@pytest.fixture(autouse=True)
def private_umask():
 old=os.umask(0o077)
 try:yield
 finally:os.umask(old)

def state(tmp):
 r=ProjectResearchRoute(tmp/"state")
 p=r.propose(PROFILE);rid=p["request_id"];digest=p["profile_sha256"]
 r.decide(rid,digest,"APPROVE");a=r.run(rid,digest)["artifact"]
 return r,p,a

def msg(rid,aid,*,op="artifact.read",key=KEY,identity=None,stamp=None,nonce=None,extra=None):
 m={"version":"krc-artifact-get/1","operation":op,"request_id":rid,"artifact_id":aid,
  "identity":IDENTITY if identity is None else identity,"auth":{"key_id":KEY_ID,
  "issued_at_epoch":int(time.time()) if stamp is None else stamp,
  "nonce":os.urandom(24).hex() if nonce is None else nonce,"mac_sha256":"0"*64}}
 if extra:m.update(extra)
 return sign_fixture(m,key)

@contextmanager
def server(tmp,r,*,peer=None,clock=time.time,limit=200*1024*1024,authority=None,enabled=True,nonce_path=None):
 a=authority or ProjectArtifactAuthority(r.root,clock=clock,limit=limit)
 b=ProjectSignedArtifactBoundary(authority=a,nonce_registry=ArtifactNonceRegistry(nonce_path or tmp/"nonce.sqlite"),
  key=KEY,peer_uid=os.getuid() if peer is None else peer,enabled=enabled)
 path=tmp/("w-"+os.urandom(3).hex()+".sock")
 srv=SignedArtifactUDSServer(path,boundary=b)
 t=threading.Thread(target=srv.serve_forever,daemon=True);t.start()
 try:yield path,b
 finally:srv.shutdown();srv.server_close();t.join(3)

def wire(path,m,*,route="/v1/artifacts/read"):
 data=json.dumps(m,separators=(",",":")).encode()
 with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
  s.settimeout(5);s.connect(str(path))
  s.sendall(b"POST "+route.encode()+b" HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nContent-Length: "+str(len(data)).encode()+b"\r\nConnection: close\r\n\r\n"+data);s.shutdown(socket.SHUT_WR)
  ret=b""
  while True:
   c=s.recv(65536)
   if not c:break
   ret+=c
 head,body=ret.split(b"\r\n\r\n",1)
 lines=head.decode("ascii").split("\r\n")
 headers=dict(x.split(": ",1) for x in lines[1:])
 assert int(headers["Content-Length"])==len(body) and headers["Connection"]=="close"
 assert headers["Cache-Control"]=="no-store" and headers["X-Content-Type-Options"]=="nosniff"
 status=int(lines[0].split()[1])
 if status!=200:assert headers["Content-Type"]=="application/json" and set(json.loads(body))=={"error"} and "X-Content-SHA256" not in headers
 return status,headers,body

def capture(case,response):
 dest=os.getenv("KRC_N39_FIXTURE_OUTPUT")
 if not dest:return
 status,headers,body=response
 h={k:headers[k] for k in ("Content-Type","Content-Length","Cache-Control","X-Content-Type-Options","Connection","X-Content-SHA256") if k in headers}
 result={"case":case,"http_status":status,"headers":h,"body_sha256":hashlib.sha256(body).hexdigest(),"body_utf8":body.decode()}
 # Synthetic response only; never include request MAC, token or live IDs.
 with open(dest,"a",encoding="utf-8") as f:f.write(json.dumps(result,sort_keys=True)+"\n")

@pytest.mark.parametrize("case,wanted",[
 ("N12",400),("N15",404),("N18",404),("N19",404),("N20_MISSING",404),("N20_CONFLICT",502),
 ("N21",410),("N22",502),("N23",502),("N24",502),("N26",413),("N27",403),
 ("N28",403),("N29",403),("N30",403),("N39_CANCEL",403),("N39_MISSING",403),("BACKEND_DB_UNAVAILABLE",503)])
def test_actual_wire_negative_matrix(tmp_path,case,wanted):
 r,p,a=state(tmp_path);rid=p["request_id"];aid=a["artifact_id"];options={};kw={}
 target=r.exchange.data/aid
 if case=="N12":kw["extra"]={"consent":True}
 elif case=="N15":rid="KS-"+"e"*32
 elif case=="N18":
  with sqlite3.connect(r.exchange.dbpath) as db:db.execute("UPDATE objects SET principal='OTHER' WHERE id=?",(aid,))
 elif case=="N19":
  q=r.propose(PROFILE);r.decide(q["request_id"],q["profile_sha256"],"APPROVE")
  rid=q["request_id"];r.run(rid,q["profile_sha256"])
 elif case=="N20_MISSING":
  with sqlite3.connect(r.requests.path) as db:db.execute("DELETE FROM requests WHERE request_id=?",(rid,))
 elif case=="N20_CONFLICT":
  with sqlite3.connect(r.requests.path) as db:db.execute("UPDATE requests SET result='{}' WHERE request_id=?",(rid,))
 elif case=="N21":options["clock"]=lambda:a["expires_at_epoch"]+1
 elif case in ("N22","N23"):target.write_bytes(b"x"*a["size_bytes"])
 elif case=="N24":target.write_bytes(b"x")
 elif case=="N26":options["limit"]=10
 elif case=="N27":options["peer"]=os.getuid()+1
 elif case=="N28":kw["key"]=b"x"*32
 elif case=="N29":kw["identity"]=dict(IDENTITY,repository="foreign/test")
 elif case=="N30":kw["stamp"]=int(time.time())-301
 elif case=="N39_CANCEL":r.decide(rid,p["profile_sha256"],"CANCEL")
 elif case=="N39_MISSING":
  with sqlite3.connect(r.consent.path) as db:db.execute("DELETE FROM artifacts WHERE request_id=?",(rid,))
 elif case=="BACKEND_DB_UNAVAILABLE":
  r.requests.path.rename(r.root/"requests.offline")
 with server(tmp_path,r,**options) as (path,b):
  response=wire(path,msg(rid,aid,**kw))
  assert response[0]==wanted
  capture(case,response)
 with sqlite3.connect(r.root/"science-replay.sqlite") as db:
  assert db.execute("SELECT COUNT(*) FROM requests").fetchone()[0]==(2 if case=="N19" else 1)

def test_N25_verified_private_spool_immune_to_subsequent_source_mutation(tmp_path,monkeypatch):
 r,p,a=state(tmp_path);rid=p["request_id"];aid=a["artifact_id"];target=r.exchange.data/aid
 original=target.read_bytes();authority=ProjectArtifactAuthority(r.root);spool=authority.spool
 def mutate_after_verified(scope):
  f,d=spool(scope);target.write_bytes(b"x"*len(original));return f,d
 monkeypatch.setattr(authority,"spool",mutate_after_verified)
 with server(tmp_path,r,authority=authority) as (path,b):
  result=wire(path,msg(rid,aid))
  assert result[0]==200 and result[2]==original and hashlib.sha256(result[2]).hexdigest()==a["sha256"]
  capture("N25_VERIFIED_SPOOL",result)
  result=wire(path,msg(rid,aid));assert result[0]==502;capture("N25_NEXT_READ_DENIED",result)

def test_descriptor_client_binary_read_and_nonce_restart(tmp_path):
 r,p,a=state(tmp_path);rid=p["request_id"];aid=a["artifact_id"];m=msg(rid,aid)
 n=tmp_path/"persistent-nonce.sqlite"
 with server(tmp_path,r,nonce_path=n) as (path,b):
  d=fetch_descriptor(path,m,key=KEY,expected_uid=os.getuid(),expected_gid=os.getgid())
  assert d==dict(a,request_id=rid)
  q,_=describe_envelope(m,KEY);assert q["operation"]=="artifact.describe" and q["auth"]["nonce"]!=m["auth"]["nonce"]
  response=wire(path,msg(rid,aid,op="artifact.describe"),route="/v1/artifacts/describe")
  assert response[0]==200 and json.loads(response[2])==d;capture("DESCRIPTOR_200",response)
  response=wire(path,m);assert response[0]==200 and len(response[2])==a["size_bytes"] and hashlib.sha256(response[2]).hexdigest()==d["sha256"];capture("READ_200",response)
 with server(tmp_path,r,nonce_path=n) as (path,b):
  response=wire(path,m);assert response[0]==403;capture("DURABLE_NONCE_RESTART",response)
  r.decide(rid,p["profile_sha256"],"CANCEL")
  with pytest.raises(DescriptorDenied) as err:fetch_descriptor(path,msg(rid,aid),key=KEY,expected_uid=os.getuid(),expected_gid=os.getgid())
  assert err.value.status==403

def test_descriptor_client_unavailable_timeout(tmp_path):
 r,p,a=state(tmp_path);m=msg(p["request_id"],a["artifact_id"])
 with pytest.raises(DescriptorDenied) as err:
  fetch_descriptor(tmp_path/"absent.sock",m,key=KEY,expected_uid=os.getuid(),expected_gid=os.getgid())
 assert err.value.status==503
 path=tmp_path/"delay.sock"
 with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as listener:
  listener.bind(str(path));listener.listen(1)
  def delay():
   with listener.accept()[0] as conn:time.sleep(.4)
  t=threading.Thread(target=delay);t.start()
  try:
   with pytest.raises(DescriptorDenied) as err:fetch_descriptor(path,m,key=KEY,expected_uid=os.getuid(),expected_gid=os.getgid(),timeout=.1)
   assert err.value.status==504
  finally:t.join()
