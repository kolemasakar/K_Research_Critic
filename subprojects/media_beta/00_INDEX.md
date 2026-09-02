# MEDIA BETA Documentation Index
Канонічний індекс документації приватного K-Research & Critic MEDIA BETA.

Version: 5.0
Status: ACTIVE / RELEASE_HOLD_OWNER_TESTING / M3_CLOSED / M4_PREFLIGHT_BLOCKED
Updated: 2026-09-02

## Product boundary

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product. `K_Research_Critic` remains the product/roadmap authority. VoiceBridge provides media/backend technology, implementation, and validation evidence.

## Canonical reading order

1. `70_M3_CLOSED_M4_PREFLIGHT_BLOCKED_CHECKPOINT_2026_09_02.md` - current recovery authority.
2. `69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md` - deferred future Hybrid C/D plan.
3. `68_M3B_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md` - completed seven-case provider evidence before closure.
4. `67_M3B_READY_FOR_AB_CHECKPOINT_2026_09_01.md` - preceding expanded-corpus readiness point.
5. `65_M3_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md` - first provider A/B result.
6. `62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md` - complete cross-repository baseline.
7. `02_ROADMAP.md`, `03_CURRENT_STATE.md`, `06_DECISION_LOG.md`, `08_CHAT_HANDOFF.md` - current roadmap/state/decisions/handoff.
8. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` - release authority.

## M3 closure

```text
M3 provider evidence: COMPLETE
first tranche: COMPLETE 3 cases x 2 providers
M3B expanded tranche: COMPLETE 4 cases x 2 providers
seven-case global winner: NOT_ESTABLISHED
M3 closure: CLOSED
current KRC prerecorded provider: AssemblyAI universal-2
Gemini prerecorded normal activation: FALSE
provider cutover now: FALSE
```

Future free-first routing is recorded but dormant:

```text
Hybrid C/D: PLANNED / NOT_IMPLEMENTED
trigger: AssemblyAI free credits exhausted
implementation before trigger: FORBIDDEN BY CURRENT PLAN
```

## M4 current state

Repository-only deployment-image parity preflight is complete.

```text
KRC managed routes in shared server: PASS_STATIC
KRC environment surface: PASS_STATIC
Node 24 runtime contract: PASS_STATIC
ffmpeg/ffprobe runtime availability: FAIL
psql runtime availability: FAIL
M4_CANARY_READY: FALSE
```

VoiceBridge authority:

`docs/history/2026-09-02_KRC_MEDIA_M4_DEPLOYMENT_IMAGE_PARITY_PREFLIGHT.md`

Next engineering step:

```text
feature-branch image parity remediation
 -> add minimum runtime media/PostgreSQL client packages
 -> add final-image CI checks
 -> no-provider-call route startup smoke
 -> full validation
 -> STOP at owner deployment/canary gate
```

## Release boundary

```text
R1 merge: HOLD
R2 backend promotion: HOLD
R3 external testers: HOLD
R4 public rollout: HOLD
RELEASE_HOLD_OWNER_TESTING: PRESERVED
```

## Recovery command

`recover KRC MEDIA BETA checkpoint 70 M3 closed M4 preflight blocked 2026-09-02`

Always verify current GitHub heads/CI before any write, deployment, provider-consuming operation, merge, or activation decision.
