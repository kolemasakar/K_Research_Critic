# KRC E2 — deployed VoiceBridge HTTP 429 investigation (2026-10-01)

Owner directive: retain existing Neon database password until successful tests; do not rotate during this phase. No credentials copied to documentation.

## Confirmed
- Existing E2 remains probe-only after rollback. Do not repeat a provider start without fresh owner decision.
- New read-only Instagram preflight returned nested `voicebridge_http_error` 429 retryable.
- Actual deployed VoiceBridge SHA `d3873bf13e60c4932ab08cae449c924051be4a37`, `src/cloud/src/server.ts`: `FixedWindowRateLimiter(config.rateLimitRequestsPerMinute)`; key `request.socket.remoteAddress || 'unknown'`; when rejected, `retry-after:60`, HTTP 429, `RATE_LIMITED`. Authentication occurs *after* this check. `/api/v1/health` bypasses rate limiter, so HTTP 200 health does not rule out a saturated public rate limit.
- Fixed window implementation in `src/cloud/src/rate_limit.ts` uses 60-second window and counts requests by IP. Actual effective `RATE_LIMIT_REQUESTS_PER_MINUTE` has not been read; do not invent it.
- Owner's Render screenshots show current VoiceBridge Neon `krc_media_beta` endpoint matching Neon production project and `MEDIA_JOB_TTL_SECONDS=3600`. Deployed retention code deletes expired jobs and STT daily records older than two days; this explains missing historical rows without proving the latest start outcome.
- Owner's AssemblyAI before/after Free balance unchanged at $48.31. No additional start executed.

## Hypothesis and discriminating test
IP-keyed limiter may group Render proxy traffic and E2 requests into one bucket. This is a plausible explanation for intermittent nested 429 but **not proven** without actual 429 response body/header and contemporaneous logs. Read-only investigation: record effective rate limit (nonsecret), compare `Retry-After`/`RATE_LIMITED` on a failed read-only call if possible, and inspect proxy/IP semantics. Do not expose tokens, DSN or account secrets. Avoid frequent probing; use a single request after cooldown. Consider separate auth-aware rate-limiting design only as a reviewed code change, not a production hotfix.

## Status
429 root cause: plausible, unconfirmed. Instagram current E2E: inconclusive. Existing E2 probe-only: verified. Isolated extra E2: pending owner-approved deletion after verification.

## Later status update (2026-10-01; historical observations above retained)

The earlier `Instagram current E2E: inconclusive` statement is now superseded. A single owner-approved real Instagram E2E job `KRCM_0074486f-4021-4bdc-a6c4-76d6625a4003` COMPLETED with Cobalt + AssemblyAI, zero reported credits, and independently verified status/one segment. Probe-only was restored. Nested VoiceBridge request/correlation ID diagnostic fix subsequently passed 395/395 isolated tests and was deployed to existing E2 as commit `3bebed84b56b3457bc064c24ce25fc7224baebfb`; Render deployment `dep-davau48u01pc73e2fr50` LIVE. Post-deploy read-only preflight and confirmation-probe safety checks PASS. Intermittent HTTP 429 root cause remains unproven. For consolidated current status and owner decisions, see `docs/media/KRC_MEDIA_OWNER_CANONICAL_CHECKPOINT_2026-10-01.md`.
