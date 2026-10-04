"""Allowlisted diagnostics for VoiceBridge HTTPError; never expose arbitrary response content."""
import json
import re
from urllib.error import HTTPError

ALLOWED_CODES = frozenset({"RATE_LIMITED", "MEDIA_PUBLIC_FREE_TIER_RATE_LIMIT", "MEDIA_PUBLIC_CONCURRENCY_LIMIT", "SERVICE_UNAVAILABLE", "INTERNAL_ERROR"})

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


def safe_error_diagnostics(values: dict[str, object]) -> dict[str, object]:
    """Revalidate the same narrow HTTP diagnostic allowlist at MCP egress."""
    result: dict[str, object] = {}
    stage = values.get("failure_stage")
    attempted = values.get("consequential_post_attempted")
    if isinstance(stage, str) and stage in {"warmup", "readiness", "start"} and isinstance(attempted, bool):
        if (stage == "start" and attempted) or (stage != "start" and not attempted):
            result["failure_stage"] = stage
            result["consequential_post_attempted"] = attempted
    retry = values.get("retry_after_seconds")
    if isinstance(retry, int) and not isinstance(retry, bool) and 0 <= retry <= 3600:
        result["retry_after_seconds"] = retry
    code = values.get("upstream_code")
    if isinstance(code, str) and code in ALLOWED_CODES:
        result["upstream_code"] = code
    for field in ("request_id", "correlation_id"):
        value = values.get(field)
        if isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,80}", value):
            result[field] = value
    return result
