import sys
import sqlite3
import hashlib
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from n39_github_anchor_export import audit_head,manifest
from krc_research.stage131_n39_audit_journal import N39AuditJournal

def fixture(tmp_path):
    anchor=[(0,"0"*64)]
    db=tmp_path/"private"/"audit.sqlite"
    journal=N39AuditJournal(db,anchor_checker=lambda seq,head:(seq,head)==anchor[0])
    intent=journal.record_intent(ticket_digest="b"*64,operator_id="synthetic",
        action="issue",principal="K_Science",request_id="synthetic-request",
        artifact_id="synthetic-artifact",grant_ref="synthetic-only",
        event_id="n39-test-event-00000001")
    return db,intent

def test_export_exact_chain_head_no_sensitive_payload(tmp_path):
    db,intent=fixture(tmp_path)
    assert audit_head(db)==(1,intent["head_sha256"])
    path,data=manifest(db,journal_id="n39-isolated-demo-20261115",
        prior_commit_sha="a"*40,source_commit_sha="b"*40,
        phase="INTENT",demo_only=True)
    assert data["sequence"]==1 and data["chain_head_sha256"]==intent["head_sha256"]
    assert "synthetic" in str(data) and "ticket_digest" not in str(data)
    assert path.endswith(intent["head_sha256"]+".json")
def test_reject_real_anchor_without_approved_issuer(tmp_path):
    db,_=fixture(tmp_path)
    with pytest.raises(ValueError,match="REAL_ANCHOR_NEEDS"):
        manifest(db,journal_id="n39-isolated-demo-20261115",
            prior_commit_sha="a"*40,source_commit_sha="b"*40,phase="INTENT",demo_only=False)
def test_reject_corrupted_journal_even_if_index_present(tmp_path):
    db,_=fixture(tmp_path)
    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE events SET entry_hash=? WHERE seq=1",("0"*64,))
    with pytest.raises(ValueError,match="AUDIT_CHAIN_MISMATCH"):
        audit_head(db)
def test_reject_invalid_commit_hash(tmp_path):
    db,_=fixture(tmp_path)
    with pytest.raises(ValueError,match="INVALID_PRIOR_SHA"):
        manifest(db,journal_id="n39-isolated-demo-20261115",
            prior_commit_sha="invalid",source_commit_sha="b"*40,phase="INTENT",demo_only=True)
