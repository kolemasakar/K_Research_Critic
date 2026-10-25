import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.upv_series_recalc import audit_upv_series
ROOT=Path(__file__).resolve().parent
def records():
    return json.loads((ROOT/"fixtures"/"ref27_upv_table_i.json").read_text())
def test_all_nine_ref27_specimens_exact_matches_are_not_fabricated():
    r=audit_upv_series(records())
    assert len(r["specimens"])==9
    assert r["total_recomputed_differences"]==27
    assert r["exact_matches"]==19
    assert r["within_tolerance_rows"]==3
    assert not r["raw_measurements_independently_verified"]
def test_one_mps_is_explicit_not_default_tolerance():
    strict=audit_upv_series(records())
    relaxed=audit_upv_series(records(),tolerance_m_per_s="1")
    assert relaxed["within_tolerance_rows"]==9
    assert strict["within_tolerance_rows"]<9
    assert relaxed["tolerance_m_per_s"]=="1"
