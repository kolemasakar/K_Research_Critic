import os
import time
import json
import tempfile
from pathlib import Path
import pytest
from krc_research.stage131_n39_consent_policy import N39ConsentPolicy
from krc_research.consent_custody128 import ConsentCustody128,fingerprint
from krc_research.stage131_signed_artifact_boundary import SignedArtifactReadBoundary
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
from krc_research.request_ledger119 import RequestLedger
from krc_research.artifact_exchange import ArtifactExchange
from krc_research.stage131_signed_artifact_read import sign_fixture

PRINCIPAL="K_Science"
REQUEST="KS-"+"a"*32
KEY=b"synthetic-retrieval-secret-key-only"
IDENTITY={"principal":PRINCIPAL,"repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}

def signed(artifact,nonce):
    return sign_fixture({"version":"krc-artifact-get/1","operation":"artifact.read",
       "request_id":REQUEST,"artifact_id":artifact,"identity":IDENTITY,
       "auth":{"key_id":"k","issued_at_epoch":int(time.time()),
               "nonce":nonce,"mac_sha256":"0"*64}},KEY)

def seed_test_provenance(policy, ref="synthetic-historic-only"):
    # SQLite fixture only; not evidence of authentic owner approval.
    with policy._db() as db:
        db.execute("INSERT INTO origin VALUES(?,?,?,0)",(PRINCIPAL,REQUEST,ref))

def setup(tmp_path,policy):
    ledger=RequestLedger(tmp_path/"ledger.sqlite")
    payload={"task_id":"synthetic"}
    ledger.admit(principal=PRINCIPAL,request_id=REQUEST,operation="research.profile.validate",payload=payload)
    ledger.complete(principal=PRINCIPAL,request_id=REQUEST,operation="research.profile.validate",payload=payload,result={"status":"completed"})
    store=ArtifactExchange(tmp_path/"store")
    art=store.store_bytes(b"historic-immutable-artifact",principal=PRINCIPAL,request_id=REQUEST,filename="test.bin")
    boundary=SignedArtifactReadBoundary(exchange=store,ledger=ledger,nonce_registry=ArtifactNonceRegistry(tmp_path/"nonce.sqlite"),
      keyring={"k":KEY},trusted_peer_identities={os.getuid():IDENTITY},enabled=True,
      retrieval_authorizer=policy.is_authorized if policy else None)
    return art,boundary

def test_n39_missing_original_and_fail_closed_default(tmp_path):
    art,boundary=setup(tmp_path,None)
    denied=boundary.execute(signed(art["artifact_id"],"n39-missing-0000001"),peer_uid=os.getuid())
    assert denied=={"http_status":403,"content_type":"application/json","body":{"error":"FORBIDDEN"}}
    assert "body_bytes" not in denied and "body_file" not in denied
    policy=N39ConsentPolicy(tmp_path/"consent.sqlite",synthetic_test_mode=True)
    art2,b2=setup(tmp_path/"other",policy)
    assert b2.execute(signed(art2["artifact_id"],"n39-missing-0000002"),peer_uid=os.getuid())["http_status"]==403

def test_n39_revocation_independent_retrieval_grant_and_atomic_decision(tmp_path):
    policy=N39ConsentPolicy(tmp_path/"consent.sqlite",synthetic_test_mode=True)
    context={"request_id":REQUEST,"principal":PRINCIPAL,"consent_ref":"synthetic-owner-grant-00001"}
    assert not policy.record_original(custody=lambda _: True,context=context)
    seed_test_provenance(policy)
    art,b=setup(tmp_path/"run",policy)
    artifact_id=art["artifact_id"]
    # Original completed consent never authorizes a read by itself.
    assert b.execute(signed(artifact_id,"n39-origin-only-00001"),peer_uid=os.getuid())["http_status"]==403
    policy.record_read_grant(principal=PRINCIPAL,request_id=REQUEST,artifact_id=artifact_id,
        grant_ref="independent-retrieval-grant",expires=time.time()+100)
    assert b.execute(signed(artifact_id,"n39-before-revoke-0001"),peer_uid=os.getuid())["http_status"]==200
    policy.revoke_original(principal=PRINCIPAL,request_id=REQUEST)
    # Historical revocation does not erase an independently issued live retrieval right.
    assert b.execute(signed(artifact_id,"n39-after-revoke-00001"),peer_uid=os.getuid())["http_status"]==200
    policy.revoke_read_grant(principal=PRINCIPAL,request_id=REQUEST,artifact_id=artifact_id)
    assert b.execute(signed(artifact_id,"n39-read-revoked-0001"),peer_uid=os.getuid())["http_status"]==403
    assert policy.is_authorized(principal=PRINCIPAL,request_id=REQUEST,artifact_id=artifact_id) is False

def test_n39_no_read_grant_on_missing_origin_and_expired_grant(tmp_path):
    policy=N39ConsentPolicy(tmp_path/"consent.sqlite",synthetic_test_mode=True)
    with pytest.raises(ValueError,match="ORIGINAL_CONSENT_PROVENANCE_MISSING"):
        policy.record_read_grant(principal=PRINCIPAL,request_id=REQUEST,
            artifact_id="a"*48,grant_ref="independent",expires=time.time()+100)
    seed_test_provenance(policy,"synthetic-owner-grant-00002")
    art,b=setup(tmp_path/"run",policy)
    now=[1000.0]
    policy.clock=lambda:now[0]
    policy.record_read_grant(principal=PRINCIPAL,request_id=REQUEST,artifact_id=art["artifact_id"],grant_ref="time-scoped",expires=1001)
    assert policy.is_authorized(principal=PRINCIPAL,request_id=REQUEST,artifact_id=art["artifact_id"])
    now[0]=1001
    assert b.execute(signed(art["artifact_id"],"n39-grant-expired-001"),peer_uid=os.getuid())["http_status"]==403

@pytest.mark.skipif(os.geteuid()!=0,reason="requires real root-owned isolated ConsentCustody receipt")
def test_n39_real_root_owned_custody_fixture(tmp_path):
    # Run ONLY as root in a disposable test environment; never touch installed grants.
    approvals=tmp_path/"synthetic-approvals"
    approvals.mkdir(mode=0o700)
    replay=tmp_path/"private-replay"
    replay.mkdir(mode=0o700)
    context={"request_id":REQUEST,"principal":PRINCIPAL,
        "task_id":"synthetic","operation":"research.profile.validate",
        "profile_ref":"profile","evidence_refs":[],"payload_sha256":"a"*64,
        "consent_ref":"synthetic-root-owned-approval"}
    now=int(time.time())
    ref=context["consent_ref"]
    (approvals/(ref+".json")).write_text(json.dumps({"consent_ref":ref,
        "context_sha256":fingerprint(context),"approver":"synthetic-test-root",
        "approved_at":now-1,"expires_at":now+60}))
    os.chmod(approvals/(ref+".json"),0o600)
    custody=ConsentCustody128(replay/"consumed.sqlite",approvals_dir=approvals)
    policy=N39ConsentPolicy(tmp_path/"consent.sqlite",synthetic_test_mode=True)
    assert policy.record_original(custody=custody,context=context)
    art,b=setup(tmp_path/"run",policy)
    assert b.execute(signed(art["artifact_id"],"n39-root-no-read-0001"),peer_uid=os.getuid())["http_status"]==403
    policy.record_read_grant(principal=PRINCIPAL,request_id=REQUEST,artifact_id=art["artifact_id"],
       grant_ref="independent-root-test",expires=time.time()+30)
    policy.revoke_original(principal=PRINCIPAL,request_id=REQUEST)
    assert b.execute(signed(art["artifact_id"],"n39-root-after-revoke"),peer_uid=os.getuid())["http_status"]==200
    assert not policy.record_original(custody=custody,context=context)


def test_n39_no_new_science_dispatch_without_fresh_custody():
    from krc_research.stage131_pre_dispatch_custody_gate import execute_with_custody,AuthorizationGateDenied
    import hashlib
    context={"request_id":REQUEST,"task_id":"synthetic","operation":"research.profile.validate",
        "principal":PRINCIPAL,"profile_ref":"profile","evidence_refs":[],
        "payload_sha256":hashlib.sha256(b"synthetic").hexdigest(),
        "consent_ref":"n39-absent-original-consent"}
    dispatched=[]
    def dispatch(operation,payload,principal,*,request_id):
        dispatched.append(request_id)
        return {"status":"PENDING"}
    with pytest.raises(AuthorizationGateDenied,match="CONSENT_DENIED"):
        execute_with_custody(dispatch,authorizer=lambda _:False,context=context,
            operation="research.profile.validate",payload={"task_id":"synthetic"},
            principal=PRINCIPAL,request_id=REQUEST)
    assert not dispatched

def test_n39_revoke_first_wins_atomic_authorization(tmp_path):
    policy=N39ConsentPolicy(tmp_path/"consent.sqlite",synthetic_test_mode=True)
    seed_test_provenance(policy,"synthetic-consent-race")
    art="c"*48
    policy.record_read_grant(principal=PRINCIPAL,request_id=REQUEST,
        artifact_id=art,grant_ref="retrieval-race",expires=time.time()+60)
    # A read authorized before revocation has an earlier linearization point.
    assert policy.is_authorized(principal=PRINCIPAL,request_id=REQUEST,artifact_id=art)
    policy.revoke_read_grant(principal=PRINCIPAL,request_id=REQUEST,artifact_id=art)
    # Revocation committed first: future authorization must fail.
    assert not policy.is_authorized(principal=PRINCIPAL,request_id=REQUEST,artifact_id=art)
