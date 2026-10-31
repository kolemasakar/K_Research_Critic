import pytest
from krc_research.stage131_pre_dispatch_custody_gate import execute_with_custody,AuthorizationGateDenied
C={"request_id":"R","task_id":"task-0001","operation":"research.profile.validate","principal":"K_Science","profile_ref":"p","evidence_refs":[],"payload_sha256":"a"*64,"consent_ref":"grant-ref-placeholder"}
calls=[]
def dispatch(op,payload,principal,*,request_id):
    calls.append("dispatch")
    return {"task_id":payload["task_id"],"operation":op,"status":"PENDING","engine_result":{},"scientific_approval":False}
def run(authorizer,context=C):
    return execute_with_custody(dispatch,authorizer=authorizer,context=context,operation=C["operation"],payload={"task_id":C["task_id"]},principal=C["principal"],request_id=C["request_id"])
def test_missing_or_boolean_authorizer_denied_before_dispatch():
    calls.clear()
    with pytest.raises(AuthorizationGateDenied):run(True)
    with pytest.raises(AuthorizationGateDenied):run(None)
    assert not calls
def test_denied_custody_never_dispatches():
    calls.clear()
    with pytest.raises(AuthorizationGateDenied,match="CONSENT_DENIED"):run(lambda ctx:False)
    assert not calls
def test_context_binding_prevents_dispatch():
    calls.clear()
    with pytest.raises(AuthorizationGateDenied,match="CONTEXT_MISMATCH"):run(lambda ctx:True,{**C,"principal":"Other"})
    assert not calls
def test_synthetic_trusted_authorizer_permits_shape_validation_only():
    calls.clear()
    assert run(lambda ctx:True)["scientific_approval"] is False
    assert calls==["dispatch"]
