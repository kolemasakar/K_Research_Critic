# MEDIA BETA Operations Runbook
Операційна інструкція для безпечного розгортання, тестування, відкату та керування закритою beta-версією.

Version: 1.0
Status: PREDEPLOY
Updated: 2026-08-17

## 1. Safety rules

- never deploy media beta over the existing production VoiceBridge service;
- never commit secrets;
- never paste provider secrets into GPT instructions;
- never merge a draft media PR solely to simplify testing unless explicitly approved;
- verify production health before and after beta deployment;
- do not expose tester access codes in reports, checkpoints, screenshots, or documentation commits.

## 2. Dedicated Render beta deployment

Repository:

`kolemasakar/VoiceBridge`

Branch:

`agent/krc-media-transcript`

Blueprint:

`render.media-beta.yaml`

Expected service name:

`voicebridge-krc-media-beta-kolemasakar`

Expected public endpoint:

`https://voicebridge-krc-media-beta-kolemasakar.onrender.com`

### Render procedure

1. Open Render Dashboard.
2. Select New -> Blueprint.
3. Connect `kolemasakar/VoiceBridge`.
4. Select branch `agent/krc-media-transcript` if Render does not infer the configured branch.
5. Select `render.media-beta.yaml` as the Blueprint file.
6. Confirm the service is a separate Free service and not `voicebridge-cloud-us`.
7. Configure required secrets in the Render Dashboard.
8. Deploy.
9. Record deployment timestamp and resulting endpoint in `03_CURRENT_STATE.md`.

## 3. Required environment secrets

### `KRC_MEDIA_ACTION_TOKEN`

Purpose:

Server-to-server bearer token used by the GPT Action.

Requirements:

- long random value;
- separate from VoiceBridge test token;
- never given to beta testers;
- same value later configured as the GPT Builder Action bearer credential.

### `KRC_MEDIA_BETA_CODES`

Purpose:

Closed-beta tester admission codes.

Recommended initial set:

- owner code;
- tester 1 code;
- tester 2 code;
- tester 3 code.

Requirements:

- independent random values;
- at least 16 random characters recommended;
- only distribute one code per tester;
- rotate a single compromised tester code without changing provider credentials when implementation/config supports it.

### `ASSEMBLYAI_API_KEY`

Purpose:

Fallback STT provider credential.

Requirements:

- server-side only;
- verify project privacy/model-training configuration before broader rollout;
- monitor remaining free credit during beta.

## 4. Fixed beta resource configuration

Initial approved beta limits:

```text
MEDIA_MAX_DURATION_SECONDS=3600
MEDIA_MAX_CONCURRENT_JOBS=1
MEDIA_DAILY_STT_SECONDS=7200
MEDIA_JOB_TTL_SECONDS=3600
```

Fallback audio target:

```text
mono
16 kHz
~32 kbps speech-oriented audio
```

Do not increase these limits during beta without recording a new decision in `06_DECISION_LOG.md`.

## 5. Health checks

### Beta backend

Check:

`GET https://voicebridge-krc-media-beta-kolemasakar.onrender.com/api/v1/health`

Expected:

- HTTP 200;
- service status `ok`;
- media capability configured;
- expected supported platform/language hints;
- beta limits consistent with configuration.

### Production regression guard

Also check:

`GET https://voicebridge-cloud-us.onrender.com/api/v1/health`

Expected:

- production endpoint remains healthy;
- production streaming VoiceBridge version/behavior remains unchanged.

## 6. Live backend test order

Run in this order:

1. invalid/no Action bearer token;
2. invalid beta tester code;
3. valid tester code + short video with captions;
4. same URL reuse behavior;
5. valid tester code + short video without usable captions -> AssemblyAI fallback;
6. Ukrainian source;
7. Russian source;
8. English source;
9. auto language detection;
10. >60 minute video rejection;
11. concurrency rejection;
12. daily quota behavior;
13. provider cleanup state.

Do not begin GPT Builder integration until these backend tests are acceptable.

## 7. GPT Builder beta procedure

Create a new GPT. Do not edit the published production GPT.

Name:

`K-Research & Critic - MEDIA BETA`

Use:

- instructions: `prompts/GPT_STORE_MEDIA_BETA_INSTRUCTIONS.md`;
- Action schema: `gpt_store/actions/media_beta_openapi.yaml`;
- bearer auth value: same secret as beta backend `KRC_MEDIA_ACTION_TOKEN`;
- distribution: unlisted/link-only where supported;
- public privacy policy URL if Builder requires it.

The Action schema must point only to the dedicated beta Render endpoint.

## 8. Tester onboarding

Each tester receives:

- beta GPT link;
- one tester access code;
- short instruction: provide YouTube URL, then provide beta code only when prompted;
- warning not to share the code;
- request to report failures with video URL, approximate time, visible error, and whether captions were expected.

Do not give testers:

- `KRC_MEDIA_ACTION_TOKEN`;
- `ASSEMBLYAI_API_KEY`;
- Render credentials.

## 9. Monitoring during beta

Track at minimum:

- number of media jobs;
- captions vs AssemblyAI fallback share;
- total STT seconds reserved/used;
- Render outbound bandwidth trend;
- AssemblyAI remaining credits;
- median/typical transcription latency;
- failed media fetches;
- provider cleanup failures;
- YouTube/yt-dlp errors;
- user-visible workflow failures after transcript acquisition.

## 10. Rollback

If beta backend is unstable:

- disable or suspend only the dedicated beta Render service;
- keep production VoiceBridge running;
- do not change public K-Research & Critic;
- preserve draft PRs for diagnosis;
- record failure in `03_CURRENT_STATE.md` and `06_DECISION_LOG.md` if architectural action is required.

If a tester code leaks:

- revoke/rotate the affected code;
- do not rotate AssemblyAI key unless provider exposure occurred;
- do not rotate the GPT Action bearer token unless that secret was exposed.

If the GPT Action bearer token leaks:

- rotate `KRC_MEDIA_ACTION_TOKEN` in Render;
- update the beta GPT Builder Action credential;
- retest authentication.

## 11. Promotion rule

Closed beta must not be promoted to public media production until:

- all critical tests pass;
- resource consumption is measured;
- privacy gates pass;
- Free-plan behavior is validated;
- an explicit user decision authorizes promotion.