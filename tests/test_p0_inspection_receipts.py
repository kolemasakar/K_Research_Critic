import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.inspection_receipts import InspectionReceipt,audit_receipt,append_entry,verify_chain
def receipt(**kw):
    x=dict(source_id="S1",origin_id="O1",doi="10.1234/abc",document_sha256="a"*64,
    inspected_sections=("methods","results"),passage_locators=("p2 fig1",),
    checked_at="2026-10-25T11:00:00+02:00",inspector_id="reviewer-1",
    method="FULL_TEXT",evidence_relation="SUPPORTS",external_trace_id="trace-1",trace_verified=False)
    x.update(kw)
    return InspectionReceipt(**x)
def test_unattested_receipt_fails_closed():
    assert not audit_receipt(receipt())["eligible_for_independent_claim_review"]
def test_bare_metadata_never_accepts():
    assert not audit_receipt(receipt(method="METADATA_ONLY",trace_verified=True))["eligible_for_independent_claim_review"]
def test_missing_hash_rejected():
    assert "document_hash_missing" in audit_receipt(receipt(document_sha256="x"))["shortfalls"]
def test_verified_external_trace_is_only_receipt_gate():
    x=audit_receipt(receipt(trace_verified=True))
    assert x["eligible_for_independent_claim_review"] and not x["scientific_truth_verified"]
def test_chain_tamper_detected():
    rows=append_entry([],{"a":1});rows=append_entry(rows,{"b":2})
    assert verify_chain(rows)["count"]==2
    rows[0]["payload"]["a"]=5
    with pytest.raises(ValueError):verify_chain(rows)
