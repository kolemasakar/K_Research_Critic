"""Compare three explicit definitions of source Table-I percentage group averages.

All three methods are hypotheses computed from transcribed published UPV
values, not proof of the authors' own original rounding procedure.
"""
from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict
from .upv_series_recalc import audit_upv_series

PUBLISHED={"N":[18,13,4],"K":[18,12,5],"KV":[19,13,5]}
def rnd(x):
    return int(x.quantize(Decimal("1"),rounding=ROUND_HALF_UP))
def alternatives(rows):
    audit_upv_series(rows)
    groups=defaultdict(list)
    for r in rows:
        name=r["specimen_id"].split("-")[0]
        if name not in PUBLISHED:raise ValueError("Unexpected study group")
        groups[name].append(r)
    if set(groups)!=set(PUBLISHED) or any(len(group)!=3 for group in groups.values()):
        raise ValueError("Expected 3 groups of 3 physical specimens")
    out=[]
    for name in ("N","K","KV"):
        group=groups[name]
        values=[]
        for r in group:
            a,s,d=(Decimal(str(r[k])) for k in ("upv_airdry","upv_saturated","upv_dry"))
            values.append([(s-d)/d*100,(a-d)/d*100,(s-a)/a*100])
        mean=lambda key:sum(Decimal(str(r[key])) for r in group)/Decimal(3)
        a,s,d=(mean(k) for k in ("upv_airdry","upv_saturated","upv_dry"))
        ratio_of_group_means=[rnd(z) for z in ((s-d)/d*100,(a-d)/d*100,(s-a)/a*100)]
        mean_individual_unrounded=[rnd(sum(v[j] for v in values)/3) for j in range(3)]
        mean_individual_rounded=[rnd(sum(Decimal(rnd(v[j])) for v in values)/3) for j in range(3)]
        reported=PUBLISHED[name]
        out.append({"group":name,"source_reported_pct":reported,
                    "ratio_of_group_means":ratio_of_group_means,
                    "mean_of_unrounded_individual_pct":mean_individual_unrounded,
                    "mean_of_rounded_individual_pct":mean_individual_rounded,
                    "method_matches_source":{
                        "ratio_of_group_means":ratio_of_group_means==reported,
                        "mean_of_unrounded_individual_pct":mean_individual_unrounded==reported,
                        "mean_of_rounded_individual_pct":mean_individual_rounded==reported}})
    candidates=["ratio_of_group_means","mean_of_unrounded_individual_pct","mean_of_rounded_individual_pct"]
    consistent=[m for m in candidates if all(x["method_matches_source"][m] for x in out)]
    return {"schema":"KRC-REF27-PCT-ALTERNATIVES-1","groups":out,
            "methods_matching_all_groups":consistent,
            "unique_original_method_inferable":len(consistent)==1,
            "authors_original_rounding_method_proven":False,
            "scientific_measurements_validated":False}
