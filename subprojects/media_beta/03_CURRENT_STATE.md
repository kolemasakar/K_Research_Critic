# MEDIA BETA Current State
Канонічний знімок фактичного стану реалізації для відновлення роботи без припущень.

Version: 1.2
Status: ACTIVE_CHECKPOINT
Checkpoint date: 2026-08-17

## Executive state

Current phase: `A3 - Dedicated Render beta deployment`

Current state:

`CODE_READY / CI_GREEN / RENDER_API_BRIDGE_READY / BETA_SERVICE_LIVE / SERVICE_SECRETS_PENDING`

The dedicated Render MEDIA BETA service exists and is live on the Free plan. The beta health endpoint returns HTTP 200. Media transcription is not fully configured yet because the three service-level beta secrets are still missing.

## Repositories

KRC:
- repo `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- draft PR #8;
- `main` and the published GPT remain unchanged.

VoiceBridge:
- repo `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- draft PR #28;
- production service remains unchanged.

## Render beta evidence

Dedicated service:

`voicebridge-krc-media-beta-kolemasakar`

Service ID:

`srv-da1kic5bedkc73d6fk60`

Endpoint:

`https://voicebridge-krc-media-beta-kolemasakar.onrender.com`

Bootstrap run `32051889378`: PASS.

Verified:
- branch `agent/krc-media-transcript`;
- plan `free`;
- initial deploy created.

Post-bootstrap inspect run `32052056782`: PASS.

Latest deploy:
- ID `dep-da1kictbedkc73d6fm7g`;
- status `live`;
- commit `4047fabde211b5459f80691713ebc1db7e505b51`.

Health:
- HTTP 200;
- `status=ok`;
- version `0.6.0`;
- media mode `closed_beta`;
- providers `youtube_captions`, `assemblyai_stt`;
- `configured=false`;
- platform `youtube`;
- language hints `auto`, `uk`, `ru`, `en`;
- `subtitle_first=true`;
- max duration 3600 sec;
- max concurrent jobs 1;
- daily STT budget 7200 sec.

`configured=false` is expected until the remaining media secrets are configured.

## Render control

GitHub Actions secret `RENDER_API_KEY` is configured in VoiceBridge and validated. Its value is not stored in repository files or logs.

Control assets:
- `.github/workflows/render-media-beta-control.yml`;
- `.github/workflows/render-media-beta-bootstrap.yml`;
- `.github/workflows/render-media-beta-post-bootstrap-inspect.yml`.

Production target `voicebridge-cloud-us` is not selected by these beta deployment operations.

## Remaining service-level secrets

Configure only on the dedicated beta Render service:
- `KRC_MEDIA_ACTION_TOKEN`;
- `KRC_MEDIA_BETA_CODES`;
- `ASSEMBLYAI_API_KEY`.

Never record their values in repository documentation, checkpoints, reports, or chat output.

## Completed gates

- architecture isolation: COMPLETE;
- resource guards: COMPLETE_IN_CODE;
- GitHub -> Render bridge: COMPLETE;
- beta service creation: COMPLETE;
- Free plan verification: COMPLETE;
- branch isolation verification: COMPLETE;
- initial beta deploy: LIVE;
- beta health reachability: COMPLETE;
- media provider configuration: PENDING SECRETS.

## Not complete

- `media_transcript.configured=true` validation;
- real captions test;
- AssemblyAI fallback test;
- UK/RU/EN live tests;
- auto-language test;
- provider cleanup verification;
- quota/concurrency live tests;
- separate GPT Builder beta;
- GPT Preview/Free-plan tests;
- tester rollout;
- public media release.

## Exact next action

Configure the three service-level secrets on the dedicated beta Render service. Then repeat read-only `/api/v1/health` inspection. Do not start A4 transcript acceptance until `media_transcript.configured=true`.

Do not merge PR #8 or PR #28 merely to continue beta validation.
