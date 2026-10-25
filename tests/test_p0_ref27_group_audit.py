import json,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.ref27_group_audit import audit_ref27_group_averages
def fixture():
    return json.loads((Path(__file__).resolve().parent/"fixtures"/"ref27_upv_table_i.json").read_text())
def test_group_summary():
    r=audit_ref27_group_averages(fixture())
    assert r["group_values_checked"]==18
    assert r["group_values_matching"]==18
    assert r["delta_arithmetic_exact_matches"]==19
    assert not r["independent_experimental_validation"]
def test_k_group_percent_uses_ratio_of_means():
    r=audit_ref27_group_averages(fixture())
    k=next(x for x in r["groups"] if x["group"]=="K")
    assert k["recomputed_rounded"]["pct_airdry_dry"]==12
def test_missing_specimen():
    with pytest.raises(ValueError):audit_ref27_group_averages(fixture()[:-1])
