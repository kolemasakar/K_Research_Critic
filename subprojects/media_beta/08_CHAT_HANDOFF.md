# MEDIA BETA Chat Handoff
Канонічний документ відновлення та переходу між чатами для продовження MEDIA BETA.

Version: 1.4
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

## Approved beta baseline

Limits: 4 testers, max video 60 min, concurrency 1, fallback budget 7200 sec/UTC day, captions use no STT budget, languages auto/uk/ru/en.

Transcript is source content only. Independent claim verification begins only after CriticProfile approval.

## Current checkpoint

`A3_COMPLETE / A4_SERVER_SIDE_YOUTUBE_INGRESS_BLOCKED / ARCHITECTURE_DECISION_REQUIRED`

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
- production VoiceBridge isolated.

## A4.1 evidence

URL:
`https://www.youtube.com/watch?v=DZLzmQ2kwaA`

Pre-fetch checks PASS:
- bearer token;
- invalid beta-code rejection;
- owner beta-code acceptance;
- job creation.

Attempt 1:
- job `KRCB_1c137194-3b23-4ed9-ab1e-fa5a49255cc9`;
- YouTube anti-bot FAIL;
- STT 0.

Attempt 2 after `web_embedded,android_vr`:
- job `KRCB_03d37ccd-4059-4b0c-9675-6f2568d4c207`;
- same FAIL;
- STT 0.

Attempt 3 after `mweb` + PO provider:
- job `KRCB_981465dc-e400-470f-a236-c5414c26bd63`;
- same FAIL;
- STT 0.

Error in all three server-side attempts:
`Sign in to confirm you're not a bot`.

## Decisive diagnostic

One-shot VoiceBridge Docker diagnostic:
- run `32060462596`;
- job `95480351954`.

Verified:
- bgutil provider starts and `/ping` works;
- yt-dlp `2026.07.04`;
- Node.js EJS runtime works;
- yt-dlp reports `PO Token Providers: bgutil:http-1.3.1 (external)`;
- the same URL still receives the YouTube bot challenge.

Therefore R2 is wired correctly. The current server-side Render/GitHub-cloud path is blocked by YouTube datacenter/cloud anti-bot enforcement. Do not continue blind client/PO-token retries.

The diagnostic workflow was removed after use.

## Recommended next architecture - pending user approval

`client-assisted / browser-assisted ingress`

```text
YouTube URL
 -> one-time beta media session
 -> VoiceBridge browser helper/extension
 -> captions or tab audio acquired through tester residential IP
 -> derived captions/audio uploaded to beta backend
 -> AssemblyAI only if captions unavailable
 -> timestamped transcript
 -> claim inventory
 -> CriticProfile
 -> user approval
 -> Research / Critic
```

Reasons:
- avoids datacenter YouTube fetch;
- no personal YouTube cookies in Render;
- no residential proxy subscription;
- preserves Free Render objective;
- reuses existing VoiceBridge browser capability.

Alternatives requiring explicit approval:
- paid residential proxy for URL-only server UX;
- personal YouTube cookies in cloud, not recommended as default.

## Exact next task

Obtain user architecture decision. Recommended approval: client-assisted browser ingestion for closed beta.

After approval, implement A4.2 on feature branches only and retest the same acceptance URL.

## Do-not-do list

Do not merge PR #8/#28 automatically, deploy beta over production, alter the published KRC GPT, expose credentials/tester codes, claim transcript acceptance before live evidence, bypass CriticProfile approval, store personal YouTube cookies in repository/chat, or continue blind server-side retries.

## Terminal markers

`MEDIA_BETA_HANDOFF_V1_4`

`A4_SERVER_SIDE_YOUTUBE_INGRESS_BLOCKED`

`CLIENT_ASSISTED_ARCHITECTURE_DECISION_NEXT`

`PRODUCTION_ISOLATED_DRAFT_PRS_UNMERGED`
