"""End-to-end MCP error mapping tests: no external provider work."""
import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from plugins.krc_migration_candidate.mcp_canary.r3c import (
    VoiceBridgeBinding, VoiceBridgeError, _sanitized_backend_error, call_voicebridge,
)

def failure(body, status=429, headers=None):
    return HTTPError("https://example.invalid", status, "failure", headers or {}, io.BytesIO(body))

class Tests(unittest.TestCase):
    def setUp(self):
        self.binding = VoiceBridgeBinding(base_url="https://example.invalid", bearer_token="test-token")
    def call(self, exc):
        with patch("plugins.krc_migration_candidate.mcp_canary.r3c.urlopen", side_effect=exc):
            with self.assertRaises(VoiceBridgeError) as caught:
                call_voicebridge(self.binding, "GET", "/api/v1/media/managed/preflight", None, {})
        return _sanitized_backend_error(caught.exception)
    def test_voicebridge_429(self):
        body = json.dumps({"error": {"code": "RATE_LIMITED", "message": "private"}, "request_id": "req_123"}).encode()
        result = self.call(failure(body, headers={"Retry-After": "60"}))
        self.assertEqual(result["error"]["upstream_code"], "RATE_LIMITED")
        self.assertEqual(result["error"]["retry_after_seconds"], 60)
        self.assertEqual(result["error"]["request_id"], "req_123")
        self.assertNotIn("private", repr(result))
    def test_proxy_429(self):
        result = self.call(failure(b"<html>proxy</html>"))
        self.assertEqual(result["error"]["http_status"], 429)
        self.assertNotIn("upstream_code", result["error"])
    def test_503(self):
        result = self.call(failure(b"{}", status=503))
        self.assertTrue(result["error"]["retryable"])
        self.assertEqual(result["error"]["http_status"], 503)

if __name__ == "__main__":
    unittest.main()
