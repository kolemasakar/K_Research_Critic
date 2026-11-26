"""Stage134 offline DOI, metadata provenance and source-lineage audit.

Never contacts providers. A supplied hash proves consistency with the supplied
JSON snapshot, not that Crossref/Europe PMC actually served it. Client-declared
lineage does not prove independent scientific origin or source inspection.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from jsonschema import Draft202012Validator, FormatChecker

from .stage131_bibliography_http import _safe_url
from .stage131_bibliography_probe import europe_pmc_query_url
from .stage131_bibliography_reconcile import reconcile_metadata

_ROOT = Path(__file__).resolve().parents[2]
_INPUT_SCHEMA = _ROOT / "schemas/stage134/bibliography_provenance_input_v1.schema.json"
_RESULT_SCHEMA = _ROOT / "schemas/stage134/bibliography_provenance_result_v1.schema.json"
_DOI = re.compile(r"10\.[0-9]{4,9}/[A-Za-z0-9._;()/:+\-]{1,180}\Z", re.ASCII)
_SHA = re.compile(r"[a-f0-9]{64}\Z", re.ASCII)
_MAX_BUNDLE_BYTES = 524288
_MAX_CAPTURE_BYTES = 262144


class Stage134Denied(ValueError):
    """Deterministic fail-closed data-contract rejection."""


def _canonical(value):
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError, OverflowError, RecursionError, UnicodeError):
        raise Stage134Denied("NON_CANONICAL_JSON") from None


def normalize_stage134_doi(value):
    """Restricted, lossless ASCII DOI subset; ambiguous DOI variants are rejected."""
    if not isinstance(value, str) or _DOI.fullmatch(value) is None:
        raise Stage134Denied("INVALID_DOI")
    if any(x in (".", "..") for x in value.split("/")):
        raise Stage134Denied("INVALID_DOI")
    return value.lower()


def _schema(filename):
    return json.loads((_ROOT / "schemas/stage134" / filename).read_text(encoding="utf-8"))


def _check_schema(value, filename, denial):
    schema = _schema(filename)
    if not Draft202012Validator(schema, format_checker=FormatChecker()).is_valid(value):
        raise Stage134Denied(denial)


def _captured_at(value):
    try:
        if not isinstance(value, str) or value.endswith("z"):
            raise ValueError()
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.utcoffset() is not None
    except ValueError:
        return False


def _expected_provider_url(provider, doi):
    if provider == "crossref":
        return "https://api.crossref.org/works/" + quote(doi, safe="")
    if provider == "europe_pmc":
        return europe_pmc_query_url(doi)
    raise Stage134Denied("INVALID_PROVIDER")


def _snapshot(capture, doi):
    provider = capture["provider"]
    url = capture["url"]
    if url != _expected_provider_url(provider, doi) or _safe_url(url) != provider:
        raise Stage134Denied("CAPTURE_URL_MISMATCH")
    if not _captured_at(capture["captured_at"]):
        raise Stage134Denied("INVALID_CAPTURE_TIMESTAMP")
    payload = capture["payload"]
    raw = _canonical(payload)
    if len(raw) > _MAX_CAPTURE_BYTES:
        raise Stage134Denied("CAPTURE_TOO_LARGE")
    digest = hashlib.sha256(raw).hexdigest()
    if not _SHA.fullmatch(capture["payload_sha256"]) or digest != capture["payload_sha256"]:
        raise Stage134Denied("CAPTURE_HASH_MISMATCH")
    if provider == "crossref":
        msg = payload.get("message")
        if not isinstance(msg, dict) or not isinstance(msg.get("DOI"), str):
            raise Stage134Denied("INVALID_CROSSREF_RESPONSE")
        status = "MATCH" if normalize_stage134_doi(msg["DOI"]) == doi else "MISMATCH"
    else:
        result_list = payload.get("resultList")
        if not isinstance(result_list, dict) or not isinstance(result_list.get("result"), list):
            raise Stage134Denied("INVALID_EUROPE_PMC_RESPONSE")
        items = result_list["result"]
        if len(items) > 128 or any(not isinstance(item, dict) for item in items):
            raise Stage134Denied("INVALID_EUROPE_PMC_RESPONSE")
        hits = [item for item in items if isinstance(item.get("doi"), str)
                and normalize_stage134_doi(item["doi"]) == doi]
        if len(hits) > 1:
            raise Stage134Denied("DUPLICATE_PROVIDER_RECORD")
        status = ("MATCH" if hits else
                  "NOT_FOUND" if not items else "MISMATCH")
    return {"provider": provider, "url": url, "captured_at": capture["captured_at"],
            "payload_sha256": digest, "doi_status": status,
            "integrity_status": "CANONICAL_PAYLOAD_HASH_MATCH_ONLY"}


def _lineage_groups(sources):
    """Collapse declared shared origins and citations; never certify independence."""
    by_id = {s["source_id"]: s for s in sources}
    if len({s["source_id"].casefold() for s in sources}) != len(sources):
        raise Stage134Denied("DUPLICATE_SOURCE_ID")
    for source in sources:
        if source["source_id"] in source["derived_from"]:
            raise Stage134Denied("LINEAGE_CYCLE")
        if any(parent not in by_id for parent in source["derived_from"]):
            raise Stage134Denied("UNKNOWN_PARENT_SOURCE")
    visited = set()
    visiting = set()

    def visit(source_id):
        if source_id in visiting:
            raise Stage134Denied("LINEAGE_CYCLE")
        if source_id in visited:
            return
        visiting.add(source_id)
        for parent in by_id[source_id]["derived_from"]:
            visit(parent)
        visiting.remove(source_id)
        visited.add(source_id)

    for source_id in by_id:
        visit(source_id)
    leader = {source_id: source_id for source_id in by_id}

    def root(source_id):
        while leader[source_id] != source_id:
            source_id = leader[source_id]
        return source_id

    def union(a, b):
        a, b = root(a), root(b)
        if a != b:
            leader[max(a, b)] = min(a, b)

    by_origin = {}
    for source in sources:
        origin = source["origin_id"].casefold()
        if origin in by_origin:
            union(source["source_id"], by_origin[origin])
        else:
            by_origin[origin] = source["source_id"]
        for parent in source["derived_from"]:
            union(source["source_id"], parent)

    groups = {}
    for source in sources:
        groups.setdefault(root(source["source_id"]), []).append(source)
    result = []
    for key in sorted(groups):
        group = groups[key]
        result.append({
            "source_ids": sorted(s["source_id"] for s in group),
            "origin_ids": sorted({s["origin_id"] for s in group}),
            "claimed_inspected_sources": sum(
                s["access"] in ("FULL_TEXT", "METHODS_RESULTS_EXCERPT")
                for s in group),
        })
    return sorted(result, key=lambda g: g["source_ids"][0])


def audit_stage134_provenance(bundle):
    """Pure, source-only audit. Never accepts network permission or scientific grants."""
    _check_schema(bundle, "bibliography_provenance_input_v1.schema.json", "INVALID_BUNDLE_SCHEMA")
    raw_bundle = _canonical(bundle)
    if len(raw_bundle) > _MAX_BUNDLE_BYTES:
        raise Stage134Denied("BUNDLE_TOO_LARGE")
    doi = normalize_stage134_doi(bundle["doi"])
    captures = {}
    snapshots = []
    for capture in bundle["captures"]:
        if capture["provider"] in captures:
            raise Stage134Denied("DUPLICATE_PROVIDER")
        snapshot = _snapshot(capture, doi)
        captures[capture["provider"]] = capture
        snapshots.append(snapshot)
    snapshots.sort(key=lambda snap: snap["provider"])
    statuses = {snap["provider"]: snap["doi_status"] for snap in snapshots}
    checks = {"title": "NOT_CHECKED", "year": "NOT_CHECKED"}
    if "MISMATCH" in statuses.values():
        metadata = "DOI_MISMATCH"
    elif statuses.get("crossref") == "MATCH" and statuses.get("europe_pmc") == "NOT_FOUND":
        metadata = "COVERAGE_GAP_METADATA_ONLY"
    elif len(captures) < 2 or "NOT_FOUND" in statuses.values():
        metadata = "PARTIAL_METADATA_ONLY"
    else:
        merged = reconcile_metadata(doi, captures["crossref"]["payload"],
                                    captures["europe_pmc"]["payload"])
        if merged["status"] == "DOI_MISMATCH":
            metadata = "DOI_MISMATCH"
        else:
            checks = merged.get("field_checks", checks)
            if merged["status"] == "FIELDS_MATCH_METADATA_ONLY":
                metadata = "TWO_PROVIDER_FIELDS_MATCH_METADATA_ONLY"
            elif "MISMATCH" in checks.values():
                metadata = "METADATA_CONFLICT_REVIEW"
            else:
                metadata = "INCOMPLETE_METADATA_REVIEW"
    lineage = _lineage_groups(bundle["sources"])
    shortfalls = ["PROVIDER_ORIGIN_NOT_AUTHENTICATED",
                  "INDEPENDENT_SCIENTIFIC_ORIGINS_NOT_VERIFIED"]
    if metadata != "TWO_PROVIDER_FIELDS_MATCH_METADATA_ONLY":
        shortfalls.append("METADATA_RECONCILIATION_INCOMPLETE")
    if bundle["sources"]:
        shortfalls.append("SOURCE_LINEAGE_SELF_DECLARED_ONLY")
    result = {
        "version": "KRC-STAGE134-BIBLIOGRAPHY-PROVENANCE-RESULT/1",
        "doi": doi,
        "input_sha256": hashlib.sha256(raw_bundle).hexdigest(),
        "metadata_status": metadata,
        "metadata_field_checks": checks,
        "provider_snapshots": snapshots,
        "provenance_status": "PROVIDER_ORIGIN_NOT_AUTHENTICATED",
        "lineage_groups": lineage,
        "scientific_independence": {
            "status": "NOT_ESTABLISHED_FROM_METADATA_OR_DECLARED_LINEAGE",
            "verified_origin_count": 0,
            "scientific_truth_verified": False,
            "full_text_verified": False,
        },
        "shortfalls": shortfalls,
        "decision": "HUMAN_EVIDENCE_REVIEW_REQUIRED",
    }
    _check_schema(result, "bibliography_provenance_result_v1.schema.json", "INVALID_RESULT_SCHEMA")
    return result
