# VoiceBridge proxy IP and rate-limiter design review

Date: 2026-10-01. Research-only audit; no VoiceBridge or E2 production changes and no new MEDIA work.

## Source-derived facts

Inspected VoiceBridge deployed commit `d3873bf13e60c4932ab08cae449c924051be4a37`:
- `src/cloud/src/server.ts` lines 223-225: `clientKey(request)` returns `request.socket.remoteAddress || "unknown"` only. It does not inspect `X-Forwarded-For` or `Forwarded`.
- Same file: a `FixedWindowRateLimiter(config.rateLimitRequestsPerMinute)` is instantiated per server process. Its `allow(clientKey(request))` executes before authentication. Rejected requests return HTTP 429 `RATE_LIMITED`, `Retry-After: 60`.
- `src/cloud/src/rate_limit.ts`: in-memory map keyed by the passed string; each entry counts requests in a 60-second fixed window. Restart resets this in-memory state. Multi-instance global limits are not guaranteed by this implementation.
- `src/cloud/src/config.ts` and `public_media_admission.ts`: in public MEDIA mode, effective maximum is `min(configured RATE_LIMIT_REQUESTS_PER_MINUTE, 60)`. Owner supplied cropped Render screenshot showing configured 60; thus effective configured public-mode limit is 60/minute if screenshot represents the active environment.

## Implications and evidence gaps

The implementation rate-limits by TCP peer IP, not by authenticated route identity or end-user identity. If a reverse proxy presents the same `remoteAddress` for different external clients, their requests share one bucket. **No actual runtime socket IP, trusted proxy chain or causal link to historical 429 has been observed.** Do not assert that Render definitely rewrites all requests to one IP. Current Render log queries exposed only app logs, no request records in the checked period. Successful health checks are not evidence against non-health throttling.

## Decision

Do not immediately replace `remoteAddress` with unvalidated `X-Forwarded-For`: client-supplied headers can be spoofed unless a documented, verified trusted proxy boundary overwrites and validates them. Do not remove throttling or simply raise the limit to mask unknown causes. Preserve FREE_ONLY and current E2 probe-only configuration.

If a future naturally occurring 429 is captured, correlate allowlisted nested request/correlation IDs and Retry-After with same-window app logs. To distinguish proxy aggregation, develop a separate nonsecret, privacy-minimizing diagnostic that reports only an ephemeral keyed digest/classification of the observed peer and trusted proxy metadata (not raw IP or credentials), with explicit review and owner approval before any production instrumentation. Consider authenticated-principal-based limiter after authentication only together with a separate pre-authentication IP abuse guard; this is a **design option**, not an approved production change. Validate fixed-window and concurrent-request behavior in isolated tests before any deploy.

Status: source audit PASS; configured limit 60/min; shared proxy IP cause UNCONFIRMED; no code changes. See `KRC_MEDIA_OWNER_CANONICAL_CHECKPOINT_2026-10-01.md` and `KRC_VOICEBRIDGE_RATE_LIMIT_RUNTIME_EVIDENCE_GATE_2026-10-01.md`.
