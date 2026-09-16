from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANARY_DIR = ROOT / "plugins" / "krc_migration_candidate" / "mcp_canary"
SERVER = CANARY_DIR / "server.py"
MEDIA_CONTRACT = ROOT / "plugins" / "krc_migration_candidate" / "contracts" / "media_tools.yaml"
CORE = ROOT / "prompts" / "GPT_STORE_INSTRUCTIONS.md"
SKILL = ROOT / "plugins" / "krc_migration_candidate" / "skills" / "krc_core" / "SKILL.md"

# Load the repository-only protocol core directly from source instead of importing
# the candidate package. This intentionally avoids generating __pycache__ binary
# artifacts inside the directory that repository secret-scans inspect as text.
_NAMESPACE: dict[str, object] = {"__name__": "krc_mcp_canary_test_module"}
exec(compile(SERVER.read_text(encoding="utf-8"), str(SERVER), "exec"), _NAMESPACE)
CANARY_TOOL_NAME = _NAMESPACE["CANARY_TOOL_NAME"]
MCP_PROTOCOL_VERSION = _NAMESPACE["MCP_PROTOCOL_VERSION"]
canary_result = _NAMESPACE["canary_result"]
dispatch_mcp = _NAMESPACE["dispatch_mcp"]


def _request(method: str, *, params: dict | None = None, request_id: int = 1) -> dict:
    message: dict = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params is not None:
        message["params"] = params
    return message


def test_canary_tool_is_discoverable_and_explicitly_read_only() -> None:
    response = dispatch_mcp(_request("tools/list"))
    assert response is not None
    tools = response["result"]["tools"]
    assert len(tools) == 1
    tool = tools[0]
    assert tool["name"] == CANARY_TOOL_NAME
    assert tool["inputSchema"] == {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    }
    assert tool["annotations"] == {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }


def test_canary_result_is_deterministic_sanitized_and_non_mutating() -> None:
    first = dispatch_mcp(_request("tools/call", params={"name": CANARY_TOOL_NAME, "arguments": {}}))
    second = dispatch_mcp(_request("tools/call", params={"name": CANARY_TOOL_NAME, "arguments": {}}))
    assert first == second
    assert first is not None

    result = first["result"]["structuredContent"]
    assert result == {
        "service": "krc-media-mcp-canary",
        "status": "ok",
        "mutation": False,
        "provider_work": False,
        "media_operation_target_count": 13,
        "voicebridge_binding": "not_enabled",
        "execution_tools": "not_enabled",
    }
    assert first["result"]["isError"] is False
    assert json.loads(first["result"]["content"][0]["text"]) == result

    copy_one = canary_result()
    copy_one["status"] = "changed-locally"
    assert canary_result()["status"] == "ok"


def test_canary_protocol_core_supports_discovery_call_and_legacy_initialize() -> None:
    initialize = dispatch_mcp(
        _request(
            "initialize",
            params={
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1"},
            },
        )
    )
    assert initialize is not None
    assert initialize["result"]["protocolVersion"] == "2025-11-25"
    assert initialize["result"]["capabilities"] == {"tools": {}}

    fallback = dispatch_mcp(_request("initialize", params={"protocolVersion": "unsupported"}))
    assert fallback is not None
    assert fallback["result"]["protocolVersion"] == MCP_PROTOCOL_VERSION

    assert dispatch_mcp({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None


def test_canary_rejects_unknown_tools_and_arguments_fail_closed() -> None:
    unknown = dispatch_mcp(_request("tools/call", params={"name": "unknown", "arguments": {}}))
    assert unknown is not None
    assert unknown["error"]["code"] == -32602

    unexpected_args = dispatch_mcp(
        _request("tools/call", params={"name": CANARY_TOOL_NAME, "arguments": {"url": "not-allowed"}})
    )
    assert unexpected_args is not None
    assert unexpected_args["error"]["code"] == -32602


def test_canary_core_contains_no_network_or_process_execution_imports() -> None:
    tree = ast.parse(SERVER.read_text(encoding="utf-8"))
    imported_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".", 1)[0])

    assert imported_roots.isdisjoint(
        {
            "aiohttp",
            "httpx",
            "requests",
            "socket",
            "subprocess",
            "urllib",
        }
    )


def test_canary_contains_no_live_endpoint_or_secret_material() -> None:
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in CANARY_DIR.rglob("*")
        if path.is_file() and path.suffix in {".py", ".md", ".yaml", ".yml", ".json", ".toml", ".txt"}
    )
    lowered = text.lower()
    assert re.search(r"https?://", text) is None
    assert "sk-proj-" not in lowered
    assert "sk-live-" not in lowered
    assert "bearer eyj" not in lowered
    assert "prof_" not in text


def test_canary_introduces_no_deployment_packaging() -> None:
    forbidden_names = {
        "Dockerfile",
        "render.yaml",
        "render.yml",
        "mcp.json",
        ".mcp.json",
        ".app.json",
        "docker-compose.yml",
        "docker-compose.yaml",
    }
    assert not any(path.name in forbidden_names for path in CANARY_DIR.rglob("*"))


def test_existing_media_13_operation_contract_is_unchanged() -> None:
    contract = yaml.safe_load(MEDIA_CONTRACT.read_text(encoding="utf-8"))
    assert contract["operation_count"] == 13
    assert len(contract["tools"]) == 13
    assert canary_result()["media_operation_target_count"] == 13


def test_existing_core_skill_snapshot_remains_exact() -> None:
    text = SKILL.read_text(encoding="utf-8")
    begin = "<!-- BEGIN KRC CORE EXACT SNAPSHOT -->\n"
    end = "\n<!-- END KRC CORE EXACT SNAPSHOT -->"
    snapshot = text.split(begin, 1)[1].split(end, 1)[0].rstrip("\n")
    canonical = CORE.read_text(encoding="utf-8").rstrip("\n")
    assert snapshot == canonical
