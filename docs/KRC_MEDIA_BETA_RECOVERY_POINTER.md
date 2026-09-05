# K-Research & Critic - MEDIA BETA Recovery Pointer
Канонічний покажчик поточного стану MEDIA BETA після розділення приватного та публічного Action-контрактів і підготовки public Cobalt schema.

Status: ACTIVE POINTER / CHECKPOINT 83 / R2 REPOSITORY READY / LIVE COBALT DEPLOYMENT + CANARY PENDING / R3 HOLD
Updated: 2026-09-05

`K-Research & Critic - MEDIA BETA` remains an additive MEDIA capability planned for the existing published `K-Research & Critic` identity.

## Current canonical checkpoint

Repository:

`kolemasakar/K_Research_Critic`

Branch:

`main`

Path:

`subprojects/media_beta/83_R2_PUBLIC_ACTION_SCHEMA_REPOSITORY_READY_2026_09_05.md`

## Current gate state

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

## Action contract split

Private MEDIA BETA compatibility contract:

```text
gpt_store/actions/media_managed_beta_openapi.yaml
version: 0.6.0-a9.10
status: preserved for private/historical beta compatibility
```

Initial public MEDIA candidate contract:

```text
gpt_store/actions/media_public_cobalt_openapi.yaml
version: 0.7.0-r2-cobalt
status: repository candidate / not publicly activated
```

The public contract exposes only the accepted initial URL routes. It does not expose Supadata credit operations, ScrapeCreators paid retrieval operations, local attachment transcription, or attachment probe operations.

KRC schema validation baseline:

```text
commit: 24331dcd517c2a4b528b1e45bee7f9d835df613f
Tests: 33931976922 / SUCCESS
```

## Current live backend

Last confirmed live MEDIA baseline:

```text
Render MEDIA service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
live deploy: dep-dadfu1mq1p3s73dgv5m0
live commit: 7c8806713ea75b0809b638f102e31d8d3af86150
autoDeploy: no
```

The current live backend still contains the Supadata public path. The Cobalt public candidate has not been deployed.

Immediate rollback target for the next Cobalt deployment:

`7c8806713ea75b0809b638f102e31d8d3af86150`

Historical original R2 rollback baseline:

`2f0f02769dbdf2e8240e6b08867ecef2faaede16`

## Current VoiceBridge candidate

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
current synchronized head: 5003689ad2fe4c850d47dc7777c50470820b0bff
Cobalt implementation commit: 4384b8dc8ef949ded7859495808b7f138eb8244d
current-head Validate: 33917780763 / SUCCESS
implementation Validate: 33916332270 / SUCCESS
implementation cloud tests: 239 passed / 0 failed
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true
```

## Public free-only routing target

```text
YouTube   -> self-hosted Cobalt -> AssemblyAI universal-2 -> durable KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 -> durable KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 -> durable KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 -> durable KRCM/Neon
```

Public Action rules:

```text
Supadata public route: inactive
ScrapeCreators public paid route: forbidden
paid retrieval fallback: none
paid STT fallback: none
user beta access code: not exposed
Action bearer: server-side
```

## Active STT policy

```text
KRC_MEDIA_STT_PROVIDER=assemblyai
AssemblyAI model=universal-2
AssemblyAI continuation=Free balance only
paid AssemblyAI continuation=forbidden
post-AssemblyAI target=Gemini prerecorded
Gemini automatic cutover=not implemented
Gemini Free public activation=separate disclosure + explicit consent gate
paid Gemini fallback=none
```

## Public KRC boundary

The existing published `K-Research & Critic` GPT remains unchanged. No public MEDIA Action has been attached in Builder. The current Core manifest therefore continues to record Actions as disabled and still matches the live public Builder state.

## Retained invariant

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

Recovery must start from checkpoint 83.

Before any state-changing action, re-read exact GitHub heads/CI, current Render live deploy, PR #45 state, and the current KRC public Builder state. Do not deploy, mutate Render/Neon, merge PR #45, activate Gemini, or update the public GPT without fresh explicit owner authorization.
