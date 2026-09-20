from __future__ import annotations

import json
import os
from hashlib import sha256
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from time import monotonic, sleep
from typing import Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from .http_server import (
    HEALTH_PATH,
    MAX_BODY_BYTES,
    MCP_PATH,
    HttpConfig,
    HttpResponse,
    _authorize,
    _headers_lower,
    _json_response,
    _rpc_error,
    _validate_modern_headers,
    _validate_origin,
)
from .oauth import GLOBAL_OAUTH_STATE, OAuthState, handle_oauth_request
from .r3c import VoiceBridgeBinding, VoiceBridgeError, call_voicebridge
from .r3e3 import (
    R3E3_SURFACE,
    R3E3_TOOL_NAME_SET,
    dispatch_r3e3,
    r3e3_health,
)
from .server import LEGACY_PROTOCOL_VERSION, MCP_PROTOCOL_VERSION, SERVER_NAME

R3E3_PREFLIGHT_PROBE_ENV = "KRC_R3E3_PREFLIGHT_PROBE_URL"
R3E3_REPLAY_PROBE_ENV = "KRC_R3E3_REPLAY_PROBE_JOB_ID"
R3E3_CONFIRMATION_PROBE_ONLY_ENV = "KRC_R3E3_CONFIRMATION_PROBE_ONLY"
R3E3_VOICEBRIDGE_BEARER_OVERRIDE_ENV = "KRC_R3E3_VOICEBRIDGE_BEARER_OVERRIDE"
R3E3_SCOPE_DIAGNOSTIC_TELEGRAM_JOB_ENV = "KRC_R3E3_SCOPE_DIAGNOSTIC_TELEGRAM_JOB_ID"
_CONFIRMATION_PROBE_INVOCATIONS = 0


def _confirmation_probe_enabled() -> bool:
    return os.getenv(R3E3_CONFIRMATION_PROBE_ONLY_ENV, "").strip().lower() == "true"


def _confirmation_probe_backend(
    _binding_value: VoiceBridgeBinding,
    _method: str,
    _path: str,
    _payload: Mapping[str, object] | None,
    _query: Mapping[str, object],
) -> dict[str, object]:
    global _CONFIRMATION_PROBE_INVOCATIONS
    _CONFIRMATION_PROBE_INVOCATIONS += 1
    return {
        "status": "ok",
        "phase": "R3-E3",
        "confirmation_probe_executed": True,
        "external_mutation": False,
        "provider_work": False,
        "provider_charge": False,
        "real_media_start": False,
        "invocation_count": _CONFIRMATION_PROBE_INVOCATIONS,
    }


def _derive_r3e3_route_bearer(base_bearer: str) -> str:
    material = f"krc-media-route:r3e3:v1:{base_bearer}".encode("utf-8")
    return "r3e3-" + sha256(material).hexdigest()


def _binding(config: HttpConfig) -> VoiceBridgeBinding:
    override_bearer = os.getenv(R3E3_VOICEBRIDGE_BEARER_OVERRIDE_ENV, "").strip()
    derived_bearer = (
        _derive_r3e3_route_bearer(config.voicebridge_bearer)
        if config.voicebridge_bearer
        else None
    )
    return VoiceBridgeBinding(
        base_url=config.voicebridge_base_url,
        bearer_token=override_bearer or derived_bearer,
        timeout_seconds=config.voicebridge_timeout_seconds,
    )


_VOICEBRIDGE_WARMUP_PATH = "/api/v1/health"
_VOICEBRIDGE_WARMUP_RETRY_STATUSES = frozenset({429, 502, 503, 504})
_VOICEBRIDGE_WARMUP_BUDGET_SECONDS = 45.0
_VOICEBRIDGE_WARMUP_RETRY_DELAY_SECONDS = 2.0
_VOICEBRIDGE_WARMUP_REQUEST_TIMEOUT_SECONDS = 5.0


def _warm_voicebridge(binding: VoiceBridgeBinding) -> None:
    """Wake a free-tier VoiceBridge instance using health-only GETs.

    No MEDIA provider work is started here. The consequential POST is sent
    exactly once by _cold_start_resilient_backend after health becomes ready.
    """

    if not binding.configured or not binding.base_url:
        raise VoiceBridgeError("binding_unavailable")
    base = binding.base_url.rstrip("/")
    parsed = urlsplit(base)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise VoiceBridgeError("binding_invalid")

    deadline = monotonic() + _VOICEBRIDGE_WARMUP_BUDGET_SECONDS
    last_error = VoiceBridgeError("voicebridge_unavailable", retryable=True)
    while True:
        request = Request(
            base + _VOICEBRIDGE_WARMUP_PATH,
            headers={
                "Accept": "application/json",
                "User-Agent": "krc-media-mcp-r3e3-warmup",
            },
            method="GET",
        )
        try:
            with urlopen(
                request,
                timeout=min(
                    max(binding.timeout_seconds, 1.0),
                    _VOICEBRIDGE_WARMUP_REQUEST_TIMEOUT_SECONDS,
                ),
            ) as response:
                status = int(response.status)
                response.read(64 * 1024)
            if status == 200:
                return
            last_error = VoiceBridgeError(
                "voicebridge_http_error",
                http_status=status,
                retryable=status in _VOICEBRIDGE_WARMUP_RETRY_STATUSES,
            )
            if status not in _VOICEBRIDGE_WARMUP_RETRY_STATUSES:
                raise last_error
        except HTTPError as exc:
            status = int(exc.code)
            last_error = VoiceBridgeError(
                "voicebridge_http_error",
                http_status=status,
                retryable=status in _VOICEBRIDGE_WARMUP_RETRY_STATUSES,
            )
            if status not in _VOICEBRIDGE_WARMUP_RETRY_STATUSES:
                raise last_error from None
        except (URLError, TimeoutError, OSError):
            last_error = VoiceBridgeError("voicebridge_unavailable", retryable=True)

        if monotonic() >= deadline:
            raise last_error
        sleep(_VOICEBRIDGE_WARMUP_RETRY_DELAY_SECONDS)


def _cold_start_resilient_backend(
    binding: VoiceBridgeBinding,
    method: str,
    path: str,
    payload: Mapping[str, object] | None,
    query: Mapping[str, object],
) -> dict[str, object]:
    if method == "POST" and path == "/api/v1/media/managed/facebook-fallback":
        _warm_voicebridge(binding)
    return call_voicebridge(binding, method, path, payload, query)


def handle_r3e3_http_request(
    method: str,
    path: str,
    headers: Mapping[str, str],
    body: bytes = b"",
    *,
    config: HttpConfig | None = None,
    oauth_state: OAuthState | None = None,
) -> HttpResponse:
    config = config or HttpConfig.from_env()
    normalized = _headers_lower(headers)
    clean_path = urlsplit(path).path
    state = oauth_state or GLOBAL_OAUTH_STATE

    if config.auth_mode == "oauth" and config.public_base_url:
        oauth_response = handle_oauth_request(
            method,
            path,
            normalized,
            body,
            base_url=config.public_base_url,
            owner_code=config.owner_code,
            state=state,
        )
        if oauth_response is not None:
            return HttpResponse(
                status=oauth_response.status,
                headers=oauth_response.headers,
                body=oauth_response.body,
            )

    if clean_path == HEALTH_PATH and method == "GET":
        health = r3e3_health(_binding(config))
        health["confirmation_probe_only"] = _confirmation_probe_enabled()
        health["confirmation_probe_invocation_count"] = _CONFIRMATION_PROBE_INVOCATIONS
        return _json_response(HTTPStatus.OK, health)

    if clean_path != MCP_PATH:
        return _json_response(HTTPStatus.NOT_FOUND, {"status": "not_found"})
    if config.surface != R3E3_SURFACE:
        return _json_response(
            HTTPStatus.SERVICE_UNAVAILABLE,
            {"status": "r3e3_surface_required"},
        )
    if config.auth_mode != "oauth":
        return _json_response(
            HTTPStatus.SERVICE_UNAVAILABLE,
            {"status": "r3e3_requires_oauth"},
        )
    if not _binding(config).configured:
        return _json_response(
            HTTPStatus.SERVICE_UNAVAILABLE,
            {"status": "voicebridge_binding_unavailable"},
        )

    origin_error = _validate_origin(normalized, config)
    if origin_error:
        return origin_error
    auth_error = _authorize(normalized, config, oauth_state=state)
    if auth_error:
        return auth_error

    if method == "GET":
        return _json_response(
            HTTPStatus.METHOD_NOT_ALLOWED,
            {"status": "stateless_mcp_post_only"},
            extra_headers={"Allow": "POST"},
        )
    if method != "POST":
        return _json_response(
            HTTPStatus.METHOD_NOT_ALLOWED,
            {"status": "method_not_allowed"},
            extra_headers={"Allow": "POST"},
        )
    if len(body) > MAX_BODY_BYTES:
        return _json_response(
            HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            {"status": "request_too_large"},
        )
    if "application/json" not in normalized.get("content-type", ""):
        return _json_response(
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            {"status": "application_json_required"},
        )

    try:
        decoded = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return _json_response(
            HTTPStatus.BAD_REQUEST,
            _rpc_error(None, -32700, "Parse error"),
        )
    if not isinstance(decoded, Mapping):
        return _json_response(
            HTTPStatus.BAD_REQUEST,
            _rpc_error(None, -32600, "Invalid Request"),
        )

    request_id = decoded.get("id")
    method_name = decoded.get("method")
    header_version = normalized.get("mcp-protocol-version")
    modern = header_version == MCP_PROTOCOL_VERSION or method_name == "server/discover"
    if modern:
        validation = _validate_modern_headers(
            decoded,
            normalized,
            allowed_tool_names=R3E3_TOOL_NAME_SET,
        )
        if validation:
            status, payload = validation
            return _json_response(status, payload)
    elif method_name != "initialize" and header_version != LEGACY_PROTOCOL_VERSION:
        return _json_response(
            HTTPStatus.BAD_REQUEST,
            _rpc_error(
                request_id,
                -32022,
                "Unsupported protocol version",
                data={
                    "supported": [MCP_PROTOCOL_VERSION, LEGACY_PROTOCOL_VERSION],
                    "requested": header_version or "",
                },
            ),
        )

    if (
        _confirmation_probe_enabled()
        and method_name == "tools/call"
        and isinstance(decoded.get("params"), Mapping)
        and decoded["params"].get("name") == "media_facebook_start"
    ):
        response = dispatch_r3e3(
            decoded,
            _binding(config),
            backend_call=_confirmation_probe_backend,
        )
    else:
        response = dispatch_r3e3(
            decoded,
            _binding(config),
            backend_call=_cold_start_resilient_backend,
        )
    if response is None:
        return HttpResponse(
            status=HTTPStatus.ACCEPTED,
            headers={"Cache-Control": "no-store"},
        )
    error = response.get("error")
    if isinstance(error, Mapping) and error.get("code") == -32601 and modern:
        return _json_response(HTTPStatus.NOT_FOUND, response)
    return _json_response(HTTPStatus.OK, response)


class R3E3RequestHandler(BaseHTTPRequestHandler):
    server_version = SERVER_NAME
    sys_version = ""

    def _handle(self) -> None:
        content_length = self.headers.get("Content-Length")
        try:
            length = int(content_length) if content_length else 0
        except ValueError:
            length = MAX_BODY_BYTES + 1
        body = (
            self.rfile.read(min(length, MAX_BODY_BYTES + 1))
            if length
            else b""
        )
        response = handle_r3e3_http_request(
            self.command,
            self.path,
            dict(self.headers.items()),
            body,
        )
        self.send_response(int(response.status))
        for key, value in response.headers.items():
            self.send_header(key, value)
        if response.body:
            self.send_header("Content-Length", str(len(response.body)))
        self.end_headers()
        if response.body:
            self.wfile.write(response.body)

    do_GET = _handle
    do_POST = _handle
    do_OPTIONS = _handle
    do_DELETE = _handle

    def log_message(self, format: str, *args: object) -> None:
        super().log_message(format, *args)


class R3E3HTTPServer(ThreadingHTTPServer):
    daemon_threads = True


def _structured(response: object) -> Mapping[str, object] | None:
    if not isinstance(response, Mapping):
        return None
    result = response.get("result")
    if not isinstance(result, Mapping):
        return None
    structured = result.get("structuredContent")
    return structured if isinstance(structured, Mapping) else None


def _raw_binding(config: HttpConfig) -> VoiceBridgeBinding:
    return VoiceBridgeBinding(
        base_url=config.voicebridge_base_url,
        bearer_token=config.voicebridge_bearer,
        timeout_seconds=config.voicebridge_timeout_seconds,
    )


def run_r3e3_binding_diagnostic(
    config: HttpConfig,
    facebook_job_id: str,
    telegram_job_id: str,
    *,
    backend_call=call_voicebridge,
) -> dict[str, object]:
    """Compare raw/derived bearer scope using read-only durable job GETs."""

    summary: dict[str, object] = {
        "event": "r3e3_binding_diagnostic",
        "provider_work_started": False,
        "start_called": False,
    }
    variants = {
        "raw": _raw_binding(config),
        "derived": _binding(config),
    }
    jobs = {
        "facebook": facebook_job_id,
        "telegram": telegram_job_id,
    }
    for variant, binding in variants.items():
        for platform, job_id in jobs.items():
            key = f"{variant}_{platform}"
            try:
                payload = backend_call(
                    binding,
                    "GET",
                    f"/api/v1/media/managed/transcriptions/{job_id}",
                    None,
                    {},
                )
            except VoiceBridgeError as exc:
                summary[f"{key}_http_status"] = exc.http_status
                summary[f"{key}_code"] = exc.code
                continue
            summary[f"{key}_http_status"] = 200
            summary[f"{key}_job_match"] = payload.get("job_id") == job_id
    return summary


def run_r3e3_record_replay_probe(
    config: HttpConfig,
    job_id: str,
) -> dict[str, object]:
    """Read durable Facebook job status and segments without provider work."""

    summary: dict[str, object] = {
        "event": "r3e3_record_replay_probe",
        "status": "fail",
        "job_id": job_id,
        "provider_work_started": False,
        "start_called": False,
    }

    status_message = {
        "jsonrpc": "2.0",
        "id": "r3e3-replay-status",
        "method": "tools/call",
        "params": {
            "name": "media_non_youtube_status",
            "arguments": {"job_id": job_id},
        },
    }
    status_response = dispatch_r3e3(status_message, _binding(config))
    status_structured = _structured(status_response)
    if status_structured is None:
        summary["reason"] = "status_missing"
        return summary
    status_result = (
        status_response.get("result")
        if isinstance(status_response, Mapping)
        else None
    )
    if isinstance(status_result, Mapping) and status_result.get("isError") is True:
        summary["reason"] = "status_error"
        return summary

    segments_message = {
        "jsonrpc": "2.0",
        "id": "r3e3-replay-segments",
        "method": "tools/call",
        "params": {
            "name": "media_non_youtube_segments",
            "arguments": {"job_id": job_id, "cursor": 0, "limit": 50},
        },
    }
    segments_response = dispatch_r3e3(segments_message, _binding(config))
    segments_structured = _structured(segments_response)
    if segments_structured is None:
        summary["reason"] = "segments_missing"
        return summary
    segments_result = (
        segments_response.get("result")
        if isinstance(segments_response, Mapping)
        else None
    )
    if isinstance(segments_result, Mapping) and segments_result.get("isError") is True:
        summary["reason"] = "segments_error"
        return summary

    if (
        status_structured.get("job_id") != job_id
        or segments_structured.get("job_id") != job_id
    ):
        summary["reason"] = "job_id_mismatch"
        return summary

    summary["job_status"] = status_structured.get("status")
    summary["segment_count"] = status_structured.get("segment_count")
    segments = segments_structured.get("segments")
    summary["page_segment_count"] = len(segments) if isinstance(segments, list) else None
    summary["next_cursor"] = segments_structured.get("next_cursor")
    summary["status"] = "pass"
    return summary


def run_r3e3_preflight_lookup_probe(
    config: HttpConfig,
    source_url: str,
) -> dict[str, object]:
    """Read Facebook free-route capabilities and durable lookup; never call start."""

    summary: dict[str, object] = {
        "event": "r3e3_facebook_preflight_lookup_probe",
        "status": "fail",
        "provider_work_started": False,
        "start_called": False,
    }

    try:
        capabilities = call_voicebridge(
            _binding(config),
            "GET",
            "/api/v1/media/managed",
            None,
            {},
        )
    except VoiceBridgeError as exc:
        summary["reason"] = "capabilities_error"
        summary["capabilities_code"] = exc.code
        summary["capabilities_http_status"] = exc.http_status
        return summary

    expected = (
        capabilities.get("facebook_free_retrieval_provider") == "cobalt"
        and capabilities.get("facebook_free_retrieval_configured") is True
        and capabilities.get("facebook_paid_retrieval_configured") is False
        and capabilities.get("facebook_automatic_paid_retrieval") is False
        and capabilities.get("facebook_stt_provider") == "assemblyai"
        and capabilities.get("facebook_stt_configured") is True
    )
    if not expected:
        summary["reason"] = "capabilities_contract_mismatch"
        return summary
    summary["preflight"] = "pass"
    summary["provider"] = "cobalt"
    summary["platform"] = "facebook"
    summary["stt_provider"] = "assemblyai"
    summary["estimated_retrieval_credits"] = 0
    summary["automatic_paid_fallback"] = False

    try:
        lookup = call_voicebridge(
            _binding(config),
            "POST",
            "/api/v1/media/managed/lookup",
            {"url": source_url, "language_hint": "auto"},
            {},
        )
    except VoiceBridgeError as exc:
        summary["lookup_code"] = exc.code
        summary["lookup_http_status"] = exc.http_status
        if exc.code == "voicebridge_http_error" and exc.http_status == 404:
            summary["lookup"] = "pass_empty"
            summary["status"] = "pass"
            return summary
        summary["reason"] = "lookup_failed"
        return summary
    summary["lookup"] = "pass_existing"
    job_id = lookup.get("job_id")
    if isinstance(job_id, str):
        summary["job_id"] = job_id
    summary["status"] = "pass"
    return summary


def main() -> None:
    host = os.getenv("KRC_MCP_BIND_HOST", "127.0.0.1")
    port = int(os.getenv("PORT", os.getenv("KRC_MCP_PORT", "8000")))
    config = HttpConfig.from_env()
    probe_url = os.getenv(R3E3_PREFLIGHT_PROBE_ENV, "").strip()
    if probe_url:
        print(
            json.dumps(
                run_r3e3_preflight_lookup_probe(config, probe_url),
                separators=(",", ":"),
                sort_keys=True,
            ),
            flush=True,
        )

    replay_job_id = os.getenv(R3E3_REPLAY_PROBE_ENV, "").strip()
    scope_diag_telegram_job_id = os.getenv(
        R3E3_SCOPE_DIAGNOSTIC_TELEGRAM_JOB_ENV, ""
    ).strip()
    if replay_job_id and scope_diag_telegram_job_id:
        print(
            json.dumps(
                run_r3e3_binding_diagnostic(
                    config,
                    replay_job_id,
                    scope_diag_telegram_job_id,
                ),
                separators=(",", ":"),
                sort_keys=True,
            ),
            flush=True,
        )
    if replay_job_id:
        print(
            json.dumps(
                run_r3e3_record_replay_probe(config, replay_job_id),
                separators=(",", ":"),
                sort_keys=True,
            ),
            flush=True,
        )

    server = R3E3HTTPServer((host, port), R3E3RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
