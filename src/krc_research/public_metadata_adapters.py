"""Read-only FREE_ONLY academic metadata adapters. Never treat metadata as article inspection."""
from __future__ import annotations
import json
from urllib.request import Request, urlopen
from urllib.parse import quote, urlencode
from .doi_provenance import normalize_doi

USER_AGENT = "KRC-Scholarly-Research/0.1 (metadata-only; no paid fallback)"
MAX_BYTES = 2_000_000

def _fetch_json(url: str, timeout: int = 12) -> dict:
    if not (url.startswith("https://api.crossref.org/works/") or
            url.startswith("https://www.ebi.ac.uk/europepmc/webservices/rest/search?")):
        raise ValueError("Provider URL not allowlisted")
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=timeout) as resp:
        raw = resp.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("Metadata response too large")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("Bad metadata format")
    return payload

def crossref_doi(doi: str, *, fetch=_fetch_json) -> dict:
    normalized = normalize_doi(doi)
    p = fetch("https://api.crossref.org/works/" + quote(normalized, safe=""))
    msg = p.get("message")
    if p.get("status") != "ok" or not isinstance(msg, dict):
        raise ValueError("Invalid Crossref reply")
    if normalize_doi(msg.get("DOI", "")) != normalized:
        raise ValueError("Crossref DOI mismatch")
    return {"provider":"Crossref", "doi":normalized,
            "title":(msg.get("title") or [""])[0],
            "type":msg.get("type"), "status":"METADATA_ONLY",
            "update_records":msg.get("update-to", []),
            "relation":msg.get("relation", {}),
            "retraction_status":"NOT_CLEARED",
            "source_url":"https://api.crossref.org/works/" + quote(normalized, safe="")}

def europepmc_doi(doi: str, *, fetch=_fetch_json) -> dict:
    normalized = normalize_doi(doi)
    q = urlencode({"query":"DOI:"+normalized, "format":"json",
                   "resultType":"core", "pageSize":3})
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + q
    data = fetch(url)
    hits = data.get("resultList",{}).get("result",[])
    matching = [h for h in hits if h.get("doi") and normalize_doi(h["doi"])==normalized]
    if not matching:
        return {"provider":"EuropePMC", "doi":normalized,
                "status":"NOT_FOUND", "retraction_status":"NOT_CLEARED",
                "source_url":url}
    h = matching[0]
    return {"provider":"EuropePMC", "doi":normalized,
            "title":h.get("title"), "pmid":h.get("id"),
            "pmcid":h.get("pmcid"), "is_open_access":h.get("isOpenAccess"),
            "status":"METADATA_ONLY", "retraction_status":"NOT_CLEARED",
            "source_url":url}

def reconcile_doi(doi: str, *, crossref_fetch=_fetch_json,
                  europepmc_fetch=_fetch_json) -> dict:
    results, errors = [], {}
    for label, provider, transport in [
        ("Crossref", crossref_doi, crossref_fetch),
        ("EuropePMC", europepmc_doi, europepmc_fetch)
    ]:
        try: results.append(provider(doi, fetch=transport))
        except Exception as exc: errors[label] = type(exc).__name__ + ": " + str(exc)[:150]
    return {"doi":normalize_doi(doi), "providers":results, "errors":errors,
            "metadata_status":"PARTIAL" if errors or len(results)<2 else "RETRIEVED",
            "methods_results_verified":False,
            "independent_experiment_origins_verified":0,
            "retraction_status":"NOT_CLEARED"}
