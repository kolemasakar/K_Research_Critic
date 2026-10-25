"""FREE_ONLY read-only discovery with bounded Crossref/OpenAlex provider records.

Metadata is not evidence of scientific validity. Network failures are reported
rather than silently converted to empty results or successful searches.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

HOSTS={"api.crossref.org","api.openalex.org"}
MAX_BYTES=1_500_000

def fetch_public_json(url: str) -> dict:
    parts=urlsplit(url)
    if parts.scheme!="https" or parts.hostname not in HOSTS or parts.username or parts.password:
        raise ValueError("Non-approved bibliography provider")
    if parts.hostname=="api.crossref.org" and parts.path!="/works":
        raise ValueError("Crossref path not allowed")
    if parts.hostname=="api.openalex.org" and parts.path!="/works":
        raise ValueError("OpenAlex path not allowed")
    with urlopen(Request(url,headers={"User-Agent":"KRC-Scientific-Discovery/0.1 (free metadata only)",
                                     "Accept":"application/json"}), timeout=12) as r:
        if urlsplit(r.geturl()).hostname not in HOSTS:
            raise ValueError("Redirected outside approved providers")
        raw=r.read(MAX_BYTES+1)
    if len(raw)>MAX_BYTES:
        raise ValueError("Provider response exceeds size cap")
    payload=json.loads(raw)
    if not isinstance(payload,dict):
        raise ValueError("Invalid provider payload")
    return payload

def discover_metadata(query:str,*,provider:str,limit:int=5,fetch=fetch_public_json,now=None)->dict:
    if not isinstance(query,str) or not 4<=len(query.strip())<=200:
        raise ValueError("Query length 4..200 required")
    if provider not in {"Crossref","OpenAlex"}:
        raise ValueError("Unsupported provider")
    if not isinstance(limit,int) or isinstance(limit,bool) or not 1<=limit<=10:
        raise ValueError("Result cap 1..10 required")
    q=query.strip()
    if provider=="Crossref":
        url="https://api.crossref.org/works?"+urlencode({"query.bibliographic":q,"rows":limit})
    else:
        url="https://api.openalex.org/works?"+urlencode({"search":q,"per-page":limit})
    stamp=(now or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
    try:
        payload=fetch(url)
        if provider=="Crossref":
            if payload.get("status")!="ok" or not isinstance(payload.get("message"),dict):
                raise ValueError("Invalid Crossref data")
            block=payload["message"]
            total=block.get("total-results")
            items=block.get("items")
        else:
            block=payload
            total=block.get("meta",{}).get("count")
            items=block.get("results")
        if not isinstance(total,int) or isinstance(total,bool) or total<0 or not isinstance(items,list):
            raise ValueError("Malformed provider result counts")
        records=[]
        for x in items[:limit]:
            if not isinstance(x,dict):
                continue
            doi=x.get("DOI") if provider=="Crossref" else x.get("doi")
            title=(x.get("title") or [""])[0] if provider=="Crossref" else (x.get("display_name") or "")
            if provider=="Crossref":
                identifier=doi
                url_record=x.get("URL")
            else:
                identifier=x.get("id")
                url_record=x.get("primary_location",{}).get("landing_page_url") if isinstance(x.get("primary_location"),dict) else None
            if not isinstance(title,str) or not title.strip() or not isinstance(identifier,str) or not identifier:
                continue
            records.append({"provider_id":identifier,"title":title.strip(),
                            "doi":doi if isinstance(doi,str) else None,
                            "url":url_record if isinstance(url_record,str) else None,
                            "evidence_access":"METADATA_ONLY"})
        canonical=json.dumps({"provider":provider,"query":q,"url":url,"total":total,
                              "records":records},sort_keys=True,separators=(",",":"),
                              ensure_ascii=False).encode()
        return {"schema":"KRC-DISCOVERY-1","status":"METADATA_RETRIEVED","provider":provider,
                "query":q,"request_url":url,"executed_at":stamp,
                "results_total":total,"exported_records":len(records),
                "response_digest":hashlib.sha256(canonical).hexdigest(),
                "records":records,"scientific_evidence_verified":False}
    except Exception as exc:
        return {"schema":"KRC-DISCOVERY-1","status":"PROVIDER_FAILURE",
                "provider":provider,"query":q,"request_url":url,"executed_at":stamp,
                "error_type":type(exc).__name__,
                "results_total":None,"exported_records":0,"records":[],
                "scientific_evidence_verified":False}

def reconcile_discovery(results:list[dict])->dict:
    """Cross-provider DOI matches are two catalog records, not two studies."""
    if not isinstance(results,list) or len(results)!=2:
        raise ValueError("Expected both catalog query outputs")
    if {x.get("provider") for x in results}!={"Crossref","OpenAlex"}:
        raise ValueError("Both named catalogs required")
    if any(x.get("status")!="METADATA_RETRIEVED" for x in results):
        return {"schema":"KRC-DISCOVERY-CROSSCHECK-1","status":"PARTIAL",
                "matching_dois":[],"scientific_evidence_verified":False}
    def dois(row):
        values=set()
        for item in row["records"]:
            doi=item.get("doi")
            if not isinstance(doi,str):
                continue
            doi=doi.lower().strip()
            for prefix in ("https://doi.org/","http://doi.org/","doi:"):
                if doi.startswith(prefix):
                    doi=doi[len(prefix):]
            if doi.startswith("10.") and "/" in doi:
                values.add(doi)
        return values
    x=next(row for row in results if row["provider"]=="Crossref")
    y=next(row for row in results if row["provider"]=="OpenAlex")
    matching=sorted(dois(x)&dois(y))
    return {"schema":"KRC-DISCOVERY-CROSSCHECK-1",
            "status":"CROSS_PROVIDER_METADATA_MATCH" if matching else "NO_SHARED_DOIS_IN_RETURNED_PAGE",
            "matching_dois":matching,"unique_matched_works":len(matching),
            "scientific_evidence_verified":False,"independent_experimental_origins_verified":0}
