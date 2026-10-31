import pytest
from krc_research.stage131_safe_composition import science_result_gate,artifact_read_gate,bibliography_metadata_gate,Stage131GateDenied
from krc_research.artifact_stage117 import HardenedExchange
from krc_research.artifact_exchange import ExchangeError

def test_consent_gate_prevents_dispatch():
    def forbidden(*args,**kwargs):raise AssertionError("DISPATCHED")
    with pytest.raises(Stage131GateDenied,match="CONSENT"):
        science_result_gate(forbidden,operation="research.profile.validate",payload={"task_id":"test-task-123"},principal="K_Science",request_id="R")

def test_consent_true_still_requires_correlated_result():
    def wrong(op,payload,principal,*,request_id):
        return {"task_id":"unrelated","operation":op,"status":"PENDING","engine_result":{},"scientific_approval":False}
    with pytest.raises(ValueError,match="CORRELATION_MISMATCH"):
        science_result_gate(wrong,operation="research.profile.validate",payload={"task_id":"test-task-123"},principal="K_Science",request_id="R",consent_verified=True)

def test_artifact_read_scoped_and_expired(tmp_path):
    clock=[100.0]
    store=HardenedExchange(tmp_path/"objects",free_bytes_min=0,clock=lambda:clock[0],ttl=5)
    obj=store.store_stream([b"evidence"],principal="K_Science",request_id="REQ-1",filename="a.json")
    assert artifact_read_gate(store,obj,authenticated_principal="K_Science",expected_principal="K_Science",request_id="REQ-1",now_epoch=100)==b"evidence"
    with pytest.raises(Stage131GateDenied,match="UNAUTHORIZED"):
        artifact_read_gate(store,obj,authenticated_principal="other",expected_principal="K_Science",request_id="REQ-1",now_epoch=100)
    with pytest.raises(ExchangeError):
        artifact_read_gate(store,obj,authenticated_principal="K_Science",expected_principal="K_Science",request_id="OTHER",now_epoch=100)
    clock[0]=105
    with pytest.raises(Stage131GateDenied,match="EXPIRED"):
        artifact_read_gate(store,obj,authenticated_principal="K_Science",expected_principal="K_Science",request_id="REQ-1",now_epoch=105)

def test_bibliography_default_off():
    def forbidden(*args):raise AssertionError("NETWORK")
    assert bibliography_metadata_gate("10.1000/example",fetcher=forbidden)["status"]=="PROVIDER_DISABLED"
    assert bibliography_metadata_gate("10.1000/example",provider_approved=True,fetcher=forbidden)["status"]=="PROVIDER_DISABLED"
