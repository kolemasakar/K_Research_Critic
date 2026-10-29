"""Read-only DOI result classifier for Stage131 provider probes (no network I/O)."""
from urllib.parse import quote

def europe_pmc_query_url(doi):
    if not isinstance(doi,str) or not doi.startswith("10.") or len(doi)>255:
        raise ValueError("INVALID_DOI")
    if any(ch.isspace() for ch in doi):raise ValueError("INVALID_DOI")
    return "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="+quote("DOI:"+doi,safe="")+"&format=json&pageSize=1"

def classify_europe_pmc(doi, payload):
    if not isinstance(payload,dict):raise ValueError("INVALID_PROVIDER_RESPONSE")
    items=payload.get("resultList",{}).get("result",[])
    if not isinstance(items,list):raise ValueError("INVALID_PROVIDER_RESPONSE")
    matches=[x for x in items if isinstance(x,dict) and str(x.get("doi","")).casefold()==doi.casefold()]
    if not matches:return {"status":"NOT_FOUND","access":"NONE","doi":doi}
    item=matches[0]
    return {"status":"METADATA_ONLY","access":"OA_INDICATED" if item.get("isOpenAccess")=="Y" else "OA_NOT_INDICATED","doi":doi}

def classify_crossref(doi, payload):
    if not isinstance(payload,dict) or not isinstance(payload.get("message"),dict):
        raise ValueError("INVALID_PROVIDER_RESPONSE")
    found=payload["message"].get("DOI")
    if not isinstance(found,str) or found.casefold()!=doi.casefold():
        return {"status":"DOI_MISMATCH","access":"NONE","doi":doi}
    return {"status":"METADATA_ONLY","access":"UNVERIFIED","doi":doi}
