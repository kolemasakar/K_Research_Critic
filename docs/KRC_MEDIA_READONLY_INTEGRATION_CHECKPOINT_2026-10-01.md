# KRC MEDIA — read-only integration checkpoint (2026-10-01)

Scope: independent verification following Sentinel Remote infrastructure handoff. No MEDIA processing, paid fallback, container restart, permission change or production configuration change was performed.

## Confirmed checks

- Sentinel Remote infrastructure handoff: Desktop Commander systemd auto-start/crash/reboot tests PASS; Docker/Cobalt Tier-1 PASS (handoff evidence, not repeated destructive tests).
- Independent Desktop Commander connection to krc-cobalt: online.
- Direct R3C read-only `media_get_capabilities`: PASS; request_id `4d18b601-82b7-42c2-933c-fdf669422577`. Earlier direct calls returned HTTP 429; this result demonstrates recovery at the time of this call, **not a proven root cause or permanent fix**.
- From krc-cobalt: VoiceBridge public `/api/v1/health` HTTP 200; local Cobalt `http://127.0.0.1:9000/` HTTP 200.
- Private Plugin release inspected read-only: `0.19.7+portable.20260925`; .app.json still maps five apps (R3C, YouTube, Instagram, Facebook, Telegram). A subsequent user-provided result from the private Plugin UI independently reports successful invocation; see the Plugin UI verification below.

## MEDIA capability result (direct R3C)

- mode `zero_client_managed_beta`, configured `true`, durable_store `postgres`, restart_resilient_jobs `true`, duplicate_start_reuses_job `true`.
- platforms: youtube, instagram, facebook, telegram.
- YouTube: `gemini_youtube_url`, Gemini Free Tier only, model `gemini-3.7-flash`, consent required; Google Free Tier data-use notice must be presented before any new provider work.
- Instagram/Facebook: free Cobalt retrieval configured, AssemblyAI STT configured.
- Telegram: `telegram_public_web` retrieval and AssemblyAI STT configured.
- automatic_paid_fallback, paid_retrieval_fallback and paid_stt_fallback all `false`.
- These are configuration reports; no live provider transcription/retrieval was initiated or validated.

## Private Plugin UI verification (owner-supplied execution result)

- Owner supplied the full structured result of executing **only** `media_get_capabilities` from the private Plugin through `KRC MCP R3C Readonly`.
- Result: SUCCESS, read-only; request_id `8315a39e-d4ca-42b3-8ae3-5e6ffadb9388`; no error, no provider work, no other MEDIA tools.
- Reported capabilities match the direct R3C result: four platforms, PostgreSQL, YouTube Gemini Free Tier with consent, and disabled paid fallback.
- This confirms the **Plugin UI → R3C capabilities** route at the time of the reported test. It does not demonstrate transcription/provider success or identify the root cause of earlier HTTP 429.

## Remaining limitations and next diagnostic gate

1. If HTTP 429 recurs, correlate MCP gateway response headers/body and VoiceBridge request logs before attributing it to backend, proxy, authentication or rate limiting. Do not log bearer tokens or secret values.
2. Docker healthcheck and resource limits remain separate non-blocking infrastructure decisions; Tier-1 status alone does not prove long-term resilience.
3. Full end-to-end MEDIA processing and transcript durability remain untested in this checkpoint. Require separate owner consent before new YouTube provider work; keep paid fallback disabled.

Verdict: **Direct read-only MCP ↔ VoiceBridge PASS; owner-reported private Plugin → MEDIA read-only capabilities PASS; end-to-end MEDIA processing NOT VERIFIED.**
