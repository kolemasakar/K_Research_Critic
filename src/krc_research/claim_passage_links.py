"""Link claims to actual page-bound, hash-checked passages in local source files.

Verifies document bytes and precise quotation presence only. It does not infer
support, validate equations, independently review studies, or grant claim PASS.
"""
from __future__ import annotations
from .source_file_inspection import inspect_source_file

def verify_claim_passages(records,*,approved_root):
    if not isinstance(records,list) or not 1<=len(records)<=40:
        raise ValueError("1..40 claim-source passages required")
    seen=set();rows=[]
    for item in records:
        if not isinstance(item,dict) or set(item)!={"claim_id","source_id","path","sha256","access","passage"}:
            raise ValueError("Invalid claim passage shape")
        cid=item["claim_id"];sid=item["source_id"]
        if not isinstance(cid,str) or not cid.strip() or not isinstance(sid,str) or not sid.strip():
            raise ValueError("Claim and source IDs required")
        key=(cid,sid)
        if key in seen:raise ValueError("Duplicate claim-source locator")
        seen.add(key)
        inspection=inspect_source_file(path=item["path"],approved_root=approved_root,
            expected_sha256=item["sha256"],access=item["access"],passages=[item["passage"]])
        matching=(inspection["status"]!="HASH_MISMATCH" and
                  len(inspection["inspections"])==1 and inspection["inspections"][0]["found"])
        row={"claim_id":cid,"source_id":sid,"document_sha256":inspection["sha256"],
             "page":item["passage"]["page"],"quote_found":matching,
             "passage_sha256":inspection["inspections"][0]["exact_quote_sha256"] if matching else None,
             "status":"EXACT_PASSAGE_FOUND" if matching else "SHORTFALL",
             "independent_attestation":False,"scientific_support_verified":False}
        rows.append(row)
    return {"schema":"KRC-CLAIM-PASSAGE-1","claim_links":rows,
            "exact_quotes_found":sum(x["quote_found"] for x in rows),
            "all_quotes_found":all(x["quote_found"] for x in rows),
            "all_scientific_claims_validated":False,"publication_ready":False}
