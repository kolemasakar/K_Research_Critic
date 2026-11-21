"""Strict input rejection and partial-trace semantic regressions.
Synthetic fixtures only. No external service or owner grant is touched.
"""
import copy
import os
import pytest
from krc_research.stage133_science_input import (
    PREFLIGHT, INSPECTION, EXTERNAL_SCHEMAS, validate_external_science_payload,
)
from krc_research.stage131_project_research_route import ProjectResearchRoute, RouteDenied
from krc_research.stage132_project_post_contract import ProjectPostBoundary, IDENTITY
from krc_research.stage132_project_post_wire import OFFLINE_OPS
from krc_research.replay_registry import ReplayRegistry
from test_stage133_offline_expansion import PAYLOADS, count

@pytest.fixture(autouse=True)
def safe_umask():
    old = os.umask(0o077)
    try:
        yield
    finally:
        os.umask(old)

def change(op, path, value, delete=False):
    result = copy.deepcopy(PAYLOADS[op])
    node = result
    for part in path[:-1]:
        node = node[part]
    if delete:
        del node[path[-1]]
    else:
        node[path[-1]] = value
    return result

INVALID_PREFLIGHT = [
    (("manuscript_gate","journal_policy_checked"), "yes"),
    (("manuscript_gate","journal_policy_checked"), None),
    (("manuscript_gate","intrusive_extra"), True),
    (("manuscript_gate","detector_check_status"), "PARTIAL"),
    (("manuscript_gate","detector_check_status"), "COMPLETED"),
    (("search_runs",), [{"provider":"Crossref","query":"concrete","executed_at":None,"hit_count":0}]),
    (("search_runs",), [{"provider":"Crossref","query":"concrete","executed_at":"2026-11-20T01:00:00", "hit_count":1,"exported_records":1}]),
    (("search_runs",), [{"provider":"Crossref","query":"concrete","executed_at":None,"hit_count":1,"exported_records":2}]),
    (("search_runs",), [{"provider":"Crossref","query":"concrete","executed_at":None,"hit_count":True,"exported_records":0}]),
    (("search_runs",), [{"provider":"","query":"concrete","executed_at":None,"hit_count":0,"exported_records":0}]),
    (("claims",), [{"claim_id":"C01","required":1,"evidence":[]},{"claim_id":"C01","required":1,"evidence":[]}]),
    (("claims",), [{"claim_id":"C01","required":True,"evidence":[]}]),
    (("claims",), [{"claim_id":"C01","required":1,"evidence":[{"source_id":"S01"}]}]),
    (("claims",), [None]),
    (("user_profile_approved",), True),
    (("unexpected",), {}),
]

INVALID_INSPECTION = [
    (("receipt","trace_verified"), True),
    (("receipt","trace_verified"), "false"),
    (("receipt","document_sha256"), "a"*63),
    (("receipt","inspected_sections"), []),
    (("receipt","inspected_sections"), [""]),
    (("receipt","passage_locators"), []),
    (("receipt","checked_at"), "2026-11-20T01:00:00"),
    (("receipt","method"), "ABSTRACT_ONLY"),
    (("receipt","source_id"), ""),
    (("receipt","extra_statement"), "verified"),
    (("receipt",), []),
]

@pytest.mark.parametrize("path,value",INVALID_PREFLIGHT)
def test_preflight_nested_denials(path,value):
    assert not validate_external_science_payload(PREFLIGHT,change(PREFLIGHT,path,value))

@pytest.mark.parametrize("path,value",INVALID_INSPECTION)
def test_inspection_nested_denials(path,value):
    assert not validate_external_science_payload(INSPECTION,change(INSPECTION,path,value))

def test_missing_required_gate_and_large_limits():
    missing=change(PREFLIGHT,("manuscript_gate","journal_policy_checked"),None,delete=True)
    assert not validate_external_science_payload(PREFLIGHT,missing)
    assert not validate_external_science_payload(PREFLIGHT,change(PREFLIGHT,("claims",),[{"claim_id":"C01","required":1,"evidence":[]}]*129))
    assert not validate_external_science_payload(INSPECTION,change(INSPECTION,("receipt","passage_locators"),["p1"]*129))

@pytest.mark.parametrize("op,path,value", [
    (PREFLIGHT,("search_runs",),[{"provider":"Crossref","query":"concrete","executed_at":None,"hit_count":2,"exported_records":3}]),
    (PREFLIGHT,("manuscript_gate","journal_policy_checked"),"not-bool"),
    (PREFLIGHT,("user_profile_approved",),True),
    (INSPECTION,("receipt","trace_verified"),True),
    (INSPECTION,("receipt","checked_at"),"yesterday"),
    (INSPECTION,("receipt","document_sha256"),"wrong"),
])
def test_invalid_already_approved_payload_never_claims(tmp_path,op,path,value):
    route=ProjectResearchRoute(tmp_path/"state")
    ReplayRegistry(route.root/"science-replay.sqlite")
    profile={"purpose":"Synthetic","policy":"FREE_ONLY_OFFLINE","operation":op,"payload":copy.deepcopy(PAYLOADS[op])}
    p=route.propose(profile)
    route.decide(p["request_id"],p["profile_sha256"],"APPROVE")
    bad=change(op,path,value)
    envelope={"version":"krc-transport/2","identity":dict(IDENTITY),"request_id":p["request_id"],"operation":op,"payload":bad}
    status,_=ProjectPostBoundary(route.root,enabled=True,enabled_operations=OFFLINE_OPS).execute(envelope,trusted_principal="K_Science")
    assert status==403
    assert count(route)==0

def test_valid_partial_search_is_revise_not_loss_of_grant(tmp_path):
    partial={"provider":"Crossref","query":"concrete","executed_at":None,"hit_count":None,"exported_records":None}
    payload=change(PREFLIGHT,("search_runs",),[partial])
    assert validate_external_science_payload(PREFLIGHT,payload)
    route=ProjectResearchRoute(tmp_path/"state")
    ReplayRegistry(route.root/"science-replay.sqlite")
    p=route.propose({"purpose":"Synthetic","policy":"FREE_ONLY_OFFLINE","operation":PREFLIGHT,"payload":payload})
    route.decide(p["request_id"],p["profile_sha256"],"APPROVE")
    envelope={"version":"krc-transport/2","identity":dict(IDENTITY),"request_id":p["request_id"],"operation":PREFLIGHT,"payload":payload}
    status,_=ProjectPostBoundary(route.root,enabled=True,enabled_operations=OFFLINE_OPS).execute(envelope,trusted_principal="K_Science")
    assert status==200
    result=route.read(p["request_id"])["result"]
    assert result["status"]=="REVISE" and result["engine_result"]["result"]["search_logs"][0]["hit_count"]=="COUNT_UNAVAILABLE"
    assert result["engine_result"]["final_publication_status"]=="NO_GO"
    assert result["scientific_approval"] is False
    assert count(route)==1

def test_invalid_proposals_rejected(tmp_path):
    route=ProjectResearchRoute(tmp_path/"state")
    for op,payload in ((PREFLIGHT,change(PREFLIGHT,("manuscript_gate","journal_policy_checked"),"string")),
                       (INSPECTION,change(INSPECTION,("receipt","passage_locators"),[""]))):
        with pytest.raises(RouteDenied,match="INVALID_SCIENCE_PAYLOAD"):
            route.propose({"purpose":"Synthetic","policy":"FREE_ONLY_OFFLINE","operation":op,"payload":payload})

def test_schema_draft_and_no_legacy_bibliography():
    assert set(EXTERNAL_SCHEMAS)=={PREFLIGHT,INSPECTION}
    assert not validate_external_science_payload("research.bibliography.audit",{"dois":["10.1/test"]})
