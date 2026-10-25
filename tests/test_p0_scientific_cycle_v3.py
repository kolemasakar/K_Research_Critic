import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.scientific_cycle_v3 import run_scientific_cycle,sign_scientific_review
from krc_research.disciplinary_critic import DIMENSIONS
from krc_research.inspection_receipts import InspectionReceipt,audit_receipt
from krc_research.reviewer_attestation import attestation_body,sign_attestation
from datetime import datetime,timezone
from test_p0_integrated_research import fixture
KEY=b"k"*32
def review():
    return dict(claim_id="C01",reviewer_id="r-A",conclusion="CONDITIONAL_PASS",
          dimensions={name:dict(verdict="ADEQUATE",rationale="Reviewed scope and limitations",
                          source_ids=["S1"],passage_locators=["p2"]) for name in DIMENSIONS})
def signed():
    r=review();return [{"review":r,"signature":sign_scientific_review(r,KEY)}]
def source_attestations(p):
    r=InspectionReceipt(**p['inspection_receipts'][0])
    when=datetime(2026,10,25,15,tzinfo=timezone.utc).isoformat()
    b=attestation_body(receipt_sha256=audit_receipt(r)['receipt_sha256'],
      document_sha256=r.document_sha256,reviewer_id='r-A',checked_at=when)
    return [{'body':b,'signature':sign_attestation(b,KEY)}]
def test_signed_scientific_review_executes_but_no_publication():
    p=fixture()
    z=run_scientific_cycle(p,signed_reviews=signed(),source_attestations=source_attestations(p),
        trusted_reviewer_keys={"r-A":KEY},researcher_id="author",verified_source_ids={"S1"},
        now=datetime(2026,10,25,15,tzinfo=timezone.utc))
    assert z["disciplinary_gate"]=="CONDITIONAL_REVIEW_COMPLETE"
    assert not z["publication_ready"] and not z["scientific_truth_verified"]
def test_no_reviewer_blocks():
    z=run_scientific_cycle(fixture())
    assert z["disciplinary_gate"]=="REVISE"
def test_author_self_review_fails():
    with pytest.raises(ValueError):run_scientific_cycle(fixture(),signed_reviews=signed(),
        trusted_reviewer_keys={"r-A":KEY},researcher_id="r-A",verified_source_ids={"S1"})
def test_untrusted_signer_fails():
    with pytest.raises(ValueError):run_scientific_cycle(fixture(),signed_reviews=signed(),
        trusted_reviewer_keys={"r-A":b"z"*32},researcher_id="author",verified_source_ids={"S1"})
def test_missing_verified_sources_prevents_gate():
    z=run_scientific_cycle(fixture(),signed_reviews=signed(),
        trusted_reviewer_keys={"r-A":KEY},researcher_id="author")
    assert z["disciplinary_gate"]=="REVISE"
def test_changed_review_fails():
    x=signed();x[0]["review"]["dimensions"]["novelty"]["rationale"]="altered"
    with pytest.raises(ValueError):run_scientific_cycle(fixture(),signed_reviews=x,
        trusted_reviewer_keys={"r-A":KEY},researcher_id="author",verified_source_ids={"S1"})

def test_signed_disciplinary_review_without_source_signature_cannot_pass():
    z=run_scientific_cycle(fixture(),signed_reviews=signed(),
        trusted_reviewer_keys={"r-A":KEY},researcher_id="author",verified_source_ids={"S1"})
    assert z["disciplinary_gate"]=="REVISE" and z["final_status"]=="NO_GO"

def test_reused_specimens_block_conditional_scientific_acceptance():
    p=fixture()
    p["specimen_lineage"]=[
        {"source_id":"REF26","specimen_ids":["N-1.28","N-2.28","N-7.28"]},
        {"source_id":"REF27","specimen_ids":["N-1.28","N-2.28","N-7.28"]}]
    r=run_scientific_cycle(p)
    assert r["specimen_lineage_audit"]["shared_sample_pairs"]==1
    assert r["disciplinary_gate"]=="REVISE"
    assert r["final_status"]=="NO_GO"
