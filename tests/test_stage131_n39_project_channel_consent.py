"""Single-owner project-channel consent: no login prompt, no per-action HMAC.

The sole trusted Python handler represents the already logged-in ChatGPT
project. This is source-only; HTTP or arbitrary user-supplied JSON cannot
directly call the internal handler in an installed environment.
"""
from krc_research.stage131_n39_project_channel_consent import (
    ProjectChannelVerifier, TrustedProjectConsentAdapter
)
from krc_research.stage131_n39_single_owner_chat_consent import (
    SingleOwnerConsentLedger, ConsentDenied, profile_hash
)
import pytest

REQUEST="KS-"+"a"*32
CHAT="owner-project-workflow"
PROFILE={"research":"synthetic concrete NDT","version":1}

def setup(tmp_path):
    now=[10_000]
    verifier=ProjectChannelVerifier(clock=lambda:now[0])
    ledger=SingleOwnerConsentLedger(tmp_path/"private"/"consent.sqlite",
        verifier=verifier,authorized_principal="K_Science",clock=lambda:now[0])
    adapter=TrustedProjectConsentAdapter(ledger=ledger,verifier=verifier)
    assert ledger.propose(request_id=REQUEST,chat_id=CHAT,profile=PROFILE)
    return ledger,adapter,verifier,now

def test_logged_in_project_confirm_requires_no_second_owner_identity(tmp_path):
    ledger,adapter,_,now=setup(tmp_path)
    assert ledger.status(REQUEST)=="PROPOSED"
    assert not ledger.claim_execution(REQUEST)
    assert adapter.confirm_profile(request_id=REQUEST,chat_id=CHAT,profile=PROFILE,decision="APPROVE")
    assert ledger.status(REQUEST)=="APPROVED"
    assert not adapter.confirm_profile(request_id=REQUEST,chat_id=CHAT,profile=PROFILE,decision="APPROVE")
    assert ledger.claim_execution(REQUEST)
    assert not ledger.claim_execution(REQUEST)
    assert ledger.can_continue(REQUEST)
    assert ledger.complete(REQUEST)
    assert ledger.register_artifact(request_id=REQUEST,artifact_id="b"*48)
    assert ledger.is_authorized(principal="K_Science",request_id=REQUEST,artifact_id="b"*48)

def test_changed_profile_wrong_chat_or_untrusted_text_denied(tmp_path):
    ledger,adapter,_,now=setup(tmp_path)
    assert not adapter.confirm_profile(request_id=REQUEST,chat_id="other-chat",profile=PROFILE,decision="APPROVE")
    assert not adapter.confirm_profile(request_id=REQUEST,chat_id=CHAT,
        profile={"research":"different task"},decision="APPROVE")
    assert not ledger.decide(request_id=REQUEST,chat_id=CHAT,
        event={"decision":"APPROVE","owner_ref":"single-chatgpt-project-owner",
               "profile_sha256":profile_hash(PROFILE)})
    assert ledger.status(REQUEST)=="PROPOSED"

def test_expiry_and_cancel_single_owner_without_second_login(tmp_path):
    ledger,adapter,_,now=setup(tmp_path)
    assert adapter.confirm_profile(request_id=REQUEST,chat_id=CHAT,profile=PROFILE,decision="APPROVE")
    assert ledger.claim_execution(REQUEST)
    now[0]+=86400
    assert not ledger.can_continue(REQUEST)
    assert not ledger.complete(REQUEST)
    assert adapter.confirm_profile(request_id=REQUEST,chat_id=CHAT,profile=PROFILE,decision="CANCEL")
    assert ledger.status(REQUEST)=="CANCELLED"
    assert not ledger.claim_execution(REQUEST)

def test_cancel_after_completion_revokes_read_and_requires_new_request(tmp_path):
    ledger,adapter,_,now=setup(tmp_path)
    assert adapter.confirm_profile(request_id=REQUEST,chat_id=CHAT,profile=PROFILE,decision="APPROVE")
    assert ledger.claim_execution(REQUEST)
    assert ledger.complete(REQUEST)
    assert ledger.register_artifact(request_id=REQUEST,artifact_id="c"*48)
    assert ledger.is_authorized(principal="K_Science",request_id=REQUEST,artifact_id="c"*48)
    assert adapter.confirm_profile(request_id=REQUEST,chat_id=CHAT,profile=PROFILE,decision="CANCEL")
    assert not ledger.is_authorized(principal="K_Science",request_id=REQUEST,artifact_id="c"*48)
    assert not adapter.confirm_profile(request_id=REQUEST,chat_id=CHAT,profile=PROFILE,decision="APPROVE")
    request2="KS-"+"d"*32
    assert ledger.propose(request_id=request2,chat_id=CHAT,profile=PROFILE)
    assert adapter.confirm_profile(request_id=request2,chat_id=CHAT,profile=PROFILE,decision="APPROVE")
    assert ledger.claim_execution(request2)

def test_adapter_requires_same_private_trusted_handler(tmp_path):
    ledger,adapter,verifier,now=setup(tmp_path)
    other=ProjectChannelVerifier(clock=lambda:now[0])
    with pytest.raises(ConsentDenied,match="PROJECT_CHANNEL_VERIFIER_REQUIRED"):
        TrustedProjectConsentAdapter(ledger=ledger,verifier=other)
    with pytest.raises(ConsentDenied,match="INVALID_DECISION"):
        adapter.confirm_profile(request_id=REQUEST,chat_id=CHAT,profile=PROFILE,decision="MAYBE")
