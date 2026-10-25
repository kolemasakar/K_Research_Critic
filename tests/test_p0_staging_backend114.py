from datetime import datetime,timezone
from krc_research.interproject_contract import envelope,sign_envelope
from krc_research.staging_backend114 import execute_staging_request,staging_capabilities
NOW=datetime(2026,10,25,12,tzinfo=timezone.utc)
KEY=b"q"*32
PROFILE={"profile_id":"KSC01","version":"v1","protocol":"KRC Core","topic":"Concrete"}
def ask(op,payload,seen=None,**kwargs):
 e=envelope(task_id="ksci-stage114-0001",operation=op,payload=payload,created_at=NOW.isoformat())
 return execute_staging_request(e,secret=KEY,signature=sign_envelope(e,KEY),replay_registry=set() if seen is None else seen,now=NOW,**kwargs)
def test_readonly_inventory():
 o=staging_capabilities()
 assert len(o["operations"])==4 and not o["network_listener"] and not o["production_enabled"]
def test_profile_only_structure():
 o=ask("research.profile.validate",{"critic_profile":PROFILE})
 assert o["engine_result"]["validation"]=="STRUCTURE_VALID" and not o["scientific_approval"]
def test_bibliography_blocked_without_stub():
 assert ask("research.bibliography.audit",{"dois":["10.1234/test"]})["error"]["code"]=="OPERATION_DENIED"
def test_bibliography_synthetic():
 o=ask("research.bibliography.audit",{"dois":["10.1234/test"]},bibliography_fn=lambda dois:{"count":len(dois)})
 assert o["engine_result"]["count"]==1 and not o["scientific_approval"]
def test_replay_rejection():
 seen=set();ask("research.profile.validate",{"critic_profile":PROFILE},seen=seen)
 assert ask("research.profile.validate",{"critic_profile":PROFILE},seen=seen)["error"]["code"]=="REPLAY_REJECTED"
def test_invalid_payload():
 assert ask("research.profile.validate",{})["error"]["code"]=="INVALID_REQUEST"
def test_no_unapproved_science():
 o=ask("research.evidence.preflight",{"user_profile_approved":False,"manuscript_gate":{}})
 assert o["error"]["code"]=="INVALID_REQUEST"
