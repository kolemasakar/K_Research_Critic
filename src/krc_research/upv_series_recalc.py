"""Recalculate arithmetic consistency of a source-reported UPV series.

This uses transcription of published values (not raw instrument readings).
Discrepancies remain visible and are never silently rounded into agreement.
"""
from __future__ import annotations
from decimal import Decimal,InvalidOperation

def _number(x):
    if isinstance(x,bool):raise ValueError("Boolean is not a measurement")
    try:r=Decimal(str(x))
    except (ValueError,InvalidOperation) as exc:raise ValueError("Invalid measurement") from exc
    if not r.is_finite():raise ValueError("Nonfinite measurement")
    return r

def audit_upv_series(rows,*,tolerance_m_per_s="0"):
    if not isinstance(rows,list) or not 1<=len(rows)<=150:
        raise ValueError("1..150 rows required")
    tolerance=_number(tolerance_m_per_s)
    if tolerance<0 or tolerance>5:raise ValueError("Tolerance must be in 0..5 m/s")
    names=set();out=[]
    for row in rows:
        expected={"specimen_id","upv_airdry","upv_saturated","upv_drying","upv_dry",
                  "reported_delta_sat_dry","reported_delta_sat_airdry",
                  "reported_delta_airdry_dry"}
        if not isinstance(row,dict) or set(row)!=expected:
            raise ValueError("Invalid UPV row")
        name=row["specimen_id"]
        if not isinstance(name,str) or not name or name in names:raise ValueError("Duplicate/empty specimen")
        names.add(name)
        vals={k:_number(v) for k,v in row.items() if k!="specimen_id"}
        if any(vals[k]<=0 for k in ("upv_airdry","upv_saturated","upv_drying","upv_dry")):
            raise ValueError("UPV must be positive")
        actual={
            "sat_minus_dry":vals["upv_saturated"]-vals["upv_dry"],
            "sat_minus_airdry":vals["upv_saturated"]-vals["upv_airdry"],
            "airdry_minus_dry":vals["upv_airdry"]-vals["upv_dry"]}
        reported={"sat_minus_dry":vals["reported_delta_sat_dry"],
                  "sat_minus_airdry":vals["reported_delta_sat_airdry"],
                  "airdry_minus_dry":vals["reported_delta_airdry_dry"]}
        residual={k:actual[k]-reported[k] for k in actual}
        out.append({"specimen_id":name,"calculated_m_per_s":{k:str(v) for k,v in actual.items()},
                    "reported_m_per_s":{k:str(v) for k,v in reported.items()},
                    "residual_m_per_s":{k:str(v) for k,v in residual.items()},
                    "exact_matches":sum(x==0 for x in residual.values()),
                    "within_explicit_tolerance":all(abs(x)<=tolerance for x in residual.values())})
    return {"schema":"KRC-UPV-RECALC-1","specimens":out,
            "total_recomputed_differences":len(out)*3,
            "exact_matches":sum(x["exact_matches"] for x in out),
            "within_tolerance_rows":sum(x["within_explicit_tolerance"] for x in out),
            "tolerance_m_per_s":str(tolerance),
            "raw_measurements_independently_verified":False,
            "publication_ready":False}
