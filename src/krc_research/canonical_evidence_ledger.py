"""KRC P0 evidence ledger: fail-closed offline acceptance and legacy v1.4 adapter.

It checks the truth of ledger accounting, NOT the truth of a scientific publication.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping
import re

CLAIM_ID = re.compile(r"^C[0-9]{2,}$")
ALLOWED_ACCESS = {"FULL_TEXT", "METHODS_RESULTS_EXCERPT", "ABSTRACT_ONLY",
                  "METADATA_ONLY", "INACCESSIBLE", "UNKNOWN"}
INSPECTED_ACCESS = {"FULL_TEXT", "METHODS_RESULTS_EXCERPT"}

@dataclass(frozen=True)
class Evidence:
    source_id: str
    origin_id: str
    access: str
    support: str
    inspected_methods_results: bool
    scope_matched: bool
    provenance_verified: bool
    primary_url: str

def _is_eligible(e: Evidence) -> bool:
    return (e.access in INSPECTED_ACCESS and e.inspected_methods_results
            and e.support == "SUPPORTED" and e.scope_matched
            and e.provenance_verified and bool(e.origin_id.strip())
            and bool(e.source_id.strip()) and e.primary_url.startswith(("https://","http://")))

def assess(claim_id: str, required: int, evidence: list[Evidence]) -> dict:
    if not CLAIM_ID.fullmatch(claim_id):
        raise ValueError("Invalid claim ID")
    if not isinstance(required, int) or isinstance(required, bool) or required < 1:
        raise ValueError("Required evidence count must be positive")
    seen = set()
    accepted, excluded = [], []
    for e in evidence:
        if e.access not in ALLOWED_ACCESS:
            raise ValueError("Unknown evidence access")
        if _is_eligible(e) and e.origin_id not in seen:
            seen.add(e.origin_id)
            accepted.append(e.source_id)
        else:
            excluded.append(e.source_id)
    count = len(seen)
    return {"claim_id": claim_id, "required": required,
            "achieved_independent": count, "counted_origins": sorted(seen),
            "counted_sources": accepted, "excluded_sources": excluded,
            "verdict": "PASS" if count >= required else "SHORTFALL"}

def adapt_legacy_report(report: Mapping) -> dict:
    """Import legacy records without pretending to revalidate earlier source inspections.

    Previously claimed PASS stays 'reported_verdict' only.
    Independent verified counts are reset to zero until evidence-level
    observations are supplied to assess().
    """
    rows = report.get("claims")
    if not isinstance(rows, list):
        raise ValueError("Missing legacy claims")
    ids = [r.get("claim_id") for r in rows]
    if len(ids) != len(set(ids)) or any(not isinstance(i, str) or not CLAIM_ID.fullmatch(i) for i in ids):
        raise ValueError("Duplicate/invalid claim ID")
    if report.get("count") != len(rows):
        raise ValueError("Legacy count mismatch")
    converted = []
    for r in rows:
        required = r.get("required")
        if not isinstance(required, int) or isinstance(required, bool) or required < 1:
            raise ValueError("Invalid legacy required count")
        urls = r.get("evidence_urls", [])
        if not isinstance(urls, list) or any(not isinstance(u, str) for u in urls):
            raise ValueError("Invalid source URLs")
        converted.append({
            "claim_id": r["claim_id"], "assertion": r.get("assertion", ""),
            "required": required, "reported_verdict": r.get("verdict"),
            "reported_achieved": r.get("achieved_independent"),
            "reported_sources": r.get("source_ids"),
            "proposed_origins": r.get("proposed_origins"),
            "source_urls": urls, "source_access_reported": r.get("access"),
            "verification_status": "NOT_REVERIFIED_IN_THIS_IMPORT",
            "independent_assessment": assess(r["claim_id"], required, [])
        })
    return {"schema_version": "1.0", "imported_from": report.get("document_version"),
            "verification_level": "IMPORTED_UNVERIFIED",
            "claims": converted, "count": len(converted),
            "accepted_in_this_import": 0,
            "reported_prior_pass": sum(c["reported_verdict"] == "PASS" for c in converted)}

def validate_assessments(assessments: list[dict]) -> dict:
    ids = [r["claim_id"] for r in assessments]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate claim")
    for r in assessments:
        if r["achieved_independent"] != len(set(r["counted_origins"])):
            raise ValueError("Origin accounting mismatch")
        verdict = "PASS" if r["achieved_independent"] >= r["required"] else "SHORTFALL"
        if r["verdict"] != verdict:
            raise ValueError("Verdict mismatch")
    return {"count": len(ids), "pass": sum(r["verdict"] == "PASS" for r in assessments),
            "shortfall": sum(r["verdict"] == "SHORTFALL" for r in assessments),
            "status": "PASS"}
