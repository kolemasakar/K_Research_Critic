"""P0 isolated workflow readiness evaluator. Not a network dispatch or publication approval."""
from __future__ import annotations
import hashlib
import json

STAGES = (
    "research_start", "source_search", "source_verify", "methodology_review",
    "novelty_review", "critic_review", "manuscript_build",
    "publication_gate", "research_export",
)
IMPLEMENTED = frozenset(("research_start", "critic_review", "publication_gate", "research_export"))

def inspect_workflow(package: dict) -> dict:
    if not isinstance(package, dict):
        raise ValueError("Research package must be an object")
    if package.get("user_profile_approved") is not True:
        raise ValueError("Approved CriticProfile required")
    if not isinstance(package.get("source_manifest_sha256"), str) or len(package["source_manifest_sha256"]) != 64:
        raise ValueError("Source manifest SHA256 required")
    try:
        int(package["source_manifest_sha256"], 16)
    except ValueError as exc:
        raise ValueError("Invalid SHA256") from exc
    if package.get("scientific_approval") is True:
        raise ValueError("Untrusted package cannot approve itself")
    digest = hashlib.sha256(json.dumps(package, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()
    verified = package.get("verified_primary_sources", 0)
    if type(verified) is not int or verified < 0:
        raise ValueError("Invalid verified source count")
    missing = [s for s in STAGES if s not in IMPLEMENTED]
    return {
        "schema": "KRC-P0-WORKFLOW-READINESS-1",
        "input_sha256": digest,
        "stages": {stage: ("LOCAL_GATE_AVAILABLE" if stage in IMPLEMENTED else "NOT_IMPLEMENTED")
                   for stage in STAGES},
        "verified_primary_sources": verified,
        "critic_verdict": "REVISE",
        "publication_gate": "NO_GO",
        "scientific_approval": False,
        "service_dispatch_ready": False,
        "remaining_operations": missing,
    }
