# KRC MEDIA owner checkpoint - 2026-10-01
Контрольна точка стану KRC MEDIA, ухвалених рішень, перевірок і наступних дій.

## Scope and source of truth
- Private K-Research & Critic Plugin / MEDIA migration; do not change the separate public GPT.
- This checkpoint consolidates the October 1 Instagram E2 diagnostics and acceptance; earlier historical checkpoints retain their original time-scoped observations.
- Research branch: `agent/krc-public-media-r3-integration`; repository `kolemasakar/K_Research_Critic`. Do not infer that these commits have been merged into `main` or published as a new Plugin release.

## Verified operational state
- Existing Render Instagram E2 service `srv-dan7vsijnfac73fmrtl0` (`krc-mcp-r3e2-instagram-sentinel-v2`), Free plan, Frankfurt, autoDeploy OFF.
- Latest independently verified production deployment: `dep-davau48u01pc73e2fr50`, commit `3bebed84b56b3457bc064c24ce25fc7224baebfb`, Render `live` at 2026-10-01 19:06:29 UTC.
- Latest deployed parser reads allowlisted nested VoiceBridge `error.request_id` and `error.correlation_id`, with top-level fallback; no arbitrary response body or secrets logged. VoiceBridge deployed code nests these fields under `error`.
- Isolated full test suite on authorized `krc-cobalt` Python 3.12 environment: **395/395 PASS** in 18.62s. This is NOT GitHub Actions CI or a Python 3.13 validation.
- After latest deploy: one Instagram read-only preflight PASS (`can_continue=true`, Cobalt retrieval, AssemblyAI STT, automatic paid fallback false, estimated retrieval credits 0), request ID `436a3ac0-4132-4c6b-b91b-a3ccb77480d1`. Confirmation-probe verification returned `confirmation_probe_executed=true`, `real_media_start=false`, `provider_work=false`, `provider_charge=false`. The protective mode is effective.
- Prior owner-approved **single real Instagram E2E start**, before the nested-ID parser update, succeeded for `https://www.instagram.com/reel/Dcea3BiPTBm/`: job `KRCM_0074486f-4021-4bdc-a6c4-76d6625a4003` COMPLETED; Cobalt + AssemblyAI, 41.11675-second video, 42 STT seconds, one segment, 331 transcript characters, detected English, reported 0 credits, provider data deleted. Read-only job status and complete single-segment pagination independently confirmed. Probe-only mode restored afterward and reverified.
- Previous intermittent HTTP 429 has NOT been causally explained. VoiceBridge has a 60-second fixed-window IP-keyed limiter; its effective deployed rate and whether proxy IP grouping caused the observed 429 remain unverified. Healthy `/api/v1/health` and successful preflights do not disprove intermittent saturation.

## Owner decisions and boundaries
1. FREE_ONLY: no automatic paid retrieval or STT fallback; no paid infrastructure expansion.
2. Keep existing Neon DB password for now: owner explicitly deferred rotation until tests succeeded; completion of these tests is not blanket authorization to rotate credentials. Request a separate decision before rotation.
3. Keep existing production E2 in `KRC_R3E2_CONFIRMATION_PROBE_ONLY=true` except for a separately owner-approved bounded real execution. The single October 1 real start was authorized, completed, and the protective mode restored.
4. No additional real MEDIA provider work, environment/credential changes, service deletion, Plugin publication/sharing, or public GPT changes under this checkpoint.
5. Separate isolated acceptance E2 `srv-dav8r9ou01pc738ro880` is not confirmed deleted; owner-approved removal and tooling remain separate.
6. Preserve original source text and independently verify status/segment completeness. Historical YouTube and other platform results are in their own checkpoints; this Instagram acceptance does not validate Facebook or Telegram E2E.

## Reconciliation of earlier checkpoints
- `docs/media/KRC_E2_429_DEPLOYED_RATE_LIMIT_AUDIT_2026-10-01.md` recorded a **historical** inconclusive E2E state before the successful October 1 run; do not reuse that historical status as current.
- `docs/media/KRC_E2_LIVE_INSTAGRAM_PASS_RESTORED_PROBE_2026-10-01.md` is the authoritative single-live-run and safety restoration evidence.
- `docs/media/KRC_E2_NESTED_IDS_PATCH_395_PASS_2026-10-01.md` records code-level correction and isolated suite.
- `docs/media/KRC_E2_NESTED_IDS_DEPLOYED_READONLY_PASS_2026-10-01.md` records the latest deployment and post-deploy checks.

## Next actions (not executed)
1. Read-only, low-frequency audit of VoiceBridge effective nonsecret rate-limit configuration and request logs around any **new** 429. Correlate safe upstream code, `Retry-After`, request and correlation IDs. Do not induce rate limiting or expose secrets.
2. Evaluate auth-aware/proxy-aware rate-limiter design in a separate reviewed research change only if logs justify it. No speculative production hotfix.
3. Review remaining Facebook/Telegram E2E gates and Plugin release synchronization separately, preserving FREE_ONLY and per-platform owner consent.
4. Resolve separately whether to rotate the previously exposed Neon credential and whether to delete unused isolated E2; neither is implicitly approved here.

Checkpoint status: **Instagram E2E PASS once; latest E2 diagnostic deploy LIVE; read-only preflight and probe safety PASS; HTTP 429 root cause OPEN**.

## Later owner-provided runtime setting

Owner-supplied cropped Render screenshot confirms VoiceBridge `RATE_LIMIT_REQUESTS_PER_MINUTE=60`. With the inspected public-mode code ceiling of 60, the effective configured public-mode limit is 60 requests/minute, assuming the screenshot reflects the active deployment. The cause of intermittent 429, including whether shared proxy IP aggregation is involved, remains unproven. Supporting audit: `docs/media/KRC_VOICEBRIDGE_RATE_LIMIT_RUNTIME_EVIDENCE_GATE_2026-10-01.md`.
