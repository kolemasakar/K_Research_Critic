from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from plugins.krc_migration_candidate.mcp_canary.http_server import HttpConfig, handle_http_request
from plugins.krc_migration_candidate.mcp_canary.oauth import OAuthState, READ_SCOPE
from plugins.krc_migration_candidate.mcp_canary.r3c import (
    R3C_SURFACE,
    R3C_TOOL_NAMES,
    VoiceBridgeBinding,
    VoiceBridgeError,
    dispatch_r3c,
    r3c_health,
    tool_descriptors,
)

CONTRACT = ROOT / "plugins" / "krc_migration_candidate" / "contracts" / "media_tools.yaml"
MODERN_META = {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientCapabilities": {},
}


def _request(method: str, *, params: dict | None = None, request_id: int = 1) -> dict:
    message: dict = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params is not None:
        message["params"] = params
    return message


def test_r3c_surface_matches_exact_nine_frozen_non_execution_tools() -> None:
    contract = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    expected = tuple(
        tool["candidate_name"]
        for tool in contract["tools"]
        if tool["classification"] == "non_execution"
    )
    execution = {
        tool["candidate_name"]
        for tool in contract["tools"]
        if tool["classification"] == "execution"
    }
    assert expected == R3C_TOOL_NAMES
    assert len(R3C_TOOL_NAMES) == 9
    assert set(R3C_TOOL_NAMES).isdisjoint(execution)

    descriptors = tool_descriptors()
    assert [tool["name"] for tool in descriptors] == list(R3C_TOOL_NAMES)
    for tool in descriptors:
        assert tool["annotations"] == {
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }


def test_r3c_discovery_exposes_nine_tools_and_no_canary_or_start_tools() -> None:
    binding = VoiceBridgeBinding("https://voicebridge.invalid", "test-only-voicebridge-token")
    listed = dispatch_r3c(_request("tools/list"), binding)
    assert listed is not None
    names = [tool["name"] for tool in listed["result"]["tools"]]
    assert names == list(R3C_TOOL_NAMES)
    assert "krc_media_capabilities_canary" not in names
    assert not any(name.endswith("_start") for name in names)

    discover = dispatch_r3c(_request("server/discover", params={"_meta": MODERN_META}), binding)
    assert discover is not None
    assert "exactly nine non-execution" in discover["result"]["instructions"]


def test_r3c_dispatch_maps_only_frozen_read_routes_without_retry() -> None:
    binding = VoiceBridgeBinding("https://voicebridge.invalid", "test-only-voicebridge-token")
    calls: list[tuple[str, str, dict | None, dict]] = []

    def backend_call(_binding, method, path, payload, query):
        calls.append((method, path, dict(payload) if payload is not None else None, dict(query)))
        return {"status": "ok", "path": path}

    cases = [
        ("media_get_capabilities", {}, "GET", "/api/v1/media/public-capabilities", None, {}),
        (
            "media_youtube_preflight",
            {"url": "https://youtube.example/watch?v=1", "language_hint": "en"},
            "POST",
            "/api/v1/media/youtube-gemini/preflight",
            {"url": "https://youtube.example/watch?v=1", "language_hint": "en"},
            {},
        ),
        (
            "media_youtube_lookup",
            {"url": "https://youtube.example/watch?v=1"},
            "POST",
            "/api/v1/media/youtube-gemini/lookup",
            {"url": "https://youtube.example/watch?v=1"},
            {},
        ),
        (
            "media_youtube_status",
            {"job_id": "KRCM_test-1"},
            "GET",
            "/api/v1/media/youtube-gemini/transcriptions/KRCM_test-1",
            None,
            {},
        ),
        (
            "media_youtube_segments",
            {"job_id": "KRCM_test-1", "cursor": 2, "limit": 10},
            "GET",
            "/api/v1/media/youtube-gemini/transcriptions/KRCM_test-1/segments",
            None,
            {"cursor": 2, "limit": 10},
        ),
        (
            "media_instagram_preflight",
            {"url": "https://instagram.example/reel/1"},
            "POST",
            "/api/v1/media/managed/preflight",
            {"url": "https://instagram.example/reel/1"},
            {},
        ),
        (
            "media_instagram_lookup",
            {"url": "https://instagram.example/reel/1", "language_hint": "uk"},
            "POST",
            "/api/v1/media/managed/lookup",
            {"url": "https://instagram.example/reel/1", "language_hint": "uk"},
            {},
        ),
        (
            "media_non_youtube_status",
            {"job_id": "KRCM_test-2"},
            "GET",
            "/api/v1/media/managed/transcriptions/KRCM_test-2",
            None,
            {},
        ),
        (
            "media_non_youtube_segments",
            {"job_id": "KRCM_test-2"},
            "GET",
            "/api/v1/media/managed/transcriptions/KRCM_test-2/segments",
            None,
            {"cursor": 0, "limit": 20},
        ),
    ]

    for index, (name, arguments, method, path, payload, query) in enumerate(cases, start=1):
        response = dispatch_r3c(
            _request("tools/call", params={"name": name, "arguments": arguments}, request_id=index),
            binding,
            backend_call=backend_call,
        )
        assert response is not None
        assert response["result"]["isError"] is False
        assert calls[-1] == (method, path, payload, query)

    assert len(calls) == 9


def test_r3c_invalid_input_and_execution_names_fail_before_backend() -> None:
    binding = VoiceBridgeBinding("https://voicebridge.invalid", "test-only-voicebridge-token")
    backend_called = False

    def backend_call(*_args):
        nonlocal backend_called
        backend_called = True
        return {"unexpected": True}

    invalid = dispatch_r3c(
        _request(
            "tools/call",
            params={
                "name": "media_youtube_preflight",
                "arguments": {"url": "http://not-https.invalid"},
            },
        ),
        binding,
        backend_call=backend_call,
    )
    assert invalid is not None
    assert invalid["error"]["code"] == -32602

    execution = dispatch_r3c(
        _request("tools/call", params={"name": "media_youtube_start", "arguments": {}}),
        binding,
        backend_call=backend_call,
    )
    assert execution is not None
    assert execution["error"]["code"] == -32602
    assert backend_called is False


def test_r3c_backend_errors_are_sanitized_and_never_reflect_secret() -> None:
    secret = "test-only-voicebridge-secret-value"
    binding = VoiceBridgeBinding("https://voicebridge.invalid", secret)

    def backend_call(*_args):
        raise VoiceBridgeError("voicebridge_http_error", http_status=503, retryable=True)

    response = dispatch_r3c(
        _request("tools/call", params={"name": "media_get_capabilities", "arguments": {}}),
        binding,
        backend_call=backend_call,
    )
    assert response is not None
    assert response["result"]["isError"] is True
    structured = response["result"]["structuredContent"]
    assert structured == {
        "status": "error",
        "error": {"code": "voicebridge_http_error", "http_status": 503, "retryable": True},
    }
    assert secret not in json.dumps(response)


def test_r3c_health_reports_binding_state_without_secret_material() -> None:
    missing = r3c_health(VoiceBridgeBinding(None, None))
    configured = r3c_health(
        VoiceBridgeBinding("https://voicebridge.invalid", "test-only-voicebridge-secret-value")
    )
    assert missing["status"] == "binding_required"
    assert missing["voicebridge_binding_configured"] is False
    assert configured["status"] == "ok"
    assert configured["voicebridge_binding_configured"] is True
    assert configured["tool_count"] == 9
    assert configured["execution_tools"] == "not_enabled"
    assert "secret" not in json.dumps(configured).lower()


def test_http_r3c_requires_oauth_and_binding_then_lists_nine_tools() -> None:
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

    no_auth = handle_http_request(
        "POST",
        "/mcp",
        headers,
        json.dumps(message).encode("utf-8"),
        config=HttpConfig(
            surface=R3C_SURFACE,
            voicebridge_base_url="https://voicebridge.invalid",
            voicebridge_bearer="test-only-voicebridge-token",
        ),
    )
    assert no_auth.status == 503
    assert json.loads(no_auth.body)["status"] == "r3c_requires_oauth"

    missing_binding = handle_http_request(
        "POST",
        "/mcp",
        headers,
        json.dumps(message).encode("utf-8"),
        config=HttpConfig(
            auth_mode="oauth",
            public_base_url="https://mcp.invalid",
            surface=R3C_SURFACE,
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
    listed = handle_http_request(
        "POST",
        "/mcp",
        authorized_headers,
        json.dumps(message).encode("utf-8"),
        config=HttpConfig(
            auth_mode="oauth",
            public_base_url="https://mcp.invalid",
            surface=R3C_SURFACE,
            voicebridge_base_url="https://voicebridge.invalid",
            voicebridge_bearer="test-only-voicebridge-token",
        ),
        oauth_state=state,
    )
    assert listed.status == 200
    names = [tool["name"] for tool in json.loads(listed.body)["result"]["tools"]]
    assert names == list(R3C_TOOL_NAMES)
