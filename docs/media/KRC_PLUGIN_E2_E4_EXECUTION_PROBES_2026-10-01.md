# KRC E2–E4 integration probes — 2026-10-01

## Test URLs
- Instagram: https://www.instagram.com/reel/Dcea3BiPTBm/
- Facebook: https://www.facebook.com/NASASCaN/videos/how-nasa-uses-gravity-and-radio-waves-to-study-planets-and-moons/8368792419872400/
- Telegram: https://t.me/apod_telegram/16568 (music-only candidate; cannot validate speech-to-text quality)

## Actual calls
- Instagram `media_instagram_preflight`: FAILED with `voicebridge_http_error`, HTTP 429, retryable true.
- Instagram `media_instagram_start`: returned `status:ok`, `confirmation_probe_executed:true`, `phase:R3-E2`, `real_media_start:false`, `provider_work:false`, `provider_charge:false`, `external_mutation:false`.
- Facebook `media_facebook_start`: returned same probe-only result, `phase:R3-E3`.
- Telegram `media_telegram_start`: returned same probe-only result, `phase:R3-E4`.
- Remote krc-cobalt: Docker active, Cobalt local HTTP 200, /opt filesystem 38GB available at test time.

## Acceptance verdict
- E2/E3/E4 **confirmation probes PASS**.
- E2 preflight **FAIL HTTP 429**; cause not established.
- E2/E3/E4 actual provider retrieval, audio extraction, STT, job status, pagination, durable reread **NOT TESTED**. No job IDs produced. Do not claim end-to-end PASS.
- Telegram selected test item may lack speech; replace with verified speech video before STT acceptance.
- No provider credits used, no configuration changes, no public publication.

## Next gate
Diagnose MCP/VoiceBridge 429 using canonical service URL and safe request correlation; verify whether E2–E4 installed sentinel apps intentionally expose only confirmation probes. Deploying actual execution-capable tools requires a separate reviewed implementation, not repeated sentinel calls. Run real E2E only when the execution tools actually support it, with suitable public media and provider safeguards.
