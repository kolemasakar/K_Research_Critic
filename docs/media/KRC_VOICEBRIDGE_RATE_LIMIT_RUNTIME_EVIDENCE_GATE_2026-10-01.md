# VoiceBridge runtime rate-limit evidence gate

Date: 2026-10-01. Follow-up read-only audit; no provider starts, production mutations or secret retrieval.

## Render log capabilities actually observed
- For existing VoiceBridge Render service `srv-da1kic5bedkc73d6fk60` between 18:00 and 19:30 UTC on 2026-10-01, `list_log_label_values(type)` returned only `app`; `list_log_label_values(statusCode)` returned null. An `app` log filter for `429` returned no records. Earlier request-log query between 18:30 and 19:20 UTC returned no request records.
- This does NOT establish that no HTTP 429 occurred, nor that Render request logs are permanently unavailable. The checked service/time window did not expose them.

## Verified code-derived bounds (VoiceBridge deployed source SHA d3873bf13e60c4932ab08cae449c924051be4a37)
- Public-mode effective request limit = `min(configured RATE_LIMIT_REQUESTS_PER_MINUTE, 60)`. Parser default for configured value = 120. Effective public default = 60/minute if the runtime env variable is unset; actual runtime value is unknown.
- Fixed-window 60-second limiter uses `request.socket.remoteAddress || "unknown"` and executes before authentication; `/api/v1/health` bypasses it.
- The updated E2 diagnostics can extract allowlisted nested upstream `error.request_id` and `error.correlation_id`, and bounded numeric Retry-After. This fix has been deployed and its post-deploy read-only preflight and probe safety passed. No spontaneous 429 was captured after deployment.

## Safe next verification
- Current Render connector exposes environment-variable updates but no read-only environment-variable retrieval. Do NOT attempt to infer or overwrite runtime settings, and do NOT print all environment values to inspect one nonsecret setting.
- If the owner provides a redacted screenshot containing only `RATE_LIMIT_REQUESTS_PER_MINUTE` and public-mode status, compare the observed setting against the public 60/minute ceiling; otherwise mark runtime limit UNKNOWN.
- On a naturally recurring 429, capture only allowlisted diagnostics and inspect available app/request logs for the same window. Avoid synthetic load, extra media jobs, secrets disclosure or speculative production limiter changes.

Owner boundaries: FREE_ONLY, probe-only on existing E2, defer Neon credential rotation pending separate owner approval. This document supplements `KRC_MEDIA_OWNER_CANONICAL_CHECKPOINT_2026-10-01.md`.
