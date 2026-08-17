# MEDIA BETA Work Log
Хронологічний журнал суттєвих робіт і перевірок підпроєкту для аудиту та відновлення контексту.

Version: 1.4
Status: ACTIVE

## 2026-08-17 - Media URL upgrade initiated

Approved goal: public YouTube URL -> transcript -> material claims -> CriticProfile gate -> independent research -> Critic -> final claim verification/report. Existing text mode remains intact.

## 2026-08-17 - Feature branches and draft PRs

KRC: branch `agent/video-url-research`, draft PR #8.

VoiceBridge: branch `agent/krc-media-transcript`, draft PR #28.

Automated implementation CI reached green state.

## 2026-08-17 - Free-tier review and optimization decision

Approved direction: subtitle-first, lower bitrate fallback audio, closed beta first, sustainable free architecture later.

## 2026-08-17 - Closed MEDIA BETA controls implemented

Implemented: owner + up to 3 testers, per-tester code, max video 60 min, concurrency 1, AssemblyAI fallback budget 7200 sec/UTC day, captions outside STT quota, fallback audio mono 16 kHz ~32 kbps, separate beta GPT package, production isolation.

## 2026-08-17 - Documentation subproject created

Canonical root: `subprojects/media_beta/`.

## 2026-08-17 - GitHub to Render API bridge established

`RENDER_API_KEY` stored as VoiceBridge GitHub Actions secret.

First read-only inspect run `32050872616`: PASS / Render API HTTP 200 / beta service absent / production untouched.

## 2026-08-17 - Dedicated Free Render beta service created

Bootstrap run `32051889378`: PASS.

Created service `voicebridge-krc-media-beta-kolemasakar`, ID `srv-da1kic5bedkc73d6fk60`.

Verified branch `agent/krc-media-transcript`, plan `free`, production service not modified.

## 2026-08-17 - Initial beta deploy and health verified

Post-bootstrap inspect run `32052056782`: PASS.

Initial health: HTTP 200, `closed_beta`, subtitle-first true, limits 3600 sec / concurrency 1 / STT 7200 sec/day, `configured=false` before service-level beta configuration.

## 2026-08-17 - Beta configuration startup incident resolved

First redeploy after service configuration failed with:

`KRC_MEDIA_BETA_CODES entries must contain 12 to 128 characters.`

Cause: at least one tester-code entry was shorter than 12 characters.

Correction: tester-code value fixed; redeploy repeated; deployment reached live state. No credential values are recorded here.

## 2026-08-17 - A3 final verification completed

Final A3 verification workflow run `32055491376`:
- beta health HTTP 200;
- beta configured true;
- production `voicebridge-cloud-us` health HTTP 200;
- production `status=ok`.

Phase A3 result: COMPLETE.

## 2026-08-17 - A4.1 first live media request

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Live checks:
- bearer token authentication PASS;
- intentionally invalid beta code returned `MEDIA_BETA_ACCESS_DENIED` PASS;
- owner beta code accepted PASS;
- new job created PASS.

Attempt 1 final result:
- `FAILED`;
- `MEDIA_FETCH_FAILED`;
- YouTube reported `Sign in to confirm you're not a bot`;
- failure occurred before captions/STT;
- `stt_seconds_charged=0`.

## 2026-08-17 - A4 remediation R1

Applied explicit yt-dlp player clients `web_embedded,android_vr` to metadata, captions and audio acquisition.

CI PASS and isolated beta redeploy PASS.

Attempt 2 against the same URL:
- `FAILED` with the same YouTube anti-bot challenge;
- `stt_seconds_charged=0`.

R1 conclusion: insufficient for Render cloud ingress.

## 2026-08-17 - A4 remediation R2: PO Token Provider

Current yt-dlp guidance was reviewed. Recommended route for current YouTube enforcement is a PO Token Provider with the `mweb` client. Manual per-video PO-token extraction is not the target design.

Implemented in VoiceBridge beta branch:
- yt-dlp client changed to `mweb`;
- `bgutil-ytdlp-pot-provider` pinned to 1.3.1;
- local bgutil HTTP provider embedded in the same Render container on port 4416;
- `yt-dlp[default]` pinned to 2026.07.04;
- Node.js 24 explicitly enabled as EJS runtime;
- ffmpeg retained;
- provider stack added without personal YouTube cookies;
- no second Render service and no paid instance added.

VoiceBridge normal CI after R2: PASS.

Isolated Render remediation workflow:
- run `32059276099`;
- target only beta service ID `srv-da1kic5bedkc73d6fk60`;
- Docker build/deploy of commit `d7864ad1625f815613deaea8043b4f1786768c61` completed successfully;
- beta service reached LIVE;
- beta health/configuration PASS.

Current next operational step:
- repeat the same A4.1 URL with a new media job;
- inspect whether the PO provider resolves YouTube ingress;
- if successful, validate subtitle-first and zero STT usage;
- if the same anti-bot challenge persists, stop looping retries and evaluate a different ingress architecture before using personal cookies.

## Logging rule

Append only material implementation, deployment, acceptance, failure, architecture/provider, resource-limit, promotion, or rollback events. Never log credential values, tester codes, hidden reasoning, or full transcripts.
