# MEDIA BETA Chat Handoff
Канонічний документ відновлення та переходу між чатами для продовження MEDIA BETA.

Version: 1.2
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

`A3_COMPLETE / MEDIA_CONFIGURED / A4_NEXT`

Dedicated beta service: `voicebridge-krc-media-beta-kolemasakar`.

Service ID: `srv-da1kic5bedkc73d6fk60`.

Verified:
- plan `free`;
- branch `agent/krc-media-transcript`;
- beta deploy live;
- beta health HTTP 200;
- media mode `closed_beta`;
- `media_transcript.configured=true`;
- subtitle-first true;
- max duration 3600 sec;
- concurrency 1;
- daily STT 7200 sec;
- production VoiceBridge health HTTP 200 / `status=ok`.

Final A3 verification run: `32055491376`.

A first configuration attempt failed because one tester-code entry was shorter than the required 12 characters. The value was corrected and the redeploy succeeded. No credential values are stored in this document.

## Exact next task

Phase: `A4 - Live transcript validation`.

First action: use a short public YouTube video with usable captions and validate the subtitle-first path without AssemblyAI STT quota use. Then test a separate video that requires AssemblyAI fallback.

Use `05_TEST_PLAN.md` for the full A4 matrix.

## Do-not-do list

Do not merge PR #8/#28 automatically, deploy beta over production, alter the published KRC GPT, expose credentials or tester codes, claim transcript tests passed without live evidence, bypass CriticProfile approval, or change priority away from closed beta unless the user decides so.

## Terminal markers

`MEDIA_BETA_HANDOFF_V1_2`

`A4_LIVE_TRANSCRIPT_VALIDATION_NEXT`

`PRODUCTION_HEALTH_OK_DRAFT_PRS_UNMERGED`
