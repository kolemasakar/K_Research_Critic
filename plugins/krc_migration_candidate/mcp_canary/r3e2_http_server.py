from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Mapping
from urllib.parse import urlsplit

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
from .r3c import VoiceBridgeBinding
from .r3e2 import (
    R3E2_SURFACE,
    R3E2_TOOL_NAME_SET,
    dispatch_r3e2,
    r3e2_health,
)
from .server import LEGACY_PROTOCOL_VERSION, MCP_PROTOCOL_VERSION, SERVER_NAME

R3E2_PREFLIGHT_PROBE_ENV = "KRC_R3E2_PREFLIGHT_PROBE_URL"


def _binding(config: HttpConfig) -> VoiceBridgeBinding:
    return VoiceBridgeBinding(
        base_url=config.voicebridge_base_url,
        bearer_token=config.voicebridge_bearer,
        timeout_seconds=config.voicebridge_timeout_seconds,
    )


def handle_r3e2_http_request(
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
        return _json_response(HTTPStatus.OK, r3e2_health(_binding(config)))

    if clean_path != MCP_PATH:
        return _json_response(HTTPStatus.NOT_FOUND, {"status": "not_found"})
    if config.surface != R3E2_SURFACE:
        return _json_response(
            HTTPStatus.SERVICE_UNAVAILABLE,
            {"status": "r3e2_surface_required"},
        )
    if config.auth_mode != "oauth":
        return _json_response(
            HTTPStatus.SERVICE_UNAVAILABLE,
            {"status": "r3e2_requires_oauth"},
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
            allowed_tool_names=R3E2_TOOL_NAME_SET,
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

    response = dispatch_r3e2(decoded, _binding(config))
    if response is None:
        return HttpResponse(
            status=HTTPStatus.ACCEPTED,
            headers={"Cache-Control": "no-store"},
        )
    error = response.get("error")
    if isinstance(error, Mapping) and error.get("code") == -32601 and modern:
        return _json_response(HTTPStatus.NOT_FOUND, response)
    return _json_response(HTTPStatus.OK, response)


class R3E2RequestHandler(BaseHTTPRequestHandler):
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
        response = handle_r3e2_http_request(
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


class R3E2HTTPServer(ThreadingHTTPServer):
    daemon_threads = True


def _structured(response: object) -> Mapping[str, object] | None:
    if not isinstance(response, Mapping):
        return None
    result = response.get("result")
    if not isinstance(result, Mapping):
        return None
    structured = result.get("structuredContent")
    return structured if isinstance(structured, Mapping) else None


def run_r3e2_preflight_lookup_probe(
    config: HttpConfig,
    source_url: str,
) -> dict[str, object]:
    """Run only Instagram preflight + durable lookup; never call start."""

    summary: dict[str, object] = {
        "event": "r3e2_instagram_preflight_lookup_probe",
        "status": "fail",
        "provider_work_started": False,
        "start_called": False,
    }

    preflight_message = {
        "jsonrpc": "2.0",
        "id": "r3e2-preflight",
        "method": "tools/call",
        "params": {
            "name": "media_instagram_preflight",
            "arguments": {"url": source_url, "language_hint": "auto"},
        },
    }
    preflight_response = dispatch_r3e2(preflight_message, _binding(config))
    preflight = _structured(preflight_response)
    if preflight is None:
        summary["reason"] = "preflight_missing"
        return summary
    preflight_result = (
        preflight_response.get("result")
        if isinstance(preflight_response, Mapping)
        else None
    )
    if isinstance(preflight_result, Mapping) and preflight_result.get("isError") is True:
        summary["reason"] = "preflight_error"
        error = preflight.get("error")
        if isinstance(error, Mapping):
            summary["preflight_code"] = error.get("code")
            summary["preflight_http_status"] = error.get("http_status")
        return summary

    expected = (
        preflight.get("provider") == "cobalt"
        and preflight.get("platform") == "instagram"
        and preflight.get("estimated_retrieval_credits") == 0
        and preflight.get("automatic_paid_fallback") is False
        and preflight.get("stt_provider") == "assemblyai"
    )
    if not expected:
        summary["reason"] = "preflight_contract_mismatch"
        return summary

    summary["preflight"] = "pass"
    summary["provider"] = "cobalt"
    summary["platform"] = "instagram"
    summary["stt_provider"] = "assemblyai"
    summary["estimated_retrieval_credits"] = 0
    summary["automatic_paid_fallback"] = False

    lookup_message = {
        "jsonrpc": "2.0",
        "id": "r3e2-lookup",
        "method": "tools/call",
        "params": {
            "name": "media_instagram_lookup",
            "arguments": {"url": source_url, "language_hint": "auto"},
        },
    }
    lookup_response = dispatch_r3e2(lookup_message, _binding(config))
    lookup = _structured(lookup_response)
    if lookup is None:
        summary["reason"] = "lookup_missing"
        return summary
    lookup_result = (
        lookup_response.get("result")
        if isinstance(lookup_response, Mapping)
        else None
    )
    if isinstance(lookup_result, Mapping) and lookup_result.get("isError") is True:
        error = lookup.get("error")
        if not isinstance(error, Mapping):
            summary["reason"] = "lookup_error_unstructured"
            return summary
        code = error.get("code")
        status = error.get("http_status")
        summary["lookup_code"] = code
        summary["lookup_http_status"] = status
        if code == "voicebridge_http_error" and status == 404:
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
    probe_url = os.getenv(R3E2_PREFLIGHT_PROBE_ENV, "").strip()
    if probe_url:
        print(
            json.dumps(
                run_r3e2_preflight_lookup_probe(config, probe_url),
                separators=(",", ":"),
                sort_keys=True,
            ),
            flush=True,
        )
    server = R3E2HTTPServer((host, port), R3E2RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
