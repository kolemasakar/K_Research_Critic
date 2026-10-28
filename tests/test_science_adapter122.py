from datetime import datetime, timezone
import pytest
from krc_research.science_adapter122 import ScienceAdapter122
from krc_research.interproject_contract import envelope,sign_envelope

SECRET=b's'*32
PRINCIPAL="uid:1002"

def prepared(operation="research.profile.validate",payload=None,task="stage122-test-001"):
    payload={"critic_profile":{"profile_id":"synthetic","version":"v1","protocol":"KRC Core","topic":"Synthetic"}} if payload is None else payload
    body=envelope(task_id=task,operation=operation,payload=payload,
                  created_at=datetime.now(timezone.utc).isoformat())
    return {"science_envelope":body,"science_signature":sign_envelope(body,SECRET)}

def test_real_profile_dispatch_is_called():
    adapter=ScienceAdapter122(secret=SECRET,allowed_principals={PRINCIPAL})
    out=adapter("research.profile.validate",prepared(),PRINCIPAL)
    assert out["operation"]=="research.profile.validate"
    assert out["scientific_approval"] is False

def test_foreign_principal_rejected():
    adapter=ScienceAdapter122(secret=SECRET,allowed_principals={PRINCIPAL})
    with pytest.raises(PermissionError,match="UNAUTHORIZED"):
        adapter("research.profile.validate",prepared(),"uid:999")

def test_unknown_operation_rejected():
    adapter=ScienceAdapter122(secret=SECRET,allowed_principals={PRINCIPAL})
    with pytest.raises(PermissionError,match="OPERATION_DENIED"):
        adapter("research.other",{},PRINCIPAL)

def test_bibliography_offline_default_rejected():
    adapter=ScienceAdapter122(secret=SECRET,allowed_principals={PRINCIPAL})
    with pytest.raises(PermissionError,match="OPERATION_DENIED"):
        adapter("research.bibliography.audit",prepared("research.bibliography.audit",{"dois":[]}),PRINCIPAL)

def test_bad_signature_rejected():
    adapter=ScienceAdapter122(secret=SECRET,allowed_principals={PRINCIPAL})
    request=prepared()
    request["science_signature"]="0"*64
    with pytest.raises(ValueError,match="UNAUTHORIZED"):
        adapter("research.profile.validate",request,PRINCIPAL)

def test_replay_rejected_in_same_process():
    adapter=ScienceAdapter122(secret=SECRET,allowed_principals={PRINCIPAL})
    request=prepared()
    adapter("research.profile.validate",request,PRINCIPAL)
    with pytest.raises(ValueError,match="REPLAY_REJECTED"):
        adapter("research.profile.validate",request,PRINCIPAL)
