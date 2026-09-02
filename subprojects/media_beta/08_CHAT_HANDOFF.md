# MEDIA BETA Chat Handoff
Канонічна інструкція відновлення K-Research & Critic - MEDIA BETA у новому чаті.

Version: 4.5
Status: ACTIVE_HANDOFF / RELEASE_HOLD_OWNER_TESTING / M3_CLOSED / M4_PREFLIGHT_BLOCKED
Checkpoint date: 2026-09-02

## Recovery command

`recover KRC MEDIA BETA checkpoint 70 M3 closed M4 preflight blocked 2026-09-02`

## Mandatory recovery order

1. `subprojects/media_beta/70_M3_CLOSED_M4_PREFLIGHT_BLOCKED_CHECKPOINT_2026_09_02.md`
2. `subprojects/media_beta/69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md`
3. `subprojects/media_beta/68_M3B_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md`
4. `subprojects/media_beta/62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md`
5. `subprojects/media_beta/00_INDEX.md`
6. `subprojects/media_beta/02_ROADMAP.md`
7. `subprojects/media_beta/03_CURRENT_STATE.md`
8. `subprojects/media_beta/06_DECISION_LOG.md`
9. `subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md`

Verify current GitHub heads and CI before any write, provider-consuming operation, merge, deployment, or activation decision.

## Product / repository context

```text
K-Research & Critic
 -> public Core: K_Research_Critic/main, published/maintenance
 -> MEDIA BETA: agent/video-url-research, closed beta, release hold

VoiceBridge
 -> technology/backend source
 -> KRC migration branch: agent/krc-media-gemini-migration
 -> PR #45 draft/open/unmerged unless reverified otherwise
```

## Current provider decision

```text
M3: CLOSED
current KRC prerecorded provider: AssemblyAI universal-2
Gemini prerecorded normal activation: FALSE
provider cutover now: FALSE
```

Seven-case M3/M3B evidence remains mixed and does not establish a global quality winner.

## Deferred future plan

D029 records Hybrid C/D as a future free-first architecture only after AssemblyAI free credits are exhausted.

```text
Hybrid C/D now: NOT_IMPLEMENTED
Gemini Live future role: preferred free eligible route
Gemini unary future role: timestamps/diarization feature route when free quota permits
AssemblyAI after free credits: retained rollback/fallback; billable use disabled by default
```

No automatic paid fallback is authorized.

## M4 current state

Repository-only deployment-image parity preflight is complete.

VoiceBridge authority:

`docs/history/2026-09-02_KRC_MEDIA_M4_DEPLOYMENT_IMAGE_PARITY_PREFLIGHT.md`

Findings:

```text
managed KRC routes mounted: PASS_STATIC
environment/config surface: PASS_STATIC
ffmpeg/ffprobe required by attachment path: MISSING_FROM_RUNTIME_IMAGE
psql required by durable store: MISSING_FROM_RUNTIME_IMAGE
M4_CANARY_READY: FALSE
```

## Exact continuation point

```text
M4 IMAGE-PARITY REMEDIATION ON VOICEBRIDGE FEATURE BRANCH
```

Allowed next engineering work before another owner gate:

- patch final runtime image to provide `ffmpeg`, `ffprobe`, and `psql`;
- add CI final-image command checks;
- add no-provider-call KRC route startup smoke validation;
- run full VoiceBridge validation.

Then STOP. Do not deploy or start M4 canary without a new explicit owner authorization.

## Release boundary

```text
R1 merge: HOLD
R2 backend/production promotion: HOLD
R3 external testers: HOLD
R4 public rollout: HOLD
```

## Critical policy recovery

- Facebook: Cobalt fail -> unavailable; no automatic paid fallback.
- Telegram: public-only, zero retrieval credits.
- Local attachment: max 32 MiB, zero retrieval credits.
- AssemblyAI remains active while current free-credit plan remains in effect.
- CriticProfile gate remains before Research.
- per-claim independent cross-check accounting remains mandatory.
- A10 copy-safe summary remains mandatory.

## Terminal marker

`MEDIA_BETA_HANDOFF_V4_5_M3_CLOSED_M4_IMAGE_PARITY_REMEDIATION`
