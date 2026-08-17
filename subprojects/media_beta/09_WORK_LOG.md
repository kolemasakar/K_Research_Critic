# MEDIA BETA Work Log
Хронологічний журнал суттєвих робіт і перевірок підпроєкту для аудиту та відновлення контексту.

Version: 1.3
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

Read-only verification after correction observed:
- deploy `dep-da1l56n40ujc73bso600` live;
- beta health HTTP 200;
- `media_transcript.configured=true`;
- media mode `closed_beta`;
- plan `free`;
- branch isolation intact.

Final A3 verification workflow run `32055491376`:
- beta health HTTP 200;
- beta configured true;
- production `voicebridge-cloud-us` health HTTP 200;
- production `status=ok`.

Phase A3 result: COMPLETE.

Current next operational step: `A4 - Live transcript validation`.

Start with a short public YouTube video that has usable captions to validate subtitle-first without AssemblyAI STT quota consumption.

## Logging rule

Append only material implementation, deployment, acceptance, failure, architecture/provider, resource-limit, promotion, or rollback events. Never log credential values, tester codes, hidden reasoning, or full transcripts.
