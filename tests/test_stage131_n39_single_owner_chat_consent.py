"""Owner-approved N39 chat model: no live chat calls, signing only in synthetic test."""
import hashlib
import hmac
import time
import pytest
from krc_research.stage131_n39_single_owner_chat_consent import (
    SingleOwnerConsentLedger,SignedChatEventVerifier,ConsentDenied,canonical,profile_hash)
from krc_research.stage131_signed_artifact_boundary import SignedArtifactReadBoundary
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
from krc_research.stage131_signed_artifact_read import sign_fixture
from krc_research.request_ledger119 import RequestLedger
from krc_research.artifact_exchange import ArtifactExchange

KEY=b"synthetic-only-gateway-key-with-at-least-32-bytes"
OWNER="only-owner-chat-user"
PRINCIPAL="K_Science"
CHAT="synthetic-chat-0001"
REQUEST="KS-"+"d"*32
PROFILE={"research_profile":"synthetic scientific study","topic":"concrete testing"}
ARTIFACT=b"single-owner-generated-artifact"

def env(tmp_path):
    now=[1000]
    verifier=SignedChatEventVerifier(owner_ref=OWNER,issuer="trusted-chat-gateway",
        key=KEY,clock=lambda:now[0])
    ledger=SingleOwnerConsentLedger(tmp_path/"private"/"consent.sqlite",
        verifier=verifier,authorized_principal=PRINCIPAL,clock=lambda:now[0])
    return ledger,now

def sign(now,decision="APPROVE",*,request_id=REQUEST,chat_id=CHAT,
         digest=None,owner=OWNER,event_ref="synthetic-chat-confirmation-0001"):
    obj={"version":1,"issuer":"trusted-chat-gateway","owner_ref":owner,
         "request_id":request_id,"chat_id":chat_id,
         "profile_sha256":digest or profile_hash(PROFILE),"decision":decision,
         "event_ref":event_ref,"issued_at":now}
    obj["mac_sha256"]=hmac.new(KEY,canonical(obj),hashlib.sha256).hexdigest()
    return obj

def test_profile_confirmation_required_and_one_shot(tmp_path):
    ledger,now=env(tmp_path)
    assert ledger.propose(request_id=REQUEST,chat_id=CHAT,profile=PROFILE)
    assert ledger.status(REQUEST)=="PROPOSED"
    assert not ledger.claim_execution(REQUEST)
    assert not ledger.decide(request_id=REQUEST,chat_id=CHAT,event={"decision":"APPROVE"})
    event=sign(now[0])
    assert ledger.decide(request_id=REQUEST,chat_id=CHAT,event=event)
    assert not ledger.decide(request_id=REQUEST,chat_id=CHAT,event=event)
    assert ledger.claim_execution(REQUEST)
    assert not ledger.claim_execution(REQUEST)
    assert ledger.complete(REQUEST)
    assert not ledger.claim_execution(REQUEST)
    assert ledger.register_artifact(request_id=REQUEST,artifact_id="f"*48)
    assert ledger.is_authorized(principal=PRINCIPAL,request_id=REQUEST,artifact_id="f"*48)
    assert not ledger.is_authorized(principal="foreign",request_id=REQUEST,artifact_id="f"*48)

def test_wrong_chat_profile_owner_and_expired_confirmation_denied(tmp_path):
    ledger,now=env(tmp_path)
    ledger.propose(request_id=REQUEST,chat_id=CHAT,profile=PROFILE)
    for bad in (sign(now[0],chat_id="wrong-chat"),
                sign(now[0],digest="f"*64),sign(now[0],owner="not-owner"),
                sign(now[0]-301)):
        assert not ledger.decide(request_id=REQUEST,chat_id=CHAT,event=bad)
    assert ledger.status(REQUEST)=="PROPOSED"

def test_24h_expiry_and_explicit_cancellation(tmp_path):
    ledger,now=env(tmp_path)
    ledger.propose(request_id=REQUEST,chat_id=CHAT,profile=PROFILE)
    assert ledger.decide(request_id=REQUEST,chat_id=CHAT,event=sign(now[0]))
    now[0]+=86400
    assert ledger.status(REQUEST)=="EXPIRED"
    assert not ledger.claim_execution(REQUEST)
    now[0]-=86400
    assert ledger.decide(request_id=REQUEST,chat_id=CHAT,
        event=sign(now[0],"CANCEL",event_ref="synthetic-chat-cancel-00001"))
    assert ledger.status(REQUEST)=="CANCELLED"
    assert not ledger.claim_execution(REQUEST)

def test_cancel_after_completion_revokes_artifact_read_and_new_approval_needed(tmp_path):
    ledger,now=env(tmp_path)
    ledger.propose(request_id=REQUEST,chat_id=CHAT,profile=PROFILE)
    assert ledger.decide(request_id=REQUEST,chat_id=CHAT,event=sign(now[0]))
    assert ledger.claim_execution(REQUEST) and ledger.complete(REQUEST)
    assert ledger.register_artifact(request_id=REQUEST,artifact_id="a"*48)
    now[0]+=86401
    # 24h cap governs execution, not existing saved-artifact retention.
    assert ledger.is_authorized(principal=PRINCIPAL,request_id=REQUEST,artifact_id="a"*48)
    assert ledger.decide(request_id=REQUEST,chat_id=CHAT,
        event=sign(now[0],"CANCEL",event_ref="synthetic-chat-cancel-00002"))
    assert not ledger.is_authorized(principal=PRINCIPAL,request_id=REQUEST,artifact_id="a"*48)
    assert not ledger.decide(request_id=REQUEST,chat_id=CHAT,event=sign(now[0]))
    newreq="KS-"+"e"*32
    assert ledger.propose(request_id=newreq,chat_id=CHAT,profile=PROFILE)
    assert ledger.decide(request_id=newreq,chat_id=CHAT,event=sign(now[0],
        request_id=newreq,event_ref="new-independent-confirm-0001"))
    assert ledger.claim_execution(newreq)

def test_crash_reopen_never_reissues_execution(tmp_path):
    ledger,now=env(tmp_path)
    ledger.propose(request_id=REQUEST,chat_id=CHAT,profile=PROFILE)
    assert ledger.decide(request_id=REQUEST,chat_id=CHAT,event=sign(now[0]))
    assert ledger.claim_execution(REQUEST)
    recovered=SingleOwnerConsentLedger(tmp_path/"private"/"consent.sqlite",
        verifier=ledger.verifier,authorized_principal=PRINCIPAL,clock=lambda:now[0])
    assert recovered.status(REQUEST)=="RUNNING"
    assert not recovered.claim_execution(REQUEST)

def test_authenticated_chat_consent_with_real_artifact_scope(tmp_path):
    from krc_research.stage131_signed_artifact_read import sign_fixture
    ledger,now=env(tmp_path)
    ledger.propose(request_id=REQUEST,chat_id=CHAT,profile=PROFILE)
    assert ledger.decide(request_id=REQUEST,chat_id=CHAT,event=sign(now[0]))
    assert ledger.claim_execution(REQUEST)
    assert ledger.complete(REQUEST)
    store=ArtifactExchange(tmp_path/"objects")
    art=store.store_bytes(ARTIFACT,principal=PRINCIPAL,request_id=REQUEST,filename="test.bin")
    assert ledger.register_artifact(request_id=REQUEST,artifact_id=art["artifact_id"])
    account={"principal":PRINCIPAL,"repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}
    mac_key=b"synthetic-only-valid-signed-artifact-hmac-key"
    boundary=SignedArtifactReadBoundary(exchange=store,ledger=RequestLedger(tmp_path/"requests.sqlite"),
        nonce_registry=ArtifactNonceRegistry(tmp_path/"nonce.sqlite"),keyring={"k":mac_key},
        trusted_peer_identities={98765:account},enabled=True,retrieval_authorizer=ledger.is_authorized)
    payload={"task_id":"synthetic"}
    boundary.ledger.admit(principal=PRINCIPAL,request_id=REQUEST,operation="research.profile.validate",payload=payload)
    boundary.ledger.complete(principal=PRINCIPAL,request_id=REQUEST,operation="research.profile.validate",payload=payload,result={"status":"completed"})
    def signed(nonce):
        return sign_fixture({"version":"krc-artifact-get/1","operation":"artifact.read",
            "request_id":REQUEST,"artifact_id":art["artifact_id"],"identity":account,
            "auth":{"key_id":"k","issued_at_epoch":int(time.time()),"nonce":nonce,
                    "mac_sha256":"0"*64}},mac_key)
    valid=boundary.execute(signed("owner-chat-nonce-000001"),peer_uid=98765)
    assert valid["http_status"]==200 and valid["body_bytes"]==ARTIFACT
    assert boundary.execute(signed("owner-chat-nonce-000001"),peer_uid=98765)["http_status"]==403
    assert ledger.decide(request_id=REQUEST,chat_id=CHAT,
        event=sign(now[0],"CANCEL",event_ref="authenticated-cancel-0001"))
    denied=boundary.execute(signed("owner-chat-nonce-000002"),peer_uid=98765)
    assert denied["http_status"]==403 and "body_bytes" not in denied


def test_running_research_checks_cancel_and_24h_during_execution(tmp_path):
    ledger,now=env(tmp_path)
    assert ledger.propose(request_id=REQUEST,chat_id=CHAT,profile=PROFILE)
    assert ledger.decide(request_id=REQUEST,chat_id=CHAT,event=sign(now[0]))
    assert ledger.claim_execution(REQUEST) and ledger.can_continue(REQUEST)
    now[0]+=86400
    assert not ledger.can_continue(REQUEST)
    assert not ledger.complete(REQUEST)
    now[0]-=86400
    assert ledger.decide(request_id=REQUEST,chat_id=CHAT,
        event=sign(now[0],"CANCEL",event_ref="cancel-during-research-001"))
    assert not ledger.can_continue(REQUEST)
    assert not ledger.complete(REQUEST)
