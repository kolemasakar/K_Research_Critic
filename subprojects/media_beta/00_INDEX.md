# MEDIA BETA Documentation Index
Канонічний індекс документації приватного K-Research & Critic MEDIA BETA.

Version: 5.3
Status: ACTIVE / RELEASE_HOLD_OWNER_TESTING / M3_CLOSED / M4_OWNER_CANARY_ACCEPTED / R0_PUBLIC_KRC_UPDATE_PREFLIGHT_PLANNED
Updated: 2026-09-04

## Product boundary

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the already-published `K-Research & Critic` product. `K_Research_Critic` remains the product/roadmap authority. VoiceBridge provides media/backend technology, implementation, and validation evidence.

The public KRC is already user-accessible. The separate MEDIA BETA GPT remains owner-only. Future MEDIA integration must preserve the existing public KRC identity and keep MEDIA additive/failure-isolated.

## Canonical reading order

1. `72_M4_OWNER_CANARY_ACCEPTED_ROLLBACK_COMPLETE_CHECKPOINT_2026_09_02.md` - current operational recovery authority.
2. `planning/PUBLIC_KRC_MEDIA_INTEGRATION_UPDATE_SAFETY_PLAN_2026_09_04.md` - approved next planning/governance sequence for safe integration into the existing published KRC.
3. `71_M4_IMAGE_PARITY_READY_OWNER_CANARY_DECISION_CHECKPOINT_2026_09_02.md` - preceding image-parity/canary gate.
4. `69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md` - deferred future Hybrid C/D plan.
5. `68_M3B_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md` - completed seven-case provider evidence before M3 closure.
6. `62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md` - complete earlier cross-repository baseline.
7. `02_ROADMAP.md`, `03_CURRENT_STATE.md`, `06_DECISION_LOG.md`, `08_CHAT_HANDOFF.md` - roadmap/state/decisions/handoff.
8. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` - historical release-hold authority.

VoiceBridge technical plan for the new integration-safety sequence:

`docs/planning/2026-09-04_KRC_PUBLIC_GPT_MEDIA_INTEGRATION_SAFETY_PREFLIGHT.md`

## Current provider state

```text
M3: CLOSED
current KRC prerecorded provider: AssemblyAI universal-2
Gemini prerecorded normal activation: FALSE
provider cutover now: FALSE
Hybrid C/D: PLANNED / NOT_IMPLEMENTED
Hybrid trigger: AssemblyAI free credits exhausted plus fresh owner decision
```

## M4 accepted state

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

Canary workflow run:

`33580592224` - SUCCESS.

The isolated Render service was restored to its exact pre-canary commit after validation.

## Next gate sequence

The owner approved the following safe integration order:

```text
R0  Public KRC Update Safety Preflight
R1  Repository integration
R2  Permanent MEDIA backend promotion/readiness
R3  Update existing published KRC GPT
R4  Post-update public-access + Core regression verification
```

Current point:

```text
R0: PLANNED / NEXT
R1: HOLD
R2: HOLD
R3: HOLD
R4: HOLD
```

No live GPT change, repository merge, permanent backend promotion, or public MEDIA exposure is authorized by the planning update itself.

## Critical integration invariant

```text
MEDIA unavailable/fails -> MEDIA request unavailable/fails closed
Core KRC              -> remains user-accessible and functional
```

The public KRC must never depend on the private MEDIA BETA GPT identity.

## Recovery command

Operational recovery remains:

`recover KRC MEDIA BETA checkpoint 72 M4 owner canary accepted rollback complete 2026-09-02`

Then read the 2026-09-04 public-KRC integration safety plan before any R1/R2/R3 work.

Always verify current GitHub heads/CI, current OpenAI Builder/update capabilities, and current external infrastructure before any write, provider-consuming operation, merge, permanent deployment, or live GPT update.
