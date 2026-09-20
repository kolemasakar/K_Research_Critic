from __future__ import annotations

import json
from dataclasses import replace
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from plugins.krc_migration_candidate.mcp_canary.http_server import HttpConfig
import plugins.krc_migration_candidate.mcp_canary.r3e3_http_server as r3e3_http
from plugins.krc_migration_candidate.mcp_canary.r3c import VoiceBridgeBinding, VoiceBridgeError
from plugins.krc_migration_candidate.mcp_canary.r3e3 import (
    R3E3_EXECUTION_TOOL_NAME,
    R3E3_READ_TOOL_NAMES,
    R3E3_SURFACE,
    R3E3_TOOL_NAMES,
    dispatch_r3e3,
    r3e3_health,
    tool_descriptors,
)
from plugins.krc_migration_candidate.mcp_canary.r3e3_http_server import (
    run_r3e3_preflight_lookup_probe,
    run_r3e3_record_replay_probe,
)

FACEBOOK_URL = "https://www.facebook.com/reel/636216875539019/"
INSTAGRAM_URL = "https://www.instagram.com/reel/DF1CIrPSVmf/"


def _binding() -> VoiceBridgeBinding:
    return VoiceBridgeBinding(
        base_url="https://voicebridge.invalid",
        bearer_token="test-only-r3e3-server-token",
    )


def _config() -> HttpConfig:
    return HttpConfig(
        auth_mode="oauth",
        public_base_url="https://mcp.invalid",
        surface=R3E3_SURFACE,
        voicebridge_base_url="https://voicebridge.invalid",
        voicebridge_bearer="test-only-r3e3-server-token",
    )


def test_r3e3_surface_has_two_reads_and_one_facebook_start() -> None:
    assert R3E3_TOOL_NAMES == (
        "media_non_youtube_status",
        "media_non_youtube_segments",
        "media_facebook_start",
    )
    descriptors = tool_descriptors()
    assert [item["name"] for item in descriptors] == list(R3E3_TOOL_NAMES)
    assert len(R3E3_READ_TOOL_NAMES) == 2
    assert len(descriptors) == 3
    start = descriptors[-1]
    assert start["name"] == R3E3_EXECUTION_TOOL_NAME
    assert start["annotations"]["readOnlyHint"] is False
    assert start["annotations"]["openWorldHint"] is True
    assert "free-only Facebook route" in start["description"]
    assert "Automatic paid fallback is forbidden" in start["description"]


def test_r3e3_health_declares_exact_execution_boundary() -> None:
    health = r3e3_health(_binding())
    assert health["status"] == "ok"
    assert health["surface"] == R3E3_SURFACE
    assert health["tool_count"] == 3
    assert health["non_execution_tool_count"] == 2
    assert health["execution_tool_count"] == 1
    assert health["facebook_execution_enabled"] is True
    assert health["provider_work_started"] is False


def test_r3e3_route_bearer_derivation_is_stable(monkeypatch) -> None:
    monkeypatch.delenv("KRC_R3E3_VOICEBRIDGE_BEARER_OVERRIDE", raising=False)
    config = replace(
        _config(),
        voicebridge_bearer="general-media-action-token-123456789",
    )
    binding = r3e3_http._binding(config)
    assert binding.bearer_token == (
        "r3e3-b9e9c294b678947317d24274938f4417715d95c2c082413abe48d81633604f9d"
    )


def test_r3e3_route_bearer_override_precedes_derivation(monkeypatch) -> None:
    monkeypatch.setenv(
        "KRC_R3E3_VOICEBRIDGE_BEARER_OVERRIDE",
        "override-route-scoped-r3e3-token-123456789",
    )
    binding = r3e3_http._binding(_config())
    assert binding.bearer_token == "override-route-scoped-r3e3-token-123456789"


def test_r3e3_start_routes_only_facebook_to_free_endpoint() -> None:
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
            "job_id": "KRCM_r3e3-fixture",
            "status": "COMPLETED",
            "provider": "assemblyai",
            "provider_mode": "cobalt_retrieval_stt",
            "retrieval_provider": "cobalt",
            "retrieval_credits_charged": 0,
        }

    response = dispatch_r3e3(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "media_facebook_start",
                "arguments": {"url": FACEBOOK_URL, "language_hint": "auto"},
            },
        },
        _binding(),
        backend_call=backend,
    )
    assert response is not None
    assert observed["method"] == "POST"
    assert observed["path"] == "/api/v1/media/managed/facebook-fallback"
    assert observed["payload"] == {
        "url": FACEBOOK_URL,
        "language_hint": "auto",
    }
    assert response["result"]["structuredContent"]["job_id"] == "KRCM_r3e3-fixture"


def test_r3e3_rejects_cross_platform_and_other_execution_tools() -> None:
    calls = 0

    def backend(*_args, **_kwargs):
        nonlocal calls
        calls += 1
        return {}

    response = dispatch_r3e3(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "media_facebook_start",
                "arguments": {"url": INSTAGRAM_URL},
            },
        },
        _binding(),
        backend_call=backend,
    )
    assert response is not None
    assert response["error"]["code"] == -32602
    assert calls == 0

    for name in ("media_youtube_start", "media_instagram_start", "media_telegram_start"):
        blocked = dispatch_r3e3(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": name, "arguments": {}},
            },
            _binding(),
        )
        assert blocked is not None
        assert blocked["error"]["code"] == -32602


def test_r3e3_confirmation_probe_is_zero_side_effect(monkeypatch) -> None:
    monkeypatch.setenv("KRC_R3E3_CONFIRMATION_PROBE_ONLY", "true")
    r3e3_http._CONFIRMATION_PROBE_INVOCATIONS = 0
    result = r3e3_http._confirmation_probe_backend(
        _binding(),
        "POST",
        "/api/v1/media/managed/facebook-fallback",
        {"url": FACEBOOK_URL},
        {},
    )
    assert result["phase"] == "R3-E3"
    assert result["external_mutation"] is False
    assert result["provider_work"] is False
    assert result["provider_charge"] is False
    assert result["real_media_start"] is False
    assert result["invocation_count"] == 1

    health = r3e3_http.handle_r3e3_http_request(
        "GET",
        "/healthz",
        {},
        config=_config(),
    )
    payload = json.loads(health.body)
    assert payload["confirmation_probe_only"] is True
    assert payload["confirmation_probe_invocation_count"] == 1
    assert payload["provider_work_started"] is False


def test_r3e3_cold_start_warms_before_exactly_one_start(monkeypatch) -> None:
    events: list[str] = []

    def fake_warm(binding):
        assert binding.configured
        events.append("warm")

    def fake_call(binding, method, path, payload, query):
        assert binding.configured
        events.append("start")
        assert method == "POST"
        assert path == "/api/v1/media/managed/facebook-fallback"
        assert payload == {"url": FACEBOOK_URL}
        assert query == {}
        return {"job_id": "KRCM_warmed", "status": "PROCESSING"}

    monkeypatch.setattr(r3e3_http, "_warm_voicebridge", fake_warm)
    monkeypatch.setattr(r3e3_http, "call_voicebridge", fake_call)
    result = r3e3_http._cold_start_resilient_backend(
        _binding(),
        "POST",
        "/api/v1/media/managed/facebook-fallback",
        {"url": FACEBOOK_URL},
        {},
    )
    assert result["job_id"] == "KRCM_warmed"
    assert events == ["warm", "start"]


def test_r3e3_preflight_probe_reads_scoped_capabilities_and_lookup_only(monkeypatch) -> None:
    backend_calls: list[tuple[str, str]] = []

    def fake_call(_binding_value, method, path, payload, query):
        backend_calls.append((method, path))
        if method == "GET" and path == "/api/v1/media/managed":
            assert payload is None
            assert query == {}
            return {
                "facebook_free_retrieval_provider": "cobalt",
                "facebook_free_retrieval_configured": True,
                "facebook_paid_retrieval_configured": False,
                "facebook_automatic_paid_retrieval": False,
                "facebook_stt_provider": "assemblyai",
                "facebook_stt_configured": True,
            }
        assert method == "POST"
        assert path == "/api/v1/media/managed/lookup"
        assert payload == {"url": FACEBOOK_URL, "language_hint": "auto"}
        assert query == {}
        raise VoiceBridgeError(
            "voicebridge_http_error",
            http_status=404,
            retryable=False,
        )

    monkeypatch.setattr(r3e3_http, "call_voicebridge", fake_call)
    result = run_r3e3_preflight_lookup_probe(_config(), FACEBOOK_URL)
    assert result["status"] == "pass"
    assert result["preflight"] == "pass"
    assert result["lookup"] == "pass_empty"
    assert result["provider"] == "cobalt"
    assert result["platform"] == "facebook"
    assert result["stt_provider"] == "assemblyai"
    assert result["estimated_retrieval_credits"] == 0
    assert result["automatic_paid_fallback"] is False
    assert result["provider_work_started"] is False
    assert result["start_called"] is False
    assert backend_calls == [
        ("GET", "/api/v1/media/managed"),
        ("POST", "/api/v1/media/managed/lookup"),
    ]


def test_r3e3_record_replay_probe_never_calls_start(monkeypatch) -> None:
    calls: list[str] = []
    job_id = "KRCM_r3e3-replay"

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

    monkeypatch.setattr(r3e3_http, "dispatch_r3e3", fake_dispatch)
    result = run_r3e3_record_replay_probe(_config(), job_id)
    assert result["status"] == "pass"
    assert result["provider_work_started"] is False
    assert result["start_called"] is False
    assert calls == ["media_non_youtube_status", "media_non_youtube_segments"]
    assert "media_facebook_start" not in calls


def test_r3e3_binding_diagnostic_is_read_only_and_reports_scope(monkeypatch) -> None:
    monkeypatch.delenv("KRC_R3E3_VOICEBRIDGE_BEARER_OVERRIDE", raising=False)
    config = replace(
        _config(),
        voicebridge_bearer="legacy-r3e3-action-token-123456789",
    )
    facebook_job = "KRCM_fb-diagnostic"
    telegram_job = "KRCM_tg-diagnostic"
    calls: list[tuple[str, str, str | None]] = []

    def fake_call(binding, method, path, payload, query):
        calls.append((method, path, binding.bearer_token))
        assert method == "GET"
        assert payload is None
        assert query == {}
        if path.endswith(telegram_job):
            raise VoiceBridgeError(
                "voicebridge_http_error",
                http_status=403,
                retryable=False,
            )
        return {"job_id": facebook_job, "status": "COMPLETED"}

    result = r3e3_http.run_r3e3_binding_diagnostic(
        config,
        facebook_job,
        telegram_job,
        backend_call=fake_call,
    )

    assert result["provider_work_started"] is False
    assert result["start_called"] is False
    assert result["raw_facebook_http_status"] == 200
    assert result["raw_telegram_http_status"] == 403
    assert result["derived_facebook_http_status"] == 200
    assert result["derived_telegram_http_status"] == 403
    assert len(calls) == 4


def test_r3e3_health_reports_override_integrity_without_secret(monkeypatch) -> None:
    secret = "runtime-route-secret-123456789-abcdef"
    expected = __import__("hashlib").sha256(secret.encode("utf-8")).hexdigest()
    monkeypatch.setenv("KRC_R3E3_VOICEBRIDGE_BEARER_OVERRIDE", secret)
    monkeypatch.setenv("KRC_R3E3_OVERRIDE_EXPECTED_SHA256", expected)

    response = r3e3_http.handle_r3e3_http_request(
        "GET",
        "/healthz",
        {},
        config=_config(),
    )
    body = json.loads(response.body.decode("utf-8"))
    assert body["voicebridge_override_configured"] is True
    assert body["voicebridge_override_matches_expected_sha256"] is True
    assert secret not in response.body.decode("utf-8")
