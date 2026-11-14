"""N39 provenance recovery + root receipt scope tests (no deployed services)."""
import hashlib
import json
import sqlite3
import time
from pathlib import Path
import pytest
from krc_research.consent_custody128 import ConsentCustody128,fingerprint
from krc_research.stage131_n39_consent_policy import N39ConsentPolicy
from krc_research.stage131_n39_trust_boundaries import (
    N39ProvenanceJournal,N39RootRetrievalReceipts,N39ProtectedReadAuthorizer,_canonical)

P="K_Science"
R="KS-"+"a"*32
A="b"*48
CTX={"principal":P,"request_id":R,"consent_ref":"synthetic-real-custody-0001",
     "task_id":"t","operation":"research.profile.validate","profile_ref":"p",
     "evidence_refs":[],"payload_sha256":"a"*64}

def custody_fake(tmp_path,monkeypatch):
    """Uses actual class identity, simulated consumption evidence only."""
    instance=object.__new__(ConsentCustody128)
    instance.dir=tmp_path/"approvals"
    instance.path=str(tmp_path/"consumed.sqlite")
    instance.dir.mkdir()
    with sqlite3.connect(instance.path) as db:
        db.execute("CREATE TABLE consumed (ref TEXT PRIMARY KEY,consumed_at INTEGER NOT NULL)")
    original_receipt=b'{"synthetic":"root-owned-receipt-hash-only"}'
    evidence={"consent_ref":CTX["consent_ref"],"context_sha256":fingerprint(CTX),
              "receipt_sha256":hashlib.sha256(original_receipt).hexdigest(),
              "approver":"synthetic-root-operator","consumed_at":1000}
    consumed=[False]
    calls=[0]
    def consume(self,ctx):
        calls[0]+=1
        consumed[0]=True
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO consumed VALUES(?,?)",(ctx["consent_ref"],1000))
        return True
    def inspect(self,ctx):
        return evidence if consumed[0] and fingerprint(ctx)==evidence["context_sha256"] else None
    monkeypatch.setattr(ConsentCustody128,"__call__",consume)
    monkeypatch.setattr(ConsentCustody128,"inspect_consumed",inspect)
    return instance,consumed,calls,evidence

def test_crash_after_consumption_recovers_only_evidence_and_never_reexecutes(tmp_path,monkeypatch):
    custody,consumed,calls,evidence=custody_fake(tmp_path,monkeypatch)
    journal=N39ProvenanceJournal(tmp_path/"private"/"journal.sqlite",custody)
    saved=journal.reconcile
    def crash(*args,**kwargs):
        raise RuntimeError("SYNTHETIC_POST_CONSUME_CRASH")
    monkeypatch.setattr(journal,"reconcile",crash)
    with pytest.raises(RuntimeError,match="POST_CONSUME_CRASH"):
        journal.consume_once(CTX)
    assert consumed[0] and calls[0]==1
    assert journal.attestation(P,R) is None
    # A new process cannot consume a second time, only reconcile prior intent.
    restarted=N39ProvenanceJournal(tmp_path/"private"/"journal.sqlite",custody)
    assert restarted.consume_once(CTX) is False
    assert calls[0]==1
    assert restarted.reconcile(P,R)=="RECOVERED"
    assert restarted.attestation(P,R)==evidence
    assert restarted.reconcile(P,R)=="COMMITTED"
    assert calls[0]==1

def test_recovery_holds_without_independent_consumption_evidence(tmp_path,monkeypatch):
    custody,consumed,calls,_=custody_fake(tmp_path,monkeypatch)
    journal=N39ProvenanceJournal(tmp_path/"private"/"journal.sqlite",custody)
    assert journal.prepare(CTX)
    assert journal.reconcile(P,R)=="HOLD_UNVERIFIED"
    assert journal.attestation(P,R) is None
    assert calls[0]==0

def test_default_legacy_issuer_is_not_trusted(tmp_path):
    legacy=N39ConsentPolicy(tmp_path/"legacy.sqlite")
    assert legacy.is_authorized(principal=P,request_id=R,artifact_id=A) is False
    with pytest.raises(PermissionError,match="TRUSTED_ISSUER_REQUIRED"):
        legacy.record_read_grant(principal=P,request_id=R,artifact_id=A,
                                 grant_ref="arbitrary-issuer",expires=time.time()+60)

def test_protected_receipts_revoke_regrant_and_wrong_binding(tmp_path,monkeypatch):
    custody,consumed,calls,evidence=custody_fake(tmp_path,monkeypatch)
    journal=N39ProvenanceJournal(tmp_path/"private"/"journal.sqlite",custody)
    assert journal.consume_once(CTX)
    root=tmp_path/"root-issued-read-receipts";root.mkdir()
    import krc_research.stage131_n39_trust_boundaries as module
    # Explicitly mocks root ownership. This is NOT a root-owned filesystem acceptance test.
    def fake_root_read(directory,name):
        raw=(Path(directory)/name).read_bytes()
        obj=json.loads(raw)
        return obj,hashlib.sha256(raw).hexdigest()
    monkeypatch.setattr(module,"_read_root_json",fake_root_read)
    receipts=N39RootRetrievalReceipts(root)
    authorizer=N39ProtectedReadAuthorizer(journal=journal,receipts=receipts)
    ref="root-grant-0000000001"
    selector=hashlib.sha256(_canonical({"principal":P,"request_id":R,"artifact_id":A})).hexdigest()+".index.json"
    def put(name,obj):
        (root/name).write_text(json.dumps(obj,sort_keys=True))
    def point(grant,previous=None):
        put(selector,{"version":1,"principal":P,"request_id":R,"artifact_id":A,"active_grant_ref":grant,"previous_grant_ref":previous})
    def grant(grant_ref,*,supersedes=None,provenance=None):
        put(grant_ref+".json",{
            "version":1,"action":"grant","grant_ref":grant_ref,
            "principal":P,"request_id":R,"artifact_id":A,
            "issuer":"root-test-operator","issued_at":int(time.time())-5,
            "expires_at":int(time.time())+100,"supersedes":supersedes,
            "origin_receipt_sha256":provenance or evidence["receipt_sha256"]})
    point(ref)
    assert not authorizer(principal=P,request_id=R,artifact_id=A)
    grant(ref)
    assert authorizer(principal=P,request_id=R,artifact_id=A)
    assert not authorizer(principal=P,request_id="another-request",artifact_id=A)
    # Tampered provenance cannot be accepted, even with the correct scoped filename.
    grant(ref,provenance="f"*64)
    assert not authorizer(principal=P,request_id=R,artifact_id=A)
    grant(ref)
    put(ref+".revoked.json",{"action":"revoke","grant_ref":ref,"principal":P,
      "request_id":R,"artifact_id":A,"issuer":"root-revoker"})
    assert not authorizer(principal=P,request_id=R,artifact_id=A)
    newer="root-grant-0000000002"
    point(newer,previous=ref)
    grant(newer)
    assert not authorizer(principal=P,request_id=R,artifact_id=A)
    # Old revoked grant must not be silently replaced by a new one.
    # This is the current source contract: require explicit supersedes.
    grant(newer,supersedes=ref)
    assert authorizer(principal=P,request_id=R,artifact_id=A)
    (root/(ref+".revoked.json")).unlink()
    assert not authorizer(principal=P,request_id=R,artifact_id=A)

def test_untrusted_receipt_directory_is_rejected_without_mock(tmp_path):
    from krc_research.stage131_n39_trust_boundaries import _read_root_json
    directory=tmp_path/"untrusted";directory.mkdir()
    (directory/"fake.json").write_text("{}")
    if directory.stat().st_uid != 0:
        with pytest.raises(ValueError,match="UNTRUSTED_DIRECTORY"):
            _read_root_json(directory,"fake.json")


def test_n39_trusted_predispatch_journal_is_one_time_and_recovery_not_dispatch(tmp_path,monkeypatch):
    from krc_research.stage131_pre_dispatch_custody_gate import execute_with_durable_n39_custody,AuthorizationGateDenied
    custody,consumed,calls,_=custody_fake(tmp_path,monkeypatch)
    journal=N39ProvenanceJournal(tmp_path/"private"/"journal.sqlite",custody)
    sent=[]
    def dispatch(operation,payload,principal,*,request_id):
        sent.append((operation,request_id))
        return {"task_id":payload["task_id"],"operation":operation,"status":"PENDING","engine_result":{},"scientific_approval":False}
    kwargs={"journal":journal,"context":CTX,"operation":CTX["operation"],
            "payload":{"task_id":CTX["task_id"]},"principal":P,"request_id":R}
    result=execute_with_durable_n39_custody(dispatch,**kwargs)
    assert result["status"]=="PENDING"
    assert len(sent)==1 and calls[0]==1
    with pytest.raises(AuthorizationGateDenied,match="CONSENT_DENIED_OR_RECOVERY_HOLD"):
        execute_with_durable_n39_custody(dispatch,**kwargs)
    assert len(sent)==1 and calls[0]==1
