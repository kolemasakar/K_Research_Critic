from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from plugins.krc_migration_candidate.mcp_canary.http_server import HttpConfig
from plugins.krc_migration_candidate.mcp_canary.oauth import OAuthState, READ_SCOPE
from plugins.krc_migration_candidate.mcp_canary.r3c import R3C_TOOL_NAMES, VoiceBridgeBinding, VoiceBridgeError
from plugins.krc_migration_candidate.mcp_canary.r3e1 import (
    R3E1_EXECUTION_TOOL_NAME,
    R3E1_SURFACE,
    R3E1_TOOL_NAMES,
    dispatch_r3e1,
    r3e1_health,
    tool_descriptors,
)
from plugins.krc_migration_candidate.mcp_canary.r3e1_http_server import handle_r3e1_http_request

MODERN_META = {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientCapabilities": {},
}


def _request(method: str, *, params: dict | None = None, request_id: int = 1) -> dict:
    message: dict = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params is not None:
        message["params"] = params
    return message


def _consent() -> dict[str, object]:
    return {
        "provider": "google_gemini",
        "tier": "free",
        "data_use_acknowledged": True,
    }


def test_r3e1_exposes_nine_read_tools_plus_only_youtube_start() -> None:
    assert R3E1_TOOL_NAMES == R3C_TOOL_NAMES + ("media_youtube_start",)
    assert len(R3E1_TOOL_NAMES) == 10
    descriptors = tool_descriptors()
    names = [tool["name"] for tool in descriptors]
    assert names == list(R3E1_TOOL_NAMES)
    assert "media_instagram_start" not in names
    assert "media_facebook_start" not in names
    assert "media_telegram_start" not in names

    start = descriptors[-1]
    assert start["name"] == R3E1_EXECUTION_TOOL_NAME
    assert start["annotations"] == {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    }
    schema = start["inputSchema"]
    assert schema["required"] == ["url", "gemini_free_consent"]


def test_r3e1_start_maps_exact_youtube_route_and_consent(monkeypatch) -> None:
    binding = VoiceBridgeBinding("https://voicebridge.invalid", "test-only-voicebridge-token")
    calls: list[tuple[str, str, dict | None, dict]] = []

    def fake_call(_binding, method, path, payload, query):
        calls.append((method, path, dict(payload) if payload is not None else None, dict(query)))
        return {"status": "PROCESSING", "provider": "gemini"}

    monkeypatch.setattr(
        "plugins.krc_migration_candidate.mcp_canary.r3e1.call_voicebridge",
        fake_call,
    )
    response = dispatch_r3e1(
        _request(
            "tools/call",
            params={
                "name": "media_youtube_start",
                "arguments": {
                    "url": "https://www.youtube.com/watch?v=test",
                    "language_hint": "auto",
                    "gemini_free_consent": _consent(),
                },
            },
        ),
        binding,
    )
    assert response is not None
    assert response["result"]["isError"] is False
    assert calls == [
        (
            "POST",
            "/api/v1/media/youtube-gemini/transcriptions",
            {
                "url": "https://www.youtube.com/watch?v=test",
                "language_hint": "auto",
                "gemini_free_consent": _consent(),
            },
            {},
        )
    ]


def test_r3e1_start_requires_exact_explicit_gemini_free_consent(monkeypatch) -> None:
    binding = VoiceBridgeBinding("https://voicebridge.invalid", "test-only-voicebridge-token")
    called = False

    def fake_call(*_args):
        nonlocal called
        called = True
        return {"unexpected": True}

    monkeypatch.setattr(
        "plugins.krc_migration_candidate.mcp_canary.r3e1.call_voicebridge",
        fake_call,
    )
    bad_consents = [
        {},
        {"provider": "google_gemini", "tier": "free", "data_use_acknowledged": False},
        {"provider": "google_gemini", "tier": "paid", "data_use_acknowledged": True},
        {"provider": "other", "tier": "free", "data_use_acknowledged": True},
    ]
    for consent in bad_consents:
        response = dispatch_r3e1(
            _request(
                "tools/call",
                params={
                    "name": "media_youtube_start",
                    "arguments": {
                        "url": "https://www.youtube.com/watch?v=test",
                        "gemini_free_consent": consent,
                    },
                },
            ),
            binding,
        )
        assert response is not None
        assert response["error"]["code"] == -32602
    assert called is False


def test_r3e1_rejects_other_execution_tools_before_backend(monkeypatch) -> None:
    binding = VoiceBridgeBinding("https://voicebridge.invalid", "test-only-voicebridge-token")
    called = False

    def fake_call(*_args):
        nonlocal called
        called = True
        return {"unexpected": True}

    monkeypatch.setattr(
        "plugins.krc_migration_candidate.mcp_canary.r3e1.call_voicebridge",
        fake_call,
    )
    for name in ("media_instagram_start", "media_facebook_start", "media_telegram_start"):
        response = dispatch_r3e1(
            _request("tools/call", params={"name": name, "arguments": {}}),
            binding,
        )
        assert response is not None
        assert response["error"]["code"] == -32602
    assert called is False


def test_r3e1_backend_error_is_sanitized_and_not_retried(monkeypatch) -> None:
    secret = "test-only-voicebridge-secret-value"
    binding = VoiceBridgeBinding("https://voicebridge.invalid", secret)
    count = 0

    def fake_call(*_args):
        nonlocal count
        count += 1
        raise VoiceBridgeError("voicebridge_http_error", http_status=429, retryable=True)

    monkeypatch.setattr(
        "plugins.krc_migration_candidate.mcp_canary.r3e1.call_voicebridge",
        fake_call,
    )
    response = dispatch_r3e1(
        _request(
            "tools/call",
            params={
                "name": "media_youtube_start",
                "arguments": {
                    "url": "https://www.youtube.com/watch?v=test",
                    "gemini_free_consent": _consent(),
                },
            },
        ),
        binding,
    )
    assert response is not None
    assert count == 1
    assert response["result"]["isError"] is True
    assert response["result"]["structuredContent"] == {
        "status": "error",
        "error": {"code": "voicebridge_http_error", "http_status": 429, "retryable": True},
    }
    assert secret not in json.dumps(response)


def test_r3e1_read_only_tool_delegates_to_r3c(monkeypatch) -> None:
    binding = VoiceBridgeBinding("https://voicebridge.invalid", "test-only-voicebridge-token")

    def fake_call(_binding, method, path, payload, query):
        assert method == "GET"
        assert path == "/api/v1/media/public-capabilities"
        assert payload is None
        assert query == {}
        return {"status": "ok"}

    monkeypatch.setattr(
        "plugins.krc_migration_candidate.mcp_canary.r3c.call_voicebridge",
        fake_call,
    )
    response = dispatch_r3e1(
        _request("tools/call", params={"name": "media_get_capabilities", "arguments": {}}),
        binding,
    )
    assert response is not None
    assert response["result"]["isError"] is False


def test_r3e1_health_reports_one_execution_tool_without_secret_material() -> None:
    health = r3e1_health(
        VoiceBridgeBinding("https://voicebridge.invalid", "test-only-voicebridge-secret-value")
    )
    assert health["status"] == "ok"
    assert health["tool_count"] == 10
    assert health["non_execution_tool_count"] == 9
    assert health["execution_tool_count"] == 1
    assert health["youtube_execution_enabled"] is True
    assert health["other_execution_tools"] == "not_enabled"
    assert health["provider_work_started"] is False
    assert "secret" not in json.dumps(health).lower()


def test_http_r3e1_requires_oauth_and_binding_then_lists_ten_tools() -> None:
    message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {"_meta": MODERN_META},
    }
    headers = {
        "Content-Type": "application/json",
        "MCP-Protocol-Version": "2026-07-28",
        "Mcp-Method": "tools/list",
    }

    no_auth = handle_r3e1_http_request(
        "POST",
        "/mcp",
        headers,
        json.dumps(message).encode("utf-8"),
        config=HttpConfig(
            surface=R3E1_SURFACE,
            voicebridge_base_url="https://voicebridge.invalid",
            voicebridge_bearer="test-only-voicebridge-token",
        ),
    )
    assert no_auth.status == 503
    assert json.loads(no_auth.body)["status"] == "r3e1_requires_oauth"

    missing_binding = handle_r3e1_http_request(
        "POST",
        "/mcp",
        headers,
        json.dumps(message).encode("utf-8"),
        config=HttpConfig(
            auth_mode="oauth",
            public_base_url="https://mcp.invalid",
            surface=R3E1_SURFACE,
        ),
    )
    assert missing_binding.status == 503
    assert json.loads(missing_binding.body)["status"] == "voicebridge_binding_unavailable"

    state = OAuthState()
    access_token, _refresh, _expires, _scope = state._issue_tokens(
        client_id="test-client",
        scope=READ_SCOPE,
    )
    authorized_headers = dict(headers)
    authorized_headers["Authorization"] = "Bearer " + access_token
    listed = handle_r3e1_http_request(
        "POST",
        "/mcp",
        authorized_headers,
        json.dumps(message).encode("utf-8"),
        config=HttpConfig(
            auth_mode="oauth",
            public_base_url="https://mcp.invalid",
            surface=R3E1_SURFACE,
            voicebridge_base_url="https://voicebridge.invalid",
            voicebridge_bearer="test-only-voicebridge-token",
        ),
        oauth_state=state,
    )
    assert listed.status == 200
    names = [tool["name"] for tool in json.loads(listed.body)["result"]["tools"]]
    assert names == list(R3E1_TOOL_NAMES)
