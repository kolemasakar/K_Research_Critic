"""Conservative restart of a failed scholarly metadata search from its last page.

Stored successful page hashes remain original. Only missing pages are fetched.
No scientific evidence is credited by matching metadata.
"""
from __future__ import annotations
import hashlib,json
from urllib.parse import urlencode
from datetime import datetime,timezone
from .public_discovery import fetch_public_json

def canon(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,
            separators=(",",":"),allow_nan=False).encode()).hexdigest()

def resume_search(checkpoint,*,fetch=fetch_public_json,now=None):
    if not isinstance(checkpoint,dict) or checkpoint.get("schema")!="KRC-PAGED-SEARCH-1":
        raise ValueError("Invalid checkpoint")
    old_digest=checkpoint.get("manifest_sha256")
    if old_digest!=canon({k:v for k,v in checkpoint.items() if k!="manifest_sha256"}):
        raise ValueError("Checkpoint SHA mismatch")
    if checkpoint.get("stopping_reason")!="PROVIDER_FAILURE":
        raise ValueError("No failed page to resume")
    provider=checkpoint.get("provider");query=checkpoint.get("query");size=checkpoint.get("page_size");cap=checkpoint.get("max_pages")
    if provider not in ("Crossref","OpenAlex") or not isinstance(query,str) or not isinstance(size,int) or not 1<=size<=10 or not isinstance(cap,int) or not 1<=cap<=5:
        raise ValueError("Unsupported parameters")
    pages=checkpoint["pages"]
    if not pages or pages[-1].get("status")!="FAIL":raise ValueError("Missing failed last page")
    if len(pages)>cap:raise ValueError("Checkpoint exceeds page cap")
    total=checkpoint.get("provider_total_hits")
    if not isinstance(total,int) or isinstance(total,bool) or total<0:raise ValueError("Missing original count")
    prefix="https://api.crossref.org/works?" if provider=="Crossref" else "https://api.openalex.org/works?"
    def url(i):
        params={"query.bibliographic":query,"rows":size,"offset":(i-1)*size} if provider=="Crossref" else {"search":query,"per-page":size,"page":i}
        return prefix+urlencode(params)
    for i,p in enumerate(pages,1):
        if p.get("page")!=i or p.get("url")!=url(i) or (i<len(pages) and (p.get("status")!="PASS" or not p.get("raw_json_sha256"))):
            raise ValueError("Corrupted checkpoint page provenance")
    previous=checkpoint["records"]
    if len(previous)!=checkpoint["returned_unique_records"] or sum(p["unique_new_hits"] for p in pages[:-1])!=len(previous):
        raise ValueError("Corrupted record counts")
    new_pages=list(pages[:-1]);new_records=list(previous);seen={x["provider_id"] for x in previous}
    stop="MAX_PAGES_REACHED"
    for i in range(len(pages),cap+1):
        stamp=(now or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
        try:
            payload=fetch(url(i))
            if provider=="Crossref":
                if payload.get("status")!="ok":raise ValueError("Crossref bad status")
                block=payload.get("message",{})
                count=block.get("total-results");items=block.get("items")
            else:
                count=payload.get("meta",{}).get("count");items=payload.get("results")
            if count!=total or not isinstance(items,list):raise ValueError("Changed totals or malformed page")
            added=0
            for row in items:
                if not isinstance(row,dict):continue
                ident=row.get("DOI") if provider=="Crossref" else row.get("id")
                if not isinstance(ident,str) or not ident or ident in seen:continue
                seen.add(ident);added+=1
                doi=row.get("DOI") if provider=="Crossref" else row.get("doi")
                title=(row.get("title") or [""])[0] if provider=="Crossref" else row.get("display_name")
                new_records.append({"provider":provider,"provider_id":ident,"doi":doi,
                   "title":title if isinstance(title,str) else "","access":"METADATA_ONLY"})
            new_pages.append({"page":i,"url":url(i),"executed_at":stamp,
                "raw_json_sha256":canon(payload),"raw_hits":len(items),
                "unique_new_hits":added,"status":"PASS"})
            if not items:stop="EMPTY_PAGE";break
            if not added:stop="NO_NEW_RECORDS";break
            if i*size>=total:stop="REACHED_REPORTED_TOTAL";break
            if len(items)<size:stop="SHORT_PAGE";break
        except Exception as exc:
            new_pages.append({"page":i,"url":url(i),"executed_at":stamp,
                              "status":"FAIL","error_type":type(exc).__name__})
            stop="PROVIDER_FAILURE";break
    result={k:v for k,v in checkpoint.items() if k!="manifest_sha256"}
    result.update(pages=new_pages,records=new_records,stopping_reason=stop,
       returned_unique_records=len(new_records),
       complete_catalog_coverage=(stop=="REACHED_REPORTED_TOTAL"),
       resumed_from_sha256=old_digest)
    result["manifest_sha256"]=canon(result)
    return result
