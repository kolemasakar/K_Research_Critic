import sys
from pathlib import Path
from datetime import datetime,timezone
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.interproject_contract import envelope,sign_envelope
from krc_research.science_dispatch import handle_science_request
KEY=b"x"*32
NOW=datetime(2026,10,25,12,tzinfo=timezone.utc)
def packet(op,payload):
    body=envelope(task_id="kscience-queue-0001",operation=op,payload=payload,created_at=NOW.isoformat())
    return body,sign_envelope(body,KEY)
def invoke(op,payload,**kw):
    body,sig=packet(op,payload)
    return handle_science_request(body,secret=KEY,signature=sig,seen=kw.get("seen",set()),
                                  permitted={op},now=NOW,
                                  bibliography_fn=lambda dois:{"count":len(dois)})
def test_profile_gate_blocks_unapproved():
    with pytest.raises(ValueError):invoke("research.evidence.preflight",{"user_profile_approved":False})
def test_bibliography_uses_narrow_handler():
    x=invoke("research.bibliography.audit",{"dois":["10.1234/example"]})
    assert x["engine_result"]["count"]==1 and not x["scientific_approval"]
def test_replay_blocks_second_call():
    seen=set()
    invoke("research.bibliography.audit",{"dois":["10.1234/example"]},seen=seen)
    with pytest.raises(ValueError):invoke("research.bibliography.audit",{"dois":["10.1234/example"]},seen=seen)
def test_unmapped_admin_fails():
    with pytest.raises(ValueError):invoke("research.profile.validate",{})

def test_durable_dispatch_survives_registry_recreation():
    import tempfile
    from pathlib import Path
    from krc_research.replay_registry import ReplayRegistry
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/"replay.sqlite3"
        invoke("research.bibliography.audit",{"dois":["10.1234/example"]},seen=ReplayRegistry(path))
        with pytest.raises(ValueError):
            invoke("research.bibliography.audit",{"dois":["10.1234/example"]},seen=ReplayRegistry(path))
