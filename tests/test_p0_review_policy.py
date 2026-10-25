import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.review_policy import evaluate_review_policy
PASS={"verdict":"CONDITIONAL_RULE_CHECK_PASS"}
FAIL={"verdict":"REVISE"}
def test_development_works_without_human_reviewer():
    x=evaluate_review_policy(phase="DEVELOPMENT",automatic_critic=PASS)
    assert x["status"]=="INTERNAL_REVIEW_PASS" and not x["publication_ready"]
def test_development_revise():
    assert evaluate_review_policy(phase="DEVELOPMENT",automatic_critic=FAIL)["status"]=="REVISE"
def test_final_requires_external_reviewer():
    assert evaluate_review_policy(phase="FINAL_SCIENTIFIC_ACCEPTANCE",automatic_critic=PASS)["status"]=="AWAIT_EXTERNAL_REVIEWER"
def test_final_requires_author_approval():
    x=evaluate_review_policy(phase="FINAL_SCIENTIFIC_ACCEPTANCE",automatic_critic=PASS,external_reviewer_attested=True)
    assert x["status"]=="AWAIT_AUTHOR_APPROVAL"
def test_full_review_gates_not_journal_approval():
    x=evaluate_review_policy(phase="FINAL_SCIENTIFIC_ACCEPTANCE",automatic_critic=PASS,external_reviewer_attested=True,author_approved=True)
    assert x["status"]=="REVIEW_GATES_COMPLETE_NOT_PUBLICATION_APPROVAL"
    assert not x["scientific_truth_verified"] and not x["publication_ready"]
def test_reported_pass_alone_is_not_validated():
    with pytest.raises(ValueError):evaluate_review_policy(phase="DEVELOPMENT",automatic_critic={"verdict":"PASS"})
def test_bad_phase_denied():
    with pytest.raises(ValueError):evaluate_review_policy(phase="PUBLICATION",automatic_critic=PASS)
