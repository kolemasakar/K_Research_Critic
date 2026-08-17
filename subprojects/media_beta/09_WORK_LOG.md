# MEDIA BETA Work Log
Хронологічний журнал суттєвих робіт і перевірок підпроєкту для аудиту та відновлення контексту.

Version: 1.2
Status: ACTIVE

## 2026-08-17 - Media URL upgrade initiated

Approved goal: public YouTube URL -> transcript -> material claims -> CriticProfile gate -> independent research -> Critic -> final claim verification/report. Existing text mode remains intact.

## 2026-08-17 - Feature branches and draft PRs

KRC:
- branch `agent/video-url-research`;
- draft PR #8.

VoiceBridge:
- branch `agent/krc-media-transcript`;
- draft PR #28.

Automated implementation CI reached green state.

## 2026-08-17 - Free-tier review and optimization decision

Identified risks: Render outbound, finite AssemblyAI credits, Free Render resources, yt-dlp/YouTube changes, ChatGPT runtime limits.

Approved direction:
- subtitle-first;
- lower bitrate fallback audio;
- closed beta first;
- sustainable free architecture later.

## 2026-08-17 - Closed MEDIA BETA controls implemented

Approved and implemented:
- owner + up to 3 testers;
- per-tester code;
- max video 60 min;
- concurrency 1;
- AssemblyAI fallback budget 7200 sec/UTC day;
- captions do not consume STT quota;
- fallback audio mono 16 kHz ~32 kbps;
- separate beta GPT package;
- production isolation.

## 2026-08-17 - Documentation subproject created

Canonical root:

`subprojects/media_beta/`

Contains architecture, roadmap, current state, runbook, test plan, decision log, sustainable-free target, handoff, and work log.

## 2026-08-17 - GitHub to Render API bridge established

User created Render API credential and stored it only as VoiceBridge GitHub Actions secret `RENDER_API_KEY`.

Created `.github/workflows/render-media-beta-control.yml`.

First read-only inspect run `32050872616`:
- PASS;
- Render API HTTP 200;
- beta service not yet present;
- no deployment;
- production untouched.

## 2026-08-17 - Dedicated Free Render beta service created

Created VoiceBridge bootstrap workflow:

`.github/workflows/render-media-beta-bootstrap.yml`

Bootstrap run:

`32051889378`

Result:

`PASS`

Created dedicated service:

`voicebridge-krc-media-beta-kolemasakar`

Service ID:

`srv-da1kic5bedkc73d6fk60`

Verified:
- branch `agent/krc-media-transcript`;
- plan `free`;
- production `voicebridge-cloud-us` not modified.

## 2026-08-17 - Initial beta deploy and health verified

Created read-only post-bootstrap inspection workflow:

`.github/workflows/render-media-beta-post-bootstrap-inspect.yml`

Run:

`32052056782`

Result:

`PASS`

Observed:
- latest deploy `dep-da1kictbedkc73d6fm7g`;
- deploy status `live`;
- deployed commit `4047fabde211b5459f80691713ebc1db7e505b51`;
- beta health HTTP 200;
- media mode `closed_beta`;
- providers `youtube_captions` and `assemblyai_stt`;
- `subtitle_first=true`;
- limits 3600 sec / concurrency 1 / STT 7200 sec/day;
- `media_transcript.configured=false` because beta service-level secrets are still absent.

Current next operational step:

Configure `KRC_MEDIA_ACTION_TOKEN`, `KRC_MEDIA_BETA_CODES`, and `ASSEMBLYAI_API_KEY` on the dedicated beta Render service, then require `media_transcript.configured=true` before live transcript acceptance.

## Logging rule

Append only material implementation, deployment, acceptance, failure, architecture/provider, resource-limit, promotion, or rollback events. Never log secret values, tester codes, hidden reasoning, or full transcripts.
