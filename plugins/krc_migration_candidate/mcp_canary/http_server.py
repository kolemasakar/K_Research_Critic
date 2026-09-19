from __future__ import annotations

import hmac
import json
import os
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Mapping
from urllib.parse import urlsplit

from .oauth import GLOBAL_OAUTH_STATE, READ_SCOPE, OAuthState, handle_oauth_request
from .r3c import (
    R3C_SURFACE,
    R3C_TOOL_NAME_SET,
    VoiceBridgeBinding,
    dispatch_r3c,
    r3c_health,
)
from .server import (
    CANARY_TOOL_NAME,
    LEGACY_PROTOCOL_VERSION,
    MCP_PROTOCOL_VERSION,
    SERVER_NAME,
    canary_result,
    dispatch_mcp,
)

MCP_PATH = "/mcp"
HEALTH_PATH = "/healthz"
MAX_BODY_BYTES = 64 * 1024
SUPPORTED_PROTOCOLS = frozenset({MCP_PROTOCOL_VERSION, LEGACY_PROTOCOL_VERSION})
CANARY_SURFACE = "canary"


@dataclass(frozen=True)
class HttpConfig:
    auth_mode: str = "none"
    bearer_token: str | None = None
    allowed_origins: frozenset[str] = frozenset()
    public_base_url: str | None = None
    owner_code: str | None = None
    surface: str = CANARY_SURFACE
    voicebridge_base_url: str | None = None
    voicebridge_bearer: str | None = None
    voicebridge_timeout_seconds: float = 20.0

    @classmethod
    def from_env(cls) -> "HttpConfig":
        auth_mode = os.getenv("KRC_MCP_AUTH_MODE", "none").strip().lower()
        allowed_origins = frozenset(
            item.strip()
            for item in os.getenv("KRC_MCP_ALLOWED_ORIGINS", "").split(",")
            if item.strip()
        )
        base_url = os.getenv("KRC_MCP_PUBLIC_BASE_URL")
        if base_url:
            base_url = base_url.rstrip("/")
        voicebridge_base_url = os.getenv("KRC_VOICEBRIDGE_BASE_URL")
        if voicebridge_base_url:
            voicebridge_base_url = voicebridge_base_url.rstrip("/")
        timeout_seconds = float(os.getenv("KRC_VOICEBRIDGE_TIMEOUT_SECONDS", "20"))
        if timeout_seconds <= 0 or timeout_seconds > 60:
            raise ValueError("KRC_VOICEBRIDGE_TIMEOUT_SECONDS must be greater than 0 and at most 60")
        return cls(
            auth_mode=auth_mode,
            bearer_token=os.getenv("KRC_MCP_BEARER_TOKEN"),
            allowed_origins=allowed_origins,
            public_base_url=base_url,
            owner_code=os.getenv("KRC_MCP_OWNER_CODE"),
            surface=os.getenv("KRC_MCP_SURFACE", CANARY_SURFACE).strip().lower(),
            voicebridge_base_url=voicebridge_base_url,
            voicebridge_bearer=os.getenv("KRC_VOICEBRIDGE_BEARER"),
            voicebridge_timeout_seconds=timeout_seconds,
        )


@dataclass(frozen=True)
class HttpResponse:
    status: int
    headers: Mapping[str, str]
    body: bytes = b""


def _headers_lower(headers: Mapping[str, str]) -> dict[str, str]:
    return {str(key).lower(): str(value).strip() for key, value in headers.items()}


def _json_response(
    status: int,
    payload: Mapping[str, object],
    *,
    extra_headers: Mapping[str, str] | None = None,
) -> HttpResponse:
    response_headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff",
    }
    if extra_headers:
        response_headers.update(extra_headers)
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return HttpResponse(status=status, headers=response_headers, body=body)


def _rpc_error(request_id: object, code: int, message: str, *, data: object | None = None) -> dict[str, object]:
    error: dict[str, object] = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": "2.0", "id": request_id, "error": error}


def _authorize(
    headers: Mapping[str, str],
    config: HttpConfig,
    *,
    oauth_state: OAuthState | None = None,
) -> HttpResponse | None:
    if config.auth_mode == "none":
        return None

    authorization = headers.get("authorization", "")
    prefix = "Bearer "
    supplied = authorization[len(prefix) :] if authorization.startswith(prefix) else ""

    if config.auth_mode == "bearer":
        if not config.bearer_token:
            return _json_response(HTTPStatus.SERVICE_UNAVAILABLE, {"status": "missing_server_auth_secret"})
        if not supplied or not hmac.compare_digest(supplied, config.bearer_token):
            return _json_response(
                HTTPStatus.UNAUTHORIZED,
                {"status": "unauthorized"},
                extra_headers={"WWW-Authenticate": "Bearer"},
            )
        return None

    if config.auth_mode == "oauth":
        if not config.public_base_url:
            return _json_response(HTTPStatus.SERVICE_UNAVAILABLE, {"status": "missing_oauth_public_base_url"})
        state = oauth_state or GLOBAL_OAUTH_STATE
        if supplied and state.access_allowed(supplied, READ_SCOPE):
            return None
        metadata_url = f"{config.public_base_url}/.well-known/oauth-protected-resource"
        challenge = f'Bearer resource_metadata="{metadata_url}", scope="{READ_SCOPE}"'
        return _json_response(
            HTTPStatus.UNAUTHORIZED,
            {"status": "unauthorized"},
            extra_headers={"WWW-Authenticate": challenge},
        )

    return _json_response(HTTPStatus.SERVICE_UNAVAILABLE, {"status": "misconfigured_auth_mode"})


def _validate_origin(headers: Mapping[str, str], config: HttpConfig) -> HttpResponse | None:
    origin = headers.get("origin")
    if origin is None:
        return None
    if origin in config.allowed_origins:
        return None
    return _json_response(HTTPStatus.FORBIDDEN, {"status": "origin_forbidden"})


def _body_meta(message: Mapping[str, object]) -> Mapping[str, object] | None:
    params = message.get("params")
    if not isinstance(params, Mapping):
        return None
    meta = params.get("_meta")
    return meta if isinstance(meta, Mapping) else None


def _tool_names(config: HttpConfig) -> frozenset[str]:
    if config.surface == CANARY_SURFACE:
        return frozenset({CANARY_TOOL_NAME})
    if config.surface == R3C_SURFACE:
        return R3C_TOOL_NAME_SET
    return frozenset()


def _r3c_binding(config: HttpConfig) -> VoiceBridgeBinding:
    return VoiceBridgeBinding(
        base_url=config.voicebridge_base_url,
        bearer_token=config.voicebridge_bearer,
        timeout_seconds=config.voicebridge_timeout_seconds,
    )


def _validate_modern_headers(
    message: Mapping[str, object],
    headers: Mapping[str, str],
    *,
    allowed_tool_names: frozenset[str],
) -> tuple[int, dict[str, object]] | None:
    request_id = message.get("id")
    method = message.get("method")
    header_version = headers.get("mcp-protocol-version")
    if header_version != MCP_PROTOCOL_VERSION:
        if header_version in SUPPORTED_PROTOCOLS:
            return (
                HTTPStatus.BAD_REQUEST,
                _rpc_error(request_id, -32020, "Header mismatch: modern request requires protocol 2026-07-28"),
            )
        return (
            HTTPStatus.BAD_REQUEST,
            _rpc_error(
                request_id,
                -32022,
                "Unsupported protocol version",
                data={"supported": [MCP_PROTOCOL_VERSION], "requested": header_version or ""},
            ),
        )

    meta = _body_meta(message)
    body_version = meta.get("io.modelcontextprotocol/protocolVersion") if meta else None
    if body_version != header_version:
        return (
            HTTPStatus.BAD_REQUEST,
            _rpc_error(request_id, -32020, "Header mismatch: MCP-Protocol-Version does not match request _meta"),
        )
    client_capabilities = meta.get("io.modelcontextprotocol/clientCapabilities") if meta else None
    if not isinstance(client_capabilities, Mapping):
        return (
            HTTPStatus.BAD_REQUEST,
            _rpc_error(request_id, -32602, "Invalid params: modern request requires clientCapabilities in _meta"),
        )

    header_method = headers.get("mcp-method")
    if not isinstance(method, str) or header_method != method:
        return (
            HTTPStatus.BAD_REQUEST,
            _rpc_error(request_id, -32020, "Header mismatch: Mcp-Method does not match request method"),
        )

    if method == "tools/call":
        params = message.get("params")
        body_name = params.get("name") if isinstance(params, Mapping) else None
        if headers.get("mcp-name") != body_name or body_name not in allowed_tool_names:
            return (
                HTTPStatus.BAD_REQUEST,
                _rpc_error(request_id, -32020, "Header mismatch: Mcp-Name does not match tool name"),
            )
    return None


def handle_http_request(
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

    if config.auth_mode == "oauth" and config.public_base_url:
        oauth_response = handle_oauth_request(
            method,
            path,
            normalized,
            body,
            base_url=config.public_base_url,
            owner_code=config.owner_code,
            state=oauth_state or GLOBAL_OAUTH_STATE,
        )
        if oauth_response is not None:
            return HttpResponse(
                status=oauth_response.status,
                headers=oauth_response.headers,
                body=oauth_response.body,
            )

    if clean_path == HEALTH_PATH and method == "GET":
        if config.surface == CANARY_SURFACE:
            result = canary_result()
            return _json_response(
                HTTPStatus.OK,
                {
                    "service": result["service"],
                    "status": result["status"],
                    "mutation": result["mutation"],
                    "provider_work": result["provider_work"],
                },
            )
        if config.surface == R3C_SURFACE:
            return _json_response(HTTPStatus.OK, r3c_health(_r3c_binding(config)))
        return _json_response(HTTPStatus.SERVICE_UNAVAILABLE, {"status": "unknown_surface"})

    if clean_path != MCP_PATH:
        return _json_response(HTTPStatus.NOT_FOUND, {"status": "not_found"})

    if config.surface not in {CANARY_SURFACE, R3C_SURFACE}:
        return _json_response(HTTPStatus.SERVICE_UNAVAILABLE, {"status": "unknown_surface"})
    if config.surface == R3C_SURFACE:
        if config.auth_mode != "oauth":
            return _json_response(HTTPStatus.SERVICE_UNAVAILABLE, {"status": "r3c_requires_oauth"})
        if not _r3c_binding(config).configured:
            return _json_response(HTTPStatus.SERVICE_UNAVAILABLE, {"status": "voicebridge_binding_unavailable"})

    origin_error = _validate_origin(normalized, config)
    if origin_error:
        return origin_error

    auth_error = _authorize(normalized, config, oauth_state=oauth_state)
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
        return _json_response(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"status": "request_too_large"})
    if "application/json" not in normalized.get("content-type", ""):
        return _json_response(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"status": "application_json_required"})

    try:
        decoded = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return _json_response(HTTPStatus.BAD_REQUEST, _rpc_error(None, -32700, "Parse error"))
    if not isinstance(decoded, Mapping):
        return _json_response(HTTPStatus.BAD_REQUEST, _rpc_error(None, -32600, "Invalid Request"))

    request_id = decoded.get("id")
    method_name = decoded.get("method")
    header_version = normalized.get("mcp-protocol-version")

    modern = header_version == MCP_PROTOCOL_VERSION or method_name == "server/discover"
    if modern:
        validation = _validate_modern_headers(
            decoded,
            normalized,
            allowed_tool_names=_tool_names(config),
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

    if config.surface == R3C_SURFACE:
        response = dispatch_r3c(decoded, _r3c_binding(config))
    else:
        response = dispatch_mcp(decoded)
    if response is None:
        return HttpResponse(status=HTTPStatus.ACCEPTED, headers={"Cache-Control": "no-store"})

    error = response.get("error")
    if isinstance(error, Mapping) and error.get("code") == -32601 and modern:
        return _json_response(HTTPStatus.NOT_FOUND, response)
    return _json_response(HTTPStatus.OK, response)


class CanaryRequestHandler(BaseHTTPRequestHandler):
    server_version = SERVER_NAME
    sys_version = ""

    def _handle(self) -> None:
        content_length = self.headers.get("Content-Length")
        try:
            length = int(content_length) if content_length else 0
        except ValueError:
            length = MAX_BODY_BYTES + 1
        body = self.rfile.read(min(length, MAX_BODY_BYTES + 1)) if length else b""
        response = handle_http_request(self.command, self.path, dict(self.headers.items()), body)

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
        # Request bodies and authorization headers are never logged. OAuth owner
        # codes, access tokens, and outbound VoiceBridge credentials are never
        # emitted by this handler.
        super().log_message(format, *args)


class CanaryHTTPServer(ThreadingHTTPServer):
    daemon_threads = True


def main() -> None:
    host = os.getenv("KRC_MCP_BIND_HOST", "127.0.0.1")
    port = int(os.getenv("PORT", os.getenv("KRC_MCP_PORT", "8000")))
    server = CanaryHTTPServer((host, port), CanaryRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
