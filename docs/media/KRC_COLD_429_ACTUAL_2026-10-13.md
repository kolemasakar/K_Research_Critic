# KRC / VoiceBridge cold-start 429 — 2026-10-13 owner-pilot checkpoint

## Scope and safeguards
Private owner-pilot, FREE_ONLY. After owner ended planned pause, performed exactly one initial cold `media_get_capabilities` through R3C, before external health. No provider work, no MEDIA start POST, no paid fallback. R3C runs deployed bounded allowlisted provenance logging.

## Cold first request — FAIL, diagnostic confirmation
- Result of R3C `media_get_capabilities`: `voicebridge_http_error`, `http_status=429`, `retryable=true`, `readonly_health_attempts=22`, `readonly_health_ready=false`.
- Its returned summary: `upstream_server=cloudflare`, `edge_cf_ray=a49ccaf70d1d18cb-FRA`. This refers to the first failed upstream call resulting in the tool error.
- R3C app at **2026-10-13T07:57:19.950466563Z**: `voicebridge_readiness_http_error status=429 attempt=1 diagnostics={'upstream_server': 'cloudflare', 'edge_cf_ray': 'a49ccaf77d4d0d18-FRA'}`. **This is a distinct GET and CF-Ray from the initial failed upstream request**, not a typo.
- R3C app `POST /oauth/token` HTTP 200 at 07:57:18.802681677Z and `POST /mcp` HTTP 200 at 07:58:04.89776126Z, indicating MCP transport succeeded while its embedded VoiceBridge upstream call failed.
- No VoiceBridge app logs between 07:55 and 07:58:59; absence does not prove where 429 was generated.
- **2026-10-13T07:58:59.629117948Z** VoiceBridge app `service_started`.

## External contrast — PASS
- One external, bounded health GET from owner-controlled `krc-cobalt`, `/api/v1/health`, returned **HTTP 200** JSON status=ok, elapsed **13.352 seconds**. Successful-response headers: Content-Type application/json; charset=utf-8, Server cloudflare, x-render-origin-server Render, x-request-id f11bfe03-f9f4-4053-8785-4e929e5bc0b4, CF-RAY a49ccd386f6befff-FRA. These are NOT headers of the failed 429.
- Following the external GET, R3C `media_get_capabilities` succeeded, request_id `2797a0c9-6a9b-480c-898e-b260e1d09308`, configured=true, durable_store=postgres, automatic_paid_fallback=false.
- Conclusion: cold Render→Render traffic yields HTTP 429 while a separate external GET triggers successful wakeup. `Server: cloudflare` establishes proxy participation, not which component emitted the 429. Neither Render edge nor Cloudflare rate limiting is conclusively the originating source.

## Diagnostic gap and next safe action
- Need provider infrastructure request/edge logs matched to **both** CF-Ray values with timestamps and service IDs. The initial 429 tool response did not include x-request-id or application json code; new allowlist did not find those. Render provider support may be required.
- Consider targeted guarded recovery design using an owner-controlled external wake endpoint only if approved, securely authorized and FREE_ONLY, without a permanent keepalive. Must preserve no duplicate start, wait-for-readiness and privacy. Do not assume adding retries solves origin.
- LIVE 8–12 minute Instagram/Facebook audio verification remains open; Telegram safety block remains in force. Previous 17/17 isolated cross-repository tests PASS, full 482 PASS + 17 opt-in, but owner acceptance still PARTIAL.
