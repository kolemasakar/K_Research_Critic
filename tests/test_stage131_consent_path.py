"""Stage131 deny missing path before consent signer construction, isolated only."""
import tempfile
import unittest
from unittest.mock import patch
from krc_research.staging_service123c import make_staging_server

class ConsentPathIsolationTests(unittest.TestCase):
    def test_enabled_signer_requires_explicit_approvals_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch("krc_research.staging_service123c.ScienceAdapter122"), \
                 patch("krc_research.staging_service123c.ReplayRegistry"):
                with self.assertRaisesRegex(ValueError, "EXPLICIT_CONSENT_APPROVALS_DIRECTORY_REQUIRED"):
                    make_staging_server(
                        tmp + "/backend.sock", tmp + "/state",
                        peer_principals={987:"K_Science"},
                        uid_keys={987:{"test":b"K"*32}},
                        claim_allowlist={("K_Science","K_Science","kolemasakar/K_Science","refs/heads/main")},
                        science_secret=b"S"*32,
                        enable_internal_science_signing=True,
                    )

if __name__ == "__main__":
    unittest.main()
