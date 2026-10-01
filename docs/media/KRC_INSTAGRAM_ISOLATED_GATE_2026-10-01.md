# Instagram E2 isolated acceptance gate — 2026-10-01

## Live checks
- Current E2 v2 Render service on Free plan, Frankfurt, `autoDeploy:no`, branch `agent/krc-public-media-r3-integration`, module `r3e2_http_server`.
- At ~16:04 UTC, Instagram preflight and lookup of `https://www.instagram.com/reel/Dcea3BiPTBm/` both initially failed nested VoiceBridge HTTP 429, retryable true.
- After GET of canonical VoiceBridge `/api/v1/health` returned HTTP 200 (13.647 seconds), E2 `/healthz` confirmed `confirmation_probe_only:true`.
- Retried Instagram preflight: PASS (`can_continue:true`, `consent_required:false`, `provider:cobalt`, `stt_provider:assemblyai`, `estimated_retrieval_credits:0`, `automatic_paid_fallback:false`), request_id `25e7241b-fe8d-42b7-80ec-4cd286cb8535`.
- Retried Instagram lookup: HTTP 404, nonretryable. May indicate no durable job for URL; exact lookup semantics require checking backend contract before treating as a fault.

## Isolated real-execution prerequisites
1. Use an isolated **free-only** E2 deployment rather than changing existing probe-only production E2; verify Render service availability and plan constraints before creating it.
2. Configure the isolated service to use the canonical VoiceBridge with route-scoped authorization and `KRC_R3E2_CONFIRMATION_PROBE_ONLY=false`; do not copy or disclose secrets in documentation.
3. Confirm VoiceBridge paid fallback flags false and that STT provider work is within a free quota before actual start; preflight's zero retrieval credits estimate is not proof of zero STT usage.
4. Warm canonical health and run one E2 start on the selected URL; record actual job ID, status, segment pagination, complete transcript, repeat read, and provider accounting. A probe result `real_media_start:false` is not acceptance.
5. Do not deploy, change production flags or trigger new provider work until an isolated deployment and its budget/authorization are confirmed. The present check performed read-only operations only.

## Current verdict
Infrastructure/warmed preflight PASS; actual E2 provider E2E NOT TESTED; recurrent 429 remains an open cold-start-correlated issue.
