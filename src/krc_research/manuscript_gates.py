"""Offline gate checker for P0 manuscript acceptance. No external submissions."""
from dataclasses import dataclass, field
from typing import Sequence

@dataclass(frozen=True)
class ManuscriptGateInput:
    journal_policy_checked: bool
    search_audit_reproducible: bool
    primary_sources_inspected: bool
    novelty_reviewed: bool
    citations_validated: bool
    scientific_methods_audited: bool
    rights_and_ai_disclosure_done: bool
    human_author_approved: bool
    detector_run_records: Sequence[dict] = field(default_factory=tuple)
    detector_check_status: str = "NOT_RUN"  # actual status; detector use may require authorization
    detector_authorized: bool = False

REQUIRED = (
    "journal_policy_checked",
    "search_audit_reproducible",
    "primary_sources_inspected",
    "novelty_reviewed",
    "citations_validated",
    "scientific_methods_audited",
    "rights_and_ai_disclosure_done",
    "human_author_approved",
)

def evaluate_manuscript_gate(facts: ManuscriptGateInput) -> dict:
    missing = [key for key in REQUIRED if not getattr(facts, key)]
    if facts.detector_check_status not in {"NOT_RUN", "UNAVAILABLE", "COMPLETED"}:
        raise ValueError("Invalid detector state")
    if facts.detector_check_status == "COMPLETED" and (
        not facts.detector_authorized or not facts.detector_run_records):
        missing.append("detector_execution_provenance")
    for record in facts.detector_run_records:
        if not record.get("provider") or not record.get("checked_at") or not record.get("input_hash"):
            missing.append("detector_execution_provenance")
            break
    return {
        "status": "READY_FOR_AUTHOR_REVIEW" if not missing else "REVISE",
        "missing_gates": sorted(set(missing)),
        "detector_status": facts.detector_check_status,
        "detector_results_count": len(facts.detector_run_records),
    }
