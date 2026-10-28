"""Stage131 private artifact GET denial matrix; no external service or credentials."""
import pytest
from krc_research.artifact_stage117 import HardenedExchange
from krc_research.artifact_exchange import ExchangeError

def test_request_scope_denied(tmp_path):
    store=HardenedExchange(tmp_path/"objects",free_bytes_min=0)
    a=store.store_stream([b"private"],principal="K_Science",request_id="R1",filename="evidence.json")
    with pytest.raises(ExchangeError,match="NOT_FOUND"):
        list(store.read_stream(a["artifact_id"],principal="K_Science",request_id="R2"))
    with pytest.raises(ExchangeError,match="NOT_FOUND"):
        list(store.read_stream(a["artifact_id"],principal="other",request_id="R1"))

def test_invalid_id_and_chunk_denied(tmp_path):
    store=HardenedExchange(tmp_path/"objects",free_bytes_min=0)
    with pytest.raises(ExchangeError,match="NOT_FOUND"):
        list(store.read_stream("../secret",principal="K_Science",request_id="R"))
    with pytest.raises(ExchangeError,match="INVALID_REQUEST"):
        list(store.read_stream("a"*48,principal="K_Science",request_id="R",chunk_size=1024*1024+1))

def test_expiry_and_modified_payload_denied(tmp_path):
    clock=[100.]
    store=HardenedExchange(tmp_path/"objects",free_bytes_min=0,ttl=5,clock=lambda:clock[0])
    a=store.store_stream([b"valid"],principal="K_Science",request_id="R",filename="evidence.json")
    (store.data/a["artifact_id"]).write_bytes(b"tampered")
    with pytest.raises(ExchangeError,match="ARTIFACT_CORRUPTED"):
        list(store.read_stream(a["artifact_id"],principal="K_Science",request_id="R"))
    clock[0]=110
    with pytest.raises(ExchangeError,match="ARTIFACT_EXPIRED"):
        list(store.read_stream(a["artifact_id"],principal="K_Science",request_id="R"))
