import json,os,sqlite3,socket,threading,time,hashlib
from pathlib import Path
from krc_research.stage131_project_research_route import ProjectResearchRoute
from krc_research.stage131_project_signed_read import (
 ProjectArtifactAuthority,ProjectSignedArtifactBoundary,IDENTITY,KEY_ID)
from krc_research.stage131_signed_artifact_read import sign_fixture
from krc_research.stage131_signed_artifact_uds import SignedArtifactUDSServer
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
import pytest

KEY=b"synthetic-only-project-retrieval-key"
PROFILE={"purpose":"Synthetic N39 read","policy":"FREE_ONLY_OFFLINE",
 "operation":"research.profile.validate","payload":{"critic_profile":{
 "profile_id":"n39","version":"1","protocol":"KRC Core","topic":"Synthetic"},
 "user_profile_approved":True}}

def setup(tmp_path):
 root=tmp_path/"state"; p=ProjectResearchRoute(root).propose(PROFILE)
 r=ProjectResearchRoute(root);rid=p["request_id"];digest=p["profile_sha256"]
 r.decide(rid,digest,"APPROVE");out=r.run(rid,digest)
 return r,p,out["artifact"]

def message(rid,aid,nonce,op="artifact.read",key=KEY):
 return sign_fixture({"version":"krc-artifact-get/1","operation":op,"request_id":rid,
 "artifact_id":aid,"identity":IDENTITY,"auth":{"key_id":KEY_ID,
 "issued_at_epoch":int(time.time()),"nonce":nonce,"mac_sha256":"0"*64}},key)

def boundary(tmp_path,r,**kwargs):
 return ProjectSignedArtifactBoundary(authority=ProjectArtifactAuthority(r.root,**kwargs),
  nonce_registry=ArtifactNonceRegistry(tmp_path/"nonce.sqlite"),key=KEY,
  peer_uid=os.getuid(),enabled=True)

def test_actual_route_wire_descriptor_read_cancel_replay(tmp_path):
 r,p,a=setup(tmp_path);rid=p["request_id"];aid=a["artifact_id"];b=boundary(tmp_path,r)
 srv=SignedArtifactUDSServer(tmp_path/"wire.sock",boundary=b)
 t=threading.Thread(target=srv.serve_forever,daemon=True);t.start()
 def wire(path,msg):
  raw=json.dumps(msg).encode(); req=("POST "+path+" HTTP/1.1\r\nHost: local\r\nContent-Type: application/json\r\nContent-Length: "+str(len(raw))+"\r\n\r\n").encode()+raw
  with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
   s.settimeout(5);s.connect(str(tmp_path/"wire.sock"));s.sendall(req);s.shutdown(socket.SHUT_WR)
   data=b""
   while True:
    part=s.recv(65536)
    if not part:break
    data+=part
  head,body=data.split(b"\r\n\r\n",1);return int(head.split()[1]),head,body
 try:
  status,h,body=wire("/v1/artifacts/describe",message(rid,aid,"descriptor-nonce-0001","artifact.describe"))
  assert status==200 and json.loads(body)==dict(a,request_id=rid)
  m=message(rid,aid,"retrieval-nonce-0001")
  status,h,body=wire("/v1/artifacts/read",m)
  assert status==200 and hashlib.sha256(body).hexdigest()==a["sha256"] and a["sha256"].encode() in h
  assert wire("/v1/artifacts/read",m)[0]==403
  assert wire("/v1/artifacts/describe",message(rid,aid,"different-op-00001"))[0]==403
  r.decide(rid,p["profile_sha256"],"CANCEL")
  assert wire("/v1/artifacts/read",message(rid,aid,"cancelled-read-0001"))[0]==403
  assert wire("/v1/artifacts/describe",message(rid,aid,"cancelled-desc-0001","artifact.describe"))[0]==403
 finally:srv.shutdown();srv.server_close();t.join(3)
 with sqlite3.connect(r.root/"science-replay.sqlite") as db:
  assert db.execute("SELECT COUNT(*) FROM requests").fetchone()[0]==1

def test_scope_mac_peer_expiry_corruption_limit(tmp_path):
 r,p,a=setup(tmp_path);rid=p["request_id"];aid=a["artifact_id"];b=boundary(tmp_path,r)
 def check(msg,status):assert b.execute(msg,peer_uid=os.getuid())["http_status"]==status
 assert b.execute(message(rid,aid,"wrong-peer-0000001"),peer_uid=os.getuid()+1)["http_status"]==403
 check(message(rid,aid,"wrong-mac-00000001",key=b"bad"),403)
 check(message(rid,"a"*48,"wrong-artifact-0001"),404)
 check(message("KS-"+"a"*32,aid,"wrong-request-0001"),404)
 expired=boundary(tmp_path,r,clock=lambda:a["expires_at_epoch"]+1)
 assert expired.execute(message(rid,aid,"expired-artifact-0001"),peer_uid=os.getuid())["http_status"]==410
 limited=boundary(tmp_path,r,limit=10)
 assert limited.execute(message(rid,aid,"too-large-00000001"),peer_uid=os.getuid())["http_status"]==413
 path=r.exchange.data/aid;path.write_bytes(b"x"*a["size_bytes"])
 check(message(rid,aid,"corrupt-artifact-0001"),502)

def test_authoritative_descriptor_must_match_store(tmp_path):
 r,p,a=setup(tmp_path);rid=p["request_id"];aid=a["artifact_id"];b=boundary(tmp_path,r)
 with sqlite3.connect(r.root/"artifacts"/"index.sqlite3") as db:
  db.execute("UPDATE objects SET sha256=? WHERE id=?",("0"*64,aid))
 assert b.describe(message(rid,aid,"bad-index-desc-0001","artifact.describe"),peer_uid=os.getuid())["http_status"]==502
