import pytest
from krc_research.offline_scholarly_cycle import run_offline_cycle
BASE = {"user_profile_approved": True, "source_manifest_sha256": "a"*64,
        "search_runs": [], "sources": [], "claims": []}
def accept(req):
    return {"stage": req["stage"], "accepted": True}
def test_four_stages():
    out=run_offline_cycle(BASE, accept)
    assert len(out["stages"])==4 and out["publication_gate"]=="NO_GO"
    assert out["transport"]=="INJECTED_TEST_ONLY" and not out["network_tested"]
def test_bad_transport_denied():
    with pytest.raises(ValueError):run_offline_cycle(BASE,None)
def test_mismatched_ack_denied():
    with pytest.raises(ValueError):run_offline_cycle(BASE,lambda req:{"stage":"wrong","accepted":True})
def test_transport_denial():
    with pytest.raises(ValueError):run_offline_cycle(BASE,lambda req:{"stage":req["stage"],"accepted":False})
def test_unapproved_denied():
    with pytest.raises(ValueError):run_offline_cycle({**BASE,"user_profile_approved":False}, accept)
def test_no_evidence_does_not_approve():
    out=run_offline_cycle({**BASE,"claims":[{"claim_id":"C01","required":2,"evidence":[]}]},accept)
    assert out["stages"]["critic_review"]["claims"][0]["verdict"]=="SHORTFALL"
    assert not out["scientific_approval"]
def test_stops_on_second_stage():
    calls=[]
    def handler(req):
        calls.append(req["stage"])
        return {"stage":req["stage"],"accepted":req["stage"]!="source_verify"}
    with pytest.raises(ValueError):run_offline_cycle(BASE,handler)
    assert calls==["source_search","source_verify"]
