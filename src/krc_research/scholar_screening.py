"""Deterministic scholarly study selection ledger for a bounded retrieved corpus.

Inclusion or exclusion rationale is explicit. A screening decision does not
mean a paper was read or its scientific conclusions independently verified.
"""
from __future__ import annotations
from hashlib import sha256
import json

STATUS={"INCLUDE","EXCLUDE","UNRESOLVED"}
ACCESS={"FULL_TEXT","METHODS_RESULTS_EXCERPT","ABSTRACT_ONLY","METADATA_ONLY","INACCESSIBLE"}
MAX_STUDIES=500
def screen_studies(records:list[dict],*,search_log:dict)->dict:
    if not isinstance(records,list) or not 1<=len(records)<=MAX_STUDIES:
        raise ValueError("1..500 study records required")
    if not isinstance(search_log,dict) or set(search_log)!={"provider","query","executed_at","results_total"}:
        raise ValueError("Complete search log required")
    if not isinstance(search_log["provider"],str) or not search_log["provider"].strip():
        raise ValueError("Search provider required")
    if not isinstance(search_log["query"],str) or not search_log["query"].strip():
        raise ValueError("Exact search query required")
    from datetime import datetime
    stamp=datetime.fromisoformat(search_log["executed_at"].replace("Z","+00:00"))
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise ValueError("Search timestamp must include timezone")
    total=search_log["results_total"]
    if not isinstance(total,int) or isinstance(total,bool) or total<len(records):
        raise ValueError("Search total cannot be less than exported records")
    identifiers=set();output=[]
    for raw in records:
        if not isinstance(raw,dict) or set(raw)!={"source_id","doi","title","origin_id","access","decision","reason"}:
            raise ValueError("Invalid screening entry")
        sid=raw["source_id"]
        if not isinstance(sid,str) or not sid.strip() or sid in identifiers:
            raise ValueError("Duplicate or invalid source ID")
        identifiers.add(sid)
        if not isinstance(raw["title"],str) or not raw["title"].strip():
            raise ValueError("Study title absent")
        if raw["access"] not in ACCESS or raw["decision"] not in STATUS:
            raise ValueError("Unknown access/decision")
        if not isinstance(raw["reason"],str) or not raw["reason"].strip():
            raise ValueError("Screening justification required")
        if raw["decision"]=="INCLUDE" and not raw["origin_id"]:
            raise ValueError("Included study requires an origin ID")
        output.append({"source_id":sid,"doi":raw["doi"],"title":raw["title"],
                       "origin_id":raw["origin_id"],"access":raw["access"],
                       "decision":raw["decision"],"reason":raw["reason"],
                       "eligible_as_verified_scientific_evidence":False})
    digest=sha256(json.dumps({"search":search_log,"records":output},
                    sort_keys=True,separators=(",",":"),ensure_ascii=False,
                    allow_nan=False).encode()).hexdigest()
    counts={v:sum(x["decision"]==v for x in output) for v in sorted(STATUS)}
    return {"schema":"KRC-SCHOLARLY-SCREENING-1","screening_sha256":digest,
            "search_log":search_log,"screening_counts":counts,
            "records":output,"reproducible_screening_record":True,
            "source_content_independently_verified":False,
            "scientific_publication_ready":False}
