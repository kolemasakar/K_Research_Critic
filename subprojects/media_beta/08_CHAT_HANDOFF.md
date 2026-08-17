# MEDIA BETA Chat Handoff
Канонічний документ відновлення та переходу між чатами для продовження MEDIA BETA без втрати стану або повторного проєктування.

Version: 1.1
Status: ACTIVE_HANDOFF
Checkpoint date: 2026-08-17

## Recovery command

`recover MEDIA BETA`

Recover from repository state; do not invent missing history.

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

KRC:
- `kolemasakar/K_Research_Critic`;
- branch `agent/video-url-research`;
- draft PR #8.

VoiceBridge:
- `kolemasakar/VoiceBridge`;
- branch `agent/krc-media-transcript`;
- draft PR #28.

Production branches are `main`. Do not assume either draft PR is merged unless live GitHub state proves it.

## Approved beta architecture

```text
YouTube URL
 -> per-tester beta access
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

Limits:
- 4 intended testers;
- max video 60 min;
- concurrency 1;
- AssemblyAI fallback budget 7200 sec/UTC day;
- captions consume no STT budget;
- fallback audio mono 16 kHz ~32 kbps;
- languages auto/uk/ru/en.

Transcript is source content only. Independent claim verification begins only after CriticProfile approval.

## Current checkpoint

Marker:

`BETA_SERVICE_LIVE / SERVICE_SECRETS_PENDING`

Dedicated Render service:

`voicebridge-krc-media-beta-kolemasakar`

Service ID:

`srv-da1kic5bedkc73d6fk60`

Endpoint:

`https://voicebridge-krc-media-beta-kolemasakar.onrender.com`

Verified evidence:
- Render bootstrap run `32051889378`: PASS;
- plan: `free`;
- branch: `agent/krc-media-transcript`;
- initial deploy reached `live`;
- post-bootstrap inspect run `32052056782`: PASS;
- beta `/api/v1/health`: HTTP 200;
- media mode: `closed_beta`;
- subtitle-first: true;
- max duration: 3600 sec;
- concurrency: 1;
- daily STT: 7200 sec;
- `media_transcript.configured=false`.

Production `voicebridge-cloud-us` was not modified.

## Exact next task

Phase:

`A3 - service secret configuration`

Configure on the dedicated beta Render service only:
- `KRC_MEDIA_ACTION_TOKEN`;
- `KRC_MEDIA_BETA_CODES`;
- `ASSEMBLYAI_API_KEY`.

Do not put secret values into chat or GitHub files.

After configuration:
1. read-only health check;
2. require `media_transcript.configured=true`;
3. confirm production VoiceBridge health;
4. begin A4 live transcript tests from `05_TEST_PLAN.md`.

## Do-not-do list

Do not:
- merge PR #8 or #28 automatically;
- deploy beta over `voicebridge-cloud-us`;
- alter the published KRC GPT for beta;
- invent or expose secrets/tester codes;
- claim transcript tests passed before live evidence;
- bypass CriticProfile approval;
- switch priority to Cloudflare/local Whisper before closed beta validation unless the user changes the plan.

## Cross-chat update protocol

After meaningful work update:
- `03_CURRENT_STATE.md`;
- `02_ROADMAP.md` if phase/gate changes;
- `06_DECISION_LOG.md` if architecture/limits/providers change;
- this file if exact next action changes;
- `09_WORK_LOG.md` with material events.

## Recovery output

A recovered assistant should report current phase, completed gates, blockers, exact next action, and confirmation that production boundaries remain intact.

Terminal markers:

`MEDIA_BETA_HANDOFF_V1_1`

`A3_RENDER_SERVICE_SECRETS_PENDING`

`PRODUCTION_UNCHANGED_DRAFT_PRS_UNMERGED`
