# KRC existing E2 live pre-start gate — 2026-10-01

## Verified live, read-only
- Existing E2 Render deployment `dep-daqmsg6gekts7398n0rg` status `live`, deployed SHA `05498504171aa34815615f0ab11f8dc78705daaf` (2026-09-24). Newer repo branch SHA differs; do not assume newer docs or code have been deployed.
- Source at actual deployed SHA includes `KRC_R3E2_CONFIRMATION_PROBE_ONLY` and `_cold_start_resilient_backend`; no forced code redeploy is required to access real execution path.
- Existing E2 `/healthz` HTTP 200: `confirmation_probe_only:true`, `voicebridge_binding_configured:true`, `execution_tool_count:1`, `provider_work_started:false`.
- R3C `media_get_capabilities` PASS, request `c044671f-f27d-4023-b604-84b7ebe865c9`: `automatic_paid_fallback:false`, `paid_retrieval_fallback:false`, `paid_stt_fallback:false`, `durable_store:postgres`, `instagram_retrieval_provider:cobalt`, `instagram_stt_provider:assemblyai`.
- Instagram E2 preflight PASS, request `20a9cfde-2110-42a3-9138-09be19767f32`: `can_continue:true`, `estimated_retrieval_credits:0`, `retrieval_credits_available:null`, `stt_provider:assemblyai`. No evidence of available AssemblyAI free STT minutes or account hard spending cap.

## Blocking gate
**Do not switch probe flag to false or initiate provider work until remaining free AssemblyAI minutes and effective spending cap are verified through provider account or a trusted quota endpoint.** `paid_stt_fallback:false` only disables fallback; it does not prove primary AssemblyAI provider is within a free quota.

## Owner decision
Use existing E2 for acceptance. Delete unused extra E2 only after existing E2 acceptance verification; no delete operation is exposed by connected Render integration. New isolated E2 credentials are unnecessary.

## Controlled follow-up
1. Owner checks AssemblyAI dashboard free balance and confirms zero-charge/hard spending limit, without sharing keys.
2. Capture redacted existing E2 config and deploy SHA before one controlled flag flip.
3. After provider budget verification, set `KRC_R3E2_CONFIRMATION_PROBE_ONLY=false` on existing E2, run exactly one actual Instagram start, collect durable job status and complete segments, restore probe flag and verify no provider charges.
4. Delete extra E2 via Render UI after verification and check Render list_services to confirm absence.
