import hashlib
import sqlite3
import pytest
from krc_research.stage131_n39_audit_journal import N39AuditJournal, AuditDenied

def create(tmp_path):
    anchored=[(0,"0"*64)]
    journal=N39AuditJournal(tmp_path/"private"/"audit.sqlite",
                            anchor_checker=lambda n,h:(n,h)==anchored[0],clock=lambda:1000)
    args={"ticket_digest":"a"*64,"operator_id":"test-operator","action":"issue",
          "principal":"K_Science","request_id":"KS-"+"1"*32,"artifact_id":"b"*48,
          "grant_ref":"synthetic-grant-ref-00001","event_id":"synthetic-event-id-00001"}
    return journal,anchored,args

def test_n39_audit_requires_external_anchor_before_issuance(tmp_path):
    journal,anchor,args=create(tmp_path)
    assert journal.verify()["seq"]==0
    intent=journal.record_intent(**args)
    with pytest.raises(AuditDenied,match="AUDIT_ANCHOR_UNVERIFIED"):
        journal.check_anchored_intent(seq=1,event_id=args["event_id"])
    anchor[0]=(intent["seq"],intent["head_sha256"])
    assert journal.check_anchored_intent(seq=1,event_id=args["event_id"])
    with pytest.raises(AuditDenied,match="AUDIT_DUPLICATE_EVENT"):
        journal.record_intent(**args)

def test_n39_tampered_stored_intent_fails_even_with_old_anchor(tmp_path):
    journal,anchor,args=create(tmp_path)
    intent=journal.record_intent(**args)
    anchor[0]=(intent["seq"],intent["head_sha256"])
    with journal._db() as db:
        db.execute("UPDATE events SET event_json=? WHERE seq=1",('{"kind":"altered"}',))
    with pytest.raises(AuditDenied,match="AUDIT_CHAIN_MISMATCH"):
        journal.verify()

def test_n39_rewritten_valid_chain_denied_by_independent_anchor(tmp_path):
    journal,anchor,args=create(tmp_path)
    event=journal.record_intent(**args)
    anchor[0]=(event["seq"],event["head_sha256"])
    with journal._db() as db:
        db.execute("DELETE FROM events")
    with pytest.raises(AuditDenied,match="AUDIT_ANCHOR_UNVERIFIED"):
        journal.verify()

def test_n39_audit_missing_anchor_and_bad_ticket_fail_closed(tmp_path):
    with pytest.raises(AuditDenied,match="INDEPENDENT_ANCHOR_REQUIRED"):
        N39AuditJournal(tmp_path/"private"/"audit.sqlite",anchor_checker=None)
    journal,anchor,args=create(tmp_path)
    with pytest.raises(AuditDenied,match="INVALID_TICKET_DIGEST"):
        journal.record_intent(**{**args,"ticket_digest":"not-trusted"})
    anchor[0]=(99,"f"*64)
    with pytest.raises(AuditDenied,match="AUDIT_ANCHOR_UNVERIFIED"):
        journal.record_intent(**args)

def test_n39_audit_restart_does_not_create_unanchored_permission(tmp_path):
    journal,anchor,args=create(tmp_path)
    event=journal.record_intent(**args)
    restarted=N39AuditJournal(tmp_path/"private"/"audit.sqlite",
                              anchor_checker=lambda n,h:(n,h)==anchor[0])
    with pytest.raises(AuditDenied,match="AUDIT_ANCHOR_UNVERIFIED"):
        restarted.check_anchored_intent(seq=event["seq"],event_id=args["event_id"])
    anchor[0]=(event["seq"],event["head_sha256"])
    assert restarted.check_anchored_intent(seq=event["seq"],event_id=args["event_id"])
