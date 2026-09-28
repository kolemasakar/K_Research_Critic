from __future__ import annotations

import base64
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from plugins.krc_migration_candidate.mcp_canary.http_server import HttpConfig, handle_http_request
from plugins.krc_migration_candidate.mcp_canary.oauth import OAuthState, READ_SCOPE

BASE_URL = "https://auth-canary.example.test"
CALLBACK = "https://chatgpt.com/connector/oauth/test"
OWNER_CODE = "unit-test-owner-code-only"


def _config() -> HttpConfig:
    return HttpConfig(auth_mode="oauth", public_base_url=BASE_URL, owner_code=OWNER_CODE)


def _register(state: OAuthState, redirect_uri: str = CALLBACK) -> str:
    response = handle_http_request(
        "POST",
        "/oauth/register",
        {"Content-Type": "application/json"},
        json.dumps({"redirect_uris": [redirect_uri]}).encode(),
        config=_config(),
        oauth_state=state,
    )
    assert response.status == 201
    return json.loads(response.body)["client_id"]


def _authorize_path(client_id: str, redirect_uri: str = CALLBACK) -> str:
    verifier = "c" * 64
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return (
        "/oauth/authorize?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&code_challenge={challenge}"
        "&code_challenge_method=S256"
        f"&scope={READ_SCOPE}"
        "&state=csp-test"
    )


def test_authorization_page_csp_allows_only_registered_callback_origin() -> None:
    state = OAuthState()
    client_id = _register(state)
    response = handle_http_request(
        "GET",
        _authorize_path(client_id),
        {},
        config=_config(),
        oauth_state=state,
    )
    assert response.status == 200
    csp = response.headers["Content-Security-Policy"]
    assert "form-action 'self' https://chatgpt.com" in csp
    assert "/connector/oauth/test" not in csp
    assert "frame-ancestors 'none'" in csp


def test_unregistered_callback_is_rejected_and_not_added_to_csp() -> None:
    state = OAuthState()
    client_id = _register(state)
    response = handle_http_request(
        "GET",
        _authorize_path(client_id, "https://evil.example/callback"),
        {},
        config=_config(),
        oauth_state=state,
    )
    assert response.status == 400
    csp = response.headers["Content-Security-Policy"]
    assert "evil.example" not in csp
    assert "form-action 'self'" in csp
