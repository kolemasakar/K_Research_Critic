import hashlib
import pytest
from krc_research.stage131_project_research_route import ProjectResearchRoute, RouteDenied
from krc_research.stage131_n39_single_owner_chat_consent import canonical

PROFILE={"purpose":"Synthetic offline profile validation only",
 "policy":"FREE_ONLY_OFFLINE","operation":"research.profile.validate",
 "payload":{"critic_profile":{"profile_id":"synthetic-n39","version":"1",
 "protocol":"KRC Core","topic":"Synthetic fixture"},"user_profile_approved":True}}

def test_real_route_persisted_approval_dispatch_artifact_cancel(tmp_path):
    root=tmp_path/"private"
    p=ProjectResearchRoute(root).propose(PROFILE)
    rid,digest=p["request_id"],p["profile_sha256"]
    with pytest.raises(RouteDenied,match="APPROVAL_REQUIRED"):
        ProjectResearchRoute(root).run(rid,digest)
    with pytest.raises(RouteDenied,match="PROFILE_MISMATCH"):
        ProjectResearchRoute(root).decide(rid,"0"*64,"APPROVE")
    assert ProjectResearchRoute(root).decide(rid,digest,"APPROVE")["status"]=="APPROVED"
    result=ProjectResearchRoute(root).run(rid,digest)
    out=ProjectResearchRoute(root).read(rid)
    assert out["descriptor"]==result
    assert out["result"]["engine_result"]["validation"]=="STRUCTURE_VALID"
    assert out["result"]["scientific_approval"] is False
    assert hashlib.sha256(canonical(out["result"])).hexdigest()==result["artifact"]["sha256"]
    with pytest.raises(RouteDenied,match="APPROVAL_REQUIRED"):
        ProjectResearchRoute(root).run(rid,digest)
    assert ProjectResearchRoute(root).decide(rid,digest,"CANCEL")["status"]=="CANCELLED"
    with pytest.raises(RouteDenied,match="READ_DENIED"):
        ProjectResearchRoute(root).read(rid)

def test_unapproved_cancel_never_runs(tmp_path):
    route=ProjectResearchRoute(tmp_path/"state")
    p=route.propose(PROFILE)
    route.decide(p["request_id"],p["profile_sha256"],"CANCEL")
    with pytest.raises(RouteDenied,match="APPROVAL_REQUIRED"):
        route.run(p["request_id"],p["profile_sha256"])

def test_paid_or_network_operation_denied(tmp_path):
    route=ProjectResearchRoute(tmp_path/"state")
    with pytest.raises(RouteDenied,match="INVALID_POLICY"):
        route.propose({**PROFILE,"policy":"PAID"})
    with pytest.raises(RouteDenied,match="OFFLINE_OPERATION"):
        route.propose({**PROFILE,"operation":"research.bibliography.audit"})
