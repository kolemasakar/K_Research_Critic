import sys,hashlib
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.numeric_quote_audit import verify_reported_numbers
def sample(tmp_path):
    p=tmp_path/"source.md"
    p.write_text("Measured 53.7 MPa at 28 days.",encoding="utf8")
    return {"claim_id":"C1","source_id":"S1","path":str(p),
      "sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"access":"FULL_TEXT",
      "passage":{"page":1,"section":"RESULTS","exact_quote":"Measured 53.7 MPa at 28 days."},
      "reported_value":"53.7","reported_unit":"MPa"}
def test_literal_match(tmp_path):
    r=verify_reported_numbers([sample(tmp_path)],approved_root=tmp_path)
    assert r["matches"]==1 and not r["scientific_results_validated"]
def test_different_number(tmp_path):
    x=sample(tmp_path);x["reported_value"]="3.7"
    assert verify_reported_numbers([x],approved_root=tmp_path)["matches"]==0
def test_different_unit(tmp_path):
    x=sample(tmp_path);x["reported_unit"]="kPa"
    assert verify_reported_numbers([x],approved_root=tmp_path)["matches"]==0
def test_bad_digest(tmp_path):
    x=sample(tmp_path);x["sha256"]="b"*64
    assert verify_reported_numbers([x],approved_root=tmp_path)["matches"]==0
