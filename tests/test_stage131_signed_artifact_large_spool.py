import tempfile
from pathlib import Path
from krc_research.stage131_signed_artifact_boundary import SignedArtifactReadBoundary
from krc_research.stage131_signed_artifact_read import sign_fixture
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
from krc_research.request_ledger119 import RequestLedger
from krc_research.artifact_exchange import ExchangeError
KEY=b"synthetic-retrieval-secret-key-only"
ID={"principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}
def make(d,exchange):
    l=RequestLedger(Path(d)/"requests.sqlite")
    p={"task_id":"t"}
    q="KS-"+"a"*32
    l.admit(principal="K_Science",request_id=q,operation="research.profile.validate",payload=p)
    l.complete(principal="K_Science",request_id=q,operation="research.profile.validate",payload=p,result={"status":"completed"})
    b=SignedArtifactReadBoundary(exchange=exchange,ledger=l,nonce_registry=ArtifactNonceRegistry(Path(d)/"nonce.sqlite",clock=lambda:1000),keyring={"k":KEY},trusted_peer_identities={123:ID},enabled=True)
    m={"version":"krc-artifact-get/1","operation":"artifact.read","request_id":q,"artifact_id":"b"*48,"identity":ID,"auth":{"key_id":"k","issued_at_epoch":1000,"nonce":"1234567890123456","mac_sha256":"0"*64}}
    return b,sign_fixture(m,KEY)
class Large:
    def read_stream(self,*a,**kw):
        for i in range(12):
            yield b"x"*(256*1024)
class Broken:
    def read_stream(self,*a,**kw):
        yield b"x"*(2*1024*1024)
        raise ExchangeError("ARTIFACT_CORRUPTED")
def test_large_verified_spool_and_close():
    with tempfile.TemporaryDirectory() as d:
        b,m=make(d,Large())
        r=b.execute(m,peer_uid=123,now_epoch=1000)
        assert r["http_status"]==200 and r["size_bytes"]==3*1024*1024
        f=r["body_file"]
        try:
            assert sum(len(x) for x in iter(lambda:f.read(256*1024),b""))==r["size_bytes"]
        finally:f.close()
        assert f.closed
def test_corruption_before_first_byte():
    with tempfile.TemporaryDirectory() as d:
        b,m=make(d,Broken())
        r=b.execute(m,peer_uid=123,now_epoch=1000)
        assert r["http_status"]==502 and "body_file" not in r and "body_bytes" not in r
def test_spool_limit_denies_without_stream():
    with tempfile.TemporaryDirectory() as d:
        b,m=make(d,Large())
        b.max_artifact_bytes=1024*1024
        r=b.execute(m,peer_uid=123,now_epoch=1000)
        assert r["http_status"]==413 and "body_file" not in r
