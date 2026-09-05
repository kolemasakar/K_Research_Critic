# K-Research & Critic / MEDIA BETA - R2 Public Action Schema Repository-Ready Checkpoint 83

Date: 2026-09-05
Status: R2_REPOSITORY_READY / PUBLIC_ACTION_SCHEMA_READY / LIVE_COBALT_DEPLOYMENT_AND_CANARY_PENDING / R3_HOLD

## Scope

This checkpoint supersedes checkpoint 82 as the canonical repository recovery point.

It records completion of the repository-side Action-contract split required by the Cobalt public architecture. No Render deployment, Render environment mutation, Neon mutation, GPT Builder update, public GPT change, VoiceBridge PR merge, Gemini activation, or provider-consuming canary was performed while creating this checkpoint.

## Key architecture correction

The historical private MEDIA BETA Action contract and the future public MEDIA Action contract are intentionally separate.

Private beta contract preserved:

```text
path: gpt_store/actions/media_managed_beta_openapi.yaml
version: 0.6.0-a9.10
purpose: historical/private MEDIA BETA compatibility
contains: accepted private Supadata consent paths, local attachments, and reserved compatibility surfaces
```

Public candidate contract added:

```text
path: gpt_store/actions/media_public_cobalt_openapi.yaml
version: 0.7.0-r2-cobalt
release state: R2_REPOSITORY_CANDIDATE_NOT_PUBLICLY_ACTIVATED
purpose: initial public MEDIA Action for the existing published KRC identity
```

The public contract does not replace or redefine the private beta contract.

## Public Action route surface

The initial public schema exposes only:

```text
GET  /api/v1/media/managed
POST /api/v1/media/managed/preflight
POST /api/v1/media/managed/lookup
POST /api/v1/media/managed/transcriptions
POST /api/v1/media/managed/facebook-fallback
POST /api/v1/media/managed/telegram
GET  /api/v1/media/managed/transcriptions/{job_id}
GET  /api/v1/media/managed/transcriptions/{job_id}/segments
```

The public schema deliberately does not expose:

```text
Supadata native-credit operations
Supadata AI-credit operations
ScrapeCreators paid-retrieval operations
local attachment transcription
attachment transport probe
owner beta admission codes
provider credentials
```

`job_id` path parameters are inline for GPT Builder parser compatibility.

## Public free-only routing contract

```text
YouTube   -> self-hosted Cobalt -> AssemblyAI universal-2 -> durable KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 -> durable KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 -> durable KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 -> durable KRCM/Neon
```

Public contract declarations include:

```text
supadata_public_active=false
youtube_retrieval_provider=cobalt
youtube_retrieval_credits=0
instagram_retrieval_provider=cobalt
instagram_retrieval_credits=0
facebook_free_retrieval_provider=cobalt
facebook_paid_retrieval_configured=false
facebook_automatic_paid_retrieval=false
telegram_retrieval_provider=telegram_public_web
telegram_retrieval_credits=0
paid_retrieval_fallback=false
paid_stt_fallback=false
user_beta_access_code_required=false
owner_access_injected_server_side=true
```

The YouTube/Instagram request schema requires only a public URL plus an optional language hint. It has no Supadata credit consent field.

## KRC repository validation

Public schema hardening baseline:

```text
KRC commit: 24331dcd517c2a4b528b1e45bee7f9d835df613f
Tests workflow: 33931976922
conclusion: SUCCESS
```

The test suite now contains a dedicated public Action-schema regression at:

`tests/test_krc_media_public_cobalt_action_schema.py`

The regression verifies the bounded public route set, absence of legacy paid/attachment operations, Cobalt routing declarations, zero retrieval-credit accounting, no Supadata consent field, and inline GPT Builder job-id parameters.

An earlier attempt to overwrite the private schema failed historical private-package regressions. That result was treated as an architecture signal, not bypassed. The repository was corrected by restoring the private schema and creating the dedicated public schema. The corrected split is the accepted repository state.

## VoiceBridge backend candidate

Repository:

`kolemasakar/VoiceBridge`

```text
branch: agent/krc-media-gemini-migration
current synchronized head: 5003689ad2fe4c850d47dc7777c50470820b0bff
Cobalt implementation commit: 4384b8dc8ef949ded7859495808b7f138eb8244d
current-head Validate: 33917780763 / SUCCESS
implementation Validate: 33916332270 / SUCCESS
implementation cloud tests: 239 passed / 0 failed
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true
```

The VoiceBridge synchronized head is a documentation-only descendant of the Cobalt implementation commit.

## Current live backend baseline

The last confirmed live MEDIA baseline remains:

```text
Render service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
live deploy: dep-dadfu1mq1p3s73dgv5m0
live commit: 7c8806713ea75b0809b638f102e31d8d3af86150
autoDeploy: no
```

The live baseline still contains the Supadata public path. The Cobalt public candidate has not been deployed.

Next immediate rollback target for a Cobalt deployment:

`7c8806713ea75b0809b638f102e31d8d3af86150`

Historical original R2 rollback baseline:

`2f0f02769dbdf2e8240e6b08867ecef2faaede16`

## STT policy retained

```text
KRC prerecorded current provider: AssemblyAI universal-2
AssemblyAI use: Free balance only
paid AssemblyAI continuation: forbidden
post-AssemblyAI target: Gemini prerecorded
Gemini automatic cutover: NOT IMPLEMENTED
Gemini public Free activation: separate disclosure + explicit user consent gate
paid Gemini fallback: none
```

## Public KRC boundary

The existing published `K-Research & Critic` GPT remains unchanged. Its current Core manifest continues to record Actions as disabled because that still matches the actual public Builder state.

The new `media_public_cobalt_openapi.yaml` is a release candidate artifact only. It must not be interpreted as evidence that public MEDIA is already active.

## Gate state

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

R2 must not be marked complete until the exact accepted Cobalt VoiceBridge candidate is deployed and bounded authenticated canaries for YouTube, Instagram, Facebook, and Telegram plus Core-isolation checks pass.

## Retained invariant

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

## Recovery instruction

Recovery must start from checkpoint 83 and then re-read:

1. `docs/KRC_MEDIA_BETA_RECOVERY_POINTER.md`;
2. `gpt_store/actions/media_public_cobalt_openapi.yaml`;
3. `gpt_store/actions/media_managed_beta_openapi.yaml` to preserve private compatibility;
4. VoiceBridge branch `agent/krc-media-gemini-migration` exact head and Validate state;
5. Render current live deployment for `srv-da1kic5bedkc73d6fk60`;
6. VoiceBridge PR #45 state.

Do not deploy or mutate Render/Neon, merge PR #45, activate Gemini, or update the public GPT Builder without fresh explicit owner authorization for that state-changing gate.
