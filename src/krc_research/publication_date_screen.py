"""Strict publication-date filters for retrieved scholarly metadata.
Dates are source-reported metadata; this cannot establish first-publication
priority, research novelty, original experiment dates or scientific accuracy.
"""
from __future__ import annotations
from datetime import date, datetime
from hashlib import sha256
import json

def _date(s):
    if not isinstance(s,str):raise ValueError("Date must be ISO YYYY-MM-DD")
    if len(s)!=10:raise ValueError("Date must be exact ISO day")
    d=date.fromisoformat(s)
    if d.isoformat()!=s:raise ValueError("Non-canonical date")
    return d

def screen_publication_dates(records,*,start,end):
    low=_date(start);high=_date(end)
    if low>high:raise ValueError("Reversed search period")
    if not isinstance(records,list) or not 1<=len(records)<=500:
        raise ValueError("1..500 records required")
    seen=set();rows=[]
    for r in records:
        if not isinstance(r,dict) or set(r)!={"source_id","doi","published_date","date_source"}:
            raise ValueError("Invalid date provenance")
        sid=r["source_id"]
        if not isinstance(sid,str) or not sid or sid in seen:
            raise ValueError("Duplicate or missing source ID")
        seen.add(sid)
        stamp=r["published_date"]
        origin=r["date_source"]
        if stamp is None:
            if origin is not None:raise ValueError("Unresolved date must not claim date source")
            verdict="UNRESOLVED_DATE"
        else:
            if not isinstance(origin,str) or not origin.strip():
                raise ValueError("Reported date requires provider")
            day=_date(stamp)
            verdict="IN_PERIOD" if low<=day<=high else "OUT_OF_PERIOD"
        rows.append({"source_id":sid,"doi":r["doi"],
                     "published_date":stamp,"date_source":origin,
                     "screening_verdict":verdict,
                     "original_publication_date_independently_verified":False})
    result={"schema":"KRC-PUBLICATION-DATE-SCREEN-1",
            "period_start":start,"period_end":end,"records":rows,
            "in_period":sum(r["screening_verdict"]=="IN_PERIOD" for r in rows),
            "out_of_period":sum(r["screening_verdict"]=="OUT_OF_PERIOD" for r in rows),
            "unresolved":sum(r["screening_verdict"]=="UNRESOLVED_DATE" for r in rows),
            "scientific_validity_verified":False}
    result["manifest_sha256"]=sha256(json.dumps(result,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
    return result
