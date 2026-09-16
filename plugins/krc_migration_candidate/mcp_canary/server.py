from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Mapping

MCP_PROTOCOL_VERSION = "2026-07-28"
LEGACY_PROTOCOL_VERSION = "2025-11-25"
CANARY_TOOL_NAME = "krc_media_capabilities_canary"

_CANARY_RESULT: dict[str, object] = {
    "service": "krc-media-mcp-canary",
    "status": "ok",
    "mutation": False,
    "provider_work": False,
    "media_operation_target_count": 13,
    "voicebridge_binding": "not_enabled",
    "execution_tools": "not_enabled",
}

_TOOL_DESCRIPTOR: dict[str, object] = {
    "name": CANARY_TOOL_NAME,
    "title": "KRC MEDIA capabilities canary",
    "description": (
        "Returns deterministic repository-only KRC MEDIA canary metadata. "
        "It does not call providers, VoiceBridge, or mutate external state."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "service": {"type": "string", "const": "krc-media-mcp-canary"},
            "status": {"type": "string", "const": "ok"},
            "mutation": {"type": "boolean", "const": False},
            "provider_work": {"type": "boolean", "const": False},
            "media_operation_target_count": {"type": "integer", "const": 13},
            "voicebridge_binding": {"type": "string", "const": "not_enabled"},
            "execution_tools": {"type": "string", "const": "not_enabled"},
        },
        "required": [
            "service",
            "status",
            "mutation",
            "provider_work",
            "media_operation_target_count",
            "voicebridge_binding",
            "execution_tools",
        ],
        "additionalProperties": False,
    },
    "annotations": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
}


def canary_result() -> dict[str, object]:
    """Return a fresh deterministic canary result."""

    return deepcopy(_CANARY_RESULT)


def tool_descriptor() -> dict[str, object]:
    """Return a fresh MCP tool descriptor for discovery."""

    return deepcopy(_TOOL_DESCRIPTOR)


def _response(request_id: object, result: object) -> dict[str, object]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id: object, code: int, message: str) -> dict[str, object]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }


def dispatch_mcp(message: Mapping[str, Any]) -> dict[str, object] | None:
    """Dispatch a small transport-neutral subset of MCP for the canary.

    The function deliberately performs no I/O. A later deployment phase may
    wrap it with a supported remote HTTPS MCP transport after separate approval.
    """

    request_id = message.get("id")
    if message.get("jsonrpc") != "2.0":
        return _error(request_id, -32600, "Invalid Request")

    method = message.get("method")
    if not isinstance(method, str):
        return _error(request_id, -32600, "Invalid Request")

    if method == "notifications/initialized":
        return None

    if method == "initialize":
        params = message.get("params")
        requested_version = params.get("protocolVersion") if isinstance(params, Mapping) else None
        protocol_version = (
            requested_version
            if requested_version in {MCP_PROTOCOL_VERSION, LEGACY_PROTOCOL_VERSION}
            else MCP_PROTOCOL_VERSION
        )
        return _response(
            request_id,
            {
                "protocolVersion": protocol_version,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "krc-media-mcp-canary", "version": "0.1.0"},
            },
        )

    if method == "ping":
        return _response(request_id, {})

    if method == "tools/list":
        return _response(request_id, {"tools": [tool_descriptor()]})

    if method == "tools/call":
        params = message.get("params")
        if not isinstance(params, Mapping):
            return _error(request_id, -32602, "Invalid params")
        if params.get("name") != CANARY_TOOL_NAME:
            return _error(request_id, -32602, "Unknown tool")

        arguments = params.get("arguments", {})
        if not isinstance(arguments, Mapping) or arguments:
            return _error(request_id, -32602, "Canary tool accepts no arguments")

        result = canary_result()
        return _response(
            request_id,
            {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, sort_keys=True, separators=(",", ":")),
                    }
                ],
                "structuredContent": result,
                "isError": False,
            },
        )

    return _error(request_id, -32601, "Method not found")
