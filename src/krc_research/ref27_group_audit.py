"""Arithmetic audit of published UPV group averages and percentage ratios.

The nine values are transcribed from RTU REF27 Table I; no raw measurement
data, figure coordinates, calibration or independent replication are claimed.
"""
from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict
from .upv_series_recalc import audit_upv_series

PRINTED={"N":{"sat_dry":724,"airdry_dry":545,"sat_airdry":179,"pct_sat_dry":18,"pct_airdry_dry":13,"pct_sat_airdry":4},
         "K":{"sat_dry":706,"airdry_dry":464,"sat_airdry":242,"pct_sat_dry":18,"pct_airdry_dry":12,"pct_sat_airdry":5},
         "KV":{"sat_dry":753,"airdry_dry":520,"sat_airdry":233,"pct_sat_dry":19,"pct_airdry_dry":13,"pct_sat_airdry":5}}

def _round(x):
    return int(x.quantize(Decimal("1"),rounding=ROUND_HALF_UP))

def audit_ref27_group_averages(rows):
    base=audit_upv_series(rows)
    groups=defaultdict(list)
    for row in rows:
        name=row["specimen_id"].split("-")[0]
        if name not in PRINTED:raise ValueError("Unknown experimental specimen group")
        groups[name].append(row)
    if set(groups)!=set(PRINTED) or any(len(v)!=3 for v in groups.values()):
        raise ValueError("Expected three groups of three specimens")
    result=[]
    for name in ("N","K","KV"):
        items=groups[name]
        mean=lambda key:sum(Decimal(str(x[key])) for x in items)/Decimal(3)
        dry=mean("upv_dry");air=mean("upv_airdry");sat=mean("upv_saturated")
        # Means of reported source differences; percentage is ratio of group means.
        ds=mean("reported_delta_sat_dry")
        da=mean("reported_delta_airdry_dry")
        sa=mean("reported_delta_sat_airdry")
        computed={"sat_dry":_round(ds),"airdry_dry":_round(da),"sat_airdry":_round(sa),
           "pct_sat_dry":_round((sat-dry)/dry*100),
           "pct_airdry_dry":_round((air-dry)/dry*100),
           "pct_sat_airdry":_round((sat-air)/air*100)}
        discrepancies={k:computed[k]-v for k,v in PRINTED[name].items() if computed[k]!=v}
        result.append({"group":name,"specimens":3,"recomputed_rounded":computed,
           "printed":PRINTED[name],"discrepancies":discrepancies,
           "all_six_group_values_match":not discrepancies})
    return {"schema":"KRC-REF27-GROUP-1","groups":result,
        "group_values_checked":18,
        "group_values_matching":sum(6-len(r["discrepancies"]) for r in result),
        "delta_arithmetic_exact_matches":base["exact_matches"],
        "delta_arithmetic_count":base["total_recomputed_differences"],
        "rounding_rule":"ROUND_HALF_UP_FROM_REPORTED_VALUES_FOR_GROUP_DELTA_AND_RATIO_OF_GROUP_MEAN_UPV",
        "independent_experimental_validation":False,"graph_curve_coordinates_verified":False,
        "publication_ready":False}
