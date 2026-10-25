"""Offline bounded research stages; not network research operations."""
from .source_search_ledger import SearchRun, validate_search_run, reconcile_source_record
from .canonical_evidence_ledger import Evidence, assess, validate_assessments
from .workflow_readiness import inspect_workflow

def execute_local_stage(stage: str, package: dict) -> dict:
    gate = inspect_workflow(package)
    if stage == "source_search":
        runs = package.get("search_runs", [])
        if not isinstance(runs, list) or len(runs) > 20:
            raise ValueError("Invalid search ledger")
        return {"stage": stage, "mode": "OFFLINE_MANIFEST_ONLY",
                "records": [validate_search_run(SearchRun(**r)) for r in runs],
                "publication_gate": "NO_GO", "scientific_approval": False}
    if stage == "source_verify":
        rows = package.get("sources", [])
        if not isinstance(rows, list) or len(rows) > 100:
            raise ValueError("Invalid source ledger")
        return {"stage": stage, "mode": "METADATA_SCREENING_ONLY",
                "records": [reconcile_source_record(r) for r in rows],
                "publication_gate": "NO_GO", "scientific_approval": False}
    if stage == "critic_review":
        claims = package.get("claims", [])
        if not isinstance(claims, list) or len(claims) > 100:
            raise ValueError("Invalid claim list")
        results = [assess(c["claim_id"], c["required"], [Evidence(**e) for e in c.get("evidence", [])]) for c in claims]
        validation = validate_assessments(results)
        return {"stage": stage, "mode": "EVIDENCE_LEDGER_ONLY",
                "claims": results, "counts": validation, "critic_verdict": "REVISE",
                "publication_gate": "NO_GO", "scientific_approval": False}
    if stage == "research_export":
        return {"stage": stage, "mode": "STATUS_RECEIPT_ONLY",
                "package_digest": gate["input_sha256"], "missing_operations":gate["remaining_operations"],
                "publication_gate": "NO_GO", "scientific_approval": False}
    raise ValueError("Research stage unavailable")
