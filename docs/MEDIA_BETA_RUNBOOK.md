# MEDIA_BETA_RUNBOOK
Інструкція оператора для безпечного запуску окремої закритої MEDIA BETA без зміни production-сервісів.

Version: 0.1
Status: CLOSED_BETA
Date: 2026-08-17

## 1. Safety Boundary

Do not deploy the media beta over the existing VoiceBridge production service.

Existing production endpoint:

```text
https://voicebridge-cloud-us.onrender.com
```

Dedicated beta endpoint:

```text
https://voicebridge-krc-media-beta-kolemasakar.onrender.com
```

The public K-Research & Critic GPT must remain unchanged during closed beta.

## 2. Source Branches

VoiceBridge backend:

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-transcript
PR: 28
```

K-Research & Critic beta package:

```text
repository: kolemasakar/K_Research_Critic
branch: agent/video-url-research
PR: 8
```

Both PRs remain draft during the closed beta.

## 3. Render Deployment

Use the dedicated Render Blueprint stored in VoiceBridge:

```text
render.media-beta.yaml
```

Render Dashboard procedure:

```text
New
-> Blueprint
-> connect kolemasakar/VoiceBridge
-> branch agent/krc-media-transcript
-> Blueprint path render.media-beta.yaml
-> create/sync
```

The Blueprint creates one Free Docker web service:

```text
name: voicebridge-krc-media-beta-kolemasakar
region: frankfurt
plan: free
runtime: docker
branch: agent/krc-media-transcript
auto deploy: checksPass
Dockerfile: src/cloud/Dockerfile
Docker context: src/cloud
health check: /api/v1/health
```

Render supports `runtime: docker`, explicit `dockerfilePath`, `dockerContext`, `plan: free`, and `autoDeployTrigger: checksPass` in Blueprints.

## 4. Render Secrets

During the first Blueprint creation Render prompts for variables declared with `sync: false`.

Set:

```text
KRC_MEDIA_ACTION_TOKEN=<long random secret, 32+ characters>
KRC_MEDIA_BETA_CODES=<four comma-separated tester codes, each 16+ random characters>
ASSEMBLYAI_API_KEY=<AssemblyAI project API key>
```

Do not commit these values to GitHub.

`TEST_ACCESS_TOKEN` is generated automatically by Render for the isolated beta service.

Recommended beta code ownership:

```text
code 1: owner
code 2: tester A
code 3: tester B
code 4: tester C
```

Each tester should receive only one code.

## 5. Fixed Beta Limits

The Blueprint sets:

```text
MEDIA_MAX_DURATION_SECONDS=3600
MEDIA_MAX_CONCURRENT_JOBS=1
MEDIA_DAILY_STT_SECONDS=7200
MEDIA_JOB_TTL_SECONDS=3600
RATE_LIMIT_REQUESTS_PER_MINUTE=120
MAX_REQUEST_BODY_BYTES=32768
CORS_ALLOWED_ORIGIN=*
```

Resource behavior:

```text
YouTube captions available
-> captions path
-> no AssemblyAI STT budget used

captions unavailable
-> 32 kbps mono / 16 kHz STT audio
-> AssemblyAI fallback
-> source-duration seconds reserved from daily quota
```

The daily STT counter is intentionally in memory for the trusted closed beta. A Render restart resets it. This is not sufficient for future public anti-abuse protection.

## 6. Health Check

After the Render deploy finishes, open:

```text
https://voicebridge-krc-media-beta-kolemasakar.onrender.com/api/v1/health
```

Expected media capability characteristics:

```text
mode: closed_beta
subtitle_first: true
max_duration_seconds: 3600
max_concurrent_jobs: 1
daily_stt_seconds: 7200
providers:
  youtube_captions
  assemblyai_stt
configured: true
```

Do not continue to GPT Builder if `configured` is false.

## 7. GPT Builder - Separate Beta GPT

Create a separate GPT. Do not edit the published production GPT.

Use:

```text
Name:
K-Research & Critic - MEDIA BETA

Instructions:
prompts/GPT_STORE_MEDIA_BETA_INSTRUCTIONS.md

Action schema:
gpt_store/actions/media_beta_openapi.yaml
```

Enable:

```text
Web search
Code Interpreter & Data Analysis
Actions
```

Keep Apps and Image generation disabled unless a later approved change requires them.

Action authentication:

```text
type: API key / bearer
value: exactly the KRC_MEDIA_ACTION_TOKEN configured on the beta Render service
```

The action bearer secret is a developer secret. Testers never receive it.

## 8. Beta User Access

Distribution:

```text
Anyone with link / unlisted beta link
```

Actual media access is restricted server-side by the separate tester code.

Expected first media interaction:

```text
user sends YouTube URL + media-analysis request
-> GPT asks for beta tester code if not already supplied
-> tester supplies code
-> code is sent only to startMediaBetaTranscription
-> code is never repeated in visible output
```

Do not store tester codes in checkpoints or reusable prompts.

## 9. Mandatory Live Tests

Run in this order.

```text
B01 health endpoint reports configured=true
B02 invalid action bearer -> 401
B03 invalid tester code -> 403
B04 valid tester code + short YouTube with captions -> COMPLETED
B05 B04 transcript_source=youtube_captions
B06 B04 stt_seconds_charged=0
B07 valid tester code + no usable captions -> AssemblyAI fallback
B08 B07 transcript_source=assemblyai_stt
B09 B07 stt_seconds_charged > 0
B10 provider_data_deleted=true after successful AssemblyAI job
B11 video > 60 minutes -> MEDIA_DURATION_LIMIT
B12 two simultaneous jobs -> second job rejected/busy
B13 uk source transcription
B14 ru source transcription
B15 en source transcription
B16 automatic language mode
B17 timestamp/segment claim traceability
B18 CriticProfile approval blocks independent research before APPROVE
B19 Research -> Critic -> REVISE/PASS loop
B20 final report contains claim verification and no tester code
B21 checkpoint contains no full transcript and no tester code
B22 existing public K-Research & Critic still works unchanged
B23 existing VoiceBridge production endpoint still works unchanged
```

## 10. Quota Test

Do not intentionally burn two hours of AssemblyAI merely to test the quota.

For a dedicated engineering test, temporarily deploy the beta branch with a small `MEDIA_DAILY_STT_SECONDS` value, verify rejection after the limit, then restore:

```text
MEDIA_DAILY_STT_SECONDS=7200
```

Never alter the production VoiceBridge service for this test.

## 11. AssemblyAI Release Gate

Before expanding beta access, verify the AssemblyAI project settings/terms used by this service for provider model-training opt-out or equivalent no-training protection.

If this is not verified, keep the media feature in CLOSED_BETA / PREVIEW state.

## 12. Stop / Rollback

To stop the beta without affecting production:

```text
Render -> voicebridge-krc-media-beta-kolemasakar -> suspend/delete beta service
GPT Builder -> make MEDIA BETA private or delete it
```

No rollback is required for:

```text
voicebridge-cloud-us
published K-Research & Critic
```

because closed beta is isolated from both production surfaces.

## 13. Promotion Rule

Do not merge or publish the beta as the public media mode solely because CI is green.

Promotion requires:

```text
all relevant B01-B23 live tests PASS
privacy gate PASS
resource-use observation
Free-plan tester validation
no production regression
explicit user approval
```
