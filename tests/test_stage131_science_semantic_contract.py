import copy
import pytest
from krc_research.stage131_science_semantic_contract import validate_operation_result,SemanticContractError
P={"task_id":"t","operation":"research.evidence.preflight","status":"REVISE","scientific_approval":False,"engine_result":{"schema":"KRC-P0D-1","historical_report":None,"final_publication_status":"NO_GO","result":{"status":"REVISE","claim_ledger":{"count":0,"pass":0,"shortfall":0,"status":"PASS"},"search_logs":[],"search_reproducibility":"SHORTFALL","manuscript_gate":{"status":"REVISE","missing_gates":["search"],"detector_status":"NOT_RUN","detector_results_count":0},"submission_ready":False,"reason":"author signoff"}}}
B={"task_id":"t","operation":"research.bibliography.audit","status":"PENDING","scientific_approval":False,"engine_result":{"schema":"KRC-BIB-1","count":1,"two_provider_metadata_matches":0,"updates_detected":0,"retraction_clearance":"NOT_ESTABLISHED","full_texts_inspected":0,"records":[{"doi":"10.1000/example","metadata_status":"PARTIAL","has_recorded_updates":False,"updates_status":"NOT_AVAILABLE","retraction_clearance":"NOT_ESTABLISHED","methods_results_verified":False,"experimental_origins_verified":0,"providers":{}}]}}
I={"task_id":"t","operation":"research.inspection.review","status":"PENDING","scientific_approval":False,"engine_result":{"receipt_sha256":"a"*64,"eligible_for_independent_claim_review":False,"shortfalls":["unverified"],"scientific_truth_verified":False}}
R={"task_id":"t","operation":"research.profile.validate","status":"PENDING","scientific_approval":False,"engine_result":{"schema":"KRC-CRITICPROFILE-1","profile_id":"p","profile_version":"1","protocol":"KRC Core","validation":"STRUCTURE_VALID","approval_claimed":False,"approval_independently_verified":False,"scientific_approval":False}}
@pytest.mark.parametrize("v",[P,B,I,R])
def test_valid_source_derived(v):
    assert validate_operation_result(v,task_id="t",operation=v["operation"]).startswith("SEMANTIC_")
@pytest.mark.parametrize("field,value",[
("result",{}),("final_publication_status","AWAIT_AUTHOR_JOURNAL_SIGNOFF")])
def test_preflight_rejected(field,value):
    v=copy.deepcopy(P);v["engine_result"][field]=value
    with pytest.raises(SemanticContractError):validate_operation_result(v,task_id="t",operation=v["operation"])
def test_preflight_missing_nested_claims():
    v=copy.deepcopy(P);v["engine_result"]["result"].pop("claim_ledger")
    with pytest.raises(SemanticContractError):validate_operation_result(v,task_id="t",operation=v["operation"])
@pytest.mark.parametrize("field,value",[
("count",2),("two_provider_metadata_matches",1),("full_texts_inspected",1),("updates_detected",1)])
def test_bibliography_rejected(field,value):
    v=copy.deepcopy(B);v["engine_result"][field]=value
    with pytest.raises(SemanticContractError):validate_operation_result(v,task_id="t",operation=v["operation"])
def test_inspection_false_promotion():
    v=copy.deepcopy(I);v["engine_result"]["scientific_truth_verified"]=True
    with pytest.raises(SemanticContractError):validate_operation_result(v,task_id="t",operation=v["operation"])
def test_handler_error_not_science_error():
    v=copy.deepcopy(R);v["status"]="ERROR"
    with pytest.raises(SemanticContractError):validate_operation_result(v,task_id="t",operation=v["operation"])


@pytest.mark.parametrize("case",["empty_provider","empty_query","negative_hits","detector_approved","ready_missing","origin_bool"])
def test_consumer_semantic_mismatch_regressions(case):
    v=copy.deepcopy(B if case=="origin_bool" else P)
    if case=="origin_bool":
        v["engine_result"]["records"][0]["experimental_origins_verified"]=False
    elif case=="detector_approved":
        v["engine_result"]["result"]["manuscript_gate"]["detector_status"]="APPROVED"
    elif case=="ready_missing":
        r=v["engine_result"]["result"]
        r["search_logs"]=[{"provider":"test","query":"test","hit_count":1,"status":"REPRODUCIBLE_LOG"}]
        r["search_reproducibility"]="PASS"
        r["manuscript_gate"]["status"]="READY_FOR_AUTHOR_REVIEW"
        r["status"]="READY_FOR_AUTHOR_REVIEW"
        v["engine_result"]["final_publication_status"]="AWAIT_AUTHOR_JOURNAL_SIGNOFF"
        v["status"]="PENDING"
    else:
        log={"provider":"test","query":"test","hit_count":1,"status":"REPRODUCIBLE_LOG"}
        if case=="empty_provider":log["provider"]=" "
        if case=="empty_query":log["query"]=""
        if case=="negative_hits":log["hit_count"]=-1
        v["engine_result"]["result"]["search_logs"]=[log]
    with pytest.raises(SemanticContractError):
        validate_operation_result(v,task_id="t",operation=v["operation"])
