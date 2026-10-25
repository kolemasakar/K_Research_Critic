import hashlib
import pytest
from jsonschema import Draft202012Validator, FormatChecker
from krc_research.private_contract_details import EVIDENCE, CLAIM, RECEIPT, ERROR_SCHEMA, sanitized_error, approval_evidence_status

@pytest.mark.parametrize("schema",[EVIDENCE,CLAIM,RECEIPT,ERROR_SCHEMA])
def test_schema_valid(schema):
    Draft202012Validator.check_schema(schema)

def test_absent_evidence_rejected():
    obj={"claim_id":"C01","required":1,"evidence":[{"source_id":"S01"}]}
    assert not Draft202012Validator(CLAIM).is_valid(obj)
def test_duplicated_claim_extraneous_key_rejected():
    assert not Draft202012Validator(CLAIM).is_valid({"claim_id":"C01","required":1,"evidence":[],"scientific_approval":True})
def test_receipt_requires_trace():
    assert not Draft202012Validator(RECEIPT).is_valid({"source_id":"S01","trace_verified":True})
def test_empty_receipt_not_accepted():
    assert list(Draft202012Validator(RECEIPT,format_checker=FormatChecker()).iter_errors({}))
def test_error_sanitized():
    x=sanitized_error("secret-path-should-not-be-in-output")
    assert x["error"]=={"code":"HANDLER_ERROR","message":"Request rejected"}
    assert Draft202012Validator(ERROR_SCHEMA).is_valid(x)
def test_approval_cannot_self_certify():
    p={"profile_id":"p","version":"1"}
    r={"profile_id":"p","profile_version":"1","approved_at":"2026-10-25T12:00:00Z","author_id":"a","trace_id":"t","profile_sha256":hashlib.sha256(b"abc").hexdigest()}
    assert approval_evidence_status(p,r)=="PRESENT_UNVERIFIED"
def test_approval_wrong_revision():
    p={"profile_id":"p","version":"2"}
    r={"profile_id":"p","profile_version":"1","approved_at":"x","author_id":"a","trace_id":"t","profile_sha256":"a"*64}
    assert approval_evidence_status(p,r)=="PROFILE_MISMATCH"
