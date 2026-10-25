import sys,hashlib
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.independent_critic import run_critic
from krc_research.artifact_attestation import verify_plaintext_artifact
from krc_research.research_pipeline_v2 import run_review_cycle
from test_p0_integrated_research import fixture
def test_rule_critic_runs():
    r=run_review_cycle(fixture())
    assert r['critic']['rounds_executed']==1 and r['critic']['history'][0]['result']['verdict']=='REVISE'
    assert r['final_gate']=='NO_GO' and not r['publication_ready']
def test_repeat_is_deterministic():
    assert run_review_cycle(fixture())==run_review_cycle(fixture())
def test_reported_pass_not_accepted():
    r=run_review_cycle(fixture())
    assert r['research']['critic_iterations'][-1]['reported_critic']=='PASS'
    assert r['critic']['history'][0]['result']['verdict']=='REVISE'
def test_empty_claims_rejected():
    a=dict(claim_verdicts=[],inspection_audit=[],preflight=dict(search_reproducibility="SHORTFALL",manuscript_gate={"status":"REVISE"}),critic_iterations=[])
    assert run_critic(a)['verdict']=='REVISE'
def test_plaintext_byte_trace(tmp_path):
    p=tmp_path/'paper.txt';p.write_text('METHODS: synthetic\nRESULTS: unavailable')
    r=verify_plaintext_artifact({"document_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"passage_locators":["METHODS: synthetic"]},p,approved_root=tmp_path)
    assert r['status']=='STRUCTURAL_MATCH' and not r['independent_attestation_granted']
def test_outside_root_rejected(tmp_path):
    inside=tmp_path/'docs';inside.mkdir();p=tmp_path/'outside.txt';p.write_text('test')
    with pytest.raises(ValueError):verify_plaintext_artifact({"passage_locators":["test"]},p,approved_root=inside)
def test_artifact_change_rejected(tmp_path):
    p=tmp_path/'paper.txt';p.write_text('ABCD')
    r=verify_plaintext_artifact({"document_sha256":"0"*64,"passage_locators":["ABCD"]},p,approved_root=tmp_path)
    assert r['status']=='SHORTFALL'
