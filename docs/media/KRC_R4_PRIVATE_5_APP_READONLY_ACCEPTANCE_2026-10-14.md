# KRC R4 Private 0.1.1 — read-only five-app acceptance probe
Date: 2026-10-14. This is an independent probe through existing connected MCP apps and the installed private plugin's metadata. No MEDIA start, Gemini execution, Facebook/Instagram/Telegram processing, deploy or publication.

## Private plugin identity
Plugin Creator source `plugins_6acef8a60d708191bf37778f71e4562d`, version `0.1.1`, release `pluginrel_6acefb01efc08191a91d448928c57e47`, USER / PRIVATE. Direct `.app.json` confirmed five exact registered mappings:
- R3C `asdk_app_6aaaf8ca113c8191a4ac53f8793833a4`
- E1 `asdk_app_6ab26b061fb4819180fa096638f1e4df`
- E2 `asdk_app_6aaeae197c9081918b90e46f5bb09615`
- E3 `asdk_app_6aaf262767d8819199146dc84b8e1ee8`
- E4 `asdk_app_6aaf292e653481918c75767dea004c5c`
Prompt retains NEVER call media_telegram_start. Note this is policy-level, not a server-enforced kill switch.

## Direct readonly checks
- R3C `media_get_capabilities`: PASS, `request_id=5ba61dff-813c-4edc-975d-6af411d11ebc`, configured true; durable_store postgres, restart_resilient_jobs true; automatic_paid_fallback false, paid_retrieval_fallback false, paid_stt_fallback false. Backend advertises all four platforms. Youtube Gemini model reported `gemini-3.8-flash` (observed drift from earlier 3.7, not diagnosed here).
- E1 `media_youtube_preflight` URL `https://www.youtube.com/watch?v=jNQXAC9IVRw`: PASS, request `0ac0b7e2-e5b0-4cfa-b3f5-460ce01bc557`, can_continue true, consent_required true, consent_tier free, estimated retrieval credits 0, fallback false. No provider call.
- E2 `media_instagram_preflight` URL `https://www.instagram.com/reel/Dcea3BiPTBm/`: PASS, request `93a34b9a-6cc3-4039-bdca-8bf43926660f`, can_continue true, Cobalt retrieval + AssemblyAI STT, credits estimate 0, fallback false. No provider call.
- E3 Facebook `media_non_youtube_status` historical job `KRCM_19880d52-305d-48e5-8bf1-f793bba81391`: returned HTTP 404; correlation `fcbd8e9e-97e6-415f-afe6-45494ab38ab8`. Job previously COMPLETED with expiry `2026-10-14T03:22:10.835Z` and was independently read back before TTL. The 404 does not prove that the E3 connector fails; it does not establish a fresh status readback PASS either.
- E4 Telegram `media_non_youtube_status` historical job `KRCM_afe3cfb7-cbec-44b2-a17a-ce2d76bd3e94`: HTTP 404; correlation `e709f28a-7469-41d2-8d13-2884dacefc0b`. Earlier historical COMPLETED Telegram job has expired. No Telegram LIVE attempt was made.

## Acceptance matrix, exact scope
| Mapping | Registration | Read-only functional probe |
|---|---|---|
| R3C | PASS | PASS |
| E1 | PASS | PASS preflight |
| E2 | PASS | PASS preflight |
| E3 | PASS | PARTIAL (expired job 404) |
| E4 | PASS | PARTIAL (expired job 404) |

## Explicit limitation
These tools were called from the **current conversation** against pre-connected component apps; the plugin metadata was checked independently via Creator. This is **NOT a demonstration that a NEW chat selected into the composite private plugin successfully invokes each app through its own mappings**. A new chat in the plugin UI is still necessary for composite wiring acceptance. E4 exported live start remains blocked by current owner policy. No fake PASS, no forced fresh Telegram job.

## Verdict
All five app registrations PASS; R3C, E1, E2 read-only probes PASS; E3/E4 read-only status routes reachable but expired-id HTTP 404, PARTIAL. Composite plugin new-chat handoff OPEN. Production/global/public release HOLD.
