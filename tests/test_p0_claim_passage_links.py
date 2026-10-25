import hashlib,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.claim_passage_links import verify_claim_passages
def datum(tmp_path):
    f=tmp_path/"source.md"
    f.write_text("METHODS: ultrasonic travel times recorded.\\nRESULTS: measured speed changed with temperature.\\n",encoding="utf-8")
    return {"claim_id":"C01","source_id":"S01","path":str(f),
            "sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"access":"FULL_TEXT",
            "passage":{"page":1,"section":"METHODS","exact_quote":"ultrasonic travel times recorded"}}
def test_true_quote_found_but_not_scientific_pass(tmp_path):
    x=verify_claim_passages([datum(tmp_path)],approved_root=tmp_path)
    assert x["exact_quotes_found"]==1 and x["claim_links"][0]["quote_found"]
    assert not x["all_scientific_claims_validated"]
def test_invented_quote_shortfall(tmp_path):
    d=datum(tmp_path);d["passage"]["exact_quote"]="nonexistent independent experiment"
    assert verify_claim_passages([d],approved_root=tmp_path)["claim_links"][0]["status"]=="SHORTFALL"
def test_wrong_sha_shortfall(tmp_path):
    d=datum(tmp_path);d["sha256"]="a"*64
    assert verify_claim_passages([d],approved_root=tmp_path)["claim_links"][0]["status"]=="SHORTFALL"
def test_duplicate_locator_denied(tmp_path):
    d=datum(tmp_path)
    with pytest.raises(ValueError):verify_claim_passages([d,d],approved_root=tmp_path)
def test_outside_root_denied(tmp_path):
    d=datum(tmp_path);sub=tmp_path/"sub";sub.mkdir()
    with pytest.raises(ValueError):verify_claim_passages([d],approved_root=sub)
