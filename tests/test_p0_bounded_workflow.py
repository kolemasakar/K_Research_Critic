from datetime import datetime, timezone
import pytest
from krc_research.interproject_contract import envelope, sign_envelope
from krc_research.bounded_workflow import execute_bounded_workflow
from krc_research.replay_registry import ReplayRegistry

NOW = datetime(2026, 10, 25, 12, tzinfo=timezone.utc)
KEY = b"p" * 32
GATES = ("journal_policy_checked", "search_audit_reproducible", "primary_sources_inspected",
         "novelty_reviewed", "citations_validated", "scientific_methods_audited",
         "rights_and_ai_disclosure_done", "human_author_approved")
PAYLOAD = {"user_profile_approved": True, "source_manifest_sha256": "a" * 64,
           "manuscript_gate": {}, "claims": [], "verified_primary_sources": 0}

def call(registry, *, payload=None, signature=None, operation="research.evidence.preflight"):
    body = envelope(task_id="kscience-stage102-0001", operation=operation,
                    payload=PAYLOAD if payload is None else payload, created_at=NOW.isoformat())
    sig = sign_envelope(body, KEY) if signature is None else signature
    return execute_bounded_workflow(body, secret=KEY, signature=sig, registry=registry, now=NOW)

def test_signature(tmp_path):
    with pytest.raises(ValueError): call(ReplayRegistry(tmp_path / "a.db"), signature="0"*64)
def test_self_approval(tmp_path):
    with pytest.raises(ValueError): call(ReplayRegistry(tmp_path / "a.db"), payload={**PAYLOAD, "scientific_approval":True})
def test_operation(tmp_path):
    with pytest.raises(ValueError): call(ReplayRegistry(tmp_path / "a.db"), operation="research.bibliography.audit")
def test_profile(tmp_path):
    with pytest.raises(ValueError): call(ReplayRegistry(tmp_path / "a.db"), payload={**PAYLOAD,"user_profile_approved":False})
def test_hash(tmp_path):
    with pytest.raises(ValueError): call(ReplayRegistry(tmp_path / "a.db"), payload={**PAYLOAD,"source_manifest_sha256":"bad"})
def test_manuscript_required(tmp_path):
    with pytest.raises(ValueError): call(ReplayRegistry(tmp_path / "a.db"), payload={k:v for k,v in PAYLOAD.items() if k!="manuscript_gate"})
def test_authorized_and_durable_replay(tmp_path):
    p={**PAYLOAD,"manuscript_gate":{key:False for key in GATES}}
    r=call(ReplayRegistry(tmp_path / "a.db"), payload=p)
    assert r["status"] == "REVISE" and r["publication_gate"] == "NO_GO"
    assert not r["scientific_approval"] and not r["full_workflow_implemented"]
    with pytest.raises(ValueError): call(ReplayRegistry(tmp_path / "a.db"), payload=p)
