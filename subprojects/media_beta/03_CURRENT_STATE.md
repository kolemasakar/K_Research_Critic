# MEDIA BETA Current State
Канонічний знімок фактичного стану реалізації для відновлення роботи без припущень.

Version: 1.4
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-17

## Executive state

Current phase: `A4 - Live transcript validation`

Current state:

`A3_COMPLETE / BETA_LIVE / MEDIA_CONFIGURED / A4_YOUTUBE_INGRESS_REMEDIATION_DEPLOYED`

Dedicated Render MEDIA BETA remains live on the Free plan. Health returns HTTP 200 and `media_transcript.configured=true`. Production VoiceBridge remains isolated and was not targeted by A4 remediation.

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
- job reached `FETCHING_MEDIA`;
- final status `FAILED`;
- error `MEDIA_FETCH_FAILED`;
- YouTube response: `Sign in to confirm you're not a bot`;
- `stt_seconds_charged=0`.

Attempt 2 after `web_embedded,android_vr` client fallback:
- job again reached `FETCHING_MEDIA`;
- final status `FAILED` with the same YouTube anti-bot challenge;
- `stt_seconds_charged=0`.

Conclusion: failure occurs before captions/STT acquisition at YouTube ingress from Render cloud IP. AssemblyAI was not consumed.

## A4 YouTube ingress remediation

First remediation:
- explicit yt-dlp clients `web_embedded,android_vr`;
- deployed successfully;
- did not resolve the anti-bot challenge for the acceptance URL.

Second remediation implemented according to current yt-dlp guidance:
- yt-dlp client changed to `mweb`;
- `bgutil-ytdlp-pot-provider` 1.3.1 added;
- local PO Token Provider runs inside the same beta container on port 4416;
- no additional Render service created;
- no YouTube account cookies introduced;
- yt-dlp installed as `yt-dlp[default]==2026.07.04`;
- Node.js 24 explicitly enabled as EJS runtime;
- ffmpeg retained;
- provider remains internal to the beta container.

VoiceBridge CI after the provider changes: PASS.

Isolated Render remediation workflow run `32059276099`: PASS.

Render build/deploy of commit `d7864ad1625f815613deaea8043b4f1786768c61`: COMPLETE / LIVE.

Post-deploy beta health/configuration: PASS.

## Completed gates

- A1 architecture/isolation: COMPLETE;
- A2 resource protection in code: COMPLETE;
- A3 dedicated Render beta deployment: COMPLETE;
- beta authentication live checks: PARTIAL COMPLETE;
- YouTube anti-bot root cause: IDENTIFIED;
- first no-cookie client fallback: TESTED / INSUFFICIENT;
- PO Token Provider remediation: IMPLEMENTED / CI PASS / DEPLOYED.

## Not complete

- successful real YouTube transcript acceptance after PO remediation;
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

## Exact next action

Repeat A4.1 against the same YouTube URL using a new job after the PO Token Provider deployment.

Expected successful subtitle-first result:
- `status=COMPLETED`;
- preferably `transcript_source=youtube_captions`;
- `stt_seconds_charged=0`.

If YouTube still returns the anti-bot challenge with the PO provider stack, stop retrying the same cloud-IP strategy and evaluate the next approved ingress architecture rather than introducing personal YouTube cookies by default.

Do not merge PR #8 or PR #28 merely to continue A4 beta testing.
