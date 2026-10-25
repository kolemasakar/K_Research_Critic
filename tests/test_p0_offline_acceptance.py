import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.offline_acceptance import evaluate_payload

def manuscript(**overrides):
    m=dict(journal_policy_checked=False,search_audit_reproducible=False,
           primary_sources_inspected=False,novelty_reviewed=False,
           citations_validated=False,scientific_methods_audited=False,
           rights_and_ai_disclosure_done=False,human_author_approved=False)
    m.update(overrides);return m

def test_legacy_pass_does_not_become_new_pass():
    p={"legacy_report":{"count":1,"claims":[{
        "claim_id":"C01","required":1,"verdict":"PASS","achieved_independent":1}]},
       "search_runs":[],"manuscript_gate":manuscript()}
    r=evaluate_payload(p)
    assert r["historical_report"]["reported_pass"]==1
    assert r["result"]["claim_ledger"]["pass"]==0
    assert r["final_publication_status"]=="NO_GO"

def test_real_evidence_without_search_is_revise():
    p={"claims":[{"claim_id":"C01","required":1,"evidence":[{
        "source_id":"S01","origin_id":"O01","access":"FULL_TEXT",
        "support":"SUPPORTED","inspected_methods_results":True,
        "scope_matched":True,"provenance_verified":True,
        "primary_url":"https://example.org"}]}],
        "manuscript_gate":manuscript()}
    r=evaluate_payload(p)
    assert r["result"]["claim_ledger"]["pass"]==1
    assert r["result"]["status"]=="REVISE"
