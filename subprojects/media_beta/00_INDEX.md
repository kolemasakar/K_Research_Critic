# MEDIA BETA Documentation Index

Канонічний індекс документації K-Research & Critic MEDIA BETA.

Version: 6.1
Status: ACTIVE / CHECKPOINT_82 / R2_PUBLIC_COBALT_REPOSITORY_PASS / DEPLOYMENT_AND_CANARY_PENDING / R3_HOLD
Updated: 2026-09-04

## Product boundary

`K-Research & Critic - MEDIA BETA` is an additive MEDIA capability intended for the already-published `K-Research & Critic` product. `K_Research_Critic` remains the product/release authority. VoiceBridge provides the isolated MEDIA backend implementation and validation evidence.

Current product reality:

```text
public KRC: already published / user-accessible / unchanged
private KRC MEDIA BETA: Action-enabled test surface
future public MEDIA target: same existing public KRC identity
```

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

## Canonical reading order

1. `82_R2_PUBLIC_COBALT_RECONCILIATION_REPOSITORY_SYNC_2026_09_04.md` - current canonical recovery checkpoint.
2. `81_R2_LIVE_PROMOTION_PARTIAL_CANARY_2026_09_04.md` - previous live promotion baseline and partial canary checkpoint.
3. `80_R2C_PUBLIC_PRIVACY_RENDER_PROMOTION_READY_2026_09_04.md` - pre-promotion privacy/release plan.
4. `79_R2B_FAILURE_ISOLATION_FREE_QUOTA_PASS_2026_09_04.md` - failure-isolation evidence.
5. `78_R2A_PUBLIC_FREE_TIER_ADMISSION_PASS_2026_09_04.md` - public free-only admission policy.
6. `75_R1_REPOSITORY_INTEGRATION_COMPLETE_CHECKPOINT_2026_09_04.md` - completed R1 repository integration.
7. `planning/PUBLIC_KRC_MEDIA_INTEGRATION_UPDATE_SAFETY_PLAN_2026_09_04.md` - R0-R4 release safety plan.

Recovery pointer:

`../../docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`

VoiceBridge technical reconciliation:

`docs/history/2026-09-04_KRC_MEDIA_PUBLIC_COBALT_ROUTING_RECONCILIATION.md`

## Current repository state

KRC canonical repository:

```text
repository: kolemasakar/K_Research_Critic
branch: main
current recovery checkpoint: 82
```

VoiceBridge synchronized candidate:

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
current head: 5003689ad2fe4c850d47dc7777c50470820b0bff
Cobalt implementation: 4384b8dc8ef949ded7859495808b7f138eb8244d
current-head Validate: 33917780763 / SUCCESS
implementation Validate: 33916332270 / SUCCESS
implementation cloud: 239 passed / 0 failed
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true
```

## Current live backend versus repository candidate

```text
LIVE Render commit:          7c8806713ea75b0809b638f102e31d8d3af86150
LIVE Render deploy:          dep-dadfu1mq1p3s73dgv5m0
COBALT IMPLEMENTATION:       4384b8dc8ef949ded7859495808b7f138eb8244d
SYNCHRONIZED VOICEBRIDGE:    5003689ad2fe4c850d47dc7777c50470820b0bff
NEXT IMMEDIATE ROLLBACK:     7c8806713ea75b0809b638f102e31d8d3af86150
HISTORICAL R2 ROLLBACK:      2f0f02769dbdf2e8240e6b08867ecef2faaede16
```

The synchronized Cobalt candidate is not deployed yet.

## Current public MEDIA routing target

```text
YouTube   -> self-hosted Cobalt -> AssemblyAI universal-2 -> KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 -> KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 -> KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 -> KRCM/Neon
```

Supadata remains only as historical/private compatibility code. It is not required by `KRC_MEDIA_PUBLIC_MODE` in the current VoiceBridge repository candidate.

ScrapeCreators paid retrieval remains forbidden in public free-only mode. No automatic paid retrieval/STT fallback is authorized.

## STT provider state

```text
current KRC prerecorded provider: AssemblyAI universal-2
AssemblyAI use: Free balance only
paid AssemblyAI continuation: forbidden
post-AssemblyAI target: Gemini prerecorded
Gemini automatic cutover: NOT IMPLEMENTED
Gemini public Free activation: separate disclosure + explicit user consent gate
```

## Known package gap before R3

The recovery/checkpoint documentation, privacy candidate, VoiceBridge reconciliation note, and PR #45 are synchronized to the Cobalt architecture.

`gpt_store/actions/media_managed_beta_openapi.yaml` still describes the older Supadata-native Action request contract. It must be revised and validated before R3. The public GPT remains unchanged and has no MEDIA Action attached, so this repository mismatch is not a live-public exposure.

## Gate sequence and current point

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   LIVE BASELINE / COBALT REPOSITORY CANDIDATE PASS / DEPLOYMENT + CANARY PENDING
R3   HOLD
R4   HOLD
```

R2 is not complete. The next state-changing gate is exact deployment of the VoiceBridge Cobalt candidate followed by bounded authenticated canaries and Core-isolation verification.

## Administrative state

The accidental temporary Render service `noop` has been deleted and its absence was confirmed through the Render connector.

## Recovery command

`recover KRC MEDIA BETA checkpoint 82 public Cobalt reconciliation 2026-09-04`

Before any state-changing action, reverify current GitHub heads and CI, current Render live deployment, current PR #45 state, and current public GPT Builder configuration.
