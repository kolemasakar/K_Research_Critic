"""Stage131 safety checks: no daemon start, no network, no secrets."""
import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from krc_research.staging_entrypoint131 import (
    load_stage131_config, Stage131ConfigurationError
)

class Stage131ConfigTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.cfg = self.base / "staging.json"
        self.good = dict(
            socket_path="/run/krc-stage131/backend.sock",
            state_root="/var/lib/krc-stage131",
            peer_uid=987,
            principal="K_Science",
            key_id="test",
            transport_key_file="/etc/krc-stage131/transport.key",
            science_key_file="/etc/krc-stage131/science.key",
            client="science",
            repository="kolemasakar/K_Science",
            workflow_ref="refs/heads/main",
            enable_internal_science_signing=False,
        )
    def write(self, **overrides):
        self.cfg.write_text(json.dumps({**self.good, **overrides}))
        self.cfg.chmod(0o600)
    def check_reject(self, **kwargs):
        self.write(**kwargs)
        with patch("krc_research.staging_entrypoint131.os.geteuid", return_value=os.getuid()):
            with self.assertRaises(Stage131ConfigurationError):
                load_stage131_config(str(self.cfg))
    def test_science_signer_requires_explicit_separate_gate(self):
        self.check_reject(enable_internal_science_signing=True)
    def test_old_socket_is_denied(self):
        self.check_reject(socket_path="/run/krc-research-v2/backend.sock")
    def test_old_state_is_denied(self):
        self.check_reject(state_root="/var/lib/krc-research-v2")
    def test_old_secret_path_is_denied(self):
        self.check_reject(science_key_file="/etc/krc-research-v2/science.key")
    def test_nonprivate_config_is_denied(self):
        self.write()
        self.cfg.chmod(0o644)
        with patch("krc_research.staging_entrypoint131.os.geteuid", return_value=os.getuid()):
            with self.assertRaises(Stage131ConfigurationError):
                load_stage131_config(str(self.cfg))
    def test_unknown_config_property_is_denied(self):
        self.write(untrusted_property=True)
        with patch("krc_research.staging_entrypoint131.os.geteuid", return_value=os.getuid()):
            with self.assertRaises(Stage131ConfigurationError):
                load_stage131_config(str(self.cfg))

if __name__ == "__main__":
    unittest.main()
