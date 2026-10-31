import tempfile
from pathlib import Path
from krc_research.stage131_signed_artifact_boundary import SignedArtifactReadBoundary
from krc_research.stage131_signed_artifact_read import sign_fixture
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
from krc_research.request_ledger119 import RequestLedger
from krc_research.artifact_exchange import ExchangeError

KEY=b"synthetic-retrieval-secret-key-only"
IDENTITY={"principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}
BASE={"version":"krc-artifact-get/1","operation":"artifact.read",
      "request_id":"KS-"+"a"*32,"artifact_id":"b"*48,"identity":IDENTITY,
      "auth":{"key_id":"synthetic-only","issued_at_epoch":1000,
              "nonce":"nonce-1234567890123456","mac_sha256":"0"*64}}
class Exchange:
    def __init__(self,error=None):self.error=error
    def read_stream(self,*a,**kw):
        if self.error:raise ExchangeError(self.error)
        yield b"verified "
        yield b"synthetic"
def setup(d,*,error=None,enable=True,complete=True):
    ledger=RequestLedger(Path(d)/"request.sqlite")
    req={"task_id":"dummy"}
    claim=ledger.admit(principal="K_Science",request_id=BASE["request_id"],
                       operation="research.profile.validate",payload=req)
    if complete:ledger.complete(principal="K_Science",request_id=BASE["request_id"],
                       operation="research.profile.validate",payload=req,result={"status":"completed"})
    return SignedArtifactReadBoundary(exchange=Exchange(error),ledger=ledger,
        nonce_registry=ArtifactNonceRegistry(Path(d)/"nonce.sqlite",clock=lambda:1000),
        keyring={"synthetic-only":KEY},trusted_peer_identities={123:IDENTITY},
        enabled=enable)
def request():return sign_fixture(BASE,KEY)
def test_signed_read_success_and_denials():
    with tempfile.TemporaryDirectory() as d:
        b=setup(d)
        assert b.execute(request(),peer_uid=123,now_epoch=1000)["body_bytes"]==b"verified synthetic"
        assert b.execute(request(),peer_uid=123,now_epoch=1000)["http_status"]==403
        assert b.execute(request(),peer_uid=456,now_epoch=1000)["http_status"]==403
def test_default_off_never_reads():
    with tempfile.TemporaryDirectory() as d:
        assert setup(d,enable=False).execute(request(),peer_uid=123,now_epoch=1000)["http_status"]==404
def test_uncompleted_ledger_and_expired():
    with tempfile.TemporaryDirectory() as d:
        assert setup(d,complete=False).execute(request(),peer_uid=123,now_epoch=1000)["http_status"]==404
    with tempfile.TemporaryDirectory() as d:
        assert setup(d,error="ARTIFACT_EXPIRED").execute(request(),peer_uid=123,now_epoch=1000)["http_status"]==410
def test_corrupt_and_wrong_key():
    with tempfile.TemporaryDirectory() as d:
        assert setup(d,error="ARTIFACT_CORRUPTED").execute(request(),peer_uid=123,now_epoch=1000)["http_status"]==502
    with tempfile.TemporaryDirectory() as d:
        altered=request();altered["artifact_id"]="c"*48
        assert setup(d).execute(altered,peer_uid=123,now_epoch=1000)["http_status"]==403
