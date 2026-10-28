import json
import pytest
from krc_research.artifact_exchange import ArtifactExchange,ExchangeError,deliver_result,MIB

def test_inline_small(tmp_path):
    s=ArtifactExchange(tmp_path/"store")
    assert deliver_result({"text":"hello"},exchange=s,principal="p",request_id="r")["delivery"]=="inline"

def test_boundary_unicode_encoded(tmp_path):
    s=ArtifactExchange(tmp_path/"store")
    x=deliver_result({"text":"Ї"*550000},exchange=s,principal="p",request_id="r")
    assert x["delivery"]=="artifact"
    body=s.get_bytes(x["artifact"]["artifact_id"],principal="p",request_id="r")
    assert json.loads(body)["text"]=="Ї"*550000

def test_large_and_hash(tmp_path):
    s=ArtifactExchange(tmp_path/"store")
    out=deliver_result({"text":"x"*MIB},exchange=s,principal="p",request_id="r")
    assert out["delivery"]=="artifact"
    assert len(s.get_bytes(out["artifact"]["artifact_id"],principal="p",request_id="r"))>MIB

def test_cross_principal_denied(tmp_path):
    s=ArtifactExchange(tmp_path/"store")
    x=s.store_bytes(b"test",principal="p",request_id="r",filename="a.pdf")
    with pytest.raises(ExchangeError,match="NOT_FOUND"):
        s.get_bytes(x["artifact_id"],principal="other",request_id="r")
    with pytest.raises(ExchangeError,match="NOT_FOUND"):
        s.get_bytes(x["artifact_id"],principal="p",request_id="other")

def test_corrupted(tmp_path):
    s=ArtifactExchange(tmp_path/"store")
    x=s.store_bytes(b"abc",principal="p",request_id="r",filename="file.docx")
    (s.data/x["artifact_id"]).write_bytes(b"xyz")
    with pytest.raises(ExchangeError,match="ARTIFACT_CORRUPTED"):
        s.get_bytes(x["artifact_id"],principal="p",request_id="r")

def test_quota(tmp_path):
    s=ArtifactExchange(tmp_path/"store",max_artifact=5,max_total=5)
    s.store_bytes(b"1234",principal="p",request_id="r",filename="1.pdf")
    with pytest.raises(ExchangeError,match="STORAGE_QUOTA_EXCEEDED"):
        s.store_bytes(b"4567",principal="p",request_id="r",filename="2.pdf")

def test_per_file_limit(tmp_path):
    s=ArtifactExchange(tmp_path/"store",max_artifact=3)
    with pytest.raises(ExchangeError,match="ARTIFACT_TOO_LARGE"):
        s.store_bytes(b"1234",principal="p",request_id="r",filename="a.pdf")

def test_ttl_cleanup(tmp_path):
    now=[100]
    s=ArtifactExchange(tmp_path/"store",ttl=10,clock=lambda:now[0])
    x=s.store_bytes(b"abc",principal="p",request_id="r",filename="a.pdf")
    now[0]=111
    with pytest.raises(ExchangeError,match="ARTIFACT_EXPIRED"):
        s.get_bytes(x["artifact_id"],principal="p",request_id="r")
    assert s.cleanup_expired()==1

def test_path_rejected(tmp_path):
    s=ArtifactExchange(tmp_path/"store")
    with pytest.raises(ExchangeError,match="INVALID_REQUEST"):
        s.store_bytes(b"a",principal="p",request_id="r",filename="../secret")

def test_invalid_id_rejected(tmp_path):
    s=ArtifactExchange(tmp_path/"store")
    with pytest.raises(ExchangeError,match="NOT_FOUND"):
        s.get_bytes("../../etc/passwd",principal="p",request_id="r")

def test_symlink_rejected(tmp_path):
    s=ArtifactExchange(tmp_path/"store")
    x=s.store_bytes(b"hello",principal="p",request_id="r",filename="f")
    (s.data/x["artifact_id"]).unlink()
    (s.data/x["artifact_id"]).symlink_to("/etc/passwd")
    with pytest.raises(ExchangeError,match="ARTIFACT_UNAVAILABLE"):
        s.get_bytes(x["artifact_id"],principal="p",request_id="r")

def test_json_nan_denied(tmp_path):
    s=ArtifactExchange(tmp_path/"store")
    with pytest.raises(ExchangeError,match="INVALID_RESULT"):
        deliver_result({"x":float("nan")},exchange=s,principal="p",request_id="r")

def test_chunked_verified_read(tmp_path):
    s=ArtifactExchange(tmp_path/"store")
    x=s.store_bytes(b"abcdefgh",principal="p",request_id="r",filename="a.bin")
    assert list(s.iter_chunks(x["artifact_id"],principal="p",request_id="r",chunk_size=3))==[b"abc",b"def",b"gh"]

def test_orphan_reconciliation(tmp_path):
    s=ArtifactExchange(tmp_path/"store")
    orphan=s.data/("a"*48)
    orphan.write_bytes(b"orphan")
    assert s.reconcile_orphans()==1
    assert not orphan.exists()

def test_invalid_quotas(tmp_path):
    with pytest.raises(ExchangeError,match="INVALID_CONFIGURATION"):
        ArtifactExchange(tmp_path/"store",max_artifact=10,max_total=5)

def test_unindexed_file_not_served(tmp_path):
    s=ArtifactExchange(tmp_path/"store")
    (s.data/("a"*48)).write_bytes(b"foo")
    with pytest.raises(ExchangeError,match="NOT_FOUND"):
        s.get_bytes("a"*48,principal="p",request_id="r")
