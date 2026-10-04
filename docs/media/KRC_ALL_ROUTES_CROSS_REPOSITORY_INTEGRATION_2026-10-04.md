# KRC all-direction MEDIA integration checkpoint

Date: 2026-10-04
Status: SOURCE / LOCAL CROSS-REPOSITORY INTEGRATION PASS; LIVE PROVIDER ACCEPTANCE PENDING.
Owner priority: integrate YouTube, Instagram, Facebook and Telegram first; observe naturally occurring errors during integration rather than speculate about the historical 429.

## Exact tested source

- VoiceBridge: `029eddfd9b8ba31bfe373abe0e3ea078ff4fedd4`, branch `research/krc-peer-observation-isolated`.
- KRC: `ef069b43280ea7bf1adaa4065f6239eb22df0502`, branch `agent/krc-public-media-r3-integration`.
- Parent baselines: VoiceBridge `542b0a7b576568f5c384e1d11522b5fe9a4fea07`; KRC `a119fa456ce69b6402946444d853fb3682a1ae82`.
- Host: freshly verified `krc-cobalt`, Node `v24.21.0`, Python 3.12 test environment.

## Changes

VoiceBridge `managed_server.ts` accepts optional trusted in-process injection of the managed service, YouTube engine and public Cobalt engine. Existing production callers omit this argument and keep their original factories, handler order and admission controls. This is a testability seam, not a public endpoint or production configuration flag.

KRC adds a shared narrow revalidation helper for HTTP diagnostic metadata at MCP egress. R3C and all four execution dispatchers now consistently retain allowlisted upstream code, numeric Retry-After and safe request/correlation IDs. Arbitrary body, exception message, token and peer data are discarded. The two actual MEDIA admission error codes are now recognized by the HTTP diagnostic parser. Retryability, auth/consent, execution routing, automatic retry and provider policy are unchanged.

New cross-repository tests exercise the real Python dispatchers, unchanged urllib HTTPS transport with certificate verification, a local TLS forwarding server, actual VoiceBridge managed wrapper/handlers/engines, fake providers and explicit in-memory stores. No live URL is retrieved; no provider credential or PostgreSQL URL is used by these fixtures.

## Validation

- KRC pre-change baseline: 407/407 PASS in 19.39 seconds.
- New cross-repository integration: 9/9 PASS.
- New safe-metadata tests: 8/8 PASS.
- Focused post-final-VoiceBridge-change set: 17/17 PASS in 16.93 seconds.
- KRC full suite, integration opt-in enabled: 424/424 PASS in 41.10 seconds, exit 0.
- VoiceBridge final TypeScript build and full suite: 305/305 PASS in 89.243 seconds, exit 0.
- Both repository diffs: `git diff --check` PASS.

The first TLS fixture run passed one test but reused urllib's cached opener across different temporary test certificates; fixture isolation now resets that cache while retaining TLS verification. The first VoiceBridge regression hit an existing source-level factory-wiring assertion; the original `krcManaged.service` wiring was retained, then the complete build/regression and focused cross-repository tests passed. No acceptance is inferred from the intermediate failures.

To reproduce:
1. Build the pinned VoiceBridge `src/cloud` with Node >=24.
2. In pinned KRC run:
   `KRC_TEST_VOICEBRIDGE_ROOT=/absolute/VoiceBridge/src/cloud python3 -m pytest -q`.
3. Without the opt-in variable, only the 9 external-repository tests are skipped; the rest of the ordinary KRC suite remains runnable. OpenSSL must be available for the local TLS test certificate.

## Per-direction matrix

| Direction | Real local start/status/pages/reuse | Route/credentials | Provider path |
|---|---|---|---|
| YouTube | PASS | R3E1 -> dedicated Gemini route; R3C reads | Fake Gemini direct |
| Instagram | PASS | R3E2 -> public Cobalt route; R3C reads | Fake Cobalt + AssemblyAI |
| Facebook | PASS | R3E3 -> Facebook fallback route; R3C reads | Fake free Cobalt + AssemblyAI; paid path never called |
| Telegram | PASS | R3E4 -> Telegram public route; R3C reads | Fake Telegram public web + AssemblyAI |

All four tests validate one provider execution, completed job identity, ordered contiguous 3-segment pagination with limit=1, exact JavaScript UTF-16 transcript-character semantics (including Ukrainian and an emoji), repeated start reusing the same job without extra work, and read continuity after recreating the HTTP wrapper.

The wrapper restart reuses the SAME local engine/store objects. It proves HTTP routing/read continuity, not process/host restart durability. Fixture capabilities accurately say `durable_store=memory`. Live PostgreSQL behavior is not validated by these local fixtures.

Cross-platform starts are rejected before transport; inappropriate scoped reads are denied. Ordinary MEDIA reads add no provider calls. A deliberately saturated legacy path on localhost yields a real 429 whose safe metadata survives all five MCP dispatchers; there is no provider replay.

## Corrected scope of the 429 hypothesis

`index.ts` starts `managed_server.ts`, which wraps `createVoiceBridgeServer`. Most recognized MEDIA paths return from public/managed handlers before the legacy HTTP listener and its socket limiter.

The production SHA `d3873bf13e60c4932ab08cae449c924051be4a37` has the same managed-wrapper routing and public admission source as the research baseline before the new injection seam. Thus the previous base-server peer diagnostic gate does not prove diagnostic coverage or limiter causality for all MEDIA routes.

The local actual-wrapper test sends 65 capability reads successfully, beyond the legacy limit of 60. This is NOT live load testing and does not establish the actual production/gateway cause. No speculative limiter or forwarded-identity change is justified.

## Fresh live evidence (read-only)

- First R3C `media_get_capabilities`: `voicebridge_http_error`, HTTP 429, retryable=true; no cause or upstream IDs supplied.
- Canonical VoiceBridge health afterwards: HTTP 200, `voicebridge-cloud` v0.6.0.
- Later R3C capabilities: PASS; request `92760173-465c-4727-a16b-c42d4acc3d12`.
- R3E1 capabilities: PASS; request `e3a6ddb3-5153-4db1-aa2e-5db25baffe1b`.
- Current capabilities: all four platforms configured; durable_store=postgres; all automatic paid fallbacks false.
- YouTube preflight PASS, can_continue=true; request `2ddd9e5a-1df6-4d9a-8065-9a3e06404fa6`.
- Instagram preflight PASS, can_continue=true; request `ff43cb28-43b3-47d3-aa7b-4d44846e9495`.
- Existing E2, E3, E4 health endpoints: HTTP 200, configured bindings, `confirmation_probe_only=true`, `provider_work_started=false`.
- Render VoiceBridge remains deployed at `d3873bf13e60c4932ab08cae449c924051be4a37`; free plan, autoDeploy OFF. E2/E3/E4 are existing free services with autoDeploy OFF.
- Request-log query could not proceed because the Render tool requires a user-selected workspace. No workspace was chosen and no request-log causal conclusion is made.
- The 429 followed by later success is an observation, not proof that cold start caused it.

## Live acceptance package / remaining decisions

Source/local acceptance is complete. Full live provider acceptance is NOT complete.

Known existing candidates:
- YouTube: https://www.youtube.com/watch?v=bu_DYQAKnuQ
- Instagram: https://www.instagram.com/reel/Dcea3BiPTBm/
- Facebook: https://www.facebook.com/NASASCaN/videos/how-nasa-uses-gravity-and-radio-waves-to-study-planets-and-moons/8368792419872400/
- Telegram: the prior APOD candidate was music-only; obtain a public speech-bearing video. Do not substitute an invented URL.

Before new YouTube work, show/approve the returned notice: "Gemini Developer API Free Tier content may be used by Google to improve Google products." Previous video approvals are not assumed to authorize a new provider execution under this live acceptance.

For E2–E4, real execution requires a separately explicit bounded activation decision because deployed `KRC_R3E2_CONFIRMATION_PROBE_ONLY`, `KRC_R3E3_CONFIRMATION_PROBE_ONLY`, `KRC_R3E4_CONFIRMATION_PROBE_ONLY` remain true. Do not present confirmation probes as real starts.

Execution order after those inputs/decisions: YouTube -> Instagram -> Facebook -> Telegram, one start per direction, no concurrent starts and no automatic replay on error. Warm verified health, require capabilities/preflight safety, reuse existing COMPLETED/PROCESSING state where available, then read terminal state and EVERY segment page, independently reconcile counts, and repeat read of the SAME job. Stop that direction on uncertain charge, missing job identity or unsafe fallback; record failure and proceed only as authorized.

Restore E2–E4 probe mode after each bounded test and verify health. No credential rotation, service deletion, new paid infrastructure, main merge or Plugin publication is included. Test-only VoiceBridge injection does not itself require a production deploy to validate the already-existing routes. Any KRC diagnostic-patch rollout is a separately pinned, bounded deployment, not permission to enable peer instrumentation.

NO PRODUCTION CHANGES OR REAL MEDIA PROVIDER WORK occurred during this checkpoint. Historical 429 cause remains OPEN.
