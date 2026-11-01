"""Source-only integration: real ArtifactExchange + RequestLedger + signed UDS."""
import hashlib
import json
import os
import socket
import tempfile
import threading
import time
from pathlib import Path

from krc_research.artifact_exchange import ArtifactExchange
from krc_research.request_ledger119 import RequestLedger
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
from krc_research.stage131_signed_artifact_boundary import SignedArtifactReadBoundary
from krc_research.stage131_signed_artifact_read import sign_fixture
from krc_research.stage131_signed_artifact_uds import SignedArtifactUDSServer

KEY=b"synthetic-retrieval-secret-key-only"
IDENTITY={"principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}
REQUEST_ID="KS-"+"d"*32

def signed(artifact_id,nonce):
    return sign_fixture({
        "version":"krc-artifact-get/1","operation":"artifact.read",
        "request_id":REQUEST_ID,"artifact_id":artifact_id,"identity":IDENTITY,
        "auth":{"key_id":"test-only","issued_at_epoch":int(time.time()),
                "nonce":nonce,"mac_sha256":"0"*64}},KEY)

def configured(root,*,clock=time.time,complete=True):
    store=ArtifactExchange(root/"objects_store",clock=clock)
    ledger=RequestLedger(root/"requests.sqlite")
    payload={"task_id":"synthetic"}
    ledger.admit(principal="K_Science",request_id=REQUEST_ID,
                 operation="research.profile.validate",payload=payload)
    if complete:
        ledger.complete(principal="K_Science",request_id=REQUEST_ID,
                        operation="research.profile.validate",payload=payload,result={"status":"completed"})
    boundary=SignedArtifactReadBoundary(
        exchange=store,ledger=ledger,
        nonce_registry=ArtifactNonceRegistry(root/"nonce.sqlite"),
        keyring={"test-only":KEY},
        trusted_peer_identities={os.getuid():IDENTITY},enabled=True)
    return store,boundary

def test_real_store_signed_read_authorization_ledger_and_hash(tmp_path):
    store,boundary=configured(tmp_path)
    data=b"trusted actual store bytes"
    art=store.store_bytes(data,principal="K_Science",request_id=REQUEST_ID,filename="a.bin")
    m=signed(art["artifact_id"],"nonce-real-store-0001")
    ok=boundary.execute(m,peer_uid=os.getuid())
    assert ok["http_status"]==200
    assert ok["body_bytes"]==data
    assert ok["sha256"]==art["sha256"]==hashlib.sha256(data).hexdigest()
    assert ok["size_bytes"]==art["size_bytes"]
    assert boundary.execute(m,peer_uid=os.getuid())["http_status"]==403
    assert boundary.execute(signed(art["artifact_id"],"nonce-real-store-0002"),peer_uid=os.getuid()+100000)["http_status"]==403
    other=store.store_bytes(b"other",principal="other",request_id=REQUEST_ID,filename="other.bin")
    assert boundary.execute(signed(other["artifact_id"],"nonce-real-store-0003"),peer_uid=os.getuid())["http_status"]==404
    foreign_request=store.store_bytes(b"wrong",principal="K_Science",request_id="other-request",filename="wrong.bin")
    assert boundary.execute(signed(foreign_request["artifact_id"],"nonce-real-store-0004"),peer_uid=os.getuid())["http_status"]==404
    (store.data/art["artifact_id"]).write_bytes(b"modified actual store bytes")
    corrupted=boundary.execute(signed(art["artifact_id"],"nonce-real-store-0005"),peer_uid=os.getuid())
    assert corrupted["http_status"]==502
    assert "body_bytes" not in corrupted and "body_file" not in corrupted

def test_incomplete_ledger_and_exact_ttl_expiry(tmp_path):
    clock=[1000.0]
    store,boundary=configured(tmp_path,clock=lambda:clock[0],complete=False)
    art=store.store_bytes(b"expires",principal="K_Science",request_id=REQUEST_ID,filename="f")
    assert boundary.execute(signed(art["artifact_id"],"nonce-ledger-block-0001"),peer_uid=os.getuid())["http_status"]==404
    payload={"task_id":"synthetic"}
    boundary.ledger.complete(principal="K_Science",request_id=REQUEST_ID,
                             operation="research.profile.validate",payload=payload,result={"status":"completed"})
    clock[0]=1000.0+604800
    assert boundary.execute(signed(art["artifact_id"],"nonce-ttl-expire-0002"),peer_uid=os.getuid())["http_status"]==410

def test_real_uds_http_uses_trusted_store_and_ledger(tmp_path):
    store,boundary=configured(tmp_path)
    data=b"real trusted scoped bytes over UDS"
    art=store.store_bytes(data,principal="K_Science",request_id=REQUEST_ID,filename="a.bin")
    sock=tmp_path/"api.sock"
    server=SignedArtifactUDSServer(sock,boundary=boundary)
    th=threading.Thread(target=server.serve_forever,daemon=True)
    th.start()
    try:
        def call(msg):
            raw=json.dumps(msg,separators=(",",":")).encode()
            with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as client:
                client.settimeout(3)
                client.connect(str(sock))
                client.sendall(b"POST /v1/artifacts/read HTTP/1.1\r\nHost: local\r\nContent-Type: application/json\r\nContent-Length: "+str(len(raw)).encode()+b"\r\n\r\n"+raw)
                client.shutdown(socket.SHUT_WR)
                wire=b""
                while True:
                    part=client.recv(65536)
                    if not part:break
                    wire+=part
            return wire.split(b"\r\n\r\n",1)
        head,body=call(signed(art["artifact_id"],"nonce-uds-trusted-0001"))
        assert b"200 OK" in head
        assert body==data
        assert b"X-Content-SHA256: "+art["sha256"].encode() in head
        assert b"X-Content-Type-Options: nosniff" in head
        assert b"Content-Length: "+str(len(data)).encode() in head
        head,body=call(signed(art["artifact_id"],"nonce-uds-trusted-0001"))
        assert b"403 Forbidden" in head
    finally:
        server.shutdown();server.server_close();th.join(timeout=2)
