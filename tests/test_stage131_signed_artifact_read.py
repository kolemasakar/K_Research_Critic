import copy
import pytest
from krc_research.stage131_signed_artifact_read import canonical_bytes,verify_signed_read,sign_fixture,ArtifactReadDenied
KEY=b"synthetic-signing-key-32-bytes-only"
IDENTITY={"principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}
BODY={"version":"krc-artifact-get/1","operation":"artifact.read","request_id":"KS-"+"a"*32,"artifact_id":"b"*48,"identity":IDENTITY,"auth":{"key_id":"synthetic-only","issued_at_epoch":1000,"nonce":"nonce-1234567890123456","mac_sha256":"0"*64}}
def signed():return sign_fixture(BODY,KEY)
def verify(m,claim=lambda *a:True,identity=IDENTITY):
    return verify_signed_read(m,trusted_identity=identity,secret=KEY,nonce_claim=claim,now_epoch=1000)
def test_positive_and_exact_fixture():
    s=signed();assert len(s["auth"]["mac_sha256"])==64
    assert verify(s)["artifact_id"]=="b"*48
    assert b'"operation":"artifact.read"' in canonical_bytes(s)
    assert b"mac_sha256" not in canonical_bytes(s)
@pytest.mark.parametrize("field",["operation","request_id","artifact_id","version"])
def test_tampered_signed_field_denied(field):
    s=signed();s[field]="changed"
    with pytest.raises(ArtifactReadDenied):verify(s)
def test_wrong_identity_denied():
    with pytest.raises(ArtifactReadDenied):verify(signed(),identity={**IDENTITY,"principal":"OTHER"})
def test_replay_denied():
    seen=set()
    def claim(*a):
        if a in seen:return False
        seen.add(a);return True
    s=signed();assert verify(s,claim)
    with pytest.raises(ArtifactReadDenied,match="REPLAY_DENIED"):verify(s,claim)
def test_expired_and_wrong_key_denied():
    s=signed()
    with pytest.raises(ArtifactReadDenied,match="STALE_SIGNATURE"):
        verify_signed_read(s,trusted_identity=IDENTITY,secret=KEY,nonce_claim=lambda *a:True,now_epoch=1400)
    with pytest.raises(ArtifactReadDenied,match="BAD_SIGNATURE"):
        verify_signed_read(s,trusted_identity=IDENTITY,secret=b"another-synthetic-signing-key",nonce_claim=lambda *a:True,now_epoch=1000)
def test_missing_auth_denied():
    s=signed();del s["auth"]["nonce"]
    with pytest.raises(ArtifactReadDenied):verify(s)
