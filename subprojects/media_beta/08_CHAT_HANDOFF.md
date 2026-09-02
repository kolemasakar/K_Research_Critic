# MEDIA BETA Chat Handoff
Канонічна інструкція відновлення K-Research & Critic - MEDIA BETA у новому чаті.

Version: 4.6
Status: ACTIVE_HANDOFF / RELEASE_HOLD_OWNER_TESTING / M3_CLOSED / M4_IMAGE_PARITY_READY / OWNER_CANARY_DECISION
Checkpoint date: 2026-09-02

## Recovery command

`recover KRC MEDIA BETA checkpoint 71 M4 image parity ready owner canary decision 2026-09-02`

## Mandatory recovery order

1. `subprojects/media_beta/71_M4_IMAGE_PARITY_READY_OWNER_CANARY_DECISION_CHECKPOINT_2026_09_02.md`
2. `subprojects/media_beta/70_M3_CLOSED_M4_PREFLIGHT_BLOCKED_CHECKPOINT_2026_09_02.md`
3. `subprojects/media_beta/69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md`
4. `subprojects/media_beta/68_M3B_AB_COMPLETE_OWNER_DECISION_CHECKPOINT_2026_09_01.md`
5. `subprojects/media_beta/62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md`
6. `subprojects/media_beta/00_INDEX.md`
7. `subprojects/media_beta/02_ROADMAP.md`
8. `subprojects/media_beta/06_DECISION_LOG.md`
9. `subprojects/media_beta/53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md`

Verify current GitHub heads and CI before any write, provider-consuming operation, merge, deployment, or activation decision.

## Current provider decision

```text
M3: CLOSED
current KRC prerecorded provider: AssemblyAI universal-2
Gemini prerecorded normal activation: FALSE
provider cutover now: FALSE
Hybrid C/D: PLANNED / NOT_IMPLEMENTED until AssemblyAI free-credit trigger
```

## M4 current state

M4 repository preflight and final-image remediation are complete.

VoiceBridge acceptance authority:

`docs/history/2026-09-02_KRC_MEDIA_M4_IMAGE_PARITY_REMEDIATION_ACCEPTANCE.md`

Exact accepted evidence:

```text
VoiceBridge commit: 6a9491359795840ec9e79c9edc0ea82f595e9784
Validate run: 33577022166
krc-image-parity: SUCCESS
cloud: SUCCESS
browser-extension: SUCCESS
repository-docs: SUCCESS
```

The final runtime image contains and validates:

```text
ffmpeg
ffprobe
psql
```

The final image also passes a no-provider-call KRC managed-route startup smoke.

```text
M4_IMAGE_PARITY: PASS
M4_DEPLOYMENT: NOT_PERFORMED
M4_CANARY: NOT_RUN
```

## Exact continuation point

```text
M4 OWNER DEPLOYMENT/CANARY DECISION
```

Do not deploy or start a canary without explicit owner approval.

If owner approval is later given, first revalidate the exact target service, exact commit/image, environment presence without exposing secrets, Neon connectivity, Cobalt health, AssemblyAI operating state, Action compatibility, and rollback target.

## Release boundary

```text
R1 merge: HOLD
R2 backend/production promotion: HOLD unless separately scoped for owner canary
R3 external testers: HOLD
R4 public rollout: HOLD
```

## Critical policy recovery

- Facebook: Cobalt fail -> unavailable; no automatic paid fallback.
- Telegram: public-only, zero retrieval credits.
- Local attachment: max 32 MiB, zero retrieval credits.
- AssemblyAI remains active while current free-credit plan remains in effect.
- Hybrid C/D remains dormant until its trigger and fresh approval.
- CriticProfile gate remains before Research.
- per-claim independent cross-check accounting remains mandatory.
- A10 copy-safe summary remains mandatory.

## Terminal marker

`MEDIA_BETA_HANDOFF_V4_6_M4_IMAGE_PARITY_READY_OWNER_CANARY_DECISION`
