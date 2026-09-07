# MEDIA BETA Documentation Index

Канонічний індекс документації K-Research & Critic MEDIA BETA.

Version: 6.5
Status: ACTIVE / CHECKPOINT_86 / R2_YOUTUBE_LIVE_ACCEPTED / NON_YOUTUBE_AND_CORE_ISOLATION_PENDING / R3_HOLD
Updated: 2026-09-07

## Product boundary

`K-Research & Critic - MEDIA BETA` is an additive MEDIA capability intended for the already-published `K-Research & Critic` product. `K_Research_Critic` remains the product/release authority. VoiceBridge provides the isolated MEDIA backend implementation and validation evidence.

Current product reality:

```text
public KRC: already published / user-accessible / unchanged
private KRC MEDIA BETA: owner-only / checkpoint-86 canary package active
future public MEDIA target: same existing public KRC identity
```

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

## Canonical reading order

1. `86_R2_YOUTUBE_GEMINI_LIVE_ACCEPTANCE_R3_READINESS_HOLD_2026_09_07.md` - current canonical recovery checkpoint.
2. `85_R2_GEMINI_DIRECT_HANDOFF_REPOSITORY_SYNC_2026_09_07.md` - pre-deployment handoff checkpoint.
3. `84_R2_YOUTUBE_GEMINI_DIRECT_REPOSITORY_READY_2026_09_07.md` - accepted Gemini-direct repository pivot.
4. `83_R2_PUBLIC_ACTION_SCHEMA_REPOSITORY_READY_2026_09_05.md` - previous public Action repository checkpoint.
5. `82_R2_PUBLIC_COBALT_RECONCILIATION_REPOSITORY_SYNC_2026_09_04.md` - Cobalt routing reconciliation.
6. `81_R2_LIVE_PROMOTION_PARTIAL_CANARY_2026_09_04.md` - earlier promotion/partial canary baseline.
7. `80_R2C_PUBLIC_PRIVACY_RENDER_PROMOTION_READY_2026_09_04.md` - privacy/release plan.
8. `79_R2B_FAILURE_ISOLATION_FREE_QUOTA_PASS_2026_09_04.md` - failure-isolation evidence.
9. `78_R2A_PUBLIC_FREE_TIER_ADMISSION_PASS_2026_09_04.md` - public free-only admission policy.
10. `75_R1_REPOSITORY_INTEGRATION_COMPLETE_CHECKPOINT_2026_09_04.md` - completed R1 integration.

Recovery pointer:

`../../docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`

## Current Action contract

```text
gpt_store/actions/media_public_free_openapi.yaml
version: 0.8.0-r2-gemini-youtube
status: private canary active / public KRC not activated
```

Historical contracts remain preserved:

```text
gpt_store/actions/media_public_cobalt_openapi.yaml  version 0.7.0-r2-cobalt
gpt_store/actions/media_managed_beta_openapi.yaml   version 0.6.0-a9.10
```

## Current routing target

```text
YouTube   -> Gemini Developer API Free Tier direct public URL -> KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 Free -> KRCM/Neon
```

No paid retrieval, paid STT, paid proxy, user-cookie/login, or automatic paid fallback is authorized.

## VoiceBridge and Render state

```text
VoiceBridge repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
head: 68a39d9109455c3e9e69ffeb3a7456998f0620db
Validate: 34147736126 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true

Render service: voicebridge-krc-media-beta-kolemasakar
configured branch: agent/krc-media-gemini-migration
autoDeploy: no
live deploy: dep-dafgkjm7bikc738hmi20
live commit: 68a39d9109455c3e9e69ffeb3a7456998f0620db
status: LIVE
rollback baseline: 52499e4959aa2673f07239c73054cdbeaec0eeac
```

## Private R2 canary package

```text
instructions: prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md
manifest: gpt_store/media_r2_gemini_youtube_canary_manifest.yaml
Builder applied: true
sharing: owner-only
```

The final Action schema uses inline pagination parameters for GPT Builder compatibility.

## YouTube live acceptance

```text
capability read: PASS
explicit Gemini Free data-use consent: PASS
new Gemini provider execution: PASS
Neon durable completion: PASS
provider_model: gemini-3.7-flash
retrieval_credits_charged: 0
stt_seconds_charged: 0
segment retrieval: PASS
CriticProfile separation: PASS
duplicate durable reuse: PASS
new provider work on reuse: NO
```

## Gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   PARTIAL PASS: LIVE + YOUTUBE ACCEPTED / NON-YOUTUBE + CORE ISOLATION PENDING
R3   HOLD / NOT READY
R4   HOLD
```

Full R2 still requires current-deployment bounded Instagram, Facebook, and Telegram canaries, remaining Render/Neon delta and no-paid-fallback verification, and Core KRC failure-isolation regression.

## Next sequence

```text
1. recover checkpoint 86
2. reverify GitHub / Render / private+public Builder state
3. bounded Instagram canary
4. bounded Facebook canary
5. bounded Telegram canary
6. Render + Neon delta/no-paid-fallback verification
7. Core KRC isolation regression including forced MEDIA failure
8. if all PASS -> record full R2 PASS
9. only then -> separate explicit R3 owner gate
```

## Recovery command

`recover KRC MEDIA BETA checkpoint 86 YouTube Gemini live acceptance R3 readiness hold 2026-09-07`
