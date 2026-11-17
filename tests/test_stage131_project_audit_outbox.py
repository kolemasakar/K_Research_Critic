import json,os,sqlite3
from pathlib import Path
import pytest
from krc_research.stage131_project_audit_outbox import ProjectAuditOutbox, ZERO
from krc_research.stage131_project_research_route import ProjectResearchRoute

BASE="a"*40
SOURCE="b"*40
MERGED="c"*40
PROFILE={"purpose":"Synthetic private audit", "policy":"FREE_ONLY_OFFLINE",
 "operation":"research.profile.validate","payload":{"critic_profile":{
 "profile_id":"secret-fixture","version":"1","protocol":"KRC Core","topic":"PRIVATE_TOPIC"},
 "user_profile_approved":True}}

@pytest.fixture(autouse=True)
def private_umask():
 old=os.umask(0o077)
 try:yield
 finally:os.umask(old)

def make(tmp_path):
 r=ProjectResearchRoute(tmp_path/"state")
 p=r.propose(PROFILE)
 r.decide(p["request_id"],p["profile_sha256"],"APPROVE")
 r.run(p["request_id"],p["profile_sha256"])
 return r,p,ProjectAuditOutbox(tmp_path/"audit"/"outbox.sqlite")

def test_publish_retry_idempotence_new_state_and_prefix(tmp_path):
 r,p,o=make(tmp_path)
 first=o.prepare(r.root,base_commit=BASE,source_commit=SOURCE)
 assert first["status"]=="PENDING"
 assert o.prepare(r.root,base_commit=BASE,source_commit=SOURCE)==first
 exported=json.dumps(first)
 for private in (p["request_id"],"PRIVATE_TOPIC","secret-fixture",p["profile_sha256"]):
  assert private not in exported
 m=first["payload"]
 with pytest.raises(ValueError,match="RECEIPT_MISMATCH"):o.ack(sequence=1,head="0"*64,commit=MERGED)
 o.ack(sequence=1,head=m["chain_head_sha256"],commit=MERGED)
 assert o.status()["status"]=="PUBLISHED"
 with pytest.raises(ValueError,match="PUBLISHED_PREFIX_MISMATCH"):
  o.prepare(r.root,base_commit=MERGED,source_commit=SOURCE)
 kwargs=dict(base_commit=MERGED,source_commit=SOURCE,prior_sequence=1,
  prior_head=m["chain_head_sha256"],prior_commit=MERGED)
 assert o.prepare(r.root,**kwargs)["status"]=="UNCHANGED"
 r.decide(p["request_id"],p["profile_sha256"],"CANCEL")
 second=o.prepare(r.root,**kwargs)
 assert second["payload"]["sequence"]==2
 assert second["payload"]["previous_chain_head_sha256"]==m["chain_head_sha256"]
 assert second["payload"]["chain_head_sha256"]!=m["chain_head_sha256"]
 assert ProjectAuditOutbox(o.path).status()["status"]=="PENDING"

def test_pending_changed_base_fails_closed(tmp_path):
 r,p,o=make(tmp_path)
 o.prepare(r.root,base_commit=BASE,source_commit=SOURCE)
 with pytest.raises(ValueError,match="PENDING_BASE_CHANGED"):
  o.prepare(r.root,base_commit=MERGED,source_commit=SOURCE)

def test_tamper_journal_or_profile_fails_closed(tmp_path):
 r,p,o=make(tmp_path)
 o.prepare(r.root,base_commit=BASE,source_commit=SOURCE)
 with sqlite3.connect(o.path) as db:
  db.execute("UPDATE journal SET head=?",("0"*64,))
 with pytest.raises(ValueError,match="AUDIT_CHAIN_MISMATCH"):o.status()
 with sqlite3.connect(r.root/"consent.sqlite") as db:
  db.execute("UPDATE project_profiles SET profile_json='{}'")
 with pytest.raises(ValueError,match="PROFILE_MISMATCH"):
  o.prepare(r.root,base_commit=BASE,source_commit=SOURCE)
