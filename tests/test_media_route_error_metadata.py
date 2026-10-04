"""Uniform allowlisted diagnostic propagation for all five MCP surfaces."""
import io
import json
import sys
from pathlib import Path
from urllib.error import HTTPError
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from plugins.krc_migration_candidate.mcp_canary.r3c import VoiceBridgeBinding, VoiceBridgeError, dispatch_r3c
from plugins.krc_migration_candidate.mcp_canary.r3e1 import dispatch_r3e1
from plugins.krc_migration_candidate.mcp_canary.r3e2 import dispatch_r3e2
from plugins.krc_migration_candidate.mcp_canary.r3e3 import dispatch_r3e3
from plugins.krc_migration_candidate.mcp_canary.r3e4 import dispatch_r3e4
from plugins.krc_migration_candidate.mcp_canary.voicebridge_http_diagnostics import (
    safe_http_error_metadata, safe_error_diagnostics,
)

CASES = [
    (dispatch_r3c, "media_get_capabilities", {}),
    (dispatch_r3e1, "media_youtube_start", {"url": "https://www.youtube.com/watch?v=test",
      "gemini_free_consent": {"provider": "google_gemini", "tier": "free", "data_use_acknowledged": True}}),
    (dispatch_r3e2, "media_instagram_start", {"url": "https://www.instagram.com/reel/DF1CIrPSVmf/"}),
    (dispatch_r3e3, "media_facebook_start", {"url": "https://www.facebook.com/reel/636216875539019/"}),
    (dispatch_r3e4, "media_telegram_start", {"url": "https://t.me/techcrimes/12101"}),
]
@pytest.mark.parametrize("dispatch,name,args", CASES)
def test_all_surfaces_preserve_only_valid_diagnostic_metadata(monkeypatch, dispatch, name, args):
    safe = {"retry_after_seconds": 60, "upstream_code": "RATE_LIMITED",
            "request_id": "request_123", "correlation_id": "correlation_456"}
    diagnostics = {**safe, "token": "fixture-private-token", "body": "private body",
                   "message": "private exception", "peer_ip": "192.0.2.1"}
    def fail(*_args, **_kwargs):
        raise VoiceBridgeError("voicebridge_http_error", http_status=429,
                              retryable=True, diagnostics=diagnostics)
    binding = VoiceBridgeBinding("https://fixture.invalid", "fixture-private-token")
    message = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
               "params": {"name": name, "arguments": args}}
    if dispatch is dispatch_r3e1:
        monkeypatch.setattr("plugins.krc_migration_candidate.mcp_canary.r3e1.call_voicebridge", fail)
        response = dispatch(message, binding)
    else:
        response = dispatch(message, binding, backend_call=fail)
    detail = response["result"]["structuredContent"]["error"]
    assert detail == {"code": "voicebridge_http_error", "http_status": 429, "retryable": True, **safe}
    assert "fixture-private-token" not in json.dumps(response)

@pytest.mark.parametrize("code", ["MEDIA_PUBLIC_FREE_TIER_RATE_LIMIT", "MEDIA_PUBLIC_CONCURRENCY_LIMIT"])
def test_actual_media_admission_codes_are_not_lost(code):
    body = json.dumps({"error": {"code": code, "message": "private"}}).encode()
    error = HTTPError("https://fixture.invalid", 429, "fixture",
                      {"Retry-After": "1"}, io.BytesIO(body))
    assert safe_http_error_metadata(error) == {"upstream_code": code, "retry_after_seconds": 1}

def test_malformed_or_extra_metadata_fails_closed():
    assert safe_error_diagnostics({
        "retry_after_seconds": True, "upstream_code": "PRIVATE_TOKEN",
        "request_id": "not@an-id", "correlation_id": "x" * 81, "secret": "private",
    }) == {}
