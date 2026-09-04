# MEDIA BETA Chat Handoff
Канонічна інструкція відновлення K-Research & Critic - MEDIA BETA у новому чаті.

Version: 4.9
Status: ACTIVE_HANDOFF / CROSS_SYSTEM_CHECKPOINT_73 / R0_PUBLIC_KRC_UPDATE_PREFLIGHT_NEXT
Checkpoint date: 2026-09-04

## Recovery command

`recover KRC MEDIA BETA cross-system checkpoint 73 public KRC MEDIA VoiceBridge 2026-09-04`

## Mandatory recovery order

1. `subprojects/media_beta/73_PUBLIC_KRC_MEDIA_VOICEBRIDGE_CROSS_SYSTEM_TRANSITION_CHECKPOINT_2026_09_04.md`
2. `subprojects/media_beta/planning/PUBLIC_KRC_MEDIA_INTEGRATION_UPDATE_SAFETY_PLAN_2026_09_04.md`
3. `subprojects/media_beta/72_M4_OWNER_CANARY_ACCEPTED_ROLLBACK_COMPLETE_CHECKPOINT_2026_09_02.md`
4. `subprojects/media_beta/00_INDEX.md`
5. `subprojects/media_beta/02_ROADMAP.md`
6. `subprojects/media_beta/03_CURRENT_STATE.md`
7. `subprojects/media_beta/06_DECISION_LOG.md`
8. `subprojects/media_beta/69_POST_ASSEMBLYAI_FREE_CREDITS_HYBRID_STT_PLAN_2026_09_02.md`

VoiceBridge technical cross-reference:

`docs/history/2026-09-04_KRC_MEDIA_VOICEBRIDGE_CROSS_SYSTEM_TRANSITION_CHECKPOINT.md`

VoiceBridge public-integration technical plan:

`docs/planning/2026-09-04_KRC_PUBLIC_GPT_MEDIA_INTEGRATION_SAFETY_PREFLIGHT.md`

## Frozen cross-system state

Owner-confirmed product reality:

```text
public KRC GPT:             already published / user-accessible
private KRC MEDIA BETA GPT: owner-only / not separately published
future public identity:     same existing published KRC
```

Repository/runtime evidence:

```text
KRC main observed head:                39629886e9f1f3841661c759f75279f779a937c8
KRC MEDIA pre-checkpoint head:         5241c36460f7dfe4222ab1b4f0b933cb4da0281c
KRC MEDIA Tests:                      33870130947 / SUCCESS
KRC PR #8:                            OPEN / DRAFT / UNMERGED / DIRTY
KRC MEDIA divergence:                 ahead 568 / behind 78

VoiceBridge pre-reference head:        0252751ca3f4e04b60423cb506de630680fd83a7
VoiceBridge Validate:                 33860807242 / SUCCESS
VoiceBridge PR #45:                   OPEN / DRAFT / UNMERGED / mergeable=true
```

## Accepted MEDIA/VoiceBridge state

```text
M3: CLOSED
AssemblyAI universal-2: ACTIVE for current KRC prerecorded jobs
Gemini prerecorded normal activation: FALSE
Hybrid C/D: PLANNED / NOT IMPLEMENTED / DEFERRED

M4 image parity: PASS
M4 bounded owner canary: PASS
real Telegram -> AssemblyAI STT: PASS
Neon durability/idempotency: PASS
provider cleanup: PASS
mandatory rollback: PASS
permanent backend promotion: NOT AUTHORIZED
```

Canary run: `33580592224` / SUCCESS.

## Canonical relationships

```text
KRC public Core
  -> product/roadmap authority
  -> existing published GPT identity to preserve

KRC MEDIA BETA
  -> private closed-beta module
  -> future additive capability inside same public KRC

VoiceBridge
  -> media/backend implementation + validation
  -> no independent authority to publish/update KRC
```

Critical invariant:

```text
MEDIA failure/unavailability -> MEDIA unavailable/fails closed
Core KRC                   -> remains usable and accessible
```

## Approved gate plan

```text
R0  Public KRC Update Safety Preflight
R1  Repository integration
R2  Permanent MEDIA backend promotion/readiness
R3  Update existing published KRC GPT
R4  Post-update public-access + Core regression verification
```

Current gate state:

```text
R0: NEXT / NO LIVE CHANGE
R1: HOLD
R2: HOLD
R3: HOLD
R4: HOLD
```

R0 must verify safe edit/update of the same existing public KRC, current sharing state, Action/Privacy requirements, public URL/identity preservation, and a rollback/reconstruction snapshot.

R1 must not direct-merge PR #8 as-is; it is currently dirty/diverged and requires a dedicated integration/conflict strategy after R0 PASS.

## Critical retained policies

- Facebook: Cobalt fail -> unavailable; no automatic paid fallback.
- ScrapeCreators: inactive/reserve only.
- Telegram: public-only / zero retrieval credits.
- Local attachment: max 32 MiB / zero retrieval credits.
- AssemblyAI remains active under current free-credit operating choice.
- Hybrid C/D remains dormant until AssemblyAI free-credit exhaustion + fresh approval.
- CriticProfile gate remains before Research.
- per-claim independent cross-check accounting remains mandatory.
- A10 copy-safe summary remains mandatory.
- new GPT publication must not be required for future MEDIA integration.

## Exact continuation point

`R0 PUBLIC KRC UPDATE SAFETY PREFLIGHT / NO LIVE GPT CHANGE`

Before any state-changing action, reverify current GitHub heads/CI, current OpenAI Builder/update capabilities, and current external infrastructure.

## Terminal marker

`MEDIA_BETA_HANDOFF_V4_9_CROSS_SYSTEM_CHECKPOINT_73_R0_NEXT`
