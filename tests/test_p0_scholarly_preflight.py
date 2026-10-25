import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from krc_research.canonical_evidence_ledger import assess, Evidence
from krc_research.source_search_ledger import SearchRun
from krc_research.manuscript_gates import ManuscriptGateInput
from krc_research.scholarly_preflight import scholarly_preflight

def gate(**kwargs):
    x=dict(journal_policy_checked=True,search_audit_reproducible=True,
           primary_sources_inspected=True,novelty_reviewed=True,
           citations_validated=True,scientific_methods_audited=True,
           rights_and_ai_disclosure_done=True,human_author_approved=True)
    x.update(kwargs)
    return ManuscriptGateInput(**x)

def evidence():
    return Evidence(source_id="S1",origin_id="O1",access="FULL_TEXT",support="SUPPORTED",
                    inspected_methods_results=True,scope_matched=True,provenance_verified=True,
                    primary_url="https://example.org/")

def run(**kw):
    x=dict(provider="TestDB",query="silicon degradation",executed_at="2026-10-25T12:00:00+02:00",
           hit_count=3,exported_records=3)
    x.update(kw)
    return SearchRun(**x)

def test_full_fixture_only_ready_for_author_review():
    r=scholarly_preflight(claims=[assess("C01",1,[evidence()])],searches=[run()],manuscript=gate())
    assert r["status"]=="READY_FOR_AUTHOR_REVIEW" and r["submission_ready"] is False

def test_shortfall_blocks():
    r=scholarly_preflight(claims=[assess("C01",1,[])],searches=[run()],manuscript=gate())
    assert r["status"]=="REVISE"

def test_missing_search_count_blocks():
    r=scholarly_preflight(claims=[assess("C01",1,[evidence()])],searches=[run(hit_count=None)],manuscript=gate())
    assert r["status"]=="REVISE" and r["search_reproducibility"]=="SHORTFALL"

def test_no_search_blocks():
    r=scholarly_preflight(claims=[assess("C01",1,[evidence()])],searches=[],manuscript=gate())
    assert r["status"]=="REVISE"

def test_unapproved_author_blocks():
    r=scholarly_preflight(claims=[assess("C01",1,[evidence()])],searches=[run()],
                          manuscript=gate(human_author_approved=False))
    assert r["status"]=="REVISE"
