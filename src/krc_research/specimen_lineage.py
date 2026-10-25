"""Cross-paper specimen lineage gate independent of publication IDs.
A shared physical specimen can produce distinct observations, but repeated specimens
cannot be counted as independent specimen cohorts without documented rationale.
"""
from __future__ import annotations
import re

_ID = re.compile(r"^(N|K|KV)-([0-9]+)\.([0-9]+)$")

def normalize_specimen_id(value: str) -> str:
    if not isinstance(value,str): raise ValueError("Invalid specimen identifier")
    compact=value.strip().upper().replace(" ","")
    match=_ID.fullmatch(compact)
    if not match: raise ValueError("Expected N/K/KV-serial.age")
    return f"{match.group(1)}-{int(match.group(2))}.{int(match.group(3))}"

def audit_specimen_overlap(sources: list[dict]) -> dict:
    if not isinstance(sources,list) or not 2<=len(sources)<=50:
        raise ValueError("Provide 2..50 studies")
    seen_ids=set();normalized={}
    for item in sources:
        if not isinstance(item,dict) or set(item)!={"source_id","specimen_ids"}:
            raise ValueError("Invalid source lineage shape")
        source_id=item["source_id"]
        if not isinstance(source_id,str) or not source_id.strip() or source_id in seen_ids:
            raise ValueError("Duplicate or invalid source identity")
        seen_ids.add(source_id)
        ids=item["specimen_ids"]
        if not isinstance(ids,list) or not ids or len(ids)>500:
            raise ValueError("Invalid specimen list")
        clean=[normalize_specimen_id(v) for v in ids]
        if len(clean)!=len(set(clean)): raise ValueError("Duplicate specimen within study")
        normalized[source_id]=set(clean)
    pairs=[]
    keys=list(normalized)
    for i,a in enumerate(keys):
        for b in keys[i+1:]:
            overlap=sorted(normalized[a]&normalized[b])
            pairs.append({"source_a":a,"source_b":b,"common_specimens":overlap,
                          "common_count":len(overlap),
                          "independent_specimen_cohorts":len(overlap)==0})
    shared=[p for p in pairs if p["common_count"]]
    return {"schema":"KRC-SPECIMEN-LINEAGE-1","sources":keys,
            "pairs":pairs,"shared_sample_pairs":len(shared),
            "verdict":"REVIEW_OVERLAPPING_COHORTS" if shared else "NO_ID_OVERLAP_DETECTED",
            "scientific_independence_proven":False}
