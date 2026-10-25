import sys
from pathlib import Path
from datetime import datetime,timezone,timedelta
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.reviewer_attestation import attestation_body,sign_attestation,verify_attestation
KEY=b"x"*32
NOW=datetime(2026,10,25,12,tzinfo=timezone.utc)
def verified(**edits):
    data=dict(receipt_sha256="a"*64,document_sha256="b"*64,reviewer_id="reviewer-A",
              checked_at=NOW.isoformat())
    data.update(edits)
    b=attestation_body(**data)
    return b,sign_attestation(b,KEY)
def test_happy_signature_has_narrow_scope():
    b,s=verified()
    v=verify_attestation(b,s,trusted_reviewer_keys={"reviewer-A":KEY},
       expected_receipt_sha256="a"*64,expected_document_sha256="b"*64,
       researcher_id="author-1",now=NOW)
    assert v["verified"] and not v["scientific_truth_verified"]
def test_self_review_rejected():
    b,s=verified()
    with pytest.raises(ValueError):verify_attestation(b,s,trusted_reviewer_keys={"reviewer-A":KEY},
       expected_receipt_sha256="a"*64,expected_document_sha256="b"*64,
       researcher_id="reviewer-A",now=NOW)
def test_untrusted_reviewer_rejected():
    b,s=verified()
    with pytest.raises(ValueError):verify_attestation(b,s,trusted_reviewer_keys={},
       expected_receipt_sha256="a"*64,expected_document_sha256="b"*64,
       researcher_id="author-1",now=NOW)
def test_wrong_document_hash_rejected():
    b,s=verified()
    with pytest.raises(ValueError):verify_attestation(b,s,trusted_reviewer_keys={"reviewer-A":KEY},
       expected_receipt_sha256="a"*64,expected_document_sha256="c"*64,
       researcher_id="author-1",now=NOW)
def test_modified_signed_record_rejected():
    b,s=verified();b["checked_at"]="2026-10-25T13:00:00+00:00"
    with pytest.raises(ValueError):verify_attestation(b,s,trusted_reviewer_keys={"reviewer-A":KEY},
       expected_receipt_sha256="a"*64,expected_document_sha256="b"*64,
       researcher_id="author-1",now=NOW)
def test_expired_rejected():
    b,s=verified(checked_at=(NOW-timedelta(days=32)).isoformat())
    with pytest.raises(ValueError):verify_attestation(b,s,trusted_reviewer_keys={"reviewer-A":KEY},
       expected_receipt_sha256="a"*64,expected_document_sha256="b"*64,
       researcher_id="author-1",now=NOW)
def test_future_rejected():
    b,s=verified(checked_at=(NOW+timedelta(minutes=2)).isoformat())
    with pytest.raises(ValueError):verify_attestation(b,s,trusted_reviewer_keys={"reviewer-A":KEY},
       expected_receipt_sha256="a"*64,expected_document_sha256="b"*64,
       researcher_id="author-1",now=NOW)
