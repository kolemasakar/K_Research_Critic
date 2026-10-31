import hashlib, tempfile
from pathlib import Path
from krc_research.stage131_signed_artifact_boundary import SignedArtifactReadBoundary
from krc_research.stage131_signed_artifact_read import sign_fixture
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
from krc_research.request_ledger119 import RequestLedger
from krc_research.artifact_exchange import ExchangeError

KEY=b"synthetic-retrieval-secret-key-only"
IDENTITY={"principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}
REQ="KS-"+"a"*32
class Source:
    def __init__(self,pieces,fail=False): self.pieces=pieces;self.fail=fail
    def read_stream(self,*a,**kw):
        for p in self.pieces: yield p
        if self.fail: raise ExchangeError("ARTIFACT_CORRUPTED")

def run(pieces,fail=False):
    with tempfile.TemporaryDirectory() as d:
        ledger=RequestLedger(Path(d)/"ledger.sqlite")
        payload={"source":"fixture"}
        ledger.admit(principal="K_Science",request_id=REQ,operation="research.profile.validate",payload=payload)
        ledger.complete(principal="K_Science",request_id=REQ,operation="research.profile.validate",payload=payload,result={"status":"completed"})
        b=SignedArtifactReadBoundary(exchange=Source(pieces,fail),ledger=ledger,nonce_registry=ArtifactNonceRegistry(Path(d)/"nonce.sqlite",clock=lambda:1000),keyring={"k":KEY},trusted_peer_identities={100:IDENTITY},enabled=True)
        msg={"version":"krc-artifact-get/1","operation":"artifact.read","request_id":REQ,"artifact_id":"b"*48,"identity":IDENTITY,"auth":{"key_id":"k","issued_at_epoch":1000,"nonce":"nonce-1234567890123456","mac_sha256":"0"*64}}
        result=b.execute(sign_fixture(msg,KEY),peer_uid=100,now_epoch=1000)
        if "body_file" in result:
            f=result.pop("body_file")
            try: result["captured"]=f.read()
            finally: f.close()
        return result

def test_inline_digest_is_of_returned_bytes():
    r=run([b"abc",b"def"])
    assert r["http_status"]==200 and r["size_bytes"]==6
    assert r["sha256"]==hashlib.sha256(r["body_bytes"]).hexdigest()
def test_spooled_digest_is_of_returned_bytes():
    r=run([b"z"*700000,b"x"*700000])
    assert r["http_status"]==200 and r["size_bytes"]==1400000
    assert r["sha256"]==hashlib.sha256(r["captured"]).hexdigest()
def test_corrupt_source_never_exposes_digest_or_bytes():
    r=run([b"a"*1400000],True)
    assert r["http_status"]==502 and not any(k in r for k in ("sha256","body_bytes","body_file"))
