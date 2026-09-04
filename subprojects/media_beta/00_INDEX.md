# MEDIA BETA Documentation Index
Канонічний індекс документації приватного K-Research & Critic MEDIA BETA.

Version: 5.4
Status: ACTIVE / CROSS_SYSTEM_CHECKPOINT_73 / R0_PUBLIC_KRC_UPDATE_PREFLIGHT_NEXT
Updated: 2026-09-04

## Product boundary

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the already-published `K-Research & Critic` product. `K_Research_Critic` remains the product/roadmap authority. VoiceBridge provides media/backend technology, implementation, and validation evidence.

Owner-confirmed product reality:

```text
public KRC: already published / user-accessible
KRC MEDIA BETA: owner-only / not separately published
future public integration target: same existing public KRC identity
```

MEDIA must remain additive and failure-isolated. Public KRC must never depend on the private MEDIA BETA GPT identity.

## Canonical reading order

1. `73_PUBLIC_KRC_MEDIA_VOICEBRIDGE_CROSS_SYSTEM_TRANSITION_CHECKPOINT_2026_09_04.md` - current cross-system recovery authority.
2. `planning/PUBLIC_KRC_MEDIA_INTEGRATION_UPDATE_SAFETY_PLAN_2026_09_04.md` - approved R0-R4 integration safety plan.
3. `72_M4_OWNER_CANARY_ACCEPTED_ROLLBACK_COMPLETE_CHECKPOINT_2026_09_02.md` - accepted M4 canary evidence and rollback.
4. `69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md` - deferred future Hybrid C/D plan.
5. `68_M3B_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md` - completed provider evidence before M3 closure.
6. `62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md` - earlier complete cross-repository baseline.
7. `02_ROADMAP.md`, `03_CURRENT_STATE.md`, `06_DECISION_LOG.md`, `08_CHAT_HANDOFF.md` - roadmap/state/decisions/handoff.

VoiceBridge cross-system technical reference:

`docs/history/2026-09-04_KRC_MEDIA_VOICEBRIDGE_CROSS_SYSTEM_TRANSITION_CHECKPOINT.md`

VoiceBridge public-integration technical plan:

`docs/planning/2026-09-04_KRC_PUBLIC_GPT_MEDIA_INTEGRATION_SAFETY_PREFLIGHT.md`

## Current repository state frozen by checkpoint 73

```text
KRC main observed head:                 39629886e9f1f3841661c759f75279f779a937c8
KRC MEDIA branch pre-checkpoint head:   5241c36460f7dfe4222ab1b4f0b933cb4da0281c
KRC MEDIA Tests:                       33870130947 / SUCCESS
KRC PR #8:                             OPEN / DRAFT / UNMERGED / DIRTY
KRC MEDIA vs main:                     ahead 568 / behind 78

VoiceBridge pre-reference head:         0252751ca3f4e04b60423cb506de630680fd83a7
VoiceBridge Validate:                  33860807242 / SUCCESS
VoiceBridge PR #45:                    OPEN / DRAFT / UNMERGED / mergeable=true
```

## Current provider/runtime state

```text
M3: CLOSED
current KRC prerecorded provider: AssemblyAI universal-2
Gemini prerecorded normal activation: FALSE
provider cutover now: FALSE
Hybrid C/D: PLANNED / NOT IMPLEMENTED
Hybrid trigger: AssemblyAI free credits exhausted + fresh owner decision

M4_IMAGE_PARITY: PASS
M4_OWNER_CANARY: PASS
M4_REAL_STT: PASS
M4_DURABILITY/IDEMPOTENCY: PASS
M4_ROLLBACK: PASS
M4_PERMANENT_BACKEND_PROMOTION: NOT AUTHORIZED
```

Canary workflow: `33580592224` / SUCCESS.

## Approved next gate sequence

```text
R0  Public KRC Update Safety Preflight
R1  Repository integration
R2  Permanent MEDIA backend promotion/readiness
R3  Update existing published KRC GPT
R4  Post-update public-access + Core regression verification
```

Current point:

```text
R0: NEXT / NO LIVE CHANGE
R1: HOLD
R2: HOLD
R3: HOLD
R4: HOLD
```

R1 must not direct-merge PR #8 as-is because the branch is currently divergent/dirty. R0 must pass first, then a dedicated integration/conflict strategy is required.

## Critical invariant

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC              -> remains user-accessible and functional
```

## Recovery command

`recover KRC MEDIA BETA cross-system checkpoint 73 public KRC MEDIA VoiceBridge 2026-09-04`

Before any state-changing action, reverify current GitHub heads/CI, current OpenAI Builder/update capabilities, and current external infrastructure.
