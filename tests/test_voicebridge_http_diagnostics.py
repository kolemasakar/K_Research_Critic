import io
import json
import unittest
from urllib.error import HTTPError
from plugins.krc_migration_candidate.mcp_canary.voicebridge_http_diagnostics import safe_http_error_metadata

def error(body, headers=None, code=429):
    if isinstance(body, dict):
        body = json.dumps(body).encode()
    elif isinstance(body, str):
        body = body.encode()
    return HTTPError("https://example.invalid", code, "test", headers or {}, io.BytesIO(body))

class Tests(unittest.TestCase):
    def test_structured_rate_limit(self):
        e = error({"error": {"code": "RATE_LIMITED", "message": "secret"}, "request_id": "req_123", "correlation_id": "corr-7"}, {"Retry-After": "60"})
        self.assertEqual(safe_http_error_metadata(e), {"retry_after_seconds": 60, "upstream_code": "RATE_LIMITED", "request_id": "req_123", "correlation_id": "corr-7"})
    def test_nested_voicebridge_ids(self):
        e = error({"error": {"code": "RATE_LIMITED", "request_id": "req_nested", "correlation_id": "corr_nested", "message": "private"}}, {"Retry-After": "60"})
        self.assertEqual(safe_http_error_metadata(e), {"retry_after_seconds": 60, "upstream_code": "RATE_LIMITED", "request_id": "req_nested", "correlation_id": "corr_nested"})
    def test_proxy_html(self):
        self.assertEqual(safe_http_error_metadata(error("<html>proxy token secret</html>")), {})
    def test_oversize(self):
        self.assertEqual(safe_http_error_metadata(error("x"*4096, {"Retry-After": "30"})), {"retry_after_seconds": 30})
    def test_invalid_header_and_ids(self):
        self.assertEqual(safe_http_error_metadata(error({"error": {"code": "TOKEN_SECRET"}, "request_id": "secret@example.com"}, {"Retry-After": "99999"})), {})
    def test_503(self):
        self.assertEqual(safe_http_error_metadata(error({"error": {"code": "SERVICE_UNAVAILABLE"}}, code=503)), {"upstream_code": "SERVICE_UNAVAILABLE"})
    def test_no_leak(self):
        self.assertNotIn("token", repr(safe_http_error_metadata(error({"error": {"code": "RATE_LIMITED", "token": "secret"}}))))

if __name__ == "__main__":
    unittest.main()
