# MEDIA BETA Chat Handoff
Канонічна інструкція відновлення K-Research & Critic - MEDIA BETA у новому чаті.

Version: 4.8
Status: ACTIVE_HANDOFF / RELEASE_HOLD_OWNER_TESTING / M3_CLOSED / M4_OWNER_CANARY_ACCEPTED / R0_PUBLIC_KRC_UPDATE_PREFLIGHT_NEXT
Checkpoint date: 2026-09-02
Planning update: 2026-09-04

## Recovery command

`recover KRC MEDIA BETA checkpoint 72 M4 owner canary accepted rollback complete 2026-09-02`

Then immediately read:

`subprojects/media_beta/planning/PUBLIC_KRC_MEDIA_INTEGRATION_UPDATE_SAFETY_PLAN_2026_09_04.md`

## Mandatory recovery order

1. `subprojects/media_beta/72_M4_OWNER_CANARY_ACCEPTED_ROLLBACK_COMPLETE_CHECKPOINT_2026_09_02.md`
2. `subprojects/media_beta/planning/PUBLIC_KRC_MEDIA_INTEGRATION_UPDATE_SAFETY_PLAN_2026_09_04.md`
3. `subprojects/media_beta/00_INDEX.md`
4. `subprojects/media_beta/02_ROADMAP.md`
5. `subprojects/media_beta/03_CURRENT_STATE.md`
6. `subprojects/media_beta/06_DECISION_LOG.md`
7. `subprojects/media_beta/69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md`
8. `subprojects/media_beta/68_M3B_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md`
9. `subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md`

VoiceBridge technical safety plan:

`docs/planning/2026-09-04_KRC_PUBLIC_GPT_MEDIA_INTEGRATION_SAFETY_PREFLIGHT.md`

Verify current GitHub heads/CI, current OpenAI Builder/update capabilities, and current external infrastructure before any write, provider-consuming operation, merge, permanent deployment, or live GPT update.

## Product reality

```text
public KRC GPT:                    already published / user-accessible
private KRC MEDIA BETA GPT:        owner-only / not separately published
integration target:                existing published KRC identity
new GPT publication dependency:    FORBIDDEN
```

MEDIA must remain additive and failure-isolated:

```text
MEDIA failure/unavailability -> MEDIA unavailable/fails closed
Core KRC                   -> remains user-accessible and functional
```

## Current provider decision

```text
M3: CLOSED
current KRC prerecorded provider: AssemblyAI universal-2
Gemini prerecorded normal activation: FALSE
provider cutover now: FALSE
Hybrid C/D: PLANNED / NOT_IMPLEMENTED until AssemblyAI free-credit trigger plus fresh owner approval
```

## M4 accepted state

```text
M4_IMAGE_PARITY: PASS
M4_OWNER_CANARY: PASS
real Telegram -> AssemblyAI job: PASS
STT seconds: 53
retrieval credits: 0
provider cleanup: PASS
Neon durable readback: PASS
duplicate reuse / one STT reservation: PASS
mandatory rollback: PASS
M4_PERMANENT_BACKEND_PROMOTION: NOT_AUTHORIZED
```

VoiceBridge canary run: `33580592224` / SUCCESS.

The isolated Render service was restored to exact pre-canary commit `2f0f02769dbdf2e8240e6b08867ecef2faaede16`.

## New independent gate sequence

```text
R0  Public KRC Update Safety Preflight
R1  Repository integration
R2  Permanent MEDIA backend promotion/readiness
R3  Update existing published KRC GPT
R4  Post-update public-access + Core regression verification
```

Current gate state:

```text
R0: PLANNED / REQUIRED NEXT / NO LIVE CHANGE
R1: HOLD
R2: HOLD
R3: HOLD
R4: HOLD
```

R0 must verify the same existing public KRC can still be edited and updated without requiring a new GPT publication event; record sharing/publication state; revalidate current public Action/Privacy requirements; preserve the current KRC URL/identity; and capture the current GPT configuration sufficiently for rollback/reconstruction.

If safe update of the existing published GPT cannot be verified, STOP before merge/promotion/live GPT changes.

## Critical policy recovery

- Facebook: Cobalt fail -> unavailable; no automatic paid fallback.
- ScrapeCreators: reserve only / inactive.
- Telegram: public-only, zero retrieval credits.
- Local attachment: max 32 MiB, zero retrieval credits.
- AssemblyAI remains active while current free-credit plan remains in effect.
- Hybrid C/D remains dormant until its trigger and fresh approval.
- CriticProfile gate remains before Research.
- per-claim independent cross-check accounting remains mandatory.
- A10 copy-safe summary remains mandatory.
- public KRC identity must be preserved through future MEDIA integration.

## Exact continuation point

`R0 PUBLIC KRC UPDATE SAFETY PREFLIGHT / NO LIVE GPT CHANGE`

## Terminal marker

`MEDIA_BETA_HANDOFF_V4_8_R0_PUBLIC_KRC_UPDATE_SAFETY_PREFLIGHT_NEXT`
