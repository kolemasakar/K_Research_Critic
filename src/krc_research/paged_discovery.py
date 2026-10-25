"""Bounded, logged multi-page FREE_ONLY scholarly metadata searches.

A PRISMA-style flow is a local searched-record accounting summary, never
a claim of a complete systematic review or independent full-text inspection.
"""
from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from urllib.parse import urlencode
from .public_discovery import fetch_public_json
from .doi_provenance import normalize_doi

def paged_discovery(query,provider,*,page_size=5,max_pages=3,fetch=fetch_public_json,now=None):
    if not isinstance(query,str) or not 4<=len(query.strip())<=200:
        raise ValueError("Query must contain 4..200 characters")
    if provider not in ("Crossref","OpenAlex"):
        raise ValueError("Provider not supported")
    if not isinstance(page_size,int) or isinstance(page_size,bool) or not 1<=page_size<=10:
        raise ValueError("Invalid page size")
    if not isinstance(max_pages,int) or isinstance(max_pages,bool) or not 1<=max_pages<=5:
        raise ValueError("Invalid page cap")
    stamp=(now or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
    entries=[];pages=[];seen=set();total=None;stop="MAX_PAGES_REACHED"
    for page in range(1,max_pages+1):
        params={"query.bibliographic":query.strip(),"rows":page_size,"offset":(page-1)*page_size} if provider=="Crossref" else {"search":query.strip(),"per-page":page_size,"page":page}
        url=("https://api.crossref.org/works?" if provider=="Crossref" else "https://api.openalex.org/works?")+urlencode(params)
        try:
            payload=fetch(url)
            if provider=="Crossref":
                if payload.get("status")!="ok": raise ValueError("Crossref status invalid")
                block=payload.get("message",{})
                items=block.get("items")
                count=block.get("total-results")
            else:
                items=payload.get("results")
                count=payload.get("meta",{}).get("count")
            if not isinstance(items,list) or not isinstance(count,int) or isinstance(count,bool) or count<0:
                raise ValueError("Invalid result page")
            total=count if total is None else total
            if total!=count:raise ValueError("Search count shifted across pages")
            page_ids=[]
            for item in items:
                if not isinstance(item,dict):continue
                ident=item.get("DOI") if provider=="Crossref" else item.get("id")
                if not isinstance(ident,str) or not ident.strip():continue
                if ident in seen:continue
                seen.add(ident)
                doi=item.get("DOI") if provider=="Crossref" else item.get("doi")
                title=(item.get("title") or [""])[0] if provider=="Crossref" else item.get("display_name")
                title=title if isinstance(title,str) else ""
                entries.append({"provider":provider,"provider_id":ident,"doi":doi,
                                "title":title,"access":"METADATA_ONLY"})
                page_ids.append(ident)
            checksum=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False,
                    separators=(",",":"),allow_nan=False).encode()).hexdigest()
            pages.append({"page":page,"url":url,"executed_at":stamp,"raw_json_sha256":checksum,
                          "raw_hits":len(items),"unique_new_hits":len(page_ids),"status":"PASS"})
            if not items:
                stop="EMPTY_PAGE";break
            if not page_ids:
                stop="NO_NEW_RECORDS";break
            if page*page_size>=count:
                stop="REACHED_REPORTED_TOTAL";break
            if len(items)<page_size:
                stop="SHORT_PAGE";break
        except Exception as exc:
            pages.append({"page":page,"url":url,"executed_at":stamp,"status":"FAIL",
                          "error_type":type(exc).__name__})
            stop="PROVIDER_FAILURE";break
    result={"schema":"KRC-PAGED-SEARCH-1","provider":provider,"query":query.strip(),
            "page_size":page_size,"max_pages":max_pages,"pages":pages,
            "stopping_reason":stop,"provider_total_hits":total,
            "returned_unique_records":len(entries),"records":entries,
            "complete_catalog_coverage":bool(total is not None and stop=="REACHED_REPORTED_TOTAL"),
            "independent_scientific_evidence_count":0}
    result["manifest_sha256"]=hashlib.sha256(json.dumps(result,sort_keys=True,ensure_ascii=False,
                        separators=(",",":")).encode()).hexdigest()
    return result

def scoped_prisma_flow(runs,*,selected_dois=()):
    if not isinstance(runs,list) or not runs or len(runs)>4:
        raise ValueError("1..4 search runs required")
    identified=sum(r["returned_unique_records"] for r in runs)
    keyset=set();without_doi=0
    for r in runs:
        if r.get("schema")!="KRC-PAGED-SEARCH-1":
            raise ValueError("Invalid search run")
        for item in r["records"]:
            try:keyset.add(normalize_doi(item["doi"]))
            except (ValueError,TypeError):without_doi+=1
    included=set(selected_dois)
    if not included<=keyset:raise ValueError("Included DOI missing from retrieved page set")
    n=len(keyset)
    return {"schema":"KRC-SCOPED-PRISMA-1","records_identified":identified,
            "duplicate_doi_records":identified-without_doi-n,"records_without_valid_doi":without_doi,
            "unique_doi_records_screened":n,"records_included_for_followup":len(included),
            "records_unresolved":n-len(included),
            "full_texts_eligibility_assessed":0,"studies_included_in_synthesis":0,
            "search_failures":sum(r["stopping_reason"]=="PROVIDER_FAILURE" for r in runs),
            "scope":"RETRIEVED_PAGES_ONLY_NOT_SYSTEMATIC_REVIEW",
            "scientific_evidence_verified":False}
