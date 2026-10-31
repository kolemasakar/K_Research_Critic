import tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry

def test_nonce_replay_survives_reopen_and_scope():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/"replay.sqlite"
        r=ArtifactNonceRegistry(p,clock=lambda:1000)
        assert r.claim("key","nonce-123456789012345","K_Science")
        assert not r.claim("key","nonce-123456789012345","K_Science")
        assert not ArtifactNonceRegistry(p,clock=lambda:1001).claim("key","nonce-123456789012345","K_Science")
        assert r.claim("key","nonce-123456789012345","OTHER")
def test_concurrent_claim_only_one_wins():
    with tempfile.TemporaryDirectory() as d:
        r=ArtifactNonceRegistry(Path(d)/"replay.sqlite",clock=lambda:1000)
        with ThreadPoolExecutor(max_workers=8) as e:
            out=list(e.map(lambda _:r.claim("k","n","principal"),range(20)))
        assert out.count(True)==1
def test_ttl_expires_after_approved_window():
    with tempfile.TemporaryDirectory() as d:
        clock=[1000]
        r=ArtifactNonceRegistry(Path(d)/"replay.sqlite",clock=lambda:clock[0])
        assert r.claim("k","n","p")
        clock[0]=1901
        assert r.claim("k","n","p")
