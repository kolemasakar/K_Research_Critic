# P1 verified Instagram 599.33s media, incomplete start and Facebook discovery (2026-10-13)

## Approved task
Find appropriate test videos; execute independent admissibility check, one bounded FREE_ONLY start per verified public URL, and verify complete job, pages, audio checkpoints and cost. Keep Telegram blocked and prevent consequential POST retries on uncertainty.

## Evidence: Instagram — technically qualified video
- Public permalink: `https://www.instagram.com/tv/B3It-ECHZrA/`.
- Independent extractor: temporary user-owned `yt-dlp` under `/tmp/krc_p1_ytdlp` on krc-cobalt, no account authentication. Original MP4 downloaded strictly for metadata/speech testing and removed afterward.
- MP4 physical size **48,301,351 bytes**. Container duration **599.330249s**, within required **480–720 seconds**.
- AAC (`mp4a.40.2`), **2 channels**, **44,100 Hz** audio.
- Automated VAD `webrtcvad` (aggressiveness 2) on separate approximately 13s windows around positions 30s/300s/560s: **417/433 = 96.3%**, **403/433 = 93.1%**, **422/433 = 97.5%** speech-positive 30ms frames. These are machine detection of speech-like activity, not a human confirmation of language or spoken content. `HUMAN_AUDIO_SPOTCHECK=UNVERIFIED`.
- R3C Instagram preflight: `can_continue=true`, `automatic_paid_fallback=false`, `estimated_retrieval_credits=0`, `provider=cobalt`, `stt_provider=assemblyai`, request ID `757d1d87-ba4e-453b-9db7-61897bf33d7a`.
- Pre-start scoped lookup HTTP 404 (no reusable job found).

## Actual Instagram E2 start result
- One invocation of E2 `media_instagram_start(url,language_hint=auto)` returned **`McpServerError: Invalid params`**, no job ID or backend receipt. NO second start attempted.
- After response, read-only Instagram lookup of same URL returned HTTP 404 (`retryable=false`), request correlation `addc8b34-0423-40f6-a21f-8d020fcf3ffa`. Read-only Neon on documented `plain-snow-71973546` project (`production` default branch) returned zero managed/client jobs. The current backend DSN target has not been independently matched to this connected Neon project.
- Verdict: `INSTAGRAM_INPUT_TECHNICALLY_VERIFIED`, `INSTAGRAM_START_TOOL_CONTRACT_ERROR`, `CONSEQUENTIAL_BACKEND_START_NOT_CONFIRMED`, `NEW_JOB_NOT_OBSERVED`, `TRANSCRIPT_NOT_AVAILABLE`. Do not claim recorded credits=0 since no job-level billing artifact exists.
- Media download was a non-provider public MP4 verification, not the mediated production MEDIA STT job.

## Facebook measured rejects
Independent video extractor returned durations:
- `https://www.facebook.com/TED/videos/what-if-advertising-was-honest/960391431961127/` **211.24s**.
- `https://www.facebook.com/BFMradio/videos/mydins-managing-director-recently-suggested-that-rice-millers-were-hoarding-loca/666728469340826/` **200.8s**.
- `https://www.facebook.com/BBCGlobalFB/videos/young-people-cant-find-jobs-what-can-we-do-about-itwith-data-showing-that-gen-z-/1116161403949925/` **54.955s**.
- `https://www.facebook.com/NewsWatchPlusPH/videos/injustice-and-gross-violation-of-human-rightswatch-baguio-city-mayor-benjamin-ma/10070633926374209/` **159.799s**.
- `https://www.facebook.com/TBN/videos/god-will-suffer-with-you/540084995115487/` **370.987s**.
- Other candidates failed publicly accessible extraction or timed out; do not assign duration.
- No qualifying **480–720s** Facebook video has been verified, thus `FACEBOOK_LONG_START_NOT_RUN`.

## Safety and limitations
- No production code changes, no Telegram start, no paid fallback, no job creation confirmed.
- Vimeo/TED/YouTube descriptions or words such as '10 minute interview' were not used as video duration evidence.
- Earlier concurrent cold relay runtime patch is separately documented and read-only tests PASS. Real MEDIA acceptance still OPEN.

## Next required gates
1. Determine why the current E2 start MCP action rejects a schema-valid `{url,language_hint}` as `Invalid params`. Audit connector/tool contract and consequential action-confirmation interface, not brute-force attempts to circumvent it.
2. Find one Facebook public canonical speech video with independently measured actual MP4 length 480–720 seconds, preflight/cost check before consequential start.
3. For the confirmed Instagram video, resume one allowed start only after contract repair/explicit action confirmation and a scoped read-only lookup to prevent duplication. Poll status/segments within effective job TTL.
4. Check beginning/middle/end textual alignment against audible speech and full pagination with UTF-16/count, timecodes and credits once a COMPLETED job exists; don't convert machine VAD into human speech accuracy acceptance.
