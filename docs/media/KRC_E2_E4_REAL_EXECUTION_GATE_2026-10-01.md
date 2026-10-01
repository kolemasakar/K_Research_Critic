# KRC E2–E4 real execution gate — verified 2026-10-01

## Live evidence
- Canonical VoiceBridge `https://voicebridge-krc-media-beta-kolemasakar.onrender.com/api/v1/health` returned HTTP 200 after a cold start. R3C `media_get_capabilities` and Instagram `media_instagram_preflight` subsequently PASS. The earlier nested HTTP 429 is correlated with cold startup, not conclusively attributed.
- E2 v2, E3 and E4 `/healthz` all report `confirmation_probe_only:true`; their real execution is therefore **intentionally disabled**. E3 `/healthz` confirms override token fingerprint matches expected, without exposing secrets.
- Source files `plugins/krc_migration_candidate/mcp_canary/r3e2_http_server.py`, `r3e3_http_server.py`, `r3e4_http_server.py` each route start calls to `_confirmation_probe_backend` when corresponding env flag is `true`, and to `_cold_start_resilient_backend` otherwise. The latter warms canonical VoiceBridge via health GET before issuing exactly one POST (as demonstrated by existing `tests/test_krc_mcp_r3e3.py::test_r3e3_cold_start_warms_before_exactly_one_start` mock test; this audit did not rerun the suite).
- Exact flag names: `KRC_R3E2_CONFIRMATION_PROBE_ONLY`, `KRC_R3E3_CONFIRMATION_PROBE_ONLY`, `KRC_R3E4_CONFIRMATION_PROBE_ONLY`. **No flags changed in this audit.**

## Ordered deployment / acceptance gate
1. Validate free-only capabilities on the *actual deployed* VoiceBridge: `automatic_paid_fallback:false`, `paid_retrieval_fallback:false`, `paid_stt_fallback:false`, `durable_store:postgres`.
2. Confirm each E2–E4 route binding to canonical VoiceBridge, without printing secrets. For E3, the live health fingerprint check already PASS.
3. Prepare separate reviewed isolated deployments or explicit maintenance window for changing each probe flag to `false`, one platform at a time. Ensure no automatic paid provider execution; keep source-level controls and credential scope unchanged.
4. Warm canonical VoiceBridge `/api/v1/health` to HTTP 200, then run **one** platform preflight and **one** actual start on a public speech-bearing test video; record `job_id`, terminal status, retrieval route, STT route, segment count and paginated complete read.
5. Repeat read of the *same* job after service restart or cold start, and validate no duplicate external provider work. Test failures must not be reported as PASS or retried as another paid/real start.
6. Return to probe-only mode after test unless explicit owner decision to enable production real processing; validate `/healthz` and audit no paid fallback.

## Status and exclusions
- Read-only architecture and live configuration review: COMPLETE.
- Real provider E2E: NOT STARTED. Current deployment intentionally prevents it.
- The Telegram APOD music-only candidate is unsuitable for **speech recognition acceptance**. Replace with a verified public Telegram voice video before its real STT test.
- Do not infer `429` root cause without correlated VoiceBridge/gateway logs. Do not alter production env, restart or trigger external provider work as part of read-only diagnosis.
