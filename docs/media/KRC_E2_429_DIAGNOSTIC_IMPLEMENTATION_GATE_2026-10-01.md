# E2 / VoiceBridge 429 — reproduced and implementation gate

## Observations
- Read-only `media_instagram_preflight` for `https://www.instagram.com/reel/Dcea3BiPTBm/` reproduced `voicebridge_http_error`, HTTP 429, retryable true. No provider work or repeat `start` was performed.
- Live VoiceBridge deployed `server.ts` uses `FixedWindowRateLimiter` keyed by `request.socket.remoteAddress`, emits 429 `RATE_LIMITED` and `Retry-After: 60` on rejection. Health bypasses limiter.
- Current MCP `plugins/krc_migration_candidate/mcp_canary/r3c.py` `call_voicebridge` catches `urllib.error.HTTPError` and discards response body and headers; surfaces only `http_status` and generic `voicebridge_http_error`. Therefore **current tool output cannot prove** that a 429 originated in VoiceBridge's own limiter rather than proxy/host.
- Existing `r3e2_http_server.py` health warmup occurs **only** before POST `/api/v1/media/managed/transcriptions`; it does not exempt GET preflight from the VoiceBridge limiter. Even a successful health check does not guarantee that a subsequent POST will pass the limiter.
- Render logs available through connector are service lifecycle/build entries without per-request rate-limit details; they do not settle the question.
- Owner explicitly defers Neon password rotation until successful tests. Do not copy, expose or modify credentials. Existing E2 stays probe-only; unused isolated E2 stays pending owner verification gate.

## Bounded code/test gate (NOT YET IMPLEMENTED)
1. In MCP VoiceBridge HTTPError handling, parse a **bounded** JSON error body; preserve only allowlisted nonsecret fields (`code`, `request_id`, `correlation_id`) and allowlisted numeric `Retry-After`, alongside HTTP status. Never log headers wholesale, Authorization, response text or arbitrary proxy HTML. Maintain backward-compatible error shape.
2. Add focused unit tests: own VoiceBridge 429 with `RATE_LIMITED` and `Retry-After`, proxy 429 without VoiceBridge structured body, malformed/oversized body, missing header, 503 cold start, no sensitive response leakage. No automatic retries for consequential POST.
3. Consider explicit request-scoped authenticated limiter key behind review only after diagnosing proxy-IP collisions. Do not disable limiter or trust unauthenticated forwarded IP headers.
4. After tests and code review, stage on existing E2/VoiceBridge only with separate deployment gate. One read-only preflight after cooldown should distinguish 429 origin; capture only nonsecret diagnostic metadata.
5. Reconcile owner AssemblyAI balance ($48.31 before/after previous attempt), do not infer that no provider work occurred from balance alone. Any additional real `start` requires separate owner approval.

## Status
`429_REPRODUCED=YES`; `ROOT_CAUSE=UNPROVEN`; `READ_ONLY_ANALYSIS=COMPLETE`; `DIAGNOSTIC_PATCH=NOT_YET_IMPLEMENTED`; `LIVE_CONFIG_UNCHANGED=YES`.
