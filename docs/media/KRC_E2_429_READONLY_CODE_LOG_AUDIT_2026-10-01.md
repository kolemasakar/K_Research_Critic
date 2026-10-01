# E2 HTTP 429 follow-up: source and log audit

Date: 2026-10-01. Read-only investigation after latest E2 diagnostic deployment. No production config change, no provider work, no induced 429.

## Source evidence (deployed VoiceBridge SHA d3873bf13e60c4932ab08cae449c924051be4a37)
- `src/cloud/src/config.ts`: `RATE_LIMIT_REQUESTS_PER_MINUTE` parses with default 120; when `mediaPublicMode` is enabled, effective limit is `Math.min(configuredRateLimit, PUBLIC_MEDIA_MAX_REQUESTS_PER_MINUTE)`.
- `src/cloud/src/public_media_admission.ts`: `PUBLIC_MEDIA_MAX_REQUESTS_PER_MINUTE=60`. Thus public-mode maximum is 60/minute, potentially lower if environment overrides. Actual runtime value not verified.
- `src/cloud/src/server.ts`: rate limiter key is `request.socket.remoteAddress || "unknown"`; `FixedWindowRateLimiter` is evaluated before authentication; rejected requests receive HTTP 429 `RATE_LIMITED` with `retry-after:60`. `/api/v1/health` is an earlier bypass, so healthy response does not establish other-route availability.
- `src/cloud/src/rate_limit.ts`: fixed 60-second window keyed by the connection address. Shared reverse-proxy IP aggregation is a hypothesis, not proven for actual deployment.
- Render VoiceBridge request-log query for 2026-10-01 18:30-19:20 UTC returned zero request records; absence of records cannot establish that requests were absent or determine prior 429 origin. Do not infer no errors from this result.

## Decision / next evidence gate
- Keep existing E2 production probe-only, FREE_ONLY and current credentials unchanged. No additional media starts authorized by this audit.
- If another spontaneous 429 occurs, preserve allowlisted upstream code, Retry-After and nested request/correlation IDs from diagnostic response, and compare contemporaneous nonsecret Render request/app logs. Check effective nonsecret limit through an authorized safe method; do not print environment secrets or provoke throttling.
- Consider reviewed rate-limit key design changes only after evidence. This checkpoint does not claim the 429 issue is permanently resolved.

See `docs/media/KRC_MEDIA_OWNER_CANONICAL_CHECKPOINT_2026-10-01.md` for consolidated project decisions.
