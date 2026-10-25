import hashlib,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.source_file_inspection import inspect_source_file
def request(tmp_path,txt="METHODS: sample preparation details.\nRESULTS: trial was inconclusive."):
    p=tmp_path/"paper.txt";p.write_text(txt,encoding="utf-8")
    return dict(path=p,approved_root=tmp_path,expected_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
        access="FULL_TEXT",passages=[{"page":1,"section":"METHODS","exact_quote":"sample preparation details"},
          {"page":1,"section":"RESULTS","exact_quote":"trial was inconclusive"}])
def test_actual_bytes_and_both_sections(tmp_path):
    r=inspect_source_file(**request(tmp_path))
    assert r["status"]=="TEXT_MATCH_WITH_METHODS_RESULTS" and not r["scientific_truth_verified"]
def test_wrong_hash_shortfall(tmp_path):
    p=request(tmp_path);p["expected_sha256"]="0"*64
    assert inspect_source_file(**p)["status"]=="HASH_MISMATCH"
def test_methods_only_shortfall(tmp_path):
    p=request(tmp_path);p["passages"]=p["passages"][:1]
    assert inspect_source_file(**p)["status"]=="INSPECTION_SHORTFALL"
def test_missing_passage_shortfall(tmp_path):
    p=request(tmp_path);p["passages"][1]["exact_quote"]="RESULTS outcomes not present"
    assert inspect_source_file(**p)["status"]=="INSPECTION_SHORTFALL"
def test_parent_directory_denied(tmp_path):
    sub=tmp_path/"sub";sub.mkdir();p=request(tmp_path);p["approved_root"]=sub
    with pytest.raises(ValueError):inspect_source_file(**p)
def test_no_abstract_only(tmp_path):
    p=request(tmp_path);p["access"]="ABSTRACT_ONLY"
    with pytest.raises(ValueError):inspect_source_file(**p)
def test_symlink_input_denied(tmp_path):
    p=request(tmp_path);link=tmp_path/"sym";link.symlink_to(p["path"]);p["path"]=link
    with pytest.raises(ValueError):inspect_source_file(**p)
