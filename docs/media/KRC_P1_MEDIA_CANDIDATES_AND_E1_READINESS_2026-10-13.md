# KRC P1 — test-media candidate verification, 2026-10-13

## Admission objective
Under approved P1 runbook `docs/media/KRC_LONG_MEDIA_LIVE_TEST_PROTOCOL_2026-10-10.md`, require genuinely publicly accessible Instagram/Facebook 480–720s media with speech, independently verified duration/audio before single provider start. A YouTube comparator is permitted on its own Gemini Free consent and gate. No unsupported candidate may be promoted to VERIFIED.

## Discovered verified reference
- **YouTube TED reference**: `https://www.youtube.com/watch?v=58rMMTJUp_U` — Christi Gendron, *The Science of Lifespan — and the Impact of Your Five Senses*. Original TED speaker page `https://www.ted.com/speakers/christi_gendron` states **10:54 (654 seconds)**, English speaking TED talk. Source also corroborated on TED official topic indexes. **This verifies editorial duration/speech character on the TED edition**; exact YouTube video stream byte duration/audio track and source parity were not independently measured via `ffprobe`. Do not mark ffprobe PASS.
- R3C YouTube preflight `can_continue=true`, Gemini Free `gemini-3.7-flash`, `consent_required=true`, `automatic_paid_fallback=false`, request_id `62866b58-b097-4c9c-b49f-c11f6e40bc36`.
- Prior YouTube lookup: HTTP 404 (no matching reusable job established).
- Authorized single E1 `media_youtube_start` attempted with previously given explicit Google Gemini Free data-use consent. Result **`voicebridge_not_ready`** `failure_stage=readiness`, `consequential_post_attempted=false`, `readiness_health_attempts=22`. **No provider/media start reached**. No retry.
- Render logs for 2026-10-13 16:21 UTC show two near-simultaneous readiness 429, one `relay_rejected` and one `relay_success`, VoiceBridge `service_started` 16:21:59Z, R3C MCP 200 responses 16:22:02Z and 16:22:05Z. There is insufficient request-level attribution to claim which concurrent operation caused the rejected relay; do not conflate the failed E1 start with a successful E2E job. This suggests a cold concurrency/cooldown or start-window gate requiring isolation in P0 regression.
- These operations do not demonstrate `credits_charged=0` on a created job because there was no job; Gemini Free-only configuration was checked, no paid fallback activated.

## Instagram/Facebook discovery
- Public searches for genuine 8–12 min Instagram and Facebook posts/reels were performed. No pair of candidate canonical URLs met **all** requirements of independently sourced 480–720s duration, playable public page and speech/audio confirmation. Do not invent qualifying social URLs or perform provider starts at this stage.
- Historical E2 41.11675s and E3 180.302938s jobs remain short/medium references only, not P1 long evidence.

## Verdict
- YouTube 654s TED editorial reference: `CANDIDATE_EDITORIAL_DURATION_VERIFIED`, stream-parity/ffprobe `UNVERIFIED`.
- YouTube E1 start: `READINESS_BLOCKED_BEFORE_CONSEQUENTIAL_POST`; no long job was created by that call.
- Instagram/Facebook 480–720s accepted candidates: `NOT_FOUND_VERIFIED`.
- Telegram: `BLOCKED` by safety, no bypass.
- P1 live transcription gates: `NOT_PASSED`.
- P0 sequential cold-read three successful cycles are still valid, but **concurrent cold recovery** is a separate observed failure scenario requiring bounded independent regression. Do not silently regress previous PASS claim or imply that it proved concurrent reliability.

## Next safe actions
1. Inspect R3C request correlation + exact cold relay cooldown/lock rules for concurrent cold calls, without secrets or new execution.
2. Acquire verified Instagram/Facebook eligible media through independent player metadata or lawful non-paid `ffprobe` byte retrieval, checking real speech.
3. After admission PASS, execute exactly one free-only start per URL; inspect status/segments immediately within retention TTL, no duplicate.
4. Keep P1 open until independent actual long-media completed jobs and audio checks exist.
