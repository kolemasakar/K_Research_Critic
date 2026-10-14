# KRC P2 / R4 — owner-approved E2 scoped-404 Render deployment and read-only acceptance
Date: 2026-10-14 UTC.

## Authorization and pre-deployment
- Owner replied `1` to the requested exact deployment of E2 missing-job scoped-404 fix.
- Render service `srv-da1kic5bedkc73d6fk60`, workspace `tea-d9dsqdjrjlhs73ba1ga0`, plan free, one instance, autoDeploy=no, branch `agent/krc-media-gemini-migration`.
- Prior LIVE SHA `bdeb8824abe79cb49fac736dca0fbfa42295c9b1`. GitHub compare between bdeb8824 and `cb0cbf250a60ba42b75fc4e55f8424b0fcfe1ad7`: status ahead, ahead_by=2, behind_by=0, exactly the E2 fix and regression test, no rollback.
- Exact checkout TypeScript build PASS, targeted public Cobalt tests 9/9 PASS and full 280/280 PASS, 0 skipped/failed, exit 0.
- No main/public merge and no paid fallback or provider calls during this activity.

## Controlled Render deployment
- Triggered exactly once via Render existing service API; no clearCache requested.
- Deploy ID `dep-db7g1lqj9qps73capk30`.
- Render confirmed checked out exact commit `cb0cbf250a60ba42b75fc4e55f8424b0fcfe1ad7`, finished `2026-10-14T04:11:36.070585Z`, status `live`.

## After-deploy read-only probes
Used syntactically valid but intentionally absent `KRCM_00000000-0000-4000-8000-000000000000`; **no transcription/processing start**.
- E2 `media_non_youtube_status`: HTTP **404**, request/correlation `cc7d30bb-7e37-4e57-be39-937b597905f0` — previously E2 returned erroneous 401 due to fallback handler.
- E2 `media_non_youtube_segments`: HTTP **404**, request `a5661f84-e9d8-4727-b31c-03c3cdb2ebf9`. Both requests reached VoiceBridge; external MCP wrapper reports INVALID_ARGUMENT because backend responded error, not an invalid tool input.
- E2 `media_instagram_preflight`: PASS, `can_continue=true`, Cobalt -> AssemblyAI, estimated retrieval credits 0, automatic_paid_fallback=false, request `4287af8c-102a-46f7-9fe7-17127bfba489`.
- R3C `media_get_capabilities`: PASS, request `e3a7f3f2-f359-48a4-b10a-916fae54e8c4`, configured=true, durable_store=postgres, restart_resilient_jobs=true, duplicate_start_reuses_job=true, automatic_paid_fallback=false, paid_retrieval_fallback=false, paid_stt_fallback=false, youtube_gemini_free_tier_only=true and explicit Gemini data use consent required. Backend model currently `gemini-3.8-flash`.
- E1 `media_youtube_preflight`: PASS, `can_continue=true`, Free Tier, consent_required=true, model `gemini-3.8-flash`, request `e6b8fdb1-77fd-498e-81f9-c58e390708d5`.

## Verdict and boundaries
- Exact-sha Render rollout: **PASS**.
- E2 malformed fallback `401` for absent scoped job corrected to **expected `404` on both status and segments, PASS**.
- E2 preflight and R3C/E1 route checks: **PASS**.
- FREE_ONLY configuration: **PASS**, not independent monetary billing evidence.
- Read-after-write of an actual unexpired Instagram job on this exact deployment: **NOT TESTED**; no job created just for read-only control.
- E1's separately advertised cross-scope Instagram reads (401) not changed; token privileges deliberately not expanded.
- Telegram LIVE: **BLOCKED** by owner policy; no `media_telegram_start`.
- Global/public R4 release: **HOLD**.
