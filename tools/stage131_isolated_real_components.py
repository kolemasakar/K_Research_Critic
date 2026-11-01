"""Isolated real-component fixture for independent Sentinel N01-N40 tests.

Never starts production services. Only temporary AF_UNIX+SQLite with synthetic
credentials and real KRC validation, ledger, nonce and ArtifactExchange code.
"""
import hashlib
import os
import socket
import tempfile
import threading
import time
from contextlib import contextmanager
from pathlib import Path

from krc_research.artifact_exchange import ArtifactExchange
from krc_research.request_ledger119 import RequestLedger
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
from krc_research.stage131_signed_artifact_boundary import SignedArtifactReadBoundary
from krc_research.stage131_signed_artifact_read import sign_fixture
from krc_research.stage131_signed_artifact_uds import SignedArtifactUDSServer

TEST_KEY=b"synthetic-retrieval-secret-key-only"
TEST_IDENTITY={"principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}
TEST_REQUEST_ID="KS-"+"d"*32
TEST_OPERATION="research.profile.validate"
TEST_PAYLOAD={"task_id":"synthetic"}
TEST_BODY=b"stage131-real-component-fixture-v1"

class RealComponentsFixture:
    def __init__(self, root):
        self.root=Path(root)
        self.root.mkdir(parents=True,exist_ok=True)
        self.exchange=ArtifactExchange(self.root/"trusted-store")
        self.ledger=RequestLedger(self.root/"ledger.sqlite")
        self.nonce=ArtifactNonceRegistry(self.root/"nonce.sqlite")
        self.ledger.admit(principal="K_Science",request_id=TEST_REQUEST_ID,operation=TEST_OPERATION,payload=TEST_PAYLOAD)
        self.ledger.complete(principal="K_Science",request_id=TEST_REQUEST_ID,operation=TEST_OPERATION,payload=TEST_PAYLOAD,result={"status":"completed"})
        self.artifact=self.exchange.store_bytes(TEST_BODY,principal="K_Science",request_id=TEST_REQUEST_ID,filename="synthetic.bin")
        self.boundary=SignedArtifactReadBoundary(
            exchange=self.exchange,ledger=self.ledger,nonce_registry=self.nonce,
            keyring={"synthetic-only":TEST_KEY},
            trusted_peer_identities={os.getuid():TEST_IDENTITY},enabled=True)
        self.socket_path=self.root/"read.sock"
        self.server=None
        self.thread=None

    def signed_request(self, nonce="fixture-nonce-00000001", *, artifact_id=None, request_id=TEST_REQUEST_ID,
                       identity=None, issued_at_epoch=None):
        return sign_fixture({
            "version":"krc-artifact-get/1","operation":"artifact.read",
            "request_id":request_id,"artifact_id":artifact_id or self.artifact["artifact_id"],
            "identity":identity or TEST_IDENTITY,
            "auth":{"key_id":"synthetic-only",
                    "issued_at_epoch":int(time.time()) if issued_at_epoch is None else issued_at_epoch,
                    "nonce":nonce,"mac_sha256":"0"*64}},TEST_KEY)

    def start(self):
        if self.server is not None:raise RuntimeError("ALREADY_STARTED")
        self.server=SignedArtifactUDSServer(self.socket_path,boundary=self.boundary)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
        return str(self.socket_path)

    def close(self):
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()
            self.thread.join(timeout=3)
            self.server=None

    def descriptor(self):
        return dict(self.artifact)

@contextmanager
def isolated_real_components():
    with tempfile.TemporaryDirectory(prefix="krc-real-components-") as d:
        fixture=RealComponentsFixture(d)
        try:
            fixture.start()
            yield fixture
        finally:
            fixture.close()
