import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
S=json.loads((Path(__file__).resolve().parents[1]/"schemas/stage131/inner_science_operation_results_v1.schema.json").read_text())
V=Draft202012Validator(S)
BASE={"task_id":"task-one","status":"PENDING","scientific_approval":False}
ENGINES={
"research.profile.validate":{"schema":"KRC-CRITICPROFILE-1","profile_id":"P","profile_version":"1","protocol":"KRC Core","validation":"STRUCTURE_VALID","approval_claimed":False,"approval_independently_verified":False,"scientific_approval":False},
"research.evidence.preflight":{"schema":"KRC-P0D-1","result":{},"historical_report":None,"final_publication_status":"AWAIT_AUTHOR_JOURNAL_SIGNOFF"},
"research.bibliography.audit":{"schema":"KRC-BIB-1","count":1,"two_provider_metadata_matches":0,"updates_detected":0,"retraction_clearance":"NOT_ESTABLISHED","full_texts_inspected":0,"records":[{}]},
"research.inspection.review":{"receipt_sha256":"a"*64,"eligible_for_independent_claim_review":False,"shortfalls":["trace"],"scientific_truth_verified":False}}
@pytest.mark.parametrize("operation",list(ENGINES))
def test_operation_fields_valid_and_fails_if_missing(operation):
    e=ENGINES[operation]
    body={**BASE,"operation":operation,"engine_result":e}
    assert V.is_valid(body)
    for field in e:
        assert not V.is_valid({**body,"engine_result":{k:v for k,v in e.items() if k!=field}}),field
@pytest.mark.parametrize("operation",list(ENGINES))
def test_reject_cross_operation_engine(operation):
    other=next(x for x in ENGINES if x!=operation)
    assert not V.is_valid({**BASE,"operation":operation,"engine_result":ENGINES[other]})
def test_preflight_revise_only_and_errors_not_invented():
    b={**BASE,"operation":"research.evidence.preflight","status":"REVISE","engine_result":{**ENGINES["research.evidence.preflight"],"final_publication_status":"NO_GO"}}
    assert V.is_valid(b)
    assert not V.is_valid({**b,"status":"ERROR"})
