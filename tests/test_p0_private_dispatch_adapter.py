from datetime import datetime, timezone
from krc_research.interproject_contract import envelope, sign_envelope
from krc_research.private_dispatch_adapter import dispatch_validated

KEY=b"x"*32
NOW=datetime(2026,10,25,12,tzinfo=timezone.utc)
PROFILE={"profile_id":"K-01","version":"v1","protocol":"KRC Core","topic":"Concrete"}
def request(op,payload,**kw):
    body=envelope(task_id="kscience-private-0001",operation=op,payload=payload,created_at=NOW.isoformat())
    return dispatch_validated(body,secret=KEY,signature=sign_envelope(body,KEY),seen=set(),
                              permitted={op},now=NOW,**kw)
def test_profile_pass_but_not_approval():
    out=request("research.profile.validate",{"critic_profile":PROFILE})
    assert out["engine_result"]["approval_independently_verified"] is False
    assert not out["scientific_approval"]
def test_missing_profile_rejected():
    assert request("research.profile.validate",{})["error"]["code"]=="INVALID_REQUEST"
def test_receipt_invalid_rejected_before_processing():
    assert request("research.inspection.review",{"receipt":{"trace_verified":True}})["error"]["code"]=="INVALID_REQUEST"
def test_preflight_missing_gate_rejected():
    assert request("research.evidence.preflight",{"user_profile_approved":True})["error"]["code"]=="INVALID_REQUEST"
def test_no_network_bibliography_injected():
    out=request("research.bibliography.audit",{"dois":["10.1234/test"]},
                bibliography_fn=lambda dois:{"schema":"TEST","count":len(dois)})
    assert out["engine_result"]["count"]==1
def test_bad_signature_error_is_sanitized():
    body=envelope(task_id="kscience-private-0002",operation="research.profile.validate",
                  payload={"critic_profile":PROFILE},created_at=NOW.isoformat())
    out=dispatch_validated(body,secret=KEY,signature="0"*64,seen=set(),
                           permitted={"research.profile.validate"},now=NOW)
    assert out["error"]["code"]=="HANDLER_ERROR" and "signature" not in out["error"]["message"].lower()
def test_extra_properties_rejected():
    assert request("research.profile.validate",{"critic_profile":PROFILE,"secret":"not-allowed"})["error"]["code"]=="INVALID_REQUEST"
