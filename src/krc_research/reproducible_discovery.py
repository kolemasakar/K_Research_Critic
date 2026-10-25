"""Reproducible multi-provider discovery selection: no implicit source validation.

Deduplicates DOI aliases and preserves provider provenance, screening rationale,
unresolved records, and provider failures as separate coverage shortcomings.
"""
from __future__ import annotations
import hashlib,json
from .doi_provenance import normalize_doi

def audit_discovery_batch(results, decisions, *, require_both=True):
    if not isinstance(results,list) or not 1<=len(results)<=4:
        raise ValueError("1..4 search responses required")
    if not isinstance(decisions,dict):
        raise ValueError("Decisions mapping required")
    seen_runs=set();merged={};failed=[];unkeyed=[]
    for run in results:
        if not isinstance(run,dict) or run.get("schema")!="KRC-DISCOVERY-1":
            raise ValueError("Invalid discovery response")
        key=(run.get("provider"),run.get("query"),run.get("request_url"))
        if key in seen_runs: raise ValueError("Duplicated query run")
        seen_runs.add(key)
        if run.get("status")!="METADATA_RETRIEVED":
            failed.append({"provider":run.get("provider"),"query":run.get("query"),"error":run.get("error_type","UNKNOWN")})
            continue
        if not run.get("executed_at") or not run.get("response_digest"):
            raise ValueError("Search provenance incomplete")
        if not isinstance(run.get("records"),list) or len(run["records"])!=run.get("exported_records"):
            raise ValueError("Recorded exported count mismatch")
        for item in run["records"]:
            doi=item.get("doi")
            if not doi:
                unkeyed.append({"provider":run["provider"],"provider_id":item.get("provider_id"),"reason":"DOI_ABSENT"})
                continue
            try: normalized=normalize_doi(doi)
            except (ValueError,TypeError):
                unkeyed.append({"provider":run["provider"],"provider_id":item.get("provider_id"),"reason":"INVALID_DOI"})
                continue
            row=merged.setdefault(normalized,{"doi":normalized,"titles":set(),"providers":set(),"source_ids":set()})
            row["providers"].add(run["provider"])
            if item.get("title"):row["titles"].add(item["title"])
            row["source_ids"].add(str(item.get("provider_id")))
    if require_both and {"Crossref","OpenAlex"}-set(run.get("provider") for run in results):
        raise ValueError("Two required providers absent")
    unknown=set(decisions)-set(merged)
    if unknown: raise ValueError("Decisions for nonretrieved DOIs")
    records=[]
    for doi,row in sorted(merged.items()):
        item=decisions.get(doi)
        if not isinstance(item,dict) or set(item)!={"decision","reason"}:
            decision,reason="UNRESOLVED","NO_DOCUMENTED_SCREENING_DECISION"
        else:
            decision,reason=item["decision"],item["reason"]
            if decision not in {"INCLUDE","EXCLUDE","UNRESOLVED"} or not isinstance(reason,str) or not reason.strip():
                raise ValueError("Invalid screening decision or rationale")
        records.append({"doi":doi,"decision":decision,"reason":reason,
                        "providers":sorted(row["providers"]),"provider_ids":sorted(row["source_ids"]),
                        "titles":sorted(row["titles"]),"experimental_origins_verified":0,
                        "scientific_content_verified":False})
    serial={"runs":[{"provider":r.get("provider"),"query":r.get("query"),
                     "url":r.get("request_url"),"executed_at":r.get("executed_at"),
                     "response_digest":r.get("response_digest"),"status":r.get("status")}
                    for r in results],"records":records,"failures":failed,"unkeyed":unkeyed}
    digest=hashlib.sha256(json.dumps(serial,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
    return {"schema":"KRC-REPRODUCIBLE-DISCOVERY-1",
            "status":"PARTIAL" if failed or unkeyed or any(x["decision"]=="UNRESOLVED" for x in records) else "SCREENED_METADATA_ONLY",
            "manifest_sha256":digest,"unique_doi_records":len(records),
            "records":records,"provider_failures":failed,"unkeyed_records":unkeyed,
            "runs":serial["runs"],"independent_experimental_origins_verified":0,
            "publication_ready":False}
