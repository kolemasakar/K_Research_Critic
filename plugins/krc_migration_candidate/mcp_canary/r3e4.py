from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Callable, Mapping
from urllib.parse import urlsplit

from .r3c import (
    VoiceBridgeBinding,
    VoiceBridgeError,
    call_voicebridge,
    dispatch_r3c,
    tool_descriptors as r3c_tool_descriptors,
)
from .server import LEGACY_PROTOCOL_VERSION, MCP_PROTOCOL_VERSION, SERVER_NAME

R3E4_SURFACE = "r3e4_telegram_execution"
R3E4_SERVER_VERSION = "0.9.0"
R3E4_EXECUTION_TOOL_NAME = "media_telegram_start"
R3E4_READ_TOOL_NAMES = (
    "media_non_youtube_status",
    "media_non_youtube_segments",
)
R3E4_TOOL_NAMES = R3E4_READ_TOOL_NAMES + (R3E4_EXECUTION_TOOL_NAME,)
R3E4_TOOL_NAME_SET = frozenset(R3E4_TOOL_NAMES)
_DISABLED_EXECUTION_TOOL_NAMES = frozenset(
    {"media_youtube_start", "media_instagram_start", "media_facebook_start"}
)
_LANGUAGE_HINTS = frozenset({"auto", "uk", "ru", "en"})

_ACTION_ANNOTATIONS: dict[str, bool] = {
    "readOnlyHint": False,
    "destructiveHint": False,
    "idempotentHint": False,
    "openWorldHint": True,
}
_OBJECT_OUTPUT_SCHEMA: dict[str, object] = {"type": "object", "additionalProperties": True}
_TELEGRAM_START_INPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["url"],
    "properties": {
        "url": {"type": "string", "format": "uri"},
        "language_hint": {
            "type": "string",
            "enum": ["auto", "uk", "ru", "en"],
            "default": "auto",
        },
    },
}
_TELEGRAM_START_DESCRIPTOR: dict[str, object] = {
    "name": R3E4_EXECUTION_TOOL_NAME,
    "title": "Start Telegram MEDIA processing",
    "description": (
        "Start the free-only Telegram route through public Telegram web retrieval and "
        "AssemblyAI STT. This is the only execution tool exposed by R3-E4. Automatic paid "
        "fallback is forbidden. The action requires ChatGPT consequential-action confirmation."
    ),
    "inputSchema": _TELEGRAM_START_INPUT_SCHEMA,
    "outputSchema": _OBJECT_OUTPUT_SCHEMA,
    "annotations": _ACTION_ANNOTATIONS,
}


BackendCaller = Callable[
    [VoiceBridgeBinding, str, str, Mapping[str, object] | None, Mapping[str, object]],
    dict[str, object],
]


def tool_descriptors() -> list[dict[str, object]]:
    by_name = {item["name"]: item for item in r3c_tool_descriptors()}
    descriptors = [
        deepcopy(by_name[name])
        for name in R3E4_READ_TOOL_NAMES
    ]
    descriptors.append(deepcopy(_TELEGRAM_START_DESCRIPTOR))
    return descriptors


def r3e4_health(binding: VoiceBridgeBinding) -> dict[str, object]:
    return {
        "service": SERVER_NAME,
        "status": "ok" if binding.configured else "binding_required",
        "surface": R3E4_SURFACE,
        "tool_count": len(R3E4_TOOL_NAMES),
        "non_execution_tool_count": len(R3E4_READ_TOOL_NAMES),
        "execution_tool_count": 1,
        "telegram_execution_enabled": True,
        "other_execution_tools": "not_enabled",
        "voicebridge_binding_configured": binding.configured,
        "provider_work_started": False,
    }


def _response(request_id: object, result: object) -> dict[str, object]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id: object, code: int, message: str) -> dict[str, object]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def _complete(payload: Mapping[str, object]) -> dict[str, object]:
    result = dict(payload)
    result["resultType"] = "complete"
    result["_meta"] = {
        "io.modelcontextprotocol/serverInfo": {
            "name": SERVER_NAME,
            "version": R3E4_SERVER_VERSION,
        }
    }
    return result


def _tool_result(payload: Mapping[str, object], *, is_error: bool = False) -> dict[str, object]:
    structured = dict(payload)
    return _complete(
        {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(
                        structured,
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                }
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


def _validate_telegram_url(value: object) -> str:
    if not isinstance(value, str) or not value or len(value) > 4096:
        raise ValueError("invalid_url")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or parsed.username or parsed.password:
        raise ValueError("invalid_url")
    host = (parsed.hostname or "").lower()
    if host not in {"t.me", "telegram.me"}:
        raise ValueError("telegram_url_required")
    parts = [part for part in parsed.path.split("/") if part]
    preview = bool(parts and parts[0].lower() == "s")
    channel = parts[1] if preview and len(parts) > 1 else (parts[0] if parts else "")
    post_id = parts[2] if preview and len(parts) > 2 else (parts[1] if len(parts) > 1 else "")
    expected_parts = 3 if preview else 2
    if len(parts) != expected_parts:
        raise ValueError("telegram_media_url_required")
    if not (5 <= len(channel) <= 64) or not all(ch.isalnum() or ch == "_" for ch in channel):
        raise ValueError("telegram_media_url_required")
    if channel.lower() in {"addlist", "joinchat", "login", "proxy", "share", "socks"}:
        raise ValueError("telegram_media_url_required")
    if not post_id.isdigit() or int(post_id) <= 0:
        raise ValueError("telegram_media_url_required")
    return value

def _validate_language_hint(arguments: Mapping[str, object]) -> str | None:
    if "language_hint" not in arguments:
        return None
    value = arguments.get("language_hint")
    if not isinstance(value, str) or value not in _LANGUAGE_HINTS:
        raise ValueError("invalid_language_hint")
    return value


def _normalized_start(arguments: Mapping[str, object]) -> dict[str, object]:
    if not set(arguments).issubset({"url", "language_hint"}):
        raise ValueError("unexpected_argument")
    if "url" not in arguments:
        raise ValueError("missing_argument")
    payload: dict[str, object] = {
        "url": _validate_telegram_url(arguments.get("url")),
    }
    language_hint = _validate_language_hint(arguments)
    if language_hint is not None:
        payload["language_hint"] = language_hint
    return payload


def _rewrite_server_info(response: dict[str, object] | None) -> dict[str, object] | None:
    if response is None:
        return None
    result = response.get("result")
    if isinstance(result, dict):
        meta = result.get("_meta")
        if isinstance(meta, dict):
            meta["io.modelcontextprotocol/serverInfo"] = {
                "name": SERVER_NAME,
                "version": R3E4_SERVER_VERSION,
            }
    return response


def dispatch_r3e4(
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
                        "R3-E4 exposes two Telegram-safe read tools plus exactly one "
                        "execution operation: media_telegram_start. YouTube, Instagram, and "
                        "Facebook start operations are not exposed."
                    ),
                }
            ),
        )
    if method == "initialize":
        params = message.get("params")
        requested_version = params.get("protocolVersion") if isinstance(params, Mapping) else None
        protocol_version = (
            LEGACY_PROTOCOL_VERSION
            if requested_version != LEGACY_PROTOCOL_VERSION
            else requested_version
        )
        return _response(
            request_id,
            {
                "protocolVersion": protocol_version,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": R3E4_SERVER_VERSION},
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
    if not isinstance(name, str) or name not in R3E4_TOOL_NAME_SET:
        return _error(request_id, -32602, "Unknown tool")
    if name in _DISABLED_EXECUTION_TOOL_NAMES:
        return _error(request_id, -32602, "Unknown tool")

    if name in R3E4_READ_TOOL_NAMES:
        return _rewrite_server_info(
            dispatch_r3c(message, binding, backend_call=backend_call)
        )

    arguments = params.get("arguments", {})
    if not isinstance(arguments, Mapping):
        return _error(request_id, -32602, "Invalid params")
    try:
        payload = _normalized_start(arguments)
    except ValueError:
        return _error(request_id, -32602, "Invalid params")

    try:
        backend_payload = backend_call(
            binding,
            "POST",
            "/api/v1/media/managed/telegram",
            payload,
            {},
        )
    except VoiceBridgeError as exc:
        return _response(
            request_id,
            _tool_result(_sanitized_backend_error(exc), is_error=True),
        )
    return _response(request_id, _tool_result(backend_payload))
