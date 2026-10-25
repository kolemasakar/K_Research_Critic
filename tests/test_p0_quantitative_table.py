import sys,hashlib
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.quantitative_table import compare_table_rows
def row(tmp):
    p=tmp/"paper.md";p.write_text("Mix A 53.7 MPa and Mix B 36.7 MPa.",encoding="utf8")
    return dict(table_id="T1",row_id="A",source_id="S1",path=str(p),
        sha256=hashlib.sha256(p.read_bytes()).hexdigest(),access="FULL_TEXT",
        page=1,section="RESULTS",quote="Mix A 53.7 MPa and Mix B 36.7 MPa.",
        value="53.7",unit="MPa")
def test_table_numeric_exact_match(tmp_path):
    out=compare_table_rows([row(tmp_path)],approved_root=tmp_path)
    assert out["source_value_matches"]==1
    assert not out["independent_experimental_validation"]
def test_wrong_number_fails(tmp_path):
    r=row(tmp_path);r["value"]="153.7"
    assert compare_table_rows([r],approved_root=tmp_path)["source_value_matches"]==0
def test_wrong_unit_fails(tmp_path):
    r=row(tmp_path);r["unit"]="kPa"
    assert compare_table_rows([r],approved_root=tmp_path)["source_value_matches"]==0
def test_repeated_row_denied(tmp_path):
    r=row(tmp_path)
    with pytest.raises(ValueError):compare_table_rows([r,r],approved_root=tmp_path)
def test_invalid_unit_denied(tmp_path):
    r=row(tmp_path);r["unit"]="USD"
    with pytest.raises(ValueError):compare_table_rows([r],approved_root=tmp_path)
def test_changed_pdf_hash_fails(tmp_path):
    r=row(tmp_path);r["sha256"]="a"*64
    assert compare_table_rows([r],approved_root=tmp_path)["source_value_matches"]==0
