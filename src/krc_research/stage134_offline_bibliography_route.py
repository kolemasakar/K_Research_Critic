"""Explicitly opted-in, offline-only Stage134 bibliography result adapter.

This module never imports public_metadata_adapters or any network client.
It consumes the complete caller-approved immutable snapshot bundles, not DOIs
that could trigger a provider lookup. No installation or HTTP route is implied.
"""
import hashlib
from .stage131_n39_single_owner_chat_consent import canonical
from .stage134_bibliography_provenance import (
    Stage134Denied, audit_stage134_provenance,
)

OPERATION = "research.bibliography.audit"
SCHEMA = "KRC-BIB-PROV-1"
MAX_BUNDLES = 4
MAX_PAYLOAD_BYTES = 200000


def validate_stage134_offline_payload(payload):
    """Fail closed before proposing, approving or consuming owner consent."""
    if not isinstance(payload, dict) or set(payload) != {"offline_bundles"}:
        raise Stage134Denied("OFFLINE_BUNDLES_ONLY")
    bundles = payload["offline_bundles"]
    if not isinstance(bundles, list) or not 1 <= len(bundles) <= MAX_BUNDLES:
        raise Stage134Denied("OFFLINE_BUNDLE_COUNT")
    try:
        raw = canonical(payload)
    except (TypeError, ValueError, OverflowError, RecursionError, UnicodeError):
        raise Stage134Denied("NON_CANONICAL_PAYLOAD") from None
    if len(raw) > MAX_PAYLOAD_BYTES:
        raise Stage134Denied("OFFLINE_PAYLOAD_TOO_LARGE")
    seen = set()
    for bundle in bundles:
        audit = audit_stage134_provenance(bundle)
        doi = audit["doi"]
        if doi in seen:
            raise Stage134Denied("DUPLICATE_DOI")
        seen.add(doi)
    return hashlib.sha256(raw).hexdigest()


def audit_offline_bundles(bundles):
    """Function injected into signed dispatcher only on explicit Stage134 opt-in.

    No fetch callback is reachable, and provider payloads were supplied inside
    the owner's pinned complete profile. No scientific independence is inferred.
    """
    validate_stage134_offline_payload({"offline_bundles": bundles})
    records = []
    for bundle in bundles:
        checked = audit_stage134_provenance(bundle)
        records.append({
            "doi": checked["doi"],
            "metadata_status": checked["metadata_status"],
            "metadata_field_checks": checked["metadata_field_checks"],
            "provider_snapshots": checked["provider_snapshots"],
            "provenance_status": checked["provenance_status"],
            "lineage_groups": checked["lineage_groups"],
            "scientific_independence": checked["scientific_independence"],
            "shortfalls": checked["shortfalls"],
            "decision": checked["decision"],
            "input_sha256": checked["input_sha256"],
        })
    return {
        "schema": SCHEMA,
        "count": len(records),
        "mode": "IMMUTABLE_SUPPLIED_SNAPSHOTS_ONLY",
        "network_requests": 0,
        "full_texts_inspected": 0,
        "retraction_clearance": "NOT_ESTABLISHED",
        "independent_experimental_origins_verified": 0,
        "records": records,
    }


def validate_offline_bibliography_result(engine):
    """Strict result-shape check, no promotion to scientific approval."""
    if not isinstance(engine, dict) or set(engine) != {
        "schema", "count", "mode", "network_requests",
        "full_texts_inspected", "retraction_clearance",
        "independent_experimental_origins_verified", "records",
    }:
        return False
    rows = engine["records"]
    if (engine["schema"] != SCHEMA
        or engine["mode"] != "IMMUTABLE_SUPPLIED_SNAPSHOTS_ONLY"
        or type(engine["count"]) is not int
        or not 1 <= engine["count"] <= MAX_BUNDLES
        or not isinstance(rows, list) or len(rows) != engine["count"]
        or engine["network_requests"] != 0
        or engine["full_texts_inspected"] != 0
        or engine["independent_experimental_origins_verified"] != 0
        or engine["retraction_clearance"] != "NOT_ESTABLISHED"):
        return False
    expected = {"doi", "metadata_status", "metadata_field_checks",
                "provider_snapshots", "provenance_status", "lineage_groups",
                "scientific_independence", "shortfalls", "decision",
                "input_sha256"}
    for row in rows:
        if not isinstance(row, dict) or set(row) != expected:
            return False
        independence = row["scientific_independence"]
        if (not isinstance(independence, dict)
            or independence != {
                "status": "NOT_ESTABLISHED_FROM_METADATA_OR_DECLARED_LINEAGE",
                "verified_origin_count": 0,
                "scientific_truth_verified": False,
                "full_text_verified": False,
            }
            or row["provenance_status"] != "PROVIDER_ORIGIN_NOT_AUTHENTICATED"
            or row["decision"] != "HUMAN_EVIDENCE_REVIEW_REQUIRED"
            or not isinstance(row["input_sha256"], str)
            or len(row["input_sha256"]) != 64
            or not all(c in "0123456789abcdef" for c in row["input_sha256"])
            or not isinstance(row["shortfalls"], list)
            or not isinstance(row["provider_snapshots"], list)
            or not 1 <= len(row["provider_snapshots"]) <= 2
            or not isinstance(row["lineage_groups"], list)):
            return False
        if any(not isinstance(p, dict) or
               p.get("integrity_status") != "CANONICAL_PAYLOAD_HASH_MATCH_ONLY"
               for p in row["provider_snapshots"]):
            return False
    return True
