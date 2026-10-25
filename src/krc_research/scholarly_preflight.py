"""P0 integrated scholarly preflight; deterministic offline fixture, no tool or external calls."""
from __future__ import annotations
from .canonical_evidence_ledger import validate_assessments
from .source_search_ledger import validate_search_run, SearchRun
from .manuscript_gates import evaluate_manuscript_gate, ManuscriptGateInput

def scholarly_preflight(*, claims: list[dict], searches: list[SearchRun],
                        manuscript: ManuscriptGateInput) -> dict:
    ledger = validate_assessments(claims)
    runs = [validate_search_run(x) for x in searches]
    gate = evaluate_manuscript_gate(manuscript)
    complete_search = bool(runs) and all(r["status"] == "REPRODUCIBLE_LOG" for r in runs)
    if ledger["shortfall"] or not complete_search or gate["status"] != "READY_FOR_AUTHOR_REVIEW":
        status = "REVISE"
    else:
        status = "READY_FOR_AUTHOR_REVIEW"
    return {"status": status, "claim_ledger": ledger, "search_logs": runs,
            "search_reproducibility": "PASS" if complete_search else "SHORTFALL",
            "manuscript_gate": gate,
            "submission_ready": False,
            "reason": "Human author and journal signoff require explicit separate acceptance"}
