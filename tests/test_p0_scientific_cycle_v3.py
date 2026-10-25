import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.scientific_cycle_v3 import run_scientific_cycle,sign_scientific_review
from krc_research.disciplinary_critic import DIMENSIONS
from test_p0_integrated_research import fixture
KEY=b"k"*32
def review():
    return dict(claim_id="C01",reviewer_id="r-A",conclusion="CONDITIONAL_PASS",
          dimensions={name:dict(verdict="ADEQUATE",rationale="Reviewed scope and limitations",
                          source_ids=["S1"],passage_locators=["p2"]) for name in DIMENSIONS})
def signed():
    r=review();return [{"review":r,"signature":sign_scientific_review(r,KEY)}]
def test_signed_scientific_review_executes_but_no_publication():
    z=run_scientific_cycle(fixture(),signed_reviews=signed(),
        trusted_reviewer_keys={"r-A":KEY},researcher_id="author",verified_source_ids={"S1"})
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
