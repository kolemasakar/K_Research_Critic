import sys
from pathlib import Path
from datetime import datetime,timezone,timedelta
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.interproject_contract import envelope,sign_envelope,validate_envelope,check_replay
KEY=b"k"*32
NOW=datetime(2026,10,25,12,0,tzinfo=timezone.utc)
def build(**changes):
    args={"task_id":"kscience-req-00001","operation":"research.evidence.preflight","payload":{"x":1},"created_at":NOW.isoformat()}
    args.update(changes)
    b=envelope(**args)
    return b,sign_envelope(b,KEY)
def test_happy_route_is_authenticated_but_not_approved():
    b,s=build()
    r=validate_envelope(b,key=KEY,signature=s,now=NOW)
    assert r["authenticated"] and not r["author_approval_provided"]
def test_payload_tamper_denied():
    b,s=build();b["payload"]["x"]=2
    with pytest.raises(ValueError):validate_envelope(b,key=KEY,signature=s,now=NOW)
def test_wrong_consumer_denied():
    b,s=build(client="Other")
    with pytest.raises(ValueError):validate_envelope(b,key=KEY,signature=s,now=NOW)
def test_unapproved_operation_denied():
    with pytest.raises(ValueError):build(operation="research.admin.delete")
def test_expired_denied():
    b,s=build(created_at=(NOW-timedelta(hours=1)).isoformat())
    with pytest.raises(ValueError):validate_envelope(b,key=KEY,signature=s,now=NOW)
def test_replay_detected_with_registry():
    seen=set();check_replay("id-001",seen)
    with pytest.raises(ValueError):check_replay("id-001",seen)
def test_bad_key_rejected():
    b,s=build()
    with pytest.raises(ValueError):validate_envelope(b,key=b"too-short",signature=s,now=NOW)
