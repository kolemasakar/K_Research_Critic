import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.integrated_research import execute_research
from krc_research.inspection_receipts import InspectionReceipt,audit_receipt

def fixture():
    r=dict(source_id="S1",origin_id="O1",doi="10.1234/example",
           document_sha256="a"*64,inspected_sections=["methods","results"],
           passage_locators=["page 3 figure 2"],checked_at="2026-10-25T14:00:00+02:00",
           inspector_id="independent-reviewer",method="FULL_TEXT",
           evidence_relation="SUPPORTS",external_trace_id="trace-1",trace_verified=True)
    e=dict(source_id="S1",origin_id="O1",access="FULL_TEXT",support="SUPPORTED",
           inspected_methods_results=True,scope_matched=True,provenance_verified=True,
           primary_url="https://example.org/paper")
    gate=dict(journal_policy_checked=True,search_audit_reproducible=True,
           primary_sources_inspected=True,novelty_reviewed=True,
           citations_validated=True,scientific_methods_audited=True,
           rights_and_ai_disclosure_done=True,human_author_approved=True)
    return dict(claims=[dict(claim_id="C01",required=1,evidence=[e])],
           inspection_receipts=[r],
           search_runs=[dict(provider="Crossref",query="site:doi.org physics",
             executed_at="2026-10-25T14:00:00+02:00",hit_count=1,exported_records=1)],
           manuscript_gate=gate,
           critic_rounds=[dict(round=1,revision_id="v1",critic="REVISE"),
                          dict(round=2,revision_id="v2",critic="PASS")])
def attestation(p):
    return audit_receipt(InspectionReceipt(**p["inspection_receipts"][0]))["receipt_sha256"]
def test_no_external_attestation_fail_closed():
    r=execute_research(fixture())
    assert r["status"]=="REVISE"
    assert r["claim_verdicts"][0]["verdict"]=="SHORTFALL"
    assert not r["publication_ready"]
def test_attested_source_still_requires_real_critic():
    p=fixture()
    r=execute_research(p,attested_receipt_hashes={attestation(p)})
    assert r["claim_verdicts"][0]["verdict"]=="PASS"
    assert r["status"]=="REVIEW_PENDING_INDEPENDENT_CRITIC"
    assert not r["critic_independently_executed"]
def test_duplicate_origin_only_one_independent():
    p=fixture();p["claims"][0]["required"]=2
    p["claims"][0]["evidence"].append({**p["claims"][0]["evidence"][0]})
    r=execute_research(p,attested_receipt_hashes={attestation(p)})
    assert r["claim_verdicts"][0]["achieved_independent"]==1
    assert r["claim_verdicts"][0]["verdict"]=="SHORTFALL"
def test_missing_search_log_blocks():
    p=fixture();p["search_runs"]=[]
    r=execute_research(p,attested_receipt_hashes={attestation(p)})
    assert r["status"]=="REVISE" and r["preflight"]["search_reproducibility"]=="SHORTFALL"
def test_unauthorized_critic_round_status_invalid():
    p=fixture();p["critic_rounds"][1]["critic"]="AUTO_PASS"
    with pytest.raises(ValueError):execute_research(p)
def test_repeated_revision_blocks():
    p=fixture();p["critic_rounds"][1]["revision_id"]="v1"
    with pytest.raises(ValueError):execute_research(p)
def test_self_declared_fulltext_never_enough():
    p=fixture();p["inspection_receipts"][0]["trace_verified"]=False
    r=execute_research(p,attested_receipt_hashes={attestation(p)})
    assert r["claim_verdicts"][0]["verdict"]=="SHORTFALL"
def test_no_claims_fails():
    p=fixture();p["claims"]=[]
    with pytest.raises(ValueError):execute_research(p)
