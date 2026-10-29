"""Synthetic, unprivileged Stage131 secret custody and config validation.

No real owner grants, no live keys, no /etc writes.
"""
import json
import os
from pathlib import Path
import pytest
from krc_research.staging_entrypoint124 import secret
from krc_research.staging_entrypoint131 import Stage131ConfigurationError, load_stage131_config

def test_synthetic_secret_custody(tmp_path):
    key=tmp_path/"synthetic-only.key"
    key.write_bytes(b"s"*32)
    key.chmod(0o600)
    assert len(secret(str(key)))==32
    key.chmod(0o640)
    with pytest.raises(ValueError):
        secret(str(key))
    key.chmod(0o600)
    key.unlink()
    with pytest.raises(OSError):
        secret(str(key))

def test_config_never_accepts_internal_signer(tmp_path,monkeypatch):
    config=tmp_path/"staging.json"
    cfg={
        "socket_path":"/run/krc-stage131/backend.sock",
        "state_root":"/var/lib/krc-stage131",
        "peer_uid":os.geteuid()+1,
        "principal":"synthetic-peer",
        "key_id":"synthetic-key-id",
        "transport_key_file":"/etc/krc-stage131/transport.key",
        "science_key_file":"/etc/krc-stage131/science.key",
        "client":"synthetic-client",
        "repository":"synthetic-repo",
        "workflow_ref":"synthetic-workflow",
        "enable_internal_science_signing":True,
    }
    config.write_text(json.dumps(cfg))
    config.chmod(0o600)
    with pytest.raises(Stage131ConfigurationError,match="SCIENCE_SIGNING_REQUIRES"):
        load_stage131_config(str(config))
    config.chmod(0o644)
    with pytest.raises(Stage131ConfigurationError,match="UNSAFE_CONFIG"):
        load_stage131_config(str(config))
