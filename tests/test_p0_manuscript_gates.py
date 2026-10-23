import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from krc_research.manuscript_gates import ManuscriptGateInput, evaluate_manuscript_gate

def complete(**overrides):
    x=dict(journal_policy_checked=True,search_audit_reproducible=True,
      primary_sources_inspected=True,novelty_reviewed=True,citations_validated=True,
      scientific_methods_audited=True,rights_and_ai_disclosure_done=True,
      human_author_approved=True)
    x.update(overrides)
    return ManuscriptGateInput(**x)

def test_demo_cannot_pass():
    r=evaluate_manuscript_gate(complete(journal_policy_checked=False,
      search_audit_reproducible=False, primary_sources_inspected=False,
      novelty_reviewed=False, human_author_approved=False))
    assert r["status"]=="REVISE" and len(r["missing_gates"])==5

def test_no_detector_never_becomes_fake_score():
    r=evaluate_manuscript_gate(complete())
    assert r["status"]=="READY_FOR_AUTHOR_REVIEW" and r["detector_status"]=="NOT_RUN"
    assert r["detector_results_count"]==0

def test_unapproved_detector_blocks_claim_of_execution():
    r=evaluate_manuscript_gate(complete(detector_check_status="COMPLETED"))
    assert "detector_execution_provenance" in r["missing_gates"]

def test_detector_requires_traceable_record():
    r=evaluate_manuscript_gate(complete(detector_check_status="COMPLETED",detector_authorized=True,
      detector_run_records=({"provider":"test","checked_at":"2026-10-23T00:00:00+03:00","input_hash":"abc"},)))
    assert r["status"]=="READY_FOR_AUTHOR_REVIEW"

def test_broken_record_blocks():
    r=evaluate_manuscript_gate(complete(detector_check_status="COMPLETED",detector_authorized=True,
      detector_run_records=({"provider":"test"},)))
    assert "detector_execution_provenance" in r["missing_gates"]
