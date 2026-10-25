"""Check reported numeric literals in hash-anchored source passages.

A matching reported number and unit is not an independently validated result,
statistical inference, graph reanalysis, or experiment replication.
"""
from __future__ import annotations
from decimal import Decimal, InvalidOperation
import re
from .claim_passage_links import verify_claim_passages
NUM=re.compile(r"(?<![\d.])(-?\d+(?:\.\d+)?)(?![\d.])")

def verify_reported_numbers(rows,*,approved_root):
    if not isinstance(rows,list) or not 1<=len(rows)<=20:
        raise ValueError("1..20 numeric claims required")
    links=[]
    for row in rows:
        if not isinstance(row,dict) or set(row)!={"claim_id","source_id","path","sha256","access","passage","reported_value","reported_unit"}:
            raise ValueError("Invalid numeric claim fields")
        value=row["reported_value"];unit=row["reported_unit"]
        if isinstance(value,bool) or not isinstance(value,(int,float,str)):
            raise ValueError("Numeric value required")
        try:amount=Decimal(str(value))
        except InvalidOperation as e:raise ValueError("Numeric value invalid") from e
        if not amount.is_finite() or not isinstance(unit,str) or not 1<=len(unit)<=30:
            raise ValueError("Invalid value or unit")
        quote=row["passage"]["exact_quote"]
        numbers=[]
        for hit in NUM.finditer(quote):
            try:
                if Decimal(hit.group(1))==amount:
                    # Whole token and nearby unit are required, not a substring of 153.7.
                    trailing=quote[hit.end():].lstrip()
                    if trailing.startswith(unit) and (len(trailing)==len(unit) or not trailing[len(unit)].isalpha()):
                        numbers.append(hit.group(1))
            except InvalidOperation:
                pass
        links.append({k:row[k] for k in ("claim_id","source_id","path","sha256","access","passage")})
        row["_literal_numeric_match"]=bool(numbers)
    result=verify_claim_passages(links,approved_root=approved_root)
    out=[]
    for row,verified in zip(rows,result["claim_links"]):
        accepted=verified["quote_found"] and row["_literal_numeric_match"]
        out.append({"claim_id":row["claim_id"],"source_id":row["source_id"],
                    "page":row["passage"]["page"],"reported_value":str(row["reported_value"]),
                    "reported_unit":row["reported_unit"],
                    "status":"LITERAL_NUMBER_IN_SOURCE" if accepted else "SHORTFALL",
                    "literal_quote_found":verified["quote_found"],
                    "scientific_numeric_result_validated":False})
        del row["_literal_numeric_match"]
    return {"schema":"KRC-NUMERIC-QUOTE-1","matches":sum(x["status"]=="LITERAL_NUMBER_IN_SOURCE" for x in out),
            "rows":out,"scientific_results_validated":False,"publication_ready":False}
