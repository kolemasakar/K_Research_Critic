from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from plugins.krc_migration_candidate.mcp_canary.http_server import HttpConfig, handle_http_request
from plugins.krc_migration_candidate.mcp_canary.server import CANARY_TOOL_NAME

MODERN_META = {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientCapabilities": {},
}


def _post(message: dict, *, headers: dict[str, str] | None = None, config: HttpConfig | None = None):
    request_headers = {
        "Content-Type": "application/json",
        "MCP-Protocol-Version": "2026-07-28",
        "Mcp-Method": message["method"],
    }
    if message["method"] == "tools/call":
        request_headers["Mcp-Name"] = message["params"]["name"]
    if headers:
        request_headers.update(headers)
    return handle_http_request(
        "POST",
        "/mcp",
        request_headers,
        json.dumps(message).encode("utf-8"),
        config=config or HttpConfig(),
    )


def test_modern_discovery_and_single_tool_listing() -> None:
    discover = _post(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "server/discover",
            "params": {"_meta": MODERN_META},
        }
    )
    assert discover.status == 200
    discovered = json.loads(discover.body)["result"]
    assert discovered["supportedVersions"] == ["2026-07-28"]
    assert discovered["capabilities"] == {"tools": {}}
    assert discovered["resultType"] == "complete"
    assert discovered["cacheScope"] == "public"

    listed = _post(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {"_meta": MODERN_META},
        }
    )
    assert listed.status == 200
    tools = json.loads(listed.body)["result"]["tools"]
    assert [tool["name"] for tool in tools] == [CANARY_TOOL_NAME]
    assert tools[0]["annotations"]["readOnlyHint"] is True
    assert tools[0]["annotations"]["destructiveHint"] is False


def test_modern_canary_call_is_read_only_and_provider_free() -> None:
    response = _post(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": CANARY_TOOL_NAME,
                "arguments": {},
                "_meta": MODERN_META,
            },
        }
    )
    assert response.status == 200
    result = json.loads(response.body)["result"]["structuredContent"]
    assert result["mutation"] is False
    assert result["provider_work"] is False
    assert result["voicebridge_binding"] == "not_enabled"
    assert result["execution_tools"] == "not_enabled"


def test_modern_transport_rejects_header_body_mismatch_and_unknown_version() -> None:
    message = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {"name": CANARY_TOOL_NAME, "arguments": {}, "_meta": MODERN_META},
    }
    mismatch = _post(message, headers={"Mcp-Name": "wrong"})
    assert mismatch.status == 400
    assert json.loads(mismatch.body)["error"]["code"] == -32020

    unsupported = handle_http_request(
        "POST",
        "/mcp",
        {
            "Content-Type": "application/json",
            "MCP-Protocol-Version": "2099-01-01",
            "Mcp-Method": "tools/list",
        },
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/list",
                "params": {
                    "_meta": {
                        "io.modelcontextprotocol/protocolVersion": "2099-01-01",
                        "io.modelcontextprotocol/clientCapabilities": {},
                    }
                },
            }
        ).encode("utf-8"),
        config=HttpConfig(),
    )
    assert unsupported.status == 400
    assert json.loads(unsupported.body)["error"]["code"] == -32022


def test_origin_validation_and_optional_bearer_auth_fail_closed() -> None:
    message = {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "tools/list",
        "params": {"_meta": MODERN_META},
    }
    forbidden = _post(message, headers={"Origin": "https://unexpected.invalid"})
    assert forbidden.status == 403

    allowed = _post(
        message,
        headers={"Origin": "https://allowed.invalid"},
        config=HttpConfig(allowed_origins=frozenset({"https://allowed.invalid"})),
    )
    assert allowed.status == 200

    unauthorized = _post(message, config=HttpConfig(auth_mode="bearer", bearer_token="test-only-token"))
    assert unauthorized.status == 401
    authorized = _post(
        message,
        headers={"Authorization": "Bearer test-only-token"},
        config=HttpConfig(auth_mode="bearer", bearer_token="test-only-token"),
    )
    assert authorized.status == 200


def test_health_is_read_only_and_mcp_get_is_disabled_for_stateless_canary() -> None:
    health = handle_http_request("GET", "/healthz", {}, config=HttpConfig())
    assert health.status == 200
    payload = json.loads(health.body)
    assert payload == {
        "mutation": False,
        "provider_work": False,
        "service": "krc-media-mcp-canary",
        "status": "ok",
    }

    mcp_get = handle_http_request("GET", "/mcp", {}, config=HttpConfig())
    assert mcp_get.status == 405


def test_legacy_initialize_fallback_is_bounded_to_2025_11_25() -> None:
    legacy = handle_http_request(
        "POST",
        "/mcp",
        {"Content-Type": "application/json"},
        json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 7,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-11-25",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "1"},
                },
            }
        ).encode("utf-8"),
        config=HttpConfig(),
    )
    assert legacy.status == 200
    assert json.loads(legacy.body)["result"]["protocolVersion"] == "2025-11-25"
