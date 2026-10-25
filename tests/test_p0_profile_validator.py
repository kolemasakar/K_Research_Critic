import pytest
from datetime import datetime,timezone
from krc_research.interproject_contract import envelope, sign_envelope
from krc_research.science_dispatch import handle_science_request
from krc_research.profile_validator import validate_profile
NOW=datetime(2026,10,25,12,tzinfo=timezone.utc)
KEY=b"t"*32
PROFILE={"profile_id":"KSC-001","version":"v1.0","protocol":"Scholarly Research","topic":"UPV concrete"}
def invoke(payload,permitted=None,seen=None,signature=None):
    env=envelope(task_id="ksci-profile-0001",operation="research.profile.validate",payload=payload,created_at=NOW.isoformat())
    return handle_science_request(env,secret=KEY,signature=sign_envelope(env,KEY) if signature is None else signature,seen=set() if seen is None else seen,permitted={"research.profile.validate"} if permitted is None else permitted,now=NOW)
def test_valid_profile_no_owner_attestation():
    r=invoke({"critic_profile":PROFILE,"user_profile_approved":True})
    assert r["engine_result"]["validation"]=="STRUCTURE_VALID" and r["engine_result"]["approval_independently_verified"] is False
    assert r["scientific_approval"] is False
def test_missing_profile():
    with pytest.raises(ValueError):invoke({})
def test_unsupported_protocol():
    with pytest.raises(ValueError):validate_profile({"critic_profile":{**PROFILE,"protocol":"Other"}})
def test_no_permission():
    with pytest.raises(ValueError):invoke({"critic_profile":PROFILE},permitted={"research.evidence.preflight"})
def test_bad_signature():
    with pytest.raises(ValueError):invoke({"critic_profile":PROFILE},signature="0"*64)
def test_replay():
    seen=set();invoke({"critic_profile":PROFILE},seen=seen)
    with pytest.raises(ValueError):invoke({"critic_profile":PROFILE},seen=seen)
def test_approval_not_claimed():
    r=invoke({"critic_profile":PROFILE})
    assert not r["engine_result"]["approval_claimed"]
