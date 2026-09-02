# MEDIA BETA Documentation Index
Канонічний індекс документації приватного K-Research & Critic MEDIA BETA.

Version: 5.1
Status: ACTIVE / RELEASE_HOLD_OWNER_TESTING / M3_CLOSED / M4_IMAGE_PARITY_READY
Updated: 2026-09-02

## Product boundary

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product. `K_Research_Critic` remains the product/roadmap authority. VoiceBridge provides media/backend technology, implementation, and validation evidence.

## Canonical reading order

1. `71_M4_IMAGE_PARITY_READY_OWNER_CANARY_DECISION_CHECKPOINT_2026_09_02.md` - current recovery authority and owner deployment/canary gate.
2. `70_M3_CLOSED_M4_PREFLIGHT_BLOCKED_CHECKPOINT_2026_09_02.md` - preceding M4 preflight blocker checkpoint.
3. `69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md` - deferred future Hybrid C/D plan.
4. `68_M3B_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md` - completed seven-case provider evidence before closure.
5. `62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md` - complete cross-repository baseline.
6. `02_ROADMAP.md`, `03_CURRENT_STATE.md`, `06_DECISION_LOG.md`, `08_CHAT_HANDOFF.md` - current roadmap/state/decisions/handoff.
7. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` - release authority.

## Current provider state

```text
M3: CLOSED
current KRC prerecorded provider: AssemblyAI universal-2
Gemini prerecorded normal activation: FALSE
provider cutover now: FALSE
Hybrid C/D: PLANNED / NOT_IMPLEMENTED
Hybrid trigger: AssemblyAI free credits exhausted
```

## M4 current state

VoiceBridge feature-branch image parity remediation is accepted.

```text
ffmpeg/ffprobe in final runtime image: PASS
psql in final runtime image: PASS
final Docker image build: PASS
no-provider KRC startup smoke: PASS
VoiceBridge exact-head Validate: SUCCESS 4/4 jobs
M4_IMAGE_PARITY: PASS
M4_DEPLOYMENT: NOT_PERFORMED
M4_CANARY: NOT_RUN
M4_CANARY_AUTHORIZATION: PENDING_OWNER_DECISION
```

VoiceBridge acceptance authority:

`docs/history/2026-09-02_KRC_MEDIA_M4_IMAGE_PARITY_REMEDIATION_ACCEPTANCE.md`

Next state transition requires a separate owner decision because it may affect an external backend deployment.

## Release boundary

```text
R1 merge: HOLD
R2 backend promotion: HOLD unless separately scoped for owner canary
R3 external testers: HOLD
R4 public rollout: HOLD
RELEASE_HOLD_OWNER_TESTING: PRESERVED
```

## Recovery command

`recover KRC MEDIA BETA checkpoint 71 M4 image parity ready owner canary decision 2026-09-02`

Always verify current GitHub heads/CI before any write, deployment, provider-consuming operation, merge, or activation decision.
