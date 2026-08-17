# MEDIA BETA Work Log
Хронологічний журнал суттєвих робіт і перевірок підпроєкту для аудиту та відновлення контексту.

Version: 1.5
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

First redeploy after service configuration failed because at least one `KRC_MEDIA_BETA_CODES` entry was shorter than 12 characters.

Correction: tester-code value fixed; redeploy repeated; deployment reached live state. No credential values are recorded here.

## 2026-08-17 - A3 final verification completed

Final A3 verification workflow run `32055491376`:
- beta health HTTP 200;
- beta configured true;
- production `voicebridge-cloud-us` health HTTP 200;
- production `status=ok`.

Phase A3 result: COMPLETE.

## 2026-08-17 - A4.1 server-side acceptance attempts

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Live checks before YouTube acquisition:
- bearer token authentication PASS;
- intentionally invalid beta code returned `MEDIA_BETA_ACCESS_DENIED` PASS;
- owner beta code accepted PASS;
- job creation PASS.

Attempt 1:
- job `KRCB_1c137194-3b23-4ed9-ab1e-fa5a49255cc9`;
- `FAILED / MEDIA_FETCH_FAILED`;
- YouTube `Sign in to confirm you're not a bot`;
- `stt_seconds_charged=0`.

## 2026-08-17 - A4 remediation R1

Applied yt-dlp clients `web_embedded,android_vr` to metadata, captions and audio acquisition.

CI PASS and isolated beta redeploy PASS.

Attempt 2:
- job `KRCB_03d37ccd-4059-4b0c-9675-6f2568d4c207`;
- same anti-bot failure;
- `stt_seconds_charged=0`.

R1 conclusion: insufficient for cloud ingress.

## 2026-08-17 - A4 remediation R2: PO Token Provider

Implemented in VoiceBridge beta branch:
- yt-dlp client `mweb`;
- `bgutil-ytdlp-pot-provider` 1.3.1;
- local bgutil HTTP provider on `127.0.0.1:4416` in the same Render container;
- `yt-dlp[default]==2026.07.04`;
- Node.js 24 EJS runtime;
- ffmpeg retained;
- no personal YouTube cookies;
- no second Render service and no paid instance.

VoiceBridge CI: PASS.

Isolated Render remediation workflow run `32059276099`: PASS; beta service LIVE; health/configuration PASS.

Attempt 3:
- job `KRCB_981465dc-e400-470f-a236-c5414c26bd63`;
- same anti-bot failure;
- `stt_seconds_charged=0`.

## 2026-08-17 - PO-provider wiring diagnostic

A one-shot Docker diagnostic workflow was created only on the VoiceBridge beta branch.

Diagnostic run `32060462596`, job `95480351954` verified:
- current beta Docker image builds;
- bgutil provider starts successfully and responds to `/ping`;
- yt-dlp version `2026.07.04`;
- Node.js EJS runtime available;
- yt-dlp explicitly reports `PO Token Providers: bgutil:http-1.3.1 (external)`;
- direct simulated extraction of the same acceptance URL still ends with YouTube `Sign in to confirm you're not a bot`;
- yt-dlp return code 1.

Conclusion: R2 integration is functional. The blocker is server-side cloud/datacenter-IP YouTube anti-bot enforcement, not missing provider/plugin/runtime wiring.

The one-shot diagnostic workflow was deleted after the test.

All three A4.1 failures occurred before AssemblyAI; total STT charged by these attempts remained 0.

## 2026-08-17 - Architecture decision gate opened

Repeated server-side Render/GitHub cloud-IP retries are stopped.

Recommended next closed-beta architecture: client-assisted/browser-assisted ingestion using the tester's residential connection and existing VoiceBridge browser capability where practical.

Target:
```text
YouTube URL
 -> one-time beta session
 -> browser helper/extension acquires captions or tab audio
 -> derived captions/audio uploaded to beta backend
 -> AssemblyAI only if captions unavailable
 -> existing KRC transcript/claim workflow
```

This preserves the Free Render target and avoids placing personal YouTube cookies in cloud infrastructure.

Alternative paid residential proxy or personal-cookie strategies require explicit user approval; cookies are not the recommended default.

## Logging rule

Append only material implementation, deployment, acceptance, failure, architecture/provider, resource-limit, promotion, or rollback events. Never log credential values, tester codes, hidden reasoning, or full transcripts.
