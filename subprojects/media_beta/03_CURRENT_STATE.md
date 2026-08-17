# MEDIA BETA Current State
Канонічний знімок фактичного стану реалізації для відновлення роботи без припущень.

Version: 1.5
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-17

## Executive state

Current phase: `A4 - Live transcript validation`

Current state:

`A3_COMPLETE / BETA_LIVE / MEDIA_CONFIGURED / A4_SERVER_SIDE_YOUTUBE_INGRESS_BLOCKED / ARCHITECTURE_DECISION_REQUIRED`

Dedicated Render MEDIA BETA remains live on the Free plan. Health returns HTTP 200 and `media_transcript.configured=true`. Production VoiceBridge remains isolated. The blocker is now proven to be YouTube anti-bot enforcement against cloud/datacenter ingress, not a missing PO-token plugin or AssemblyAI failure.

## Repositories

KRC:
- repo `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- draft PR #8;
- public GPT and `main` unchanged.

VoiceBridge:
- repo `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- draft PR #28;
- production service unchanged.

## Render beta

Service: `voicebridge-krc-media-beta-kolemasakar`.

Service ID: `srv-da1kic5bedkc73d6fk60`.

Endpoint: `https://voicebridge-krc-media-beta-kolemasakar.onrender.com`.

Verified base configuration:
- plan `free`;
- media mode `closed_beta`;
- `configured=true`;
- subtitle-first true;
- max duration 3600 sec;
- max concurrent jobs 1;
- daily STT budget 7200 sec;
- language hints auto/uk/ru/en.

## A4.1 live test evidence

Test URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Authentication checks:
- bearer auth: PASS;
- invalid beta code rejected with `MEDIA_BETA_ACCESS_DENIED`: PASS;
- owner beta code accepted: PASS;
- job creation/lifecycle start: PASS.

Attempt 1:
- job `KRCB_1c137194-3b23-4ed9-ab1e-fa5a49255cc9`;
- `FETCHING_MEDIA` -> `FAILED`;
- `MEDIA_FETCH_FAILED`;
- YouTube: `Sign in to confirm you're not a bot`;
- `stt_seconds_charged=0`.

Attempt 2 after `web_embedded,android_vr` fallback:
- job `KRCB_03d37ccd-4059-4b0c-9675-6f2568d4c207`;
- same YouTube anti-bot failure;
- `stt_seconds_charged=0`.

Attempt 3 after `mweb` + PO Token Provider:
- job `KRCB_981465dc-e400-470f-a236-c5414c26bd63`;
- same YouTube anti-bot failure;
- `stt_seconds_charged=0`.

AssemblyAI has not been consumed by any of these failures.

## A4 remediation evidence

R1:
- explicit yt-dlp clients `web_embedded,android_vr`;
- CI/deploy PASS;
- live retest did not resolve the challenge.

R2:
- yt-dlp client `mweb`;
- `bgutil-ytdlp-pot-provider` 1.3.1;
- local PO Token Provider at `127.0.0.1:4416` in the same beta container;
- `yt-dlp[default]==2026.07.04`;
- Node.js 24 EJS runtime;
- ffmpeg retained;
- no personal YouTube cookies;
- no additional Render service or paid resource;
- VoiceBridge CI PASS;
- isolated Render workflow `32059276099` PASS;
- deploy LIVE and health/configuration PASS.

## Decisive PO-provider diagnostic

One-shot Docker diagnostic run `32060462596`, job `95480351954`, built the same beta image and verified:
- local bgutil provider starts and responds to `/ping`;
- yt-dlp version is `2026.07.04`;
- Node.js EJS runtime is available;
- yt-dlp reports `PO Token Providers: bgutil:http-1.3.1 (external)`;
- extraction of the acceptance URL still ends with `Sign in to confirm you're not a bot`;
- yt-dlp return code is 1.

Conclusion: the provider/plugin/runtime wiring is functional. The current failure is a cloud/datacenter-IP YouTube bot challenge that the PO-token provider does not remove. Repeating server-side Render/GitHub-runner fetch attempts is not an evidence-based next step.

The one-shot diagnostic workflow was removed after use.

## Completed gates

- A1 architecture/isolation: COMPLETE;
- A2 resource protection in code: COMPLETE;
- A3 dedicated Render beta deployment: COMPLETE;
- beta authentication live checks: PARTIAL COMPLETE;
- R1 no-cookie client fallback: TESTED / INSUFFICIENT;
- R2 PO Token Provider: IMPLEMENTED / CI PASS / DEPLOYED / INTEGRATION VERIFIED;
- server-side cloud YouTube ingress blocker: CONFIRMED.

## Not complete

- successful real YouTube transcript acceptance;
- captions-path acceptance;
- AssemblyAI fallback acceptance;
- UK/RU/EN live matrix;
- auto-language acceptance;
- >60 min rejection live check;
- concurrency rejection live check;
- quota exhaustion simulation;
- provider cleanup verification;
- separate GPT Builder beta;
- GPT Preview/Free-plan tests;
- external tester rollout;
- public media release.

## Architecture decision required

Recommended next beta ingress architecture:

`client-assisted / browser-assisted acquisition`

Target flow:
```text
YouTube URL
 -> beta job/session
 -> browser helper or existing VoiceBridge extension acquires captions/tab audio through tester residential IP
 -> upload captions/audio to isolated beta backend
 -> AssemblyAI only when captions are unavailable
 -> timestamped transcript
 -> existing KRC claim/CriticProfile workflow
```

Why recommended:
- avoids YouTube datacenter-IP anti-bot path;
- no YouTube cookies stored in Render;
- no residential proxy subscription;
- preserves Render Free plan;
- reuses existing VoiceBridge browser capability;
- suitable for owner + 2-3 tester closed beta.

Alternative architectures requiring explicit approval include paid residential proxy ingress or cloud use of personal YouTube cookies. Personal cookies are not the default recommendation.

Do not merge PR #8 or PR #28 merely to continue A4 beta testing.
