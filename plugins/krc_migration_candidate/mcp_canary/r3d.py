from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Mapping

from .server import LEGACY_PROTOCOL_VERSION, MCP_PROTOCOL_VERSION, SERVER_NAME

R3D_SURFACE = "r3d_confirmation_probe"
R3D_SERVER_VERSION = "0.4.0"
R3D_TOOL_NAME = "krc_r3d_noop_action_probe"
R3D_TOOL_NAME_SET = frozenset({R3D_TOOL_NAME})

_ACTION_ANNOTATIONS: dict[str, bool] = {
    "readOnlyHint": False,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": False,
}

_TOOL_DESCRIPTOR: dict[str, object] = {
    "name": R3D_TOOL_NAME,
    "title": "KRC R3-D no-op consequential-action probe",
    "description": (
        "Tests ChatGPT write-action confirmation semantics. The tool performs no "
        "VoiceBridge call, provider work, charge, MEDIA start, or external mutation. "
        "If invoked after confirmation it only increments an ephemeral in-process counter."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "const": "ok"},
            "phase": {"type": "string", "const": "R3-D"},
            "probe_executed": {"type": "boolean", "const": True},
            "external_mutation": {"type": "boolean", "const": False},
            "provider_work": {"type": "boolean", "const": False},
            "provider_charge": {"type": "boolean", "const": False},
            "real_media_start": {"type": "boolean", "const": False},
            "invocation_count": {"type": "integer", "minimum": 1},
        },
        "required": [
            "status",
            "phase",
            "probe_executed",
            "external_mutation",
            "provider_work",
            "provider_charge",
            "real_media_start",
            "invocation_count",
        ],
        "additionalProperties": False,
    },
    "annotations": _ACTION_ANNOTATIONS,
}


@dataclass
class R3DProbeState:
    _invocation_count: int = 0
    _lock: Lock = field(default_factory=Lock)

    def record_invocation(self) -> int:
        with self._lock:
            self._invocation_count += 1
            return self._invocation_count

    def invocation_count(self) -> int:
        with self._lock:
            return self._invocation_count


GLOBAL_R3D_PROBE_STATE = R3DProbeState()


def tool_descriptor() -> dict[str, object]:
    return deepcopy(_TOOL_DESCRIPTOR)


def r3d_health(state: R3DProbeState | None = None) -> dict[str, object]:
    probe_state = state or GLOBAL_R3D_PROBE_STATE
    return {
        "service": SERVER_NAME,
        "status": "ok",
        "surface": R3D_SURFACE,
        "tool_count": 1,
        "write_style_probe": True,
        "external_mutation": False,
        "provider_work": False,
        "provider_charge": False,
        "real_media_start": False,
        "voicebridge_binding": "not_enabled",
        "invocation_count": probe_state.invocation_count(),
    }


def _response(request_id: object, result: object) -> dict[str, object]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id: object, code: int, message: str) -> dict[str, object]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def _complete(payload: Mapping[str, object], *, cacheable: bool = False) -> dict[str, object]:
    result = dict(payload)
    result["resultType"] = "complete"
    result["_meta"] = {
        "io.modelcontextprotocol/serverInfo": {"name": SERVER_NAME, "version": R3D_SERVER_VERSION}
    }
    if cacheable:
        result["ttlMs"] = 300_000
        result["cacheScope"] = "public"
    return result


def dispatch_r3d(
    message: Mapping[str, Any],
    *,
    state: R3DProbeState | None = None,
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
                        "R3-D exposes exactly one isolated no-op write-style probe. "
                        "It performs no provider work or external mutation."
                    ),
                },
                cacheable=True,
            ),
        )
    if method == "initialize":
        params = message.get("params")
        requested = params.get("protocolVersion") if isinstance(params, Mapping) else None
        version = LEGACY_PROTOCOL_VERSION if requested != LEGACY_PROTOCOL_VERSION else requested
        return _response(
            request_id,
            {
                "protocolVersion": version,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": R3D_SERVER_VERSION},
            },
        )
    if method == "ping":
        return _response(request_id, _complete({}))
    if method == "tools/list":
        return _response(
            request_id,
            _complete({"tools": [tool_descriptor()]}, cacheable=True),
        )
    if method == "tools/call":
        params = message.get("params")
        if not isinstance(params, Mapping):
            return _error(request_id, -32602, "Invalid params")
        if params.get("name") != R3D_TOOL_NAME:
            return _error(request_id, -32602, "Unknown tool")
        arguments = params.get("arguments", {})
        if not isinstance(arguments, Mapping) or arguments:
            return _error(request_id, -32602, "R3-D probe accepts no arguments")
        probe_state = state or GLOBAL_R3D_PROBE_STATE
        count = probe_state.record_invocation()
        payload: dict[str, object] = {
            "status": "ok",
            "phase": "R3-D",
            "probe_executed": True,
            "external_mutation": False,
            "provider_work": False,
            "provider_charge": False,
            "real_media_start": False,
            "invocation_count": count,
        }
        return _response(
            request_id,
            _complete(
                {
                    "content": [
                        {"type": "text", "text": json.dumps(payload, sort_keys=True, separators=(",", ":"))}
                    ],
                    "structuredContent": payload,
                    "isError": False,
                }
            ),
        )
    return _error(request_id, -32601, "Method not found")
