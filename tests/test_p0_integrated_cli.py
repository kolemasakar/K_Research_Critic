import json,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.integrated_cli import run_file
from test_p0_integrated_research import fixture

def test_cli_cannot_import_self_asserted_attestations(tmp_path):
    p=fixture();p["attested_receipt_hashes"]=["a"*64]
    source=tmp_path/"input.json";source.write_text(json.dumps(p),encoding="utf-8")
    with pytest.raises(ValueError):run_file(source,tmp_path/"result.json")
def test_cli_no_trust_leak(tmp_path):
    source=tmp_path/"input.json";source.write_text(json.dumps(fixture()),encoding="utf-8")
    r=run_file(source,tmp_path/"result.json")
    assert r["execution_mode"]=="OFFLINE_UNATTESTED"
    assert r["output"]["claim_verdicts"][0]["verdict"]=="SHORTFALL"
    assert r["output"]["publication_ready"] is False
    assert (tmp_path/"result.json").is_file()
