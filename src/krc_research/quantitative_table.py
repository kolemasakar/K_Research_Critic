"""Trace structured quantitative rows back to SHA-checked primary text.

Compares reported values/units exactly; never infers a table from a PDF or
promotes source-reported figures to independently measured truth.
"""
from __future__ import annotations
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json,re
from .source_file_inspection import inspect_source_file

_UNITS={"MPa","kPa","m/s","km/s","mm","cm","°C","%"}
def compare_table_rows(rows,*,approved_root):
    if not isinstance(rows,list) or not 1<=len(rows)<=40:
        raise ValueError("1..40 rows required")
    seen=set();results=[]
    for row in rows:
        needed={"table_id","row_id","source_id","path","sha256","access",
                "page","section","quote","value","unit"}
        if not isinstance(row,dict) or set(row)!=needed:
            raise ValueError("Table extraction must include full provenance")
        key=(row["table_id"],row["row_id"])
        if key in seen or not all(isinstance(x,str) and x.strip() for x in key):
            raise ValueError("Duplicate or empty table row")
        seen.add(key)
        if row["unit"] not in _UNITS:
            raise ValueError("Unknown unit")
        try:
            quantity=Decimal(str(row["value"]))
        except (InvalidOperation,TypeError) as exc:
            raise ValueError("Invalid numeric value") from exc
        if not quantity.is_finite() or isinstance(row["value"],bool):
            raise ValueError("Finite nonbool number required")
        quote=row["quote"]
        if not isinstance(quote,str) or not 8<=len(quote)<=500:
            raise ValueError("Source quote required")
        descriptor={"page":row["page"],"section":row["section"],"exact_quote":quote}
        check=inspect_source_file(path=row["path"],approved_root=approved_root,
            expected_sha256=row["sha256"],access=row["access"],passages=[descriptor])
        quote_found=(check["status"]!="HASH_MISMATCH" and
                     bool(check["inspections"]) and check["inspections"][0]["found"])
        pattern=r"(?<![\d.])(-?\d+(?:\.\d+)?)(?![\d.])\s*"+re.escape(row["unit"])+r"(?![A-Za-z])"
        numeric=any(Decimal(m.group(1))==quantity for m in re.finditer(pattern,quote))
        status="SOURCE_VALUE_MATCH" if quote_found and numeric else "SHORTFALL"
        results.append({"table_id":row["table_id"],"row_id":row["row_id"],
            "source_id":row["source_id"],"page":row["page"],"value":str(quantity),
            "unit":row["unit"],"document_sha256":check["sha256"],
            "passage_sha256":sha256(quote.encode()).hexdigest(),
            "status":status,"source_reported_value_only":True,
            "experimental_result_independently_validated":False})
    digest=sha256(json.dumps(results,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return {"schema":"KRC-QUANT-TABLE-1","rows":results,"manifest_sha256":digest,
        "source_value_matches":sum(x["status"]=="SOURCE_VALUE_MATCH" for x in results),
        "all_source_values_match":all(x["status"]=="SOURCE_VALUE_MATCH" for x in results),
        "independent_experimental_validation":False,"publication_ready":False}
