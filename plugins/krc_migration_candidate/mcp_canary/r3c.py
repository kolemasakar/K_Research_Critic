from __future__ import annotations

import json
import re
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

from .server import LEGACY_PROTOCOL_VERSION, MCP_PROTOCOL_VERSION, SERVER_NAME

R3C_SURFACE = "r3c_readonly"
R3C_SERVER_VERSION = "0.3.0"
R3C_TOOL_NAMES = (
    "media_get_capabilities",
    "media_youtube_preflight",
    "media_youtube_lookup",
    "media_youtube_status",
    "media_youtube_segments",
    "media_instagram_preflight",
    "media_instagram_lookup",
    "media_non_youtube_status",
    "media_non_youtube_segments",
)
R3C_TOOL_NAME_SET = frozenset(R3C_TOOL_NAMES)
_EXECUTION_TOOL_NAMES = frozenset(
    {
        "media_youtube_start",
        "media_instagram_start",
        "media_facebook_start",
        "media_telegram_start",
    }
)
_LANGUAGE_HINTS = frozenset({"auto", "uk", "ru", "en"})
_JOB_ID_RE = re.compile(r"^KRCM_[A-Za-z0-9-]+$")

_READ_ONLY_ANNOTATIONS: dict[str, bool] = {
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": False,
}

_URL_INPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["url"],
    "properties": {
        "url": {"type": "string", "format": "uri"},
        "language_hint": {"type": "string", "enum": ["auto", "uk", "ru", "en"], "default": "auto"},
    },
}
_JOB_INPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["job_id"],
    "properties": {"job_id": {"type": "string", "pattern": r"^KRCM_[A-Za-z0-9-]+$"}},
}
_SEGMENT_INPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["job_id"],
    "properties": {
        "job_id": {"type": "string", "pattern": r"^KRCM_[A-Za-z0-9-]+$"},
        "cursor": {"type": "integer", "minimum": 0, "default": 0},
        "limit": {"type": "integer", "minimum": 1, "maximum": 50, "default": 20},
    },
}
_OBJECT_OUTPUT_SCHEMA: dict[str, object] = {"type": "object", "additionalProperties": True}

_TOOL_DESCRIPTORS: tuple[dict[str, object], ...] = (
    {
        "name": "media_get_capabilities",
        "title": "KRC MEDIA capabilities",
        "description": "Read VoiceBridge MEDIA routing and safety state. No provider work is started.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "outputSchema": _OBJECT_OUTPUT_SCHEMA,
        "annotations": _READ_ONLY_ANNOTATIONS,
    },
    {
        "name": "media_youtube_preflight",
        "title": "YouTube MEDIA preflight",
        "description": "Validate the supported YouTube route and return the Gemini Free disclosure without provider work.",
        "inputSchema": _URL_INPUT_SCHEMA,
        "outputSchema": _OBJECT_OUTPUT_SCHEMA,
        "annotations": _READ_ONLY_ANNOTATIONS,
    },
    {
        "name": "media_youtube_lookup",
        "title": "YouTube durable lookup",
        "description": "Look up reusable durable YouTube state without starting provider work.",
        "inputSchema": _URL_INPUT_SCHEMA,
        "outputSchema": _OBJECT_OUTPUT_SCHEMA,
        "annotations": _READ_ONLY_ANNOTATIONS,
    },
    {
        "name": "media_youtube_status",
        "title": "YouTube job status",
        "description": "Read an existing durable YouTube MEDIA job.",
        "inputSchema": _JOB_INPUT_SCHEMA,
        "outputSchema": _OBJECT_OUTPUT_SCHEMA,
        "annotations": _READ_ONLY_ANNOTATIONS,
    },
    {
        "name": "media_youtube_segments",
        "title": "YouTube transcript segments",
        "description": "Read a page of transcript segments from an existing YouTube MEDIA job.",
        "inputSchema": _SEGMENT_INPUT_SCHEMA,
        "outputSchema": _OBJECT_OUTPUT_SCHEMA,
        "annotations": _READ_ONLY_ANNOTATIONS,
    },
    {
        "name": "media_instagram_preflight",
        "title": "Instagram MEDIA preflight",
        "description": "Validate the supported Instagram route without retrieval or STT provider work.",
        "inputSchema": _URL_INPUT_SCHEMA,
        "outputSchema": _OBJECT_OUTPUT_SCHEMA,
        "annotations": _READ_ONLY_ANNOTATIONS,
    },
    {
        "name": "media_instagram_lookup",
        "title": "Instagram durable lookup",
        "description": "Look up reusable durable Instagram state without starting provider work.",
        "inputSchema": _URL_INPUT_SCHEMA,
        "outputSchema": _OBJECT_OUTPUT_SCHEMA,
        "annotations": _READ_ONLY_ANNOTATIONS,
    },
    {
        "name": "media_non_youtube_status",
        "title": "Non-YouTube MEDIA job status",
        "description": "Read an existing Instagram, Facebook, or Telegram MEDIA job.",
        "inputSchema": _JOB_INPUT_SCHEMA,
        "outputSchema": _OBJECT_OUTPUT_SCHEMA,
        "annotations": _READ_ONLY_ANNOTATIONS,
    },
    {
        "name": "media_non_youtube_segments",
        "title": "Non-YouTube transcript segments",
        "description": "Read a page of transcript segments from an existing Instagram, Facebook, or Telegram MEDIA job.",
        "inputSchema": _SEGMENT_INPUT_SCHEMA,
        "outputSchema": _OBJECT_OUTPUT_SCHEMA,
        "annotations": _READ_ONLY_ANNOTATIONS,
    },
)

_TOOL_ROUTES: dict[str, tuple[str, str]] = {
    "media_get_capabilities": ("GET", "/api/v1/media/public-capabilities"),
    "media_youtube_preflight": ("POST", "/api/v1/media/youtube-gemini/preflight"),
    "media_youtube_lookup": ("POST", "/api/v1/media/youtube-gemini/lookup"),
    "media_youtube_status": ("GET", "/api/v1/media/youtube-gemini/transcriptions/{job_id}"),
    "media_youtube_segments": ("GET", "/api/v1/media/youtube-gemini/transcriptions/{job_id}/segments"),
    "media_instagram_preflight": ("POST", "/api/v1/media/managed/preflight"),
    "media_instagram_lookup": ("POST", "/api/v1/media/managed/lookup"),
    "media_non_youtube_status": ("GET", "/api/v1/media/managed/transcriptions/{job_id}"),
    "media_non_youtube_segments": ("GET", "/api/v1/media/managed/transcriptions/{job_id}/segments"),
}


@dataclass(frozen=True)
class VoiceBridgeBinding:
    base_url: str | None
    bearer_token: str | None
    timeout_seconds: float = 20.0

    @property
    def configured(self) -> bool:
        return bool(self.base_url and self.bearer_token)


class VoiceBridgeError(RuntimeError):
    def __init__(self, code: str, *, http_status: int | None = None, retryable: bool = False) -> None:
        super().__init__(code)
        self.code = code
        self.http_status = http_status
        self.retryable = retryable


def tool_descriptors() -> list[dict[str, object]]:
    return deepcopy(list(_TOOL_DESCRIPTORS))


def r3c_health(binding: VoiceBridgeBinding) -> dict[str, object]:
    return {
        "service": SERVER_NAME,
        "status": "ok" if binding.configured else "binding_required",
        "surface": R3C_SURFACE,
        "mutation": False,
        "provider_work": False,
        "tool_count": len(R3C_TOOL_NAMES),
        "voicebridge_binding_configured": binding.configured,
        "execution_tools": "not_enabled",
    }


def _validate_https_url(value: object) -> str:
    if not isinstance(value, str) or not value or len(value) > 4096:
        raise ValueError("invalid_url")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError("invalid_url")
    return value


def _language_hint(arguments: Mapping[str, object]) -> str | None:
    if "language_hint" not in arguments:
        return None
    value = arguments.get("language_hint")
    if not isinstance(value, str) or value not in _LANGUAGE_HINTS:
        raise ValueError("invalid_language_hint")
    return value


def _validate_job_id(value: object) -> str:
    if not isinstance(value, str) or _JOB_ID_RE.fullmatch(value) is None:
        raise ValueError("invalid_job_id")
    return value


def _strict_keys(arguments: Mapping[str, object], allowed: frozenset[str]) -> None:
    if not set(arguments).issubset(allowed):
        raise ValueError("unexpected_argument")


def _normalized_call(name: str, arguments: Mapping[str, object]) -> tuple[str, str, dict[str, object] | None, dict[str, object]]:
    method, path_template = _TOOL_ROUTES[name]
    query: dict[str, object] = {}
    payload: dict[str, object] | None = None

    if name == "media_get_capabilities":
        _strict_keys(arguments, frozenset())
        return method, path_template, None, query

    if name in {
        "media_youtube_preflight",
        "media_youtube_lookup",
        "media_instagram_preflight",
        "media_instagram_lookup",
    }:
        _strict_keys(arguments, frozenset({"url", "language_hint"}))
        payload = {"url": _validate_https_url(arguments.get("url"))}
        language_hint = _language_hint(arguments)
        if language_hint is not None:
            payload["language_hint"] = language_hint
        return method, path_template, payload, query

    if name in {"media_youtube_status", "media_non_youtube_status"}:
        _strict_keys(arguments, frozenset({"job_id"}))
        job_id = _validate_job_id(arguments.get("job_id"))
        return method, path_template.format(job_id=job_id), None, query

    if name in {"media_youtube_segments", "media_non_youtube_segments"}:
        _strict_keys(arguments, frozenset({"job_id", "cursor", "limit"}))
        job_id = _validate_job_id(arguments.get("job_id"))
        cursor = arguments.get("cursor", 0)
        limit = arguments.get("limit", 20)
        if isinstance(cursor, bool) or not isinstance(cursor, int) or cursor < 0:
            raise ValueError("invalid_cursor")
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 50:
            raise ValueError("invalid_limit")
        query = {"cursor": cursor, "limit": limit}
        return method, path_template.format(job_id=job_id), None, query

    raise ValueError("unknown_tool")


def call_voicebridge(
    binding: VoiceBridgeBinding,
    method: str,
    path: str,
    payload: Mapping[str, object] | None,
    query: Mapping[str, object],
) -> dict[str, object]:
    if not binding.configured or not binding.base_url or not binding.bearer_token:
        raise VoiceBridgeError("binding_unavailable")
    base = binding.base_url.rstrip("/")
    parsed_base = urlsplit(base)
    if parsed_base.scheme != "https" or not parsed_base.netloc or parsed_base.username or parsed_base.password:
        raise VoiceBridgeError("binding_invalid")
    url = base + path
    if query:
        url = url + "?" + urlencode(query)
    data = None
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + binding.bearer_token,
        "User-Agent": "krc-media-mcp-r3c",
    }
    if payload is not None:
        data = json.dumps(dict(payload), separators=(",", ":")).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(request, timeout=binding.timeout_seconds) as response:
            status = int(response.status)
            raw = response.read(2 * 1024 * 1024)
    except HTTPError as exc:
        status = int(exc.code)
        raise VoiceBridgeError(
            "voicebridge_http_error",
            http_status=status,
            retryable=status in {429, 502, 503, 504},
        ) from None
    except (URLError, TimeoutError, OSError):
        raise VoiceBridgeError("voicebridge_unavailable", retryable=True) from None

    if status < 200 or status >= 300:
        raise VoiceBridgeError(
            "voicebridge_http_error",
            http_status=status,
            retryable=status in {429, 502, 503, 504},
        )
    try:
        decoded = json.loads(raw.decode("utf-8")) if raw else {}
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise VoiceBridgeError("voicebridge_invalid_response") from None
    if not isinstance(decoded, dict):
        raise VoiceBridgeError("voicebridge_invalid_response")
    return decoded


def _response(request_id: object, result: object) -> dict[str, object]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id: object, code: int, message: str) -> dict[str, object]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def _complete(payload: Mapping[str, object]) -> dict[str, object]:
    result = dict(payload)
    result["resultType"] = "complete"
    result["_meta"] = {
        "io.modelcontextprotocol/serverInfo": {"name": SERVER_NAME, "version": R3C_SERVER_VERSION}
    }
    return result


def _tool_result(payload: Mapping[str, object], *, is_error: bool = False) -> dict[str, object]:
    structured = dict(payload)
    return _complete(
        {
            "content": [
                {"type": "text", "text": json.dumps(structured, sort_keys=True, separators=(",", ":"))}
            ],
            "structuredContent": structured,
            "isError": is_error,
        }
    )


def _sanitized_backend_error(error: VoiceBridgeError) -> dict[str, object]:
    detail: dict[str, object] = {"code": error.code, "retryable": error.retryable}
    if error.http_status is not None:
        detail["http_status"] = error.http_status
    return {"status": "error", "error": detail}


BackendCaller = Callable[
    [VoiceBridgeBinding, str, str, Mapping[str, object] | None, Mapping[str, object]],
    dict[str, object],
]


def dispatch_r3c(
    message: Mapping[str, Any],
    binding: VoiceBridgeBinding,
    *,
    backend_call: BackendCaller = call_voicebridge,
) -> dict[str, object] | None:
    request_id = message.get("id")
    if message.get("jsonrpc") != "2.0":
        return _error(request_id, -32600, "Invalid Request")
    method = message.get("method")
    if not isinstance(method, str):
        return _error(request_id, -32600, "Invalid Request")
    if method == "notifications/initialized":
        return None
    if method == "server/discover":
        return _response(
            request_id,
            _complete(
                {
                    "supportedVersions": [MCP_PROTOCOL_VERSION],
                    "capabilities": {"tools": {}},
                    "instructions": (
                        "This authenticated R3-C surface exposes exactly nine non-execution KRC MEDIA tools. "
                        "It does not expose any start/execution operation."
                    ),
                }
            ),
        )
    if method == "initialize":
        params = message.get("params")
        requested_version = params.get("protocolVersion") if isinstance(params, Mapping) else None
        protocol_version = LEGACY_PROTOCOL_VERSION if requested_version != LEGACY_PROTOCOL_VERSION else requested_version
        return _response(
            request_id,
            {
                "protocolVersion": protocol_version,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": R3C_SERVER_VERSION},
            },
        )
    if method == "ping":
        return _response(request_id, _complete({}))
    if method == "tools/list":
        return _response(request_id, _complete({"tools": tool_descriptors()}))
    if method != "tools/call":
        return _error(request_id, -32601, "Method not found")

    params = message.get("params")
    if not isinstance(params, Mapping):
        return _error(request_id, -32602, "Invalid params")
    name = params.get("name")
    if not isinstance(name, str) or name not in R3C_TOOL_NAME_SET or name in _EXECUTION_TOOL_NAMES:
        return _error(request_id, -32602, "Unknown tool")
    arguments = params.get("arguments", {})
    if not isinstance(arguments, Mapping):
        return _error(request_id, -32602, "Invalid params")
    try:
        backend_method, path, payload, query = _normalized_call(name, arguments)
    except ValueError:
        return _error(request_id, -32602, "Invalid params")
    try:
        backend_payload = backend_call(binding, backend_method, path, payload, query)
    except VoiceBridgeError as exc:
        return _response(request_id, _tool_result(_sanitized_backend_error(exc), is_error=True))
    return _response(request_id, _tool_result(backend_payload))
