# MEDIA BETA Documentation Index

Канонічний індекс документації K-Research & Critic MEDIA BETA.

Version: 6.4
Status: ACTIVE / CHECKPOINT_85 / HANDOFF_READY / R2_REPOSITORY_PIVOT_READY / LIVE_GEMINI_DEPLOYMENT_AND_CANARY_PENDING / R3_HOLD
Updated: 2026-09-07

## Product boundary

`K-Research & Critic - MEDIA BETA` is an additive MEDIA capability intended for the already-published `K-Research & Critic` product. `K_Research_Critic` remains the product/release authority. VoiceBridge provides the isolated MEDIA backend implementation and validation evidence.

Current product reality:

```text
public KRC: already published / user-accessible / unchanged
private KRC MEDIA BETA: Action-enabled test surface; checkpoint-85 Builder package not applied
future public MEDIA target: same existing public KRC identity
```

Critical invariant:

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

## Canonical reading order

1. `85_R2_GEMINI_DIRECT_HANDOFF_REPOSITORY_SYNC_2026_09_07.md` - current canonical handoff/recovery checkpoint.
2. `84_R2_YOUTUBE_GEMINI_DIRECT_REPOSITORY_READY_2026_09_07.md` - accepted Gemini-direct YouTube repository pivot.
3. `83_R2_PUBLIC_ACTION_SCHEMA_REPOSITORY_READY_2026_09_05.md` - previous Cobalt public Action repository checkpoint.
4. `82_R2_PUBLIC_COBALT_RECONCILIATION_REPOSITORY_SYNC_2026_09_04.md` - Cobalt routing reconciliation checkpoint.
5. `81_R2_LIVE_PROMOTION_PARTIAL_CANARY_2026_09_04.md` - earlier live promotion/partial canary baseline.
6. `80_R2C_PUBLIC_PRIVACY_RENDER_PROMOTION_READY_2026_09_04.md` - pre-promotion privacy/release plan.
7. `79_R2B_FAILURE_ISOLATION_FREE_QUOTA_PASS_2026_09_04.md` - failure-isolation evidence.
8. `78_R2A_PUBLIC_FREE_TIER_ADMISSION_PASS_2026_09_04.md` - public free-only admission policy.
9. `75_R1_REPOSITORY_INTEGRATION_COMPLETE_CHECKPOINT_2026_09_04.md` - completed R1 repository integration.
10. `planning/PUBLIC_KRC_MEDIA_INTEGRATION_UPDATE_SAFETY_PLAN_2026_09_04.md` - R0-R4 release safety plan.

Recovery pointer:

`../../docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`

## Current Action contracts

Current mixed free-only public candidate:

```text
gpt_store/actions/media_public_free_openapi.yaml
version: 0.8.0-r2-gemini-youtube
purpose: future public MEDIA Action for existing KRC GPT
status: repository candidate / not activated in Builder
```

Historical Cobalt public candidate:

```text
gpt_store/actions/media_public_cobalt_openapi.yaml
version: 0.7.0-r2-cobalt
status: superseded as current YouTube target / retained as R2 history
```

Private MEDIA BETA compatibility contract:

```text
gpt_store/actions/media_managed_beta_openapi.yaml
version: 0.6.0-a9.10
purpose: private/historical MEDIA BETA compatibility
```

The current public candidate intentionally excludes private attachment operations, Supadata credit operations, ScrapeCreators paid retrieval, user cookies/login, paid proxy fallback, and automatic paid provider fallback.

## Current public MEDIA routing target

```text
YouTube   -> Gemini Developer API Free Tier direct public URL -> KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 Free -> KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 Free -> KRCM/Neon
```

YouTube requires explicit user consent to the Gemini Developer API Free Tier data-use boundary before new provider work. No Cobalt, AssemblyAI, Supadata, cookie/login, paid proxy, or paid Gemini fallback is allowed for YouTube.

## Why YouTube pivoted from Cobalt

The Cobalt API key was initially Facebook-only and returned `error.api.service.disabled` for YouTube. After the owner expanded the key to `facebook`, `youtube`, and `instagram`, a fresh canary progressed past that policy gate but returned:

```text
error.api.youtube.login
```

The post-change job failed before STT and charged zero retrieval credits / zero STT seconds. This established a YouTube datacenter anti-bot/login boundary incompatible with the accepted no-cookie/no-login/no-paid-proxy public policy.

## VoiceBridge repository state

Checkpoint-85 handoff baseline:

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
head: bae3db8e646baf003689c1d8a8e502d9d2ad832d
Validate: 34146243530 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true
```

Dedicated Gemini YouTube implementation:

```text
src/cloud/src/public_gemini_youtube.ts
src/cloud/tests/public_gemini_youtube.test.ts
```

The accepted candidate no longer contains the temporary Cobalt startup diagnostic used during blocker isolation.

## Current live backend versus repository candidate

Read-only verification on 2026-09-07:

```text
LIVE Render commit:       52499e4959aa2673f07239c73054cdbeaec0eeac
LIVE normal-mode deploy:  dep-dafekmid0e5s73c3sg10
configured branch:        agent/krc-media-transcript
autoDeploy:               no
REPOSITORY CANDIDATE:     bae3db8e646baf003689c1d8a8e502d9d2ad832d
IMMEDIATE LIVE BASELINE:  52499e4959aa2673f07239c73054cdbeaec0eeac
EARLIER ROLLBACK:         7c8806713ea75b0809b638f102e31d8d3af86150
HISTORICAL R2 ROLLBACK:   2f0f02769dbdf2e8240e6b08867ecef2faaede16
```

The Gemini-direct repository candidate is NOT deployed. No Render or Neon mutation is part of checkpoint 85.

## Private R2 canary package

```text
instructions: prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md
manifest: gpt_store/media_r2_gemini_youtube_canary_manifest.yaml
Builder applied: false
```

The package implements one explicit Gemini Free data-use confirmation for new YouTube provider work and forbids the old duplicate MEDIA-start/Supadata credit confirmation. CriticProfile approval remains separate.

## Privacy candidate

```text
docs/PRIVACY_POLICY.md
version: 2.2-candidate
status: PUBLIC_MEDIA_CANDIDATE / NOT_YET_ACTIVATED / FREE_TIER_ONLY
```

## Provider state

```text
YouTube public candidate: Gemini Developer API Free Tier direct URL
YouTube paid Gemini fallback: forbidden
Instagram/Facebook/Telegram prerecorded STT: AssemblyAI universal-2 Free balance only
paid AssemblyAI continuation: forbidden
Supadata public: inactive
ScrapeCreators public paid retrieval: forbidden
```

## Gate sequence and current point

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   REPOSITORY PIVOT READY / LIVE GEMINI DEPLOYMENT + AUTHENTICATED CANARY PENDING
R3   HOLD
R4   HOLD
```

R2 is not complete until the exact accepted VoiceBridge candidate is deployed, the private canary Builder package is applied, bounded authenticated canaries pass for all four platforms, and Core isolation is reverified.

## Next handoff sequence

```text
1. recover checkpoint 85
2. reverify GitHub heads/CI and Render live state
3. exact Gemini-direct VoiceBridge deploy
4. private MEDIA BETA Builder canary package switch
5. bounded four-platform authenticated canary
6. Render + Neon + Core isolation verification
7. only after R2 PASS: separate R3 owner gate
```

## Recovery command

`recover KRC MEDIA BETA checkpoint 85 Gemini direct handoff repository sync 2026-09-07`

Before any state-changing action, reverify GitHub heads/CI, Render live deployment, PR #45 state, and private/public GPT Builder configuration.
