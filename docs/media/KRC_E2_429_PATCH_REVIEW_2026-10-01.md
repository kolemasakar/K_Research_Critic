# E2 HTTP 429 diagnostic patch — review criteria

Current production unchanged. Planned patch for `plugins/krc_migration_candidate/mcp_canary/r3c.py`: parse at most 2048 bytes from HTTPError, allowlist `RATE_LIMITED` and a few documented error codes, bounded alphanumeric request IDs, numeric Retry-After 0–3600 seconds. Reject malformed, oversized or arbitrary HTML responses; never expose headers wholesale, body text or tokens. Extend VoiceBridgeError with optional diagnostics and sanitize output. Preserve existing error shape and forbid automatic retries of POST. Unit tests must distinguish structured VoiceBridge 429 from unstructured proxy 429, verify 503 and secret redaction. No deployment, password rotation or new provider work before validation.

GitHub source update via connector and remote Git network access attempts were blocked by the execution safety system; do not claim patch merged or tests run.
