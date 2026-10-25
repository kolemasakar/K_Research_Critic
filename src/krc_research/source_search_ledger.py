"""Offline searchable provenance manifest. No implicit web access or source verification."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Mapping
from .doi_provenance import normalize_doi

@dataclass(frozen=True)
class SearchRun:
    provider: str
    query: str
    executed_at: str | None
    hit_count: int | None
    exported_records: int | None
    filter_description: str = ""

def validate_search_run(run: SearchRun) -> dict:
    if not run.provider.strip() or not run.query.strip():
        raise ValueError("Provider and exact query required")
    for val in (run.hit_count, run.exported_records):
        if val is not None and (not isinstance(val, int) or isinstance(val, bool) or val < 0):
            raise ValueError("Invalid count")
    if run.executed_at:
        stamp = datetime.fromisoformat(run.executed_at.replace("Z", "+00:00"))
        if stamp.tzinfo is None or stamp.utcoffset() is None:
            raise ValueError("Timestamp requires timezone")
    ready = run.executed_at is not None and run.hit_count is not None and run.exported_records is not None
    return {"status": "REPRODUCIBLE_LOG" if ready else "PARTIAL_LOG",
            "provider": run.provider, "query": run.query,
            "hit_count": run.hit_count if run.hit_count is not None else "COUNT_UNAVAILABLE"}

def reconcile_source_record(record: Mapping) -> dict:
    """Metadata validation, never scientific-claim inspection."""
    raw = record.get("doi")
    doi = normalize_doi(raw) if raw else None
    status = record.get("access_status", "UNKNOWN")
    if status not in {"FULL_TEXT", "METHODS_RESULTS_EXCERPT", "ABSTRACT_ONLY",
                      "METADATA_ONLY", "INACCESSIBLE", "UNKNOWN"}:
        raise ValueError("Invalid access status")
    if not record.get("title") or not record.get("url"):
        raise ValueError("Missing source identity")
    return {"doi": doi, "title": record["title"], "url": record["url"],
            "access_status": status,
            "doi_metadata_verified": bool(record.get("doi_metadata_verified", False)),
            "retraction_checked": bool(record.get("retraction_checked", False)),
            "methods_results_reinspected": bool(record.get("methods_results_reinspected", False)),
            "verification_status": "REVIEW_REQUIRED"}
