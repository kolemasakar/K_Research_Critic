from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from plugins.krc_migration_candidate.mcp_canary.http_server import HttpConfig
import plugins.krc_migration_candidate.mcp_canary.r3e4_http_server as r3e4_http
from plugins.krc_migration_candidate.mcp_canary.r3c import VoiceBridgeBinding, VoiceBridgeError
from plugins.krc_migration_candidate.mcp_canary.r3e4 import (
    R3E4_EXECUTION_TOOL_NAME,
    R3E4_READ_TOOL_NAMES,
    R3E4_SURFACE,
    R3E4_TOOL_NAMES,
    dispatch_r3e4,
    r3e4_health,
    tool_descriptors,
)
from plugins.krc_migration_candidate.mcp_canary.r3e4_http_server import (
    run_r3e4_preflight_lookup_probe,
    run_r3e4_record_replay_probe,
)

TELEGRAM_URL = "https://t.me/techcrimes/12101"
FACEBOOK_URL = "https://www.facebook.com/reel/636216875539019/"


def _binding() -> VoiceBridgeBinding:
    return VoiceBridgeBinding(
        base_url="https://voicebridge.invalid",
        bearer_token="test-only-r3e4-server-token",
    )


def _config() -> HttpConfig:
    return HttpConfig(
        auth_mode="oauth",
        public_base_url="https://mcp.invalid",
        surface=R3E4_SURFACE,
        voicebridge_base_url="https://voicebridge.invalid",
        voicebridge_bearer="test-only-r3e4-server-token",
    )


def test_r3e4_surface_has_two_reads_and_one_telegram_start() -> None:
    assert R3E4_TOOL_NAMES == (
        "media_non_youtube_status",
        "media_non_youtube_segments",
        "media_telegram_start",
    )
    descriptors = tool_descriptors()
    assert [item["name"] for item in descriptors] == list(R3E4_TOOL_NAMES)
    assert len(R3E4_READ_TOOL_NAMES) == 2
    assert len(descriptors) == 3
    start = descriptors[-1]
    assert start["name"] == R3E4_EXECUTION_TOOL_NAME
    assert start["annotations"]["readOnlyHint"] is False
    assert start["annotations"]["openWorldHint"] is True
    assert "free-only Telegram route" in start["description"]
    assert "Automatic paid fallback is forbidden" in start["description"]


def test_r3e4_health_declares_exact_execution_boundary() -> None:
    health = r3e4_health(_binding())
    assert health["status"] == "ok"
    assert health["surface"] == R3E4_SURFACE
    assert health["tool_count"] == 3
    assert health["non_execution_tool_count"] == 2
    assert health["execution_tool_count"] == 1
    assert health["telegram_execution_enabled"] is True
    assert health["provider_work_started"] is False

def test_r3e4_start_routes_only_telegram_to_public_endpoint() -> None:
    observed: dict[str, object] = {}

    def backend(binding, method, path, payload, query):
        observed.update({
            "binding": binding,
            "method": method,
            "path": path,
            "payload": payload,
            "query": query,
        })
        return {
            "job_id": "KRCM_r3e4-fixture",
            "status": "COMPLETED",
            "provider": "assemblyai",
            "provider_mode": "telegram_public_stt",
            "retrieval_provider": "telegram_public_web",
            "retrieval_credits_charged": 0,
        }

    response = dispatch_r3e4(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "media_telegram_start",
                "arguments": {"url": TELEGRAM_URL, "language_hint": "auto"},
            },
        },
        _binding(),
        backend_call=backend,
    )
    assert response is not None
    assert observed["method"] == "POST"
    assert observed["path"] == "/api/v1/media/managed/telegram"
    assert observed["payload"] == {
        "url": TELEGRAM_URL,
        "language_hint": "auto",
    }
    assert response["result"]["structuredContent"]["job_id"] == "KRCM_r3e4-fixture"


def test_r3e4_rejects_cross_platform_and_other_execution_tools() -> None:
    calls = 0

    def backend(*_args, **_kwargs):
        nonlocal calls
        calls += 1
        return {}

    response = dispatch_r3e4(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "media_telegram_start",
                "arguments": {"url": FACEBOOK_URL},
            },
        },
        _binding(),
        backend_call=backend,
    )
    assert response is not None
    assert response["error"]["code"] == -32602
    assert calls == 0


def test_r3e4_confirmation_probe_is_zero_side_effect(monkeypatch) -> None:
    monkeypatch.setenv("KRC_R3E4_CONFIRMATION_PROBE_ONLY", "true")
    r3e4_http._CONFIRMATION_PROBE_INVOCATIONS = 0
    result = r3e4_http._confirmation_probe_backend(
        _binding(),
        "POST",
        "/api/v1/media/managed/telegram",
        {"url": TELEGRAM_URL},
        {},
    )
    assert result["phase"] == "R3-E4"
    assert result["external_mutation"] is False
    assert result["provider_work"] is False
    assert result["real_media_start"] is False
    assert result["invocation_count"] == 1

    health = r3e4_http.handle_r3e4_http_request(
        "GET",
        "/healthz",
        {},
        config=_config(),
    )
    payload = json.loads(health.body)
    assert payload["confirmation_probe_only"] is True
    assert payload["confirmation_probe_invocation_count"] == 1
    assert payload["provider_work_started"] is False

def test_r3e4_cold_start_warms_before_exactly_one_start(monkeypatch) -> None:
    events: list[str] = []

    def fake_warm(binding):
        assert binding.configured
        events.append("warm")

    def fake_call(binding, method, path, payload, query):
        assert binding.configured
        events.append("start")
        assert method == "POST"
        assert path == "/api/v1/media/managed/telegram"
        assert payload == {"url": TELEGRAM_URL}
        assert query == {}
        return {"job_id": "KRCM_warmed", "status": "PROCESSING"}

    monkeypatch.setattr(r3e4_http, "_warm_voicebridge", fake_warm)
    monkeypatch.setattr(r3e4_http, "call_voicebridge", fake_call)
    result = r3e4_http._cold_start_resilient_backend(
        _binding(),
        "POST",
        "/api/v1/media/managed/telegram",
        {"url": TELEGRAM_URL},
        {},
    )
    assert result["job_id"] == "KRCM_warmed"
    assert events == ["warm", "start"]


def test_r3e4_preflight_probe_reads_scoped_capabilities_and_lookup_only(monkeypatch) -> None:
    backend_calls: list[tuple[str, str]] = []

    def fake_call(_binding_value, method, path, payload, query):
        backend_calls.append((method, path))
        if method == "GET" and path == "/api/v1/media/managed":
            assert payload is None
            return {
                "telegram_public_retrieval": True,
                "telegram_retrieval_provider": "telegram_public_web",
                "telegram_retrieval_credits": 0,
                "telegram_stt_provider": "assemblyai",
                "telegram_stt_configured": True,
            }
        assert method == "POST"
        assert path == "/api/v1/media/managed/lookup"
        assert payload == {"url": TELEGRAM_URL, "language_hint": "auto"}
        raise VoiceBridgeError("voicebridge_http_error", http_status=404, retryable=False)

    monkeypatch.setattr(r3e4_http, "call_voicebridge", fake_call)
    result = run_r3e4_preflight_lookup_probe(_config(), TELEGRAM_URL)
    assert result["status"] == "pass"
    assert result["preflight"] == "pass"
    assert result["lookup"] == "pass_empty"
    assert result["provider"] == "telegram_public_web"
    assert result["platform"] == "telegram"
    assert result["stt_provider"] == "assemblyai"
    assert result["estimated_retrieval_credits"] == 0
    assert result["automatic_paid_fallback"] is False
    assert result["provider_work_started"] is False
    assert result["start_called"] is False
    assert backend_calls == [
        ("GET", "/api/v1/media/managed"),
        ("POST", "/api/v1/media/managed/lookup"),
    ]


def test_r3e4_record_replay_probe_never_calls_start(monkeypatch) -> None:
    calls: list[str] = []
    job_id = "KRCM_r3e4-replay"

    def fake_dispatch(message, _binding_value):
        name = message["params"]["name"]
        calls.append(name)
        if name == "media_non_youtube_status":
            return {
                "jsonrpc": "2.0",
                "id": "status",
                "result": {
                    "isError": False,
                    "structuredContent": {
                        "job_id": job_id,
                        "status": "COMPLETED",
                        "segment_count": 1,
                    },
                },
            }
        if name == "media_non_youtube_segments":
            return {
                "jsonrpc": "2.0",
                "id": "segments",
                "result": {
                    "isError": False,
                    "structuredContent": {
                        "job_id": job_id,
                        "segments": [{"index": 0, "text": "fixture"}],
                        "next_cursor": None,
                    },
                },
            }
        raise AssertionError(name)

    monkeypatch.setattr(r3e4_http, "dispatch_r3e4", fake_dispatch)
    result = run_r3e4_record_replay_probe(_config(), job_id)
    assert result["status"] == "pass"
    assert result["provider_work_started"] is False
    assert result["start_called"] is False
    assert calls == ["media_non_youtube_status", "media_non_youtube_segments"]
