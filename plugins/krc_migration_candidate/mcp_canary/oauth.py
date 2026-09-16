from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import threading
import time
from dataclasses import dataclass
from typing import Mapping
from urllib.parse import parse_qs, urlencode, urlsplit

READ_SCOPE = "krc.mcp.read"
OFFLINE_SCOPE = "offline_access"
SUPPORTED_SCOPES = frozenset({READ_SCOPE, OFFLINE_SCOPE})
AUTH_CODE_TTL_SECONDS = 300
ACCESS_TOKEN_TTL_SECONDS = 3600
REFRESH_TOKEN_TTL_SECONDS = 30 * 24 * 3600


@dataclass(frozen=True)
class OAuthResponse:
    status: int
    headers: Mapping[str, str]
    body: bytes = b""


@dataclass
class AuthorizationCode:
    client_id: str
    redirect_uri: str
    code_challenge: str
    scope: str
    expires_at: float


@dataclass
class TokenRecord:
    client_id: str
    scope: str
    expires_at: float


class OAuthState:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._clients: dict[str, set[str]] = {}
        self._codes: dict[str, AuthorizationCode] = {}
        self._access_tokens: dict[str, TokenRecord] = {}
        self._refresh_tokens: dict[str, TokenRecord] = {}

    @staticmethod
    def _now() -> float:
        return time.time()

    def register_client(self, redirect_uris: list[str]) -> str:
        normalized = {uri for uri in redirect_uris if _valid_redirect_uri(uri)}
        if not normalized or len(normalized) != len(redirect_uris):
            raise ValueError("invalid_redirect_uri")
        client_id = secrets.token_urlsafe(24)
        with self._lock:
            self._clients[client_id] = normalized
        return client_id

    def client_redirect_allowed(self, client_id: str, redirect_uri: str) -> bool:
        with self._lock:
            return redirect_uri in self._clients.get(client_id, set())

    def issue_code(self, *, client_id: str, redirect_uri: str, code_challenge: str, scope: str) -> str:
        code = secrets.token_urlsafe(32)
        with self._lock:
            self._codes[code] = AuthorizationCode(
                client_id=client_id,
                redirect_uri=redirect_uri,
                code_challenge=code_challenge,
                scope=scope,
                expires_at=self._now() + AUTH_CODE_TTL_SECONDS,
            )
        return code

    def exchange_code(
        self,
        *,
        code: str,
        client_id: str,
        redirect_uri: str,
        code_verifier: str,
    ) -> tuple[str, str, int, str] | None:
        with self._lock:
            record = self._codes.pop(code, None)
        if record is None or record.expires_at < self._now():
            return None
        if record.client_id != client_id or record.redirect_uri != redirect_uri:
            return None
        digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
        expected = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
        if not hmac.compare_digest(expected, record.code_challenge):
            return None
        return self._issue_tokens(client_id=client_id, scope=record.scope)

    def refresh(self, *, refresh_token: str, client_id: str) -> tuple[str, str, int, str] | None:
        with self._lock:
            record = self._refresh_tokens.pop(refresh_token, None)
        if record is None or record.expires_at < self._now() or record.client_id != client_id:
            return None
        return self._issue_tokens(client_id=client_id, scope=record.scope)

    def _issue_tokens(self, *, client_id: str, scope: str) -> tuple[str, str, int, str]:
        access_token = secrets.token_urlsafe(36)
        refresh_token = secrets.token_urlsafe(42)
        now = self._now()
        with self._lock:
            self._access_tokens[access_token] = TokenRecord(
                client_id=client_id,
                scope=scope,
                expires_at=now + ACCESS_TOKEN_TTL_SECONDS,
            )
            self._refresh_tokens[refresh_token] = TokenRecord(
                client_id=client_id,
                scope=scope,
                expires_at=now + REFRESH_TOKEN_TTL_SECONDS,
            )
        return access_token, refresh_token, ACCESS_TOKEN_TTL_SECONDS, scope

    def access_allowed(self, token: str, required_scope: str = READ_SCOPE) -> bool:
        with self._lock:
            record = self._access_tokens.get(token)
        if record is None or record.expires_at < self._now():
            return False
        return required_scope in set(record.scope.split())


GLOBAL_OAUTH_STATE = OAuthState()


def _valid_redirect_uri(uri: str) -> bool:
    parsed = urlsplit(uri)
    if parsed.scheme == "https" and bool(parsed.netloc):
        return True
    return parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"}


def _json_response(status: int, payload: Mapping[str, object]) -> OAuthResponse:
    return OAuthResponse(
        status=status,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Cache-Control": "no-store",
            "Pragma": "no-cache",
            "X-Content-Type-Options": "nosniff",
        },
        body=json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"),
    )


def _html_response(status: int, html: str) -> OAuthResponse:
    return OAuthResponse(
        status=status,
        headers={
            "Content-Type": "text/html; charset=utf-8",
            "Cache-Control": "no-store",
            "Pragma": "no-cache",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'",
            "Referrer-Policy": "no-referrer",
        },
        body=html.encode("utf-8"),
    )


def authorization_server_metadata(base_url: str) -> dict[str, object]:
    return {
        "issuer": base_url,
        "authorization_endpoint": f"{base_url}/oauth/authorize",
        "token_endpoint": f"{base_url}/oauth/token",
        "registration_endpoint": f"{base_url}/oauth/register",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code", "refresh_token"],
        "code_challenge_methods_supported": ["S256"],
        "token_endpoint_auth_methods_supported": ["none"],
        "scopes_supported": [READ_SCOPE, OFFLINE_SCOPE],
    }


def protected_resource_metadata(base_url: str) -> dict[str, object]:
    return {
        "resource": f"{base_url}/mcp",
        "authorization_servers": [base_url],
        "bearer_methods_supported": ["header"],
        "scopes_supported": [READ_SCOPE],
    }


def handle_oauth_request(
    method: str,
    path: str,
    headers: Mapping[str, str],
    body: bytes,
    *,
    base_url: str,
    owner_code: str | None,
    state: OAuthState | None = None,
) -> OAuthResponse | None:
    state = state or GLOBAL_OAUTH_STATE
    parsed = urlsplit(path)
    clean_path = parsed.path

    if clean_path in {"/.well-known/oauth-protected-resource", "/.well-known/oauth-protected-resource/mcp"} and method == "GET":
        return _json_response(200, protected_resource_metadata(base_url))
    if clean_path == "/.well-known/oauth-authorization-server" and method == "GET":
        return _json_response(200, authorization_server_metadata(base_url))

    if clean_path == "/oauth/register" and method == "POST":
        try:
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return _json_response(400, {"error": "invalid_client_metadata"})
        redirect_uris = payload.get("redirect_uris") if isinstance(payload, dict) else None
        if not isinstance(redirect_uris, list) or not all(isinstance(uri, str) for uri in redirect_uris):
            return _json_response(400, {"error": "invalid_client_metadata"})
        try:
            client_id = state.register_client(redirect_uris)
        except ValueError:
            return _json_response(400, {"error": "invalid_redirect_uri"})
        return _json_response(
            201,
            {
                "client_id": client_id,
                "client_id_issued_at": int(time.time()),
                "redirect_uris": redirect_uris,
                "token_endpoint_auth_method": "none",
                "grant_types": ["authorization_code", "refresh_token"],
                "response_types": ["code"],
            },
        )

    if clean_path == "/oauth/authorize" and method == "GET":
        query = parse_qs(parsed.query, keep_blank_values=True)
        error = _validate_authorize_query(query, state)
        if error:
            return _html_response(400, "<!doctype html><title>Authorization error</title><p>Invalid authorization request.</p>")
        hidden = "".join(
            f'<input type="hidden" name="{_escape(name)}" value="{_escape(values[0])}">'
            for name, values in query.items()
            if values
        )
        configured = owner_code is not None and bool(owner_code)
        disabled = "" if configured else " disabled"
        status = "Enter the owner authorization code." if configured else "Owner authorization is not configured yet."
        return _html_response(
            200,
            "<!doctype html><html><head><title>KRC MCP authorization</title>"
            "<style>body{font-family:system-ui;max-width:36rem;margin:3rem auto;padding:1rem}input,button{font:inherit;padding:.7rem;width:100%;box-sizing:border-box;margin:.4rem 0}</style>"
            f"</head><body><h1>KRC MCP R3-B</h1><p>{status}</p><form method=post action=/oauth/authorize>{hidden}"
            f'<input type="password" name="owner_code" autocomplete="one-time-code" required{disabled}>'
            f'<button type="submit"{disabled}>Authorize</button></form></body></html>',
        )

    if clean_path == "/oauth/authorize" and method == "POST":
        form = parse_qs(body.decode("utf-8", errors="replace"), keep_blank_values=True)
        query = {key: values for key, values in form.items() if key != "owner_code"}
        if _validate_authorize_query(query, state):
            return _html_response(400, "<!doctype html><title>Authorization error</title><p>Invalid authorization request.</p>")
        supplied = form.get("owner_code", [""])[0]
        if not owner_code:
            return _html_response(503, "<!doctype html><title>Unavailable</title><p>Owner authorization is not configured.</p>")
        if not hmac.compare_digest(supplied, owner_code):
            return _html_response(403, "<!doctype html><title>Forbidden</title><p>Authorization denied.</p>")
        client_id = query["client_id"][0]
        redirect_uri = query["redirect_uri"][0]
        code_challenge = query["code_challenge"][0]
        scope = _normalize_scope(query.get("scope", [READ_SCOPE])[0])
        code = state.issue_code(
            client_id=client_id,
            redirect_uri=redirect_uri,
            code_challenge=code_challenge,
            scope=scope,
        )
        params = {"code": code}
        state_value = query.get("state", [""])[0]
        if state_value:
            params["state"] = state_value
        separator = "&" if "?" in redirect_uri else "?"
        return OAuthResponse(status=302, headers={"Location": f"{redirect_uri}{separator}{urlencode(params)}", "Cache-Control": "no-store"})

    if clean_path == "/oauth/token" and method == "POST":
        form = parse_qs(body.decode("utf-8", errors="replace"), keep_blank_values=True)
        grant_type = form.get("grant_type", [""])[0]
        client_id = form.get("client_id", [""])[0]
        if grant_type == "authorization_code":
            result = state.exchange_code(
                code=form.get("code", [""])[0],
                client_id=client_id,
                redirect_uri=form.get("redirect_uri", [""])[0],
                code_verifier=form.get("code_verifier", [""])[0],
            )
        elif grant_type == "refresh_token":
            result = state.refresh(refresh_token=form.get("refresh_token", [""])[0], client_id=client_id)
        else:
            return _json_response(400, {"error": "unsupported_grant_type"})
        if result is None:
            return _json_response(400, {"error": "invalid_grant"})
        access_token, refresh_token, expires_in, scope = result
        return _json_response(
            200,
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "expires_in": expires_in,
                "scope": scope,
            },
        )

    return None


def _validate_authorize_query(query: Mapping[str, list[str]], state: OAuthState) -> str | None:
    def one(name: str) -> str:
        values = query.get(name, [])
        return values[0] if len(values) == 1 else ""

    if one("response_type") != "code":
        return "unsupported_response_type"
    client_id = one("client_id")
    redirect_uri = one("redirect_uri")
    if not client_id or not redirect_uri or not state.client_redirect_allowed(client_id, redirect_uri):
        return "invalid_client"
    if one("code_challenge_method") != "S256" or not one("code_challenge"):
        return "invalid_request"
    try:
        _normalize_scope(one("scope") or READ_SCOPE)
    except ValueError:
        return "invalid_scope"
    return None


def _normalize_scope(scope: str) -> str:
    requested = set(scope.split()) if scope.strip() else {READ_SCOPE}
    if READ_SCOPE not in requested or not requested <= SUPPORTED_SCOPES:
        raise ValueError("invalid_scope")
    return " ".join(sorted(requested))


def _escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )
