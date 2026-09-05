# MEDIA BETA Documentation Index

Канонічний індекс документації K-Research & Critic MEDIA BETA.

Version: 6.2
Status: ACTIVE / CHECKPOINT_83 / R2_REPOSITORY_READY / LIVE_COBALT_DEPLOYMENT_AND_CANARY_PENDING / R3_HOLD
Updated: 2026-09-05

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

1. `83_R2_PUBLIC_ACTION_SCHEMA_REPOSITORY_READY_2026_09_05.md` - current canonical recovery checkpoint.
2. `82_R2_PUBLIC_COBALT_RECONCILIATION_REPOSITORY_SYNC_2026_09_04.md` - Cobalt routing reconciliation checkpoint.
3. `81_R2_LIVE_PROMOTION_PARTIAL_CANARY_2026_09_04.md` - live promotion baseline and partial Supadata canary checkpoint.
4. `80_R2C_PUBLIC_PRIVACY_RENDER_PROMOTION_READY_2026_09_04.md` - pre-promotion privacy/release plan.
5. `79_R2B_FAILURE_ISOLATION_FREE_QUOTA_PASS_2026_09_04.md` - failure-isolation evidence.
6. `78_R2A_PUBLIC_FREE_TIER_ADMISSION_PASS_2026_09_04.md` - public free-only admission policy.
7. `75_R1_REPOSITORY_INTEGRATION_COMPLETE_CHECKPOINT_2026_09_04.md` - completed R1 repository integration.
8. `planning/PUBLIC_KRC_MEDIA_INTEGRATION_UPDATE_SAFETY_PLAN_2026_09_04.md` - R0-R4 release safety plan.

Recovery pointer:

`../../docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`

## Action contracts

Private MEDIA BETA contract preserved:

```text
gpt_store/actions/media_managed_beta_openapi.yaml
version: 0.6.0-a9.10
purpose: private/historical MEDIA BETA compatibility
```

Initial public MEDIA candidate:

```text
gpt_store/actions/media_public_cobalt_openapi.yaml
version: 0.7.0-r2-cobalt
purpose: future public MEDIA Action for existing KRC GPT
status: repository candidate / not activated in Builder
```

The public candidate intentionally excludes private attachment operations, Supadata credit-consent operations, and reserved paid Facebook retrieval operations.

KRC schema regression:

```text
baseline commit: 24331dcd517c2a4b528b1e45bee7f9d835df613f
Tests: 33931976922 / SUCCESS
```

## VoiceBridge repository state

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

Supadata remains historical/private compatibility code and is not part of the initial public Action contract. ScrapeCreators paid retrieval remains forbidden in public free-only mode. No automatic paid retrieval/STT fallback is authorized.

## STT provider state

```text
current KRC prerecorded provider: AssemblyAI universal-2
AssemblyAI use: Free balance only
paid AssemblyAI continuation: forbidden
post-AssemblyAI target: Gemini prerecorded
Gemini automatic cutover: NOT IMPLEMENTED
Gemini public Free activation: separate disclosure + explicit user consent gate
```

## Gate sequence and current point

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   REPOSITORY READY / LIVE COBALT DEPLOYMENT + BOUNDED CANARY PENDING
R3   HOLD
R4   HOLD
```

The repository-side public Action schema gap recorded in checkpoint 82 is closed. R2 is still not complete because the exact Cobalt backend candidate has not been deployed and validated by the bounded four-platform canary.

## Administrative state

The accidental temporary Render service `noop` has been deleted and its absence was confirmed through the Render connector.

## Recovery command

`recover KRC MEDIA BETA checkpoint 83 public Action schema repository ready 2026-09-05`

Before any state-changing action, reverify current GitHub heads and CI, current Render live deployment, current PR #45 state, and current public GPT Builder configuration.
