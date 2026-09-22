from __future__ import annotations

import base64
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True

from plugins.krc_migration_candidate.mcp_canary.oauth import (
    LEGACY_CHATGPT_CLIENT_ID,
    LEGACY_CHATGPT_REDIRECT_URI,
    READ_SCOPE,
    RestartSafeOAuthState,
    oauth_state_from_env,
)

CALLBACK = "https://chatgpt.example.test/oauth/callback"
KEY = "restart-safe-oauth-signing-key-0123456789abcdef"


def _challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def test_restart_safe_oauth_preserves_established_client_tokens_across_restart() -> None:
    verifier = "restart-safe-pkce-verifier-abcdefghijklmnopqrstuvwxyz"
    first_process = RestartSafeOAuthState(KEY)
    client_id = first_process.register_client([CALLBACK])
    code = first_process.issue_code(
        client_id=client_id,
        redirect_uri=CALLBACK,
        code_challenge=_challenge(verifier),
        scope=READ_SCOPE,
    )
    issued = first_process.exchange_code(
        code=code,
        client_id=client_id,
        redirect_uri=CALLBACK,
        code_verifier=verifier,
    )
    assert issued is not None
    access_token, refresh_token, expires_in, scope = issued
    assert expires_in > 0
    assert scope == READ_SCOPE

    after_restart = RestartSafeOAuthState(KEY)
    assert after_restart.client_redirect_allowed(client_id, CALLBACK) is True
    assert after_restart.access_allowed(access_token, READ_SCOPE) is True

    refreshed = after_restart.refresh(
        refresh_token=refresh_token,
        client_id=client_id,
    )
    assert refreshed is not None
    rotated_access, returned_refresh, _, rotated_scope = refreshed
    assert rotated_scope == READ_SCOPE
    assert returned_refresh == refresh_token

    next_restart = RestartSafeOAuthState(KEY)
    assert next_restart.access_allowed(rotated_access, READ_SCOPE) is True
    assert next_restart.refresh(
        refresh_token=refresh_token,
        client_id=client_id,
    ) is not None


def test_authorization_code_is_single_use_and_does_not_survive_restart() -> None:
    verifier = "restart-safe-pkce-verifier-abcdefghijklmnopqrstuvwxyz"
    state = RestartSafeOAuthState(KEY)
    client_id = state.register_client([CALLBACK])
    code = state.issue_code(
        client_id=client_id,
        redirect_uri=CALLBACK,
        code_challenge=_challenge(verifier),
        scope=READ_SCOPE,
    )
    first = state.exchange_code(
        code=code,
        client_id=client_id,
        redirect_uri=CALLBACK,
        code_verifier=verifier,
    )
    second = state.exchange_code(
        code=code,
        client_id=client_id,
        redirect_uri=CALLBACK,
        code_verifier=verifier,
    )
    assert first is not None
    assert second is None

    pending = state.issue_code(
        client_id=client_id,
        redirect_uri=CALLBACK,
        code_challenge=_challenge(verifier),
        scope=READ_SCOPE,
    )
    restarted = RestartSafeOAuthState(KEY)
    assert restarted.client_redirect_allowed(client_id, CALLBACK) is True
    assert restarted.exchange_code(
        code=pending,
        client_id=client_id,
        redirect_uri=CALLBACK,
        code_verifier=verifier,
    ) is None


def test_restart_safe_oauth_wrong_signing_key_and_tamper_fail_closed() -> None:
    original = RestartSafeOAuthState(KEY)
    client_id = original.register_client([CALLBACK])
    access_token, refresh_token, _, _ = original._issue_tokens(
        client_id=client_id,
        scope=READ_SCOPE,
    )

    other = RestartSafeOAuthState("different-restart-safe-key-abcdefghijklmnopqrstuvwxyz")
    assert other.client_redirect_allowed(client_id, CALLBACK) is False
    assert other.access_allowed(access_token, READ_SCOPE) is False
    assert other.refresh(refresh_token=refresh_token, client_id=client_id) is None

    tampered_access = access_token[:-1] + ("A" if access_token[-1] != "A" else "B")
    assert original.access_allowed(tampered_access, READ_SCOPE) is False


def test_restart_safe_oauth_allows_only_exact_legacy_chatgpt_pair() -> None:
    state = RestartSafeOAuthState(KEY)
    assert state.client_redirect_allowed(LEGACY_CHATGPT_CLIENT_ID, LEGACY_CHATGPT_REDIRECT_URI) is True
    assert state.client_redirect_allowed(LEGACY_CHATGPT_CLIENT_ID, CALLBACK) is False
    assert state.client_redirect_allowed("wrong-client", LEGACY_CHATGPT_REDIRECT_URI) is False


def test_legacy_chatgpt_pair_upgrades_into_restart_safe_tokens() -> None:
    verifier = "legacy-chatgpt-pkce-verifier-abcdefghijklmnopqrstuvwxyz"
    first_process = RestartSafeOAuthState(KEY)
    code = first_process.issue_code(
        client_id=LEGACY_CHATGPT_CLIENT_ID,
        redirect_uri=LEGACY_CHATGPT_REDIRECT_URI,
        code_challenge=_challenge(verifier),
        scope=READ_SCOPE,
    )
    issued = first_process.exchange_code(
        code=code,
        client_id=LEGACY_CHATGPT_CLIENT_ID,
        redirect_uri=LEGACY_CHATGPT_REDIRECT_URI,
        code_verifier=verifier,
    )
    assert issued is not None
    access_token, refresh_token, _, scope = issued
    assert scope == READ_SCOPE

    after_restart = RestartSafeOAuthState(KEY)
    assert after_restart.access_allowed(access_token, READ_SCOPE) is True
    assert after_restart.refresh(
        refresh_token=refresh_token,
        client_id=LEGACY_CHATGPT_CLIENT_ID,
    ) is not None


def test_restart_safe_oauth_factory_is_opt_in_and_validates_key(monkeypatch) -> None:
    monkeypatch.delenv("KRC_MCP_OAUTH_SIGNING_KEY", raising=False)
    assert type(oauth_state_from_env()).__name__ == "OAuthState"

    monkeypatch.setenv("KRC_MCP_OAUTH_SIGNING_KEY", KEY)
    assert isinstance(oauth_state_from_env(), RestartSafeOAuthState)

    monkeypatch.setenv("KRC_MCP_OAUTH_SIGNING_KEY", "short")
    try:
        oauth_state_from_env()
    except ValueError as exc:
        assert str(exc) == "oauth_signing_key_too_short"
    else:
        raise AssertionError("short OAuth signing key must fail closed")


def test_restart_safe_oauth_expired_tokens_fail_closed() -> None:
    state = RestartSafeOAuthState(KEY)
    client_id = state.register_client([CALLBACK])
    expired_access = state._encode(
        "access",
        {
            "client_id": client_id,
            "scope": READ_SCOPE,
            "exp": 0,
            "nonce": "expired-access",
        },
    )
    expired_refresh = state._encode(
        "refresh",
        {
            "client_id": client_id,
            "scope": READ_SCOPE,
            "exp": 0,
            "nonce": "expired-refresh",
        },
    )
    assert state.access_allowed(expired_access, READ_SCOPE) is False
    assert state.refresh(refresh_token=expired_refresh, client_id=client_id) is None
