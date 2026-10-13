"""Feature-gated, one-shot external cold wake. No media/provider calls.

The relay implementation is deployed separately and MUST hardcode the fixed
VoiceBridge /api/v1/health destination. This client never accepts a target URL
from a user/tool payload, and never follows redirects with bearer credentials.
"""
from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None

def _configured() -> tuple[str, str] | None:
    if os.environ.get("KRC_WAKE_RELAY_ENABLED") != "1":
        return None
    url = os.environ.get("KRC_WAKE_RELAY_URL", "")
    token = os.environ.get("KRC_WAKE_RELAY_TOKEN", "")
    pinned_host = os.environ.get("KRC_WAKE_RELAY_HOST", "")
    try:
        part = urlsplit(url)
    except ValueError:
        return None
    if (part.scheme != "https" or not part.hostname or part.username
            or part.password or part.port not in (None, 443)
            or part.query or part.fragment or part.path != "/krc-wake/v1"
            or not pinned_host or part.hostname != pinned_host
            or part.hostname in ("localhost", "127.0.0.1", "::1")
            or len(token) < 32 or len(token) > 256):
        return None
    return url, token

def attempt_external_wake() -> str:
    """Return only a fixed status enum; never expose tokens, URLs, or raw payloads."""
    configured = _configured()
    if not configured:
        return "disabled"
    url, token = configured
    request = Request(
        url, data=b'{"action":"wake_voicebridge"}', method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + token,
            "User-Agent": "krc-p0-cold-wake",
        },
    )
    try:
        with build_opener(_NoRedirect()).open(request, timeout=35) as response:
            if int(response.status) != 200:
                return "relay_rejected"
            raw = response.read(513)
            if len(raw) > 512:
                return "relay_invalid"
            data = json.loads(raw.decode("utf-8"))
            if isinstance(data, dict) and data.get("status") in {"ready", "woken"}:
                return "relay_success"
            return "relay_invalid"
    except HTTPError:
        return "relay_rejected"
    except (OSError, URLError, TimeoutError, ValueError, UnicodeDecodeError):
        return "relay_unavailable"
