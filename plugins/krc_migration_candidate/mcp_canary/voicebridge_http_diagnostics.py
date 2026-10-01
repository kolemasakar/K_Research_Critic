"""Allowlisted diagnostics for VoiceBridge HTTPError; never expose arbitrary response content."""
import json
import re
from urllib.error import HTTPError

ALLOWED_CODES = frozenset({"RATE_LIMITED", "SERVICE_UNAVAILABLE", "INTERNAL_ERROR"})

def safe_http_error_metadata(exc: HTTPError) -> dict[str, object]:
    result: dict[str, object] = {}
    retry_after = exc.headers.get("Retry-After") if exc.headers else None
    if isinstance(retry_after, str) and re.fullmatch(r"[0-9]{1,4}", retry_after.strip()):
        seconds = int(retry_after.strip())
        if seconds <= 3600:
            result["retry_after_seconds"] = seconds
    try:
        raw = exc.read(2049)
        if len(raw) > 2048:
            return result
        parsed = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return result
    if not isinstance(parsed, dict):
        return result
    error = parsed.get("error")
    if not isinstance(error, dict):
        error = parsed
    code = error.get("code")
    if isinstance(code, str) and code in ALLOWED_CODES:
        result["upstream_code"] = code
    for field in ("request_id", "correlation_id"):
        value = error.get(field)
        if value is None:
            value = parsed.get(field)
        if isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,80}", value):
            result[field] = value
    return result
