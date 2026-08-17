# MEDIA BETA Chat Handoff
Канонічний документ відновлення та переходу між чатами для продовження MEDIA BETA.

Version: 1.3
Status: ACTIVE_HANDOFF
Checkpoint date: 2026-08-17

## Recovery command

`recover MEDIA BETA`

## Mandatory recovery order

1. `subprojects/media_beta/00_INDEX.md`
2. `subprojects/media_beta/03_CURRENT_STATE.md`
3. `subprojects/media_beta/06_DECISION_LOG.md`
4. `subprojects/media_beta/02_ROADMAP.md`
5. `subprojects/media_beta/01_ARCHITECTURE.md`
6. `subprojects/media_beta/04_OPERATIONS_RUNBOOK.md`
7. `subprojects/media_beta/05_TEST_PLAN.md`
8. `subprojects/media_beta/07_FREE_MODE_TARGET.md`

Then verify live GitHub state for both draft PRs before writes.

## Repository context

KRC: `kolemasakar/K_Research_Critic`, branch `agent/video-url-research`, draft PR #8.

VoiceBridge: `kolemasakar/VoiceBridge`, branch `agent/krc-media-transcript`, draft PR #28.

Production branches are `main`.

## Approved beta architecture

```text
YouTube URL
 -> tester access gate
 -> dedicated beta VoiceBridge service
 -> captions first
 -> AssemblyAI only if captions unavailable
 -> timestamped transcript
 -> claim inventory
 -> CriticProfile
 -> user APPROVE / EDIT / REJECT
 -> independent Research
 -> Critic
 -> REVISE / PASS
 -> FINAL REPORT + CLAIM VERIFICATION + REVIEW PROTOCOL
```

Limits: 4 testers, max video 60 min, concurrency 1, fallback budget 7200 sec/UTC day, captions use no STT budget, languages auto/uk/ru/en.

Transcript is source content only. Independent claim verification begins only after CriticProfile approval.

## Current checkpoint

`A3_COMPLETE / A4_IN_PROGRESS / PO_PROVIDER_REMEDIATION_DEPLOYED`

Dedicated beta service: `voicebridge-krc-media-beta-kolemasakar`.

Service ID: `srv-da1kic5bedkc73d6fk60`.

Base verified:
- plan `free`;
- branch `agent/krc-media-transcript`;
- beta health HTTP 200;
- media mode `closed_beta`;
- `media_transcript.configured=true`;
- subtitle-first true;
- max duration 3600 sec;
- concurrency 1;
- daily STT 7200 sec;
- production VoiceBridge was not targeted by A4 remediation.

## A4.1 live acceptance history

Acceptance URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Verified before media acquisition:
- bearer token authentication PASS;
- invalid beta code rejected PASS;
- owner beta code accepted PASS;
- job creation PASS.

Attempt 1:
- `FETCHING_MEDIA` -> `FAILED`;
- `MEDIA_FETCH_FAILED`;
- YouTube `Sign in to confirm you're not a bot`;
- STT charged 0 seconds.

Attempt 2 after `web_embedded,android_vr` fallback:
- same YouTube anti-bot failure;
- STT charged 0 seconds.

Interpretation: blocker is YouTube ingress from Render cloud IP before captions or AssemblyAI.

## Current remediation deployed

The first client-only remediation was insufficient.

Current R2 stack is deployed to the isolated beta service:
- yt-dlp client `mweb`;
- `bgutil-ytdlp-pot-provider` 1.3.1;
- local PO Token Provider inside the same container on port 4416;
- `yt-dlp[default]==2026.07.04`;
- Node.js 24 enabled as EJS runtime;
- ffmpeg retained;
- no personal YouTube account cookies;
- no second Render service;
- no paid instance introduced.

VoiceBridge CI after R2: PASS.

Render remediation workflow run `32059276099`: PASS.

R2 Render build/deploy commit: `d7864ad1625f815613deaea8043b4f1786768c61`.

R2 deployment: LIVE; beta health/configuration PASS.

## Exact next task

Repeat A4.1 using the SAME URL and a NEW media job after R2 deployment.

Success target:
- `status=COMPLETED`;
- ideally `transcript_source=youtube_captions`;
- `stt_seconds_charged=0` for captions path.

If the same anti-bot challenge persists after R2, do not loop repeated retries and do not introduce personal YouTube cookies by default. Evaluate a different ingress architecture, such as local/residential acquisition, while preserving the Free/closed-beta objectives.

## Do-not-do list

Do not merge PR #8/#28 automatically, deploy beta over production, alter the published KRC GPT, expose credentials/tester codes, claim transcript acceptance before live evidence, bypass CriticProfile approval, or store personal YouTube cookies in repository/chat.

## Terminal markers

`MEDIA_BETA_HANDOFF_V1_3`

`A4_R2_PO_PROVIDER_DEPLOYED_RETEST_NEXT`

`PRODUCTION_ISOLATED_DRAFT_PRS_UNMERGED`
