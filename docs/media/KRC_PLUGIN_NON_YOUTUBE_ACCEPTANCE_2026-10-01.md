# KRC private Plugin — non-YouTube acceptance checkpoint (2026-10-01)

Scope: Instagram, Facebook, Telegram; read-only infrastructure and capability checks, no provider execution without a real public media URL and consequential-action confirmation.

## Executed live
- R3C `media_get_capabilities` attempted once; tool returned `voicebridge_http_error`, HTTP 429, `retryable=true`. Earlier successful R3C capability checks are historical and do not prove current health.
- Desktop Commander `list_devices`: krc-cobalt online; other listed machines offline.
- krc-cobalt read-only commands: Docker service `active`; local Cobalt HTTP 200 at `127.0.0.1:9000`.
- A guessed VoiceBridge Render hostname returned HTTP 404; this is **not** a verified canonical service URL and is **not** evidence of VoiceBridge outage. Do not reuse that hostname as fact.
- No public Instagram/Facebook/Telegram test URLs were supplied for this acceptance run; do not invent a real public media URL. No new media jobs started.

## Acceptance gates
1. Identify and check canonical VoiceBridge health URL from existing non-secret project configuration or documentation.
2. Correlate R3C HTTP 429 gateway headers/request ID and VoiceBridge logs (without secrets) to isolate rate limiting/auth/proxy/backend; no root cause yet.
3. For each of Instagram, Facebook, Telegram: obtain an actual public video with audio and permissions, preflight where available, one owner-confirmed free-only start, status until terminal, segment pagination, durable repeat-read, zero paid fallback; capture provider and failure codes.
4. Validate duplicate-start reuse using existing jobs without deliberately triggering a second provider job; validate cold start and retry semantics in a separate controlled test.
5. Document PASS/FAIL/BLOCKED per platform. Do not mark E2–E4 fully accepted based solely on configured capabilities or sentinel no-op probes.

## Current verdict
- Infrastructure: remote connection and local Cobalt PASS at test time.
- R3C current capability check: FAIL HTTP 429, retryable; root cause unproven.
- Instagram/Facebook/Telegram full E2E: NOT TESTED in this run (no real URLs, no execution).
- No changes to production, secrets, plugin mappings, paid services, or publication.
