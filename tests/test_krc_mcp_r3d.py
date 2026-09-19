from __future__ import annotations

import base64
import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from plugins.krc_migration_candidate.mcp_canary.http_server import HttpConfig
from plugins.krc_migration_candidate.mcp_canary.oauth import OAuthState, READ_SCOPE
from plugins.krc_migration_candidate.mcp_canary.r3d import (
    R3D_SURFACE,
    R3D_TOOL_NAME,
    R3DProbeState,
    dispatch_r3d,
    r3d_health,
    tool_descriptor,
)
from plugins.krc_migration_candidate.mcp_canary.r3d_http_server import handle_r3d_http_request

BASE_URL = "https://r3d.example.test"
CALLBACK = "https://chatgpt.example.test/oauth/callback"
OWNER_CODE = "unit-test-owner-code-only"
MODERN_META = {
    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
    "io.modelcontextprotocol/clientCapabilities": {},
}


def _config() -> HttpConfig:
    return HttpConfig(
        auth_mode="oauth",
        public_base_url=BASE_URL,
        owner_code=OWNER_CODE,
        surface=R3D_SURFACE,
    )


def _pkce(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def _access_token(state: OAuthState) -> str:
    registration = handle_r3d_http_request(
        "POST",
        "/oauth/register",
        {"Content-Type": "application/json"},
        json.dumps({"redirect_uris": [CALLBACK]}).encode(),
        config=_config(),
        oauth_state=state,
    )
    assert registration.status == 201
    client_id = json.loads(registration.body)["client_id"]
    verifier = "r" * 64
    challenge = _pkce(verifier)
    query = (
        "response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={CALLBACK}"
        f"&code_challenge={challenge}"
        "&code_challenge_method=S256"
        f"&scope={READ_SCOPE}"
        "&state=r3d-test"
    )
    granted = handle_r3d_http_request(
        "POST",
        "/oauth/authorize",
        {"Content-Type": "application/x-www-form-urlencoded"},
        f"{query}&owner_code={OWNER_CODE}".encode(),
        config=_config(),
        oauth_state=state,
    )
    assert granted.status == 302
    code = parse_qs(urlsplit(granted.headers["Location"]).query)["code"][0]
    token = handle_r3d_http_request(
        "POST",
        "/oauth/token",
        {"Content-Type": "application/x-www-form-urlencoded"},
        (
            "grant_type=authorization_code"
            f"&code={code}"
            f"&client_id={client_id}"
            f"&redirect_uri={CALLBACK}"
            f"&code_verifier={verifier}"
        ).encode(),
        config=_config(),
        oauth_state=state,
    )
    assert token.status == 200
    return json.loads(token.body)["access_token"]


def _modern_post(message: dict, token: str, state: OAuthState):
    headers = {
        "Content-Type": "application/json",
        "MCP-Protocol-Version": "2026-07-28",
        "Mcp-Method": message["method"],
        "Authorization": f"Bearer {token}",
    }
    if message["method"] == "tools/call":
        headers["Mcp-Name"] = message["params"]["name"]
    return handle_r3d_http_request(
        "POST",
        "/mcp",
        headers,
        json.dumps(message).encode(),
        config=_config(),
        oauth_state=state,
    )


def test_r3d_descriptor_is_write_style_but_non_destructive() -> None:
    descriptor = tool_descriptor()
    assert descriptor["name"] == R3D_TOOL_NAME
    annotations = descriptor["annotations"]
    assert annotations["readOnlyHint"] is False
    assert annotations["destructiveHint"] is False
    assert annotations["idempotentHint"] is True
    assert annotations["openWorldHint"] is False
    text = descriptor["description"]
    assert "no VoiceBridge call" in text
    assert "provider work" in text
    assert "external mutation" in text


def test_r3d_core_call_only_mutates_ephemeral_counter() -> None:
    state = R3DProbeState()
    assert r3d_health(state)["invocation_count"] == 0
    response = dispatch_r3d(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": R3D_TOOL_NAME, "arguments": {}},
        },
        state=state,
    )
    assert response is not None
    payload = response["result"]["structuredContent"]
    assert payload == {
        "status": "ok",
        "phase": "R3-D",
        "probe_executed": True,
        "external_mutation": False,
        "provider_work": False,
        "provider_charge": False,
        "real_media_start": False,
        "invocation_count": 1,
    }
    assert r3d_health(state)["invocation_count"] == 1


def test_r3d_health_declares_zero_external_side_effects() -> None:
    health = r3d_health(R3DProbeState())
    assert health["surface"] == R3D_SURFACE
    assert health["tool_count"] == 1
    assert health["write_style_probe"] is True
    assert health["external_mutation"] is False
    assert health["provider_work"] is False
    assert health["provider_charge"] is False
    assert health["real_media_start"] is False
    assert health["voicebridge_binding"] == "not_enabled"


def test_r3d_http_requires_oauth_and_never_requires_voicebridge() -> None:
    wrong_auth = HttpConfig(auth_mode="none", surface=R3D_SURFACE)
    response = handle_r3d_http_request(
        "POST",
        "/mcp",
        {"Content-Type": "application/json"},
        b"{}",
        config=wrong_auth,
    )
    assert response.status == 503
    assert json.loads(response.body)["status"] == "r3d_requires_oauth"

    health = handle_r3d_http_request("GET", "/healthz", {}, config=wrong_auth)
    assert health.status == 200
    payload = json.loads(health.body)
    assert payload["voicebridge_binding"] == "not_enabled"
    assert payload["provider_work"] is False


def test_r3d_oauth_discovery_exposes_exactly_one_write_style_probe() -> None:
    state = OAuthState()
    token = _access_token(state)
    listed = _modern_post(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {"_meta": MODERN_META},
        },
        token,
        state,
    )
    assert listed.status == 200
    tools = json.loads(listed.body)["result"]["tools"]
    assert [tool["name"] for tool in tools] == [R3D_TOOL_NAME]
    assert tools[0]["annotations"]["readOnlyHint"] is False


def test_r3d_oauth_tool_call_returns_noop_evidence() -> None:
    state = OAuthState()
    token = _access_token(state)
    called = _modern_post(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": R3D_TOOL_NAME,
                "arguments": {},
                "_meta": MODERN_META,
            },
        },
        token,
        state,
    )
    assert called.status == 200
    result = json.loads(called.body)["result"]["structuredContent"]
    assert result["probe_executed"] is True
    assert result["external_mutation"] is False
    assert result["provider_work"] is False
    assert result["provider_charge"] is False
    assert result["real_media_start"] is False
