"""Conservative metadata cross-check: never infer fulltext or scientific independence."""
from .stage131_bibliography_adapter import lookup_doi_metadata

def reconcile_metadata(doi, crossref_payload, europe_pmc_payload):
    c = crossref_payload.get("message") if isinstance(crossref_payload,dict) else None
    results = europe_pmc_payload.get("resultList",{}).get("result",[]) if isinstance(europe_pmc_payload,dict) else None
    if not isinstance(c,dict) or not isinstance(results,list):
        return {"status":"INVALID_PROVIDER_RESPONSE","doi":doi}
    e=next((v for v in results if isinstance(v,dict) and isinstance(v.get("doi"),str) and v["doi"].casefold()==doi.casefold()),None)
    if not isinstance(c.get("DOI"),str) or c["DOI"].casefold()!=doi.casefold() or e is None:
        return {"status":"DOI_MISMATCH_OR_ABSENT","doi":doi}
    def norm(v):
        return " ".join(str(v).casefold().split()) if v is not None else ""
    a=c.get("title")
    ct=norm(a[0] if isinstance(a,list) and a else None)
    et=norm(e.get("title"))
    year=None
    dateparts=c.get("published",{}).get("date-parts") if isinstance(c.get("published"),dict) else None
    if isinstance(dateparts,list) and dateparts and isinstance(dateparts[0],list) and dateparts[0]: year=dateparts[0][0]
    ey=e.get("pubYear")
    checks={
      "title":"MATCH" if ct and et and ct==et else "MISMATCH" if ct and et else "MISSING",
      "year":"MATCH" if year is not None and ey is not None and str(year)==str(ey) else "MISMATCH" if year is not None and ey is not None else "MISSING",
    }
    return {"status":"FIELDS_MATCH_METADATA_ONLY" if all(x=="MATCH" for x in checks.values()) else "REVIEW_REQUIRED",
            "doi":doi,"field_checks":checks,"full_text_verified":False,"experimental_independence_verified":False}
