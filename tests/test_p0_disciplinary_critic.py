import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.disciplinary_critic import scientific_review,DIMENSIONS
def review():
    return {"claim_id":"C01","reviewer_id":"reviewer-A","conclusion":"CONDITIONAL_PASS",
            "dimensions":{key:{"verdict":"ADEQUATE","rationale":"Reviewer checked source evidence",
                         "source_ids":["S01"],"passage_locators":["page 2"]}
                          for key in DIMENSIONS}}
def test_authenticated_complete_review_still_not_scientific_proof():
    r=scientific_review(review(),verified_source_ids={"S01"},reviewer_authenticated=True)
    assert r["verdict"]=="CONDITIONAL_REVIEW_PASS" and not r["scientific_truth_verified"]
def test_review_without_auth_does_not_pass():
    r=scientific_review(review(),verified_source_ids={"S01"})
    assert r["verdict"]=="REVISE"
def test_source_not_verified_blocks_all_dimensions():
    r=scientific_review(review(),verified_source_ids=set(),reviewer_authenticated=True)
    assert r["verdict"]=="REVISE" and len(r["shortfalls"])==10
def test_counterevidence_shortfall_blocks():
    p=review();p["dimensions"]["counterevidence"]["verdict"]="SHORTFALL"
    r=scientific_review(p,verified_source_ids={"S01"},reviewer_authenticated=True)
    assert "counterevidence" in r["shortfalls"] and r["verdict"]=="REVISE"
def test_methodology_gap_blocks():
    p=review();p["dimensions"]["uncertainty"]["passage_locators"]=[]
    assert scientific_review(p,verified_source_ids={"S01"},reviewer_authenticated=True)["verdict"]=="REVISE"
def test_missing_dimension_rejected():
    p=review();p["dimensions"].pop("novelty")
    with pytest.raises(ValueError):scientific_review(p,verified_source_ids={"S01"})
def test_missing_rationale_rejected():
    p=review();p["dimensions"]["study_design"]["rationale"]=""
    with pytest.raises(ValueError):scientific_review(p,verified_source_ids={"S01"})
