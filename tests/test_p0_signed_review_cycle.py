import sys
from datetime import datetime,timezone
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from test_p0_integrated_research import fixture
from krc_research.inspection_receipts import InspectionReceipt,audit_receipt
from krc_research.reviewer_attestation import attestation_body,sign_attestation
from krc_research.research_pipeline_v2 import run_review_cycle
KEY=b"z"*32
NOW=datetime(2026,10,25,15,tzinfo=timezone.utc)
def signed(p):
    r=InspectionReceipt(**p["inspection_receipts"][0])
    b=attestation_body(receipt_sha256=audit_receipt(r)["receipt_sha256"],
        document_sha256=r.document_sha256,reviewer_id="r1",checked_at=NOW.isoformat())
    return [{"body":b,"signature":sign_attestation(b,KEY)}]
def test_signed_review_is_eligible_but_not_published():
    p=fixture()
    r=run_review_cycle(p,attestations=signed(p),
        trusted_reviewer_keys={"r1":KEY},researcher_id="author",now=NOW)
    assert r["verified_reviewer_attestations"]==1
    assert r["research"]["claim_verdicts"][0]["verdict"]=="PASS"
    assert not r["publication_ready"]
def test_without_external_reviewer_is_shortfall():
    r=run_review_cycle(fixture())
    assert r["research"]["claim_verdicts"][0]["verdict"]=="SHORTFALL"
def test_attestation_not_from_same_author():
    p=fixture()
    with pytest.raises(ValueError):run_review_cycle(p,attestations=signed(p),
        trusted_reviewer_keys={"r1":KEY},researcher_id="r1",now=NOW)
def test_untrusted_signer_fails():
    p=fixture()
    with pytest.raises(ValueError):run_review_cycle(p,attestations=signed(p),
        trusted_reviewer_keys={"r1":b"b"*32},researcher_id="author",now=NOW)
def test_missing_server_trust_config_denied():
    p=fixture()
    with pytest.raises(ValueError):run_review_cycle(p,attestations=signed(p))
def test_mismatched_receipt_denied():
    p=fixture()
    p["inspection_receipts"][0]["document_sha256"]="e"*64
    with pytest.raises(ValueError):run_review_cycle(p,attestations=signed(fixture()),
        trusted_reviewer_keys={"r1":KEY},researcher_id="author",now=NOW)

def test_contradictory_source_is_visible_and_blocks_gate():
    p=fixture()
    contradict={**p["claims"][0]["evidence"][0],
                "source_id":"S2","origin_id":"O2","support":"CONTRADICTS"}
    p["claims"][0]["evidence"].append(contradict)
    r=run_review_cycle(p,attestations=signed(p),
        trusted_reviewer_keys={"r1":KEY},researcher_id="author",now=NOW)
    assert r["unresolved_conflicts"]
    assert r["unresolved_conflicts"][0]["source_id"]=="S2"
    assert r["final_gate"]=="NO_GO"
