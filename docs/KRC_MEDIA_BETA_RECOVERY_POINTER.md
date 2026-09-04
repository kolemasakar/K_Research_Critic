# K-Research & Critic - MEDIA BETA Recovery Pointer
Канонічний покажчик поточного стану MEDIA BETA після R2 live promotion, невдалого YouTube Supadata canary та repository-only переходу public YouTube/Instagram на self-hosted Cobalt.

Status: ACTIVE POINTER / R2 LIVE BASELINE / PUBLIC COBALT CANDIDATE REPOSITORY PASS / DEPLOYMENT + CANARY PENDING / R3 HOLD
Updated: 2026-09-04

`K-Research & Critic - MEDIA BETA` remains an additive MEDIA capability planned for the existing published `K-Research & Critic` identity.

## Current canonical checkpoint

Repository:

`kolemasakar/K_Research_Critic`

Branch:

`main`

Path:

`subprojects/media_beta/82_R2_PUBLIC_COBALT_RECONCILIATION_REPOSITORY_SYNC_2026_09_04.md`

## Current gate state

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

## Current live backend

Read-only Render recheck confirms:

```text
Render MEDIA service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
live deploy: dep-dadfu1mq1p3s73dgv5m0
live commit: 7c8806713ea75b0809b638f102e31d8d3af86150
status: live
autoDeploy: no
```

Current live still contains the Supadata public path. It is the immediate rollback point for the next exact Cobalt candidate deployment.

Historical original R2 rollback baseline:

`2f0f02769dbdf2e8240e6b08867ecef2faaede16`

## Current repository candidate

VoiceBridge:

```text
repository: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
current synchronized head: 5003689ad2fe4c850d47dc7777c50470820b0bff
Cobalt implementation commit: 4384b8dc8ef949ded7859495808b7f138eb8244d
Validate current head: 33917780763 / SUCCESS
Validate implementation: 33916332270 / SUCCESS
implementation cloud tests: 239 passed / 0 failed
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true
```

The current VoiceBridge head is a documentation-only descendant of the Cobalt implementation commit. The Cobalt candidate has not been deployed.

## Public free-only routing target

```text
YouTube   -> self-hosted Cobalt -> AssemblyAI universal-2 -> durable KRCM/Neon
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2 -> durable KRCM/Neon
Facebook  -> self-hosted Cobalt -> AssemblyAI universal-2 -> durable KRCM/Neon
Telegram  -> public Telegram web -> AssemblyAI universal-2 -> durable KRCM/Neon
```

Supadata remains historical/private compatibility code but is no longer required by `KRC_MEDIA_PUBLIC_MODE` in the repository candidate.

Paid retrieval fallback remains forbidden. ScrapeCreators remains inactive in public free-only mode.

## Canary finding

Private YouTube Action canary attempts failed closed on the Supadata public/free-tier dependency. No successful transcript was produced and no paid fallback was enabled.

This triggered architecture reconciliation rather than further weakening of the Supadata guard.

The next live validation must occur only after exact deployment of the synchronized Cobalt candidate and must cover:

```text
YouTube via Cobalt
Instagram via Cobalt
Facebook via Cobalt
Telegram via public web
Action authentication
provider/quota fail-closed behavior
Core KRC isolation
no paid fallback
no secret/transcript leakage
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

## Administrative state

The accidental temporary Render service `noop` was manually deleted by the owner and deletion was confirmed through the Render connector.

## Public KRC boundary

The existing published `K-Research & Critic` GPT remains unchanged. No public MEDIA Action has been attached in Builder. R3 remains a separate explicit owner gate.

## Retained invariant

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains user-accessible and functional
```

Recovery must start from checkpoint 82.

Before any state-changing action, re-read exact GitHub heads/CI, current Render live deploy, PR #45 state, and the current KRC public Builder state. Do not deploy, mutate Render/Neon, merge PR #45, activate Gemini, or update the public GPT without fresh explicit owner authorization.
