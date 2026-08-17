# MEDIA BETA Current State
Канонічний знімок фактичного стану реалізації для відновлення роботи без припущень.

Version: 1.3
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-17

## Executive state

Current phase: `A4 - Live transcript validation`

Current state:

`CODE_READY / CI_GREEN / RENDER_API_BRIDGE_READY / BETA_SERVICE_LIVE / MEDIA_CONFIGURED / A3_COMPLETE`

Dedicated Render MEDIA BETA is live on the Free plan. All three service-level beta secrets are configured. Health returns HTTP 200 and `media_transcript.configured=true`. Production VoiceBridge health was rechecked separately and remains `status=ok`.

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

## Render beta evidence

Service:
`voicebridge-krc-media-beta-kolemasakar`

Service ID:
`srv-da1kic5bedkc73d6fk60`

Endpoint:
`https://voicebridge-krc-media-beta-kolemasakar.onrender.com`

Verified configuration:
- branch `agent/krc-media-transcript`;
- plan `free`;
- media mode `closed_beta`;
- providers `youtube_captions`, `assemblyai_stt`;
- `configured=true`;
- language hints `auto`, `uk`, `ru`, `en`;
- `subtitle_first=true`;
- max duration 3600 sec;
- max concurrent jobs 1;
- daily STT budget 7200 sec.

Latest successful post-secret deploy observed by inspect:
- deploy ID `dep-da1l56n40ujc73bso600`;
- status `live`;
- commit `7aa415247835d337373888db932f89549feb14c5`.

Final A3 verification workflow:
- run `32055491376`;
- beta health HTTP 200;
- beta media mode `closed_beta`;
- beta media configured `true`;
- production `voicebridge-cloud-us` health HTTP 200;
- production status `ok`.

## Configuration incident resolved

First redeploy after adding secrets failed at runtime because at least one `KRC_MEDIA_BETA_CODES` entry was shorter than the required 12 characters.

Observed startup error:
`KRC_MEDIA_BETA_CODES entries must contain 12 to 128 characters.`

The tester-code value was corrected and redeployed successfully. No secret values are recorded here.

## Completed gates

- A1 architecture/isolation: COMPLETE;
- A2 resource protection in code: COMPLETE;
- GitHub -> Render API bridge: COMPLETE;
- dedicated Free Render beta service: COMPLETE;
- branch isolation: COMPLETE;
- beta service secrets configured: COMPLETE;
- beta health HTTP 200: COMPLETE;
- `media_transcript.configured=true`: COMPLETE;
- production health final check: COMPLETE;
- A3 Render beta deployment: COMPLETE.

## Not complete

- real YouTube captions-path acceptance;
- real AssemblyAI fallback acceptance;
- UK/RU/EN live media tests;
- auto-language test;
- invalid tester-code behavior live check;
- >60 min rejection live check;
- concurrency rejection live check;
- quota exhaustion simulation;
- provider cleanup verification;
- separate GPT Builder beta;
- GPT Preview/Free-plan tests;
- external tester rollout;
- public media release.

## Exact next action

Begin A4 live transcript validation from `05_TEST_PLAN.md`.

First acceptance should use a short public YouTube video with usable captions to validate the subtitle-first path without consuming AssemblyAI STT quota. Then test an STT-fallback video separately.

Do not merge PR #8 or PR #28 merely to perform A4 beta testing.
