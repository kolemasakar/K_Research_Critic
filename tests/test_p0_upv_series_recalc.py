import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.upv_series_recalc import audit_upv_series
def row():
    return dict(specimen_id="N-1.28",upv_airdry=4614,upv_saturated=4804,
      upv_drying=4430,upv_dry=4032,reported_delta_sat_dry=771,
      reported_delta_sat_airdry=190,reported_delta_airdry_dry=582)
def test_exact_one_unit_discrepancy_visible():
    x=audit_upv_series([row()])
    assert x["specimens"][0]["residual_m_per_s"]["sat_minus_dry"]=="1"
    assert x["exact_matches"]==2
    assert not x["specimens"][0]["within_explicit_tolerance"]
def test_explicit_one_unit_tolerance():
    assert audit_upv_series([row()],tolerance_m_per_s="1")["within_tolerance_rows"]==1
def test_wrong_reported_result_is_detected():
    p=row();p["reported_delta_sat_dry"]=700
    assert audit_upv_series([p],tolerance_m_per_s="1")["within_tolerance_rows"]==0
def test_duplicate_specimens_denied():
    with pytest.raises(ValueError):audit_upv_series([row(),row()])
def test_no_unsafe_tolerance():
    with pytest.raises(ValueError):audit_upv_series([row()],tolerance_m_per_s="40")
def test_nonfinite_denied():
    p=row();p["upv_dry"]="NaN"
    with pytest.raises(ValueError):audit_upv_series([p])
