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

## Fresh end-to-end YouTube run (owner consent; 2026-10-01)

- Owner explicitly acknowledged Google Gemini Free Tier data-use notice for a fresh run of `https://www.youtube.com/watch?v=bu_DYQAKnuQ`.
- Initial start returned transient `voicebridge_unavailable`; read-only lookup found a newly created PROCESSING job. No duplicate start was attempted.
- New job `KRCM_9d4c8eb0-2f09-432e-bc86-1c330cc3a5d6` subsequently COMPLETED: 30 segments, server-reported `transcript_characters=47393`, credits charged 0, no provider error.
- Read-only segment pagination returned all 30 segments, indices 0–29, `next_cursor=null`, and repeat status/segment read confirmed durable retrieval. Segment text lengths sum to **47383 JS UTF-16 code units**, 10 fewer than server-reported 47393. This discrepancy is **unresolved**; do not claim exact character-count match. No timestamps were supplied.
- Full original returned segment text archived without rewriting in `docs/media/KRC_VIDEO_TRANSCRIPT_42_FRESH_2026-10-01.md` (commit `40d85b6366e901f20c47735172c29dbe73d780d0`).
- This run demonstrates retrieval/transcription and repeat read for this video. It does not prove the scientific correctness of claims in the video or all providers' general reliability.

Current gate: transcript available for claim extraction and source-based fact-check; investigate the 10-character accounting discrepancy separately.
