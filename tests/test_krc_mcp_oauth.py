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

from plugins.krc_migration_candidate.mcp_canary.http_server import HttpConfig, handle_http_request
from plugins.krc_migration_candidate.mcp_canary.oauth import OAuthState, READ_SCOPE

BASE_URL = "https://auth-canary.example.test"
CALLBACK = "https://chatgpt.example.test/oauth/callback"
OWNER_CODE = "unit-test-owner-code-only"


def _config(owner_code: str | None = OWNER_CODE) -> HttpConfig:
    return HttpConfig(auth_mode="oauth", public_base_url=BASE_URL, owner_code=owner_code)


def _pkce(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def _register(state: OAuthState) -> str:
    response = handle_http_request(
        "POST",
        "/oauth/register",
        {"Content-Type": "application/json"},
        json.dumps({"redirect_uris": [CALLBACK]}).encode(),
        config=_config(),
        oauth_state=state,
    )
    assert response.status == 201
    return json.loads(response.body)["client_id"]


def _authorize_and_exchange(state: OAuthState) -> tuple[str, str, str]:
    client_id = _register(state)
    verifier = "a" * 64
    challenge = _pkce(verifier)
    query = (
        "response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={CALLBACK}"
        f"&code_challenge={challenge}"
        "&code_challenge_method=S256"
        f"&scope={READ_SCOPE}%20offline_access"
        "&state=opaque-test-state"
    )
    page = handle_http_request(
        "GET",
        f"/oauth/authorize?{query}",
        {},
        config=_config(),
        oauth_state=state,
    )
    assert page.status == 200
    assert OWNER_CODE.encode() not in page.body

    body = f"{query}&owner_code={OWNER_CODE}".encode()
    granted = handle_http_request(
        "POST",
        "/oauth/authorize",
        {"Content-Type": "application/x-www-form-urlencoded"},
        body,
        config=_config(),
        oauth_state=state,
    )
    assert granted.status == 302
    redirect = granted.headers["Location"]
    parsed = urlsplit(redirect)
    values = parse_qs(parsed.query)
    assert values["state"] == ["opaque-test-state"]
    code = values["code"][0]

    token = handle_http_request(
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
    payload = json.loads(token.body)
    assert payload["token_type"] == "Bearer"
    assert payload["expires_in"] > 0
    assert READ_SCOPE in payload["scope"].split()
    return client_id, payload["access_token"], payload["refresh_token"]


def test_oauth_metadata_is_discoverable_and_scoped() -> None:
    state = OAuthState()
    resource = handle_http_request(
        "GET",
        "/.well-known/oauth-protected-resource",
        {},
        config=_config(),
        oauth_state=state,
    )
    assert resource.status == 200
    resource_body = json.loads(resource.body)
    assert resource_body["resource"] == f"{BASE_URL}/mcp"
    assert resource_body["authorization_servers"] == [BASE_URL]
    assert resource_body["scopes_supported"] == [READ_SCOPE]

    metadata = handle_http_request(
        "GET",
        "/.well-known/oauth-authorization-server",
        {},
        config=_config(),
        oauth_state=state,
    )
    assert metadata.status == 200
    body = json.loads(metadata.body)
    assert body["issuer"] == BASE_URL
    assert body["authorization_endpoint"] == f"{BASE_URL}/oauth/authorize"
    assert body["token_endpoint"] == f"{BASE_URL}/oauth/token"
    assert body["registration_endpoint"] == f"{BASE_URL}/oauth/register"
    assert body["code_challenge_methods_supported"] == ["S256"]
    assert body["token_endpoint_auth_methods_supported"] == ["none"]


def test_oauth_mcp_fails_closed_before_authorization() -> None:
    response = handle_http_request(
        "POST",
        "/mcp",
        {"Content-Type": "application/json"},
        b"{}",
        config=_config(),
        oauth_state=OAuthState(),
    )
    assert response.status == 401
    challenge = response.headers["WWW-Authenticate"]
    assert "resource_metadata=" in challenge
    assert READ_SCOPE in challenge
    assert OWNER_CODE.encode() not in response.body


def test_oauth_pkce_flow_authorizes_only_after_owner_code() -> None:
    state = OAuthState()
    client_id, access_token, _ = _authorize_and_exchange(state)
    assert client_id
    assert state.access_allowed(access_token, READ_SCOPE) is True

    bad = handle_http_request(
        "POST",
        "/oauth/token",
        {"Content-Type": "application/x-www-form-urlencoded"},
        b"grant_type=authorization_code&code=missing&client_id=missing&redirect_uri=https%3A%2F%2Fexample.test&code_verifier=x",
        config=_config(),
        oauth_state=state,
    )
    assert bad.status == 400
    assert json.loads(bad.body)["error"] == "invalid_grant"


def test_oauth_access_token_unlocks_mcp_but_owner_code_never_does() -> None:
    state = OAuthState()
    _, access_token, _ = _authorize_and_exchange(state)
    modern = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {
            "_meta": {
                "io.modelcontextprotocol/protocolVersion": "2026-07-28",
                "io.modelcontextprotocol/clientCapabilities": {},
            }
        },
    }
    headers = {
        "Content-Type": "application/json",
        "MCP-Protocol-Version": "2026-07-28",
        "Mcp-Method": "tools/list",
        "Authorization": f"Bearer {access_token}",
    }
    allowed = handle_http_request(
        "POST",
        "/mcp",
        headers,
        json.dumps(modern).encode(),
        config=_config(),
        oauth_state=state,
    )
    assert allowed.status == 200
    tools = json.loads(allowed.body)["result"]["tools"]
    assert len(tools) == 1
    assert tools[0]["name"] == "krc_media_capabilities_canary"

    wrong_boundary = dict(headers)
    wrong_boundary["Authorization"] = f"Bearer {OWNER_CODE}"
    denied = handle_http_request(
        "POST",
        "/mcp",
        wrong_boundary,
        json.dumps(modern).encode(),
        config=_config(),
        oauth_state=state,
    )
    assert denied.status == 401


def test_oauth_refresh_token_rotates_and_preserves_read_scope() -> None:
    state = OAuthState()
    client_id, first_access, refresh_token = _authorize_and_exchange(state)
    response = handle_http_request(
        "POST",
        "/oauth/token",
        {"Content-Type": "application/x-www-form-urlencoded"},
        f"grant_type=refresh_token&refresh_token={refresh_token}&client_id={client_id}".encode(),
        config=_config(),
        oauth_state=state,
    )
    assert response.status == 200
    payload = json.loads(response.body)
    assert payload["access_token"] != first_access
    assert payload["refresh_token"] != refresh_token
    assert state.access_allowed(payload["access_token"], READ_SCOPE) is True

    replay = handle_http_request(
        "POST",
        "/oauth/token",
        {"Content-Type": "application/x-www-form-urlencoded"},
        f"grant_type=refresh_token&refresh_token={refresh_token}&client_id={client_id}".encode(),
        config=_config(),
        oauth_state=state,
    )
    assert replay.status == 400
    assert json.loads(replay.body)["error"] == "invalid_grant"


def test_oauth_owner_code_is_fail_closed_and_never_returned() -> None:
    state = OAuthState()
    client_id = _register(state)
    verifier = "b" * 64
    challenge = _pkce(verifier)
    query = (
        "response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={CALLBACK}"
        f"&code_challenge={challenge}"
        "&code_challenge_method=S256"
        f"&scope={READ_SCOPE}"
    )
    unconfigured = handle_http_request(
        "POST",
        "/oauth/authorize",
        {"Content-Type": "application/x-www-form-urlencoded"},
        f"{query}&owner_code=anything".encode(),
        config=_config(owner_code=None),
        oauth_state=state,
    )
    assert unconfigured.status == 503
    assert b"anything" not in unconfigured.body

    wrong = handle_http_request(
        "POST",
        "/oauth/authorize",
        {"Content-Type": "application/x-www-form-urlencoded"},
        f"{query}&owner_code=wrong-value".encode(),
        config=_config(),
        oauth_state=state,
    )
    assert wrong.status == 403
    assert b"wrong-value" not in wrong.body
    assert OWNER_CODE.encode() not in wrong.body


def test_oauth_dynamic_registration_rejects_unsafe_redirects() -> None:
    state = OAuthState()
    for uri in ["http://evil.example/callback", "javascript:alert(1)", "not-a-url"]:
        response = handle_http_request(
            "POST",
            "/oauth/register",
            {"Content-Type": "application/json"},
            json.dumps({"redirect_uris": [uri]}).encode(),
            config=_config(),
            oauth_state=state,
        )
        assert response.status == 400
        assert json.loads(response.body)["error"] == "invalid_redirect_uri"
