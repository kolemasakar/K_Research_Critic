from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from plugins.krc_migration_candidate.mcp_canary.http_server import HttpConfig
import plugins.krc_migration_candidate.mcp_canary.r3e2_http_server as r3e2_http
from plugins.krc_migration_candidate.mcp_canary.r3c import VoiceBridgeBinding, VoiceBridgeError
from plugins.krc_migration_candidate.mcp_canary.r3e2 import (
    R3E2_EXECUTION_TOOL_NAME,
    R3E2_READ_TOOL_NAMES,
    R3E2_SURFACE,
    R3E2_TOOL_NAMES,
    dispatch_r3e2,
    r3e2_health,
    tool_descriptors,
)
from plugins.krc_migration_candidate.mcp_canary.r3e2_http_server import (
    run_r3e2_preflight_lookup_probe,
)

INSTAGRAM_URL = "https://www.instagram.com/reel/DF1CIrPSVmf/"
YOUTUBE_URL = "https://www.youtube.com/watch?v=jNQXAC9IVRw"


def _binding() -> VoiceBridgeBinding:
    return VoiceBridgeBinding(
        base_url="https://voicebridge.invalid",
        bearer_token="test-only-r3e2-server-token",
    )


def test_r3e2_surface_exposes_only_instagram_relevant_reads_plus_one_start() -> None:
    assert R3E2_TOOL_NAMES == (
        "media_instagram_preflight",
        "media_instagram_lookup",
        "media_non_youtube_status",
        "media_non_youtube_segments",
        "media_instagram_start",
    )
    descriptors = tool_descriptors()
    assert [item["name"] for item in descriptors] == list(R3E2_TOOL_NAMES)
    assert len(descriptors) == 5
    assert len(R3E2_READ_TOOL_NAMES) == 4

    start = descriptors[-1]
    assert start["name"] == R3E2_EXECUTION_TOOL_NAME
    annotations = start["annotations"]
    assert annotations["readOnlyHint"] is False
    assert annotations["destructiveHint"] is False
    assert annotations["idempotentHint"] is False
    assert annotations["openWorldHint"] is True
    description = start["description"]
    assert "free-only Instagram route" in description
    assert "Automatic paid fallback is forbidden" in description
    assert "confirmation" in description


def test_r3e2_health_declares_exact_execution_boundary() -> None:
    health = r3e2_health(_binding())
    assert health["status"] == "ok"
    assert health["surface"] == R3E2_SURFACE
    assert health["tool_count"] == 5
    assert health["non_execution_tool_count"] == 4
    assert health["execution_tool_count"] == 1
    assert health["instagram_execution_enabled"] is True
    assert health["other_execution_tools"] == "not_enabled"
    assert health["provider_work_started"] is False


def test_r3e2_start_routes_only_supported_instagram_url() -> None:
    observed: dict[str, object] = {}

    def backend(binding, method, path, payload, query):
        observed.update(
            {
                "binding": binding,
                "method": method,
                "path": path,
                "payload": payload,
                "query": query,
            }
        )
        return {
            "job_id": "KRCM_r3e2-fixture",
            "status": "COMPLETED",
            "provider": "assemblyai",
            "provider_mode": "cobalt_retrieval_stt",
            "retrieval_provider": "cobalt",
            "retrieval_credits_charged": 0,
        }

    response = dispatch_r3e2(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "media_instagram_start",
                "arguments": {
                    "url": INSTAGRAM_URL,
                    "language_hint": "auto",
                },
            },
        },
        _binding(),
        backend_call=backend,
    )
    assert response is not None
    assert observed["method"] == "POST"
    assert observed["path"] == "/api/v1/media/managed/transcriptions"
    assert observed["payload"] == {
        "url": INSTAGRAM_URL,
        "language_hint": "auto",
    }
    result = response["result"]["structuredContent"]
    assert result["job_id"] == "KRCM_r3e2-fixture"
    assert result["retrieval_credits_charged"] == 0


def test_r3e2_rejects_non_instagram_start_before_backend() -> None:
    calls = 0

    def backend(*_args, **_kwargs):
        nonlocal calls
        calls += 1
        return {}

    response = dispatch_r3e2(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "media_instagram_start",
                "arguments": {"url": YOUTUBE_URL, "language_hint": "auto"},
            },
        },
        _binding(),
        backend_call=backend,
    )
    assert response is not None
    assert response["error"]["code"] == -32602
    assert calls == 0


def test_r3e2_does_not_expose_other_start_tools() -> None:
    for name in (
        "media_youtube_start",
        "media_facebook_start",
        "media_telegram_start",
    ):
        response = dispatch_r3e2(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": name, "arguments": {}},
            },
            _binding(),
        )
        assert response is not None
        assert response["error"]["code"] == -32602


def test_r3e2_preflight_lookup_probe_never_calls_start(monkeypatch) -> None:
    calls: list[str] = []

    def fake_dispatch(message, _binding):
        name = message["params"]["name"]
        calls.append(name)
        if name == "media_instagram_preflight":
            return {
                "jsonrpc": "2.0",
                "id": "r3e2-preflight",
                "result": {
                    "isError": False,
                    "structuredContent": {
                        "provider": "cobalt",
                        "platform": "instagram",
                        "estimated_retrieval_credits": 0,
                        "automatic_paid_fallback": False,
                        "stt_provider": "assemblyai",
                    },
                },
            }
        if name == "media_instagram_lookup":
            return {
                "jsonrpc": "2.0",
                "id": "r3e2-lookup",
                "result": {
                    "isError": True,
                    "structuredContent": {
                        "status": "error",
                        "error": {
                            "code": "voicebridge_http_error",
                            "http_status": 404,
                            "retryable": False,
                        },
                    },
                },
            }
        raise AssertionError(name)

    monkeypatch.setattr(
        "plugins.krc_migration_candidate.mcp_canary.r3e2_http_server.dispatch_r3e2",
        fake_dispatch,
    )
    config = HttpConfig(
        auth_mode="oauth",
        public_base_url="https://mcp.invalid",
        surface=R3E2_SURFACE,
        voicebridge_base_url="https://voicebridge.invalid",
        voicebridge_bearer="test-only-r3e2-server-token",
    )
    result = run_r3e2_preflight_lookup_probe(config, INSTAGRAM_URL)

    assert result["status"] == "pass"
    assert result["preflight"] == "pass"
    assert result["lookup"] == "pass_empty"
    assert result["provider_work_started"] is False
    assert result["start_called"] is False
    assert calls == ["media_instagram_preflight", "media_instagram_lookup"]
    assert "media_instagram_start" not in json.dumps(calls)


def test_r3e2_backend_error_is_sanitized() -> None:
    def backend(*_args, **_kwargs):
        raise VoiceBridgeError(
            "voicebridge_http_error",
            http_status=403,
            retryable=False,
        )

    response = dispatch_r3e2(
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "media_instagram_start",
                "arguments": {"url": INSTAGRAM_URL},
            },
        },
        _binding(),
        backend_call=backend,
    )
    assert response is not None
    result = response["result"]
    assert result["isError"] is True
    assert result["structuredContent"] == {
        "status": "error",
        "error": {
            "code": "voicebridge_http_error",
            "retryable": False,
            "http_status": 403,
        },
    }


def test_r3e2_confirmation_probe_mode_is_zero_side_effect(monkeypatch) -> None:
    monkeypatch.setenv("KRC_R3E2_CONFIRMATION_PROBE_ONLY", "true")
    r3e2_http._CONFIRMATION_PROBE_INVOCATIONS = 0

    result = r3e2_http._confirmation_probe_backend(
        _binding(),
        "POST",
        "/api/v1/media/managed/transcriptions",
        {"url": INSTAGRAM_URL, "language_hint": "auto"},
        {},
    )
    assert result == {
        "status": "ok",
        "phase": "R3-E2",
        "confirmation_probe_executed": True,
        "external_mutation": False,
        "provider_work": False,
        "provider_charge": False,
        "real_media_start": False,
        "invocation_count": 1,
    }

    health = r3e2_http.handle_r3e2_http_request(
        "GET",
        "/healthz",
        {},
        config=HttpConfig(
            auth_mode="oauth",
            public_base_url="https://mcp.invalid",
            surface=R3E2_SURFACE,
            voicebridge_base_url="https://voicebridge.invalid",
            voicebridge_bearer="test-only-r3e2-server-token",
        ),
    )
    assert health.status == 200
    payload = json.loads(health.body)
    assert payload["confirmation_probe_only"] is True
    assert payload["confirmation_probe_invocation_count"] == 1
    assert payload["provider_work_started"] is False
