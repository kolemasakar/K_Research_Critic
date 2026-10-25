"""KRC P0: bounded public bibliography metadata audit, not full-text validation.

Provider results are merely bibliographic checks; NEVER promote them to scientific evidence.
"""
from __future__ import annotations
from .doi_provenance import normalize_doi
from .public_metadata_adapters import crossref_doi, europepmc_doi, crossref_editorial_updates

MAX_BATCH=24

def audit_bibliography(dois: list[str], *, crossref_fetch=None, europepmc_fetch=None,
                       updates_fetch=None) -> dict:
    if not isinstance(dois,list) or not 1 <= len(dois) <= MAX_BATCH:
        raise ValueError("Provide 1..24 DOIs")
    normalized=[normalize_doi(d) for d in dois]
    if len(set(normalized))!=len(normalized):
        raise ValueError("Duplicate DOI")
    rows=[]
    for doi in normalized:
        provider_results={}
        for name, fn, transport in (
            ("crossref",crossref_doi,crossref_fetch),
            ("europepmc",europepmc_doi,europepmc_fetch),
            ("editorial_updates",crossref_editorial_updates,updates_fetch),
        ):
            try:
                provider_results[name]=fn(doi) if transport is None else fn(doi,fetch=transport)
            except Exception as exc:
                provider_results[name]={"status":"ERROR","error_type":type(exc).__name__,
                                        "detail":str(exc)[:160]}
        cross=provider_results["crossref"]
        pmc=provider_results["europepmc"]
        upd=provider_results["editorial_updates"]
        metadata_good=(cross.get("status")=="METADATA_ONLY"
                       and pmc.get("status")=="METADATA_ONLY")
        rows.append({"doi":doi, "metadata_status":"TWO_PROVIDER_MATCH" if metadata_good else "PARTIAL",
                     "has_recorded_updates": bool(upd.get("updates")),
                     "updates_status":upd.get("status","ERROR"),
                     "retraction_clearance":"NOT_ESTABLISHED",
                     "methods_results_verified":False,
                     "experimental_origins_verified":0,
                     "providers":provider_results})
    return {"schema":"KRC-BIB-1","count":len(rows),
            "two_provider_metadata_matches":sum(r["metadata_status"]=="TWO_PROVIDER_MATCH" for r in rows),
            "updates_detected":sum(r["has_recorded_updates"] for r in rows),
            "retraction_clearance":"NOT_ESTABLISHED","full_texts_inspected":0,"records":rows}
