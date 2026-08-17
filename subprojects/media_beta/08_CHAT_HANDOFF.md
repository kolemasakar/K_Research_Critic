# MEDIA BETA Chat Handoff
Канонічний документ відновлення та переходу між чатами для продовження MEDIA BETA без втрати стану або повторного проєктування.

Version: 1.0
Status: ACTIVE_HANDOFF
Checkpoint date: 2026-08-17

## 1. Recovery command

When a new chat starts for this subproject, the intended user command may be as short as:

`recover MEDIA BETA`

The assistant must then recover from repository state rather than inventing missing history.

## 2. Mandatory recovery sources

Read in this order:

1. `subprojects/media_beta/00_INDEX.md`
2. `subprojects/media_beta/03_CURRENT_STATE.md`
3. `subprojects/media_beta/06_DECISION_LOG.md`
4. `subprojects/media_beta/02_ROADMAP.md`
5. `subprojects/media_beta/01_ARCHITECTURE.md`
6. `subprojects/media_beta/04_OPERATIONS_RUNBOOK.md`
7. `subprojects/media_beta/05_TEST_PLAN.md`
8. `subprojects/media_beta/07_FREE_MODE_TARGET.md`

Then verify live GitHub state for both feature branches and draft PRs before making writes.

## 3. Repository context

Primary repository:

`kolemasakar/K_Research_Critic`

Active media branch:

`agent/video-url-research`

Draft PR:

`#8`

Backend dependency:

`kolemasakar/VoiceBridge`

Active backend branch:

`agent/krc-media-transcript`

Draft PR:

`#28`

Production branches in both repositories:

`main`

Do not assume either draft PR is merged unless live GitHub state proves it.

## 4. Product context

The current work is NOT a replacement of K-Research & Critic.

It is an additive media-input extension with two tracks:

- first: CLOSED MEDIA BETA for owner + up to three testers;
- later: sustainable free public media architecture.

Existing K-Research & Critic text mode remains production baseline.

Existing VoiceBridge production streaming service remains production baseline.

## 5. Approved closed-beta architecture

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

- 4 intended testers total;
- max video 60 minutes;
- concurrency 1;
- global AssemblyAI fallback budget 7200 sec/UTC day;
- captions consume no STT budget;
- fallback audio mono 16 kHz approximately 32 kbps;
- languages auto/uk/ru/en.

## 6. Non-negotiable semantic boundary

Transcript is source content only.

It may be acquired before CriticProfile approval to determine subject/risk and identify material claims.

Independent verification of the claims starts only after user approval of CriticProfile.

The video/transcript must never corroborate its own factual claim.

## 7. Current implementation checkpoint

At this checkpoint:

- KRC media/beta code exists on feature branch;
- VoiceBridge media/beta backend code exists on feature branch;
- automated CI was green for both implementation branches before/following beta code validation;
- both PRs are draft and unmerged;
- separate beta Render Blueprint exists in VoiceBridge;
- documentation subproject exists in KRC.

Not yet completed:

- dedicated beta Render service is not live-validated;
- beta secrets are not configured on a dedicated service;
- no real YouTube caption/STT beta acceptance has been completed;
- separate MEDIA BETA GPT has not been live-validated in Builder;
- no external tester rollout has occurred.

Always re-read `03_CURRENT_STATE.md` because it may supersede this checkpoint.

## 8. Exact next task at this checkpoint

Phase:

`A3 - Dedicated Render beta deployment`

Next action:

Create a separate Render Blueprint service from `kolemasakar/VoiceBridge`, branch `agent/krc-media-transcript`, Blueprint file `render.media-beta.yaml`.

Target service:

`voicebridge-krc-media-beta-kolemasakar`

Production service that must remain untouched:

`voicebridge-cloud-us`

Then configure only in Render Dashboard:

- `KRC_MEDIA_ACTION_TOKEN`;
- `KRC_MEDIA_BETA_CODES`;
- `ASSEMBLYAI_API_KEY`.

After deployment, validate beta and production `/api/v1/health` before any GPT Builder work.

## 9. Do-not-do list on recovery

Do not:

- restart architecture design from zero;
- switch directly to Cloudflare/local Whisper before closed beta validation unless user changes priority;
- merge PR #8 or #28 automatically;
- deploy beta over production VoiceBridge;
- edit the published K-Research & Critic GPT for beta testing;
- invent Render or AssemblyAI secret values;
- place secrets or tester codes in GitHub;
- claim live tests passed without actual live evidence;
- skip the CriticProfile approval boundary.

## 10. Cross-chat update protocol

Before ending a chat after meaningful work:

1. update `03_CURRENT_STATE.md` with the actual completed state;
2. update `02_ROADMAP.md` statuses if a phase/gate changed;
3. append a decision to `06_DECISION_LOG.md` if architecture, limits, providers, or rollout rules changed;
4. update this `08_CHAT_HANDOFF.md` if the exact next action changed materially;
5. verify draft PR state and CI;
6. never write secret values into the handoff.

## 11. Recovery output expected from a new assistant

After reading repository state, the assistant should return a concise recovery summary containing:

- current phase;
- completed gates;
- open blockers;
- exact next action;
- confirmation that production boundaries remain intact.

It should not ask the user to repeat information already contained in these canonical documents.

## 12. Terminal handoff marker

Current marker:

`MEDIA_BETA_HANDOFF_V1`

Current next phase marker:

`A3_RENDER_BETA_DEPLOYMENT`

Current safety marker:

`PRODUCTION_UNCHANGED_DRAFT_PRS_UNMERGED`