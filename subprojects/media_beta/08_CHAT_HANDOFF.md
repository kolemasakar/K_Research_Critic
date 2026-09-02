# MEDIA BETA Chat Handoff
Канонічна інструкція відновлення K-Research & Critic - MEDIA BETA у новому чаті.

Version: 4.7
Status: ACTIVE_HANDOFF / RELEASE_HOLD_OWNER_TESTING / M3_CLOSED / M4_OWNER_CANARY_ACCEPTED
Checkpoint date: 2026-09-02

## Recovery command

`recover KRC MEDIA BETA checkpoint 72 M4 owner canary accepted rollback complete 2026-09-02`

## Mandatory recovery order

1. `subprojects/media_beta/72_M4_OWNER_CANARY_ACCEPTED_ROLLBACK_COMPLETE_CHECKPOINT_2026_09_02.md`
2. `subprojects/media_beta/71_M4_IMAGE_PARITY_READY_OWNER_CANARY_DECISION_CHECKPOINT_2026_09_02.md`
3. `subprojects/media_beta/69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md`
4. `subprojects/media_beta/68_M3B_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md`
5. `subprojects/media_beta/62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md`
6. `subprojects/media_beta/00_INDEX.md`
7. `subprojects/media_beta/02_ROADMAP.md`
8. `subprojects/media_beta/06_DECISION_LOG.md`
9. `subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md`

Verify current GitHub heads and CI plus current external infrastructure before any write, provider-consuming operation, merge, permanent deployment, or activation decision.

## Current provider decision

```text
M3: CLOSED
current KRC prerecorded provider: AssemblyAI universal-2
Gemini prerecorded normal activation: FALSE
provider cutover now: FALSE
Hybrid C/D: PLANNED / NOT_IMPLEMENTED until AssemblyAI free-credit trigger plus fresh owner approval
```

## M4 current state

M4 final-image parity and bounded owner-only canary are accepted.

VoiceBridge authorities:

`docs/history/2026-09-02_KRC_MEDIA_M4_IMAGE_PARITY_REMEDIATION_ACCEPTANCE.md`

`docs/history/2026-09-02_KRC_MEDIA_M4_OWNER_CANARY_ACCEPTANCE.md`

Exact canary evidence:

```text
M4 target: 6a9491359795840ec9e79c9edc0ea82f595e9784
workflow run: 33580592224
result: SUCCESS
isolated Render service: voicebridge-krc-media-beta-kolemasakar
real Telegram -> AssemblyAI job: PASS
STT seconds: 53
retrieval credits: 0
provider cleanup: PASS
Neon durable readback: PASS
duplicate reuse / one STT reservation: PASS
invalid/private Telegram boundary: PASS
mandatory rollback: PASS
restored pre-canary commit: 2f0f02769dbdf2e8240e6b08867ecef2faaede16
```

The one-shot canary workflow was removed after execution. No permanent M4 backend promotion occurred.

```text
M4_IMAGE_PARITY: PASS
M4_OWNER_CANARY: PASS
M4_PERMANENT_BACKEND_PROMOTION: NOT_AUTHORIZED
```

## Exact continuation point

```text
OWNER POST-CANARY DECISION
R1 MERGE AND R2 BACKEND PROMOTION REMAIN SEPARATE GATES
```

Before R1 or R2, revalidate current repository heads/CI, scope/diff, Render live baseline, rollback target, environment presence without exposing secrets, Neon connectivity, provider state, and release-hold invariants.

## Release boundary

```text
R1 merge: HOLD
R2 backend/production promotion: HOLD
R3 external testers: HOLD
R4 public rollout: HOLD
```

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

## Terminal marker

`MEDIA_BETA_HANDOFF_V4_7_M4_OWNER_CANARY_ACCEPTED_POST_CANARY_GATE`
