# MEDIA BETA Documentation Index
Канонічний індекс документації приватного K-Research & Critic MEDIA BETA.

Version: 5.2
Status: ACTIVE / RELEASE_HOLD_OWNER_TESTING / M3_CLOSED / M4_OWNER_CANARY_ACCEPTED
Updated: 2026-09-02

## Product boundary

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product. `K_Research_Critic` remains the product/roadmap authority. VoiceBridge provides media/backend technology, implementation, and validation evidence.

## Canonical reading order

1. `72_M4_OWNER_CANARY_ACCEPTED_ROLLBACK_COMPLETE_CHECKPOINT_2026_09_02.md` - current recovery authority and post-canary owner gate.
2. `71_M4_IMAGE_PARITY_READY_OWNER_CANARY_DECISION_CHECKPOINT_2026_09_02.md` - preceding image-parity/canary gate.
3. `69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md` - deferred future Hybrid C/D plan.
4. `68_M3B_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md` - completed seven-case provider evidence before M3 closure.
5. `62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md` - complete earlier cross-repository baseline.
6. `02_ROADMAP.md`, `03_CURRENT_STATE.md`, `06_DECISION_LOG.md`, `08_CHAT_HANDOFF.md` - roadmap/state/decisions/handoff.
7. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` - release authority.

## Current provider state

```text
M3: CLOSED
current KRC prerecorded provider: AssemblyAI universal-2
Gemini prerecorded normal activation: FALSE
provider cutover now: FALSE
Hybrid C/D: PLANNED / NOT_IMPLEMENTED
Hybrid trigger: AssemblyAI free credits exhausted plus fresh owner decision
```

## M4 current state

VoiceBridge final-image remediation and bounded owner-only live canary are accepted.

```text
ffmpeg/ffprobe in final runtime image: PASS
psql in final runtime image: PASS
M4_IMAGE_PARITY: PASS
M4_OWNER_CANARY: PASS
real Telegram -> AssemblyAI STT: PASS
Neon durability: PASS
idempotent duplicate reuse: PASS
provider cleanup: PASS
mandatory rollback: PASS
M4_PERMANENT_BACKEND_PROMOTION: NOT_AUTHORIZED
```

VoiceBridge acceptance authorities:

`docs/history/2026-09-02_KRC_MEDIA_M4_IMAGE_PARITY_REMEDIATION_ACCEPTANCE.md`

`docs/history/2026-09-02_KRC_MEDIA_M4_OWNER_CANARY_ACCEPTANCE.md`

Canary workflow run:

`33580592224` - SUCCESS.

The isolated Render service was restored to its exact pre-canary commit after validation.

## Release boundary

```text
R1 merge: HOLD
R2 backend promotion: HOLD
R3 external testers: HOLD
R4 public rollout: HOLD
RELEASE_HOLD_OWNER_TESTING: PRESERVED
```

## Recovery command

`recover KRC MEDIA BETA checkpoint 72 M4 owner canary accepted rollback complete 2026-09-02`

Always verify current GitHub heads/CI and current external infrastructure before any write, provider-consuming operation, merge, permanent deployment, or activation decision.
