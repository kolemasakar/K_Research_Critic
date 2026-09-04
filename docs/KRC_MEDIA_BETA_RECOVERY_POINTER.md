# K-Research & Critic - MEDIA BETA Recovery Pointer
Канонічний покажчик на поточний стан MEDIA BETA після завершення R2-C public privacy, AssemblyAI Free evidence та exact Render promotion planning без deployment.

Status: ACTIVE POINTER / R2-C COMPLETE / R2 PROMOTION READY FOR EXPLICIT OWNER AUTHORIZATION / NO DEPLOYMENT
Updated: 2026-09-04

`K-Research & Critic - MEDIA BETA` remains an additive MEDIA capability planned for the existing published `K-Research & Critic` identity.

## Current canonical checkpoint

Repository:

`kolemasakar/K_Research_Critic`

Branch:

`main`

Path:

`subprojects/media_beta/80_R2C_PUBLIC_PRIVACY_RENDER_PROMOTION_READY_2026_09_04.md`

## Current gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B PASS
R2-C COMPLETE
R2   PROMOTION READY FOR EXPLICIT OWNER AUTHORIZATION / NOT PROMOTED
R3   HOLD
R4   HOLD
```

## Current verified candidate state

```text
VoiceBridge migration branch: agent/krc-media-gemini-migration
VoiceBridge R2-C head: 3a00d67bac0883a55f0f9c5eacf16e11acae85fe
VoiceBridge Validate: 33894722818 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true

MEDIA public platforms: youtube, telegram, instagram, facebook
Action auth boundary: server-to-server Bearer token
Public beta codes: not exposed / not required
Internal admission principal: derived server-side from Action token
Supadata: Free only / <=100 credits per month / 1 request per second
Public MEDIA request cap: <=60 per minute with 1-second minimum interval
Public MEDIA concurrency: 1
KRC AssemblyAI project safety cap: <=7200 STT seconds/day
Facebook retrieval: Cobalt free path
ScrapeCreators in public free-only mode: forbidden
Automatic paid fallback: none
Core/legacy route boundary: bypasses public MEDIA admission guard
```

## AssemblyAI account evidence

Owner-supplied Billing evidence dated 2026-09-04 confirms:

```text
Plan Details: Free
free credits spent: $1.68
free credits remaining: $48.32
Pay-as-you-go: not active in the shown Billing view
Upgrade Plan: separate explicit action
```

Paid AssemblyAI continuation remains forbidden.

Owner product decision:

```text
while AssemblyAI Free remains available -> keep AssemblyAI universal-2 for KRC prerecorded STT
after AssemblyAI Free exhaustion -> target Gemini prerecorded STT
paid AssemblyAI fallback -> forbidden
```

The Gemini automatic cutover is not currently implemented. `gemini-3.5-transcribe` remains the existing prerecorded candidate and requires a separately validated post-exhaustion activation path.

## Public privacy state

`docs/PRIVACY_POLICY.md` is now prepared as:

```text
Version: 2.0-candidate
Status: PUBLIC_MEDIA_CANDIDATE / NOT_YET_ACTIVATED / FREE_TIER_ONLY
```

It covers the initial four-platform public MEDIA scope, free-only provider policy, retention/cleanup, failure isolation and future Gemini Free disclosure/consent requirement.

Public Gemini Free processing must not be silent: before sending public-user media to Gemini Free, the user must receive the provider/data-use disclosure and explicitly consent. No consent -> fail closed.

## Authenticated Render baseline

```text
MEDIA service: voicebridge-krc-media-beta-kolemasakar
service id: srv-da1kic5bedkc73d6fk60
Render service branch: agent/krc-media-transcript
autoDeploy: no
current live deploy id: dep-dabnvs3tqb8s73d1c68g
current live deploy commit: 2f0f02769dbdf2e8240e6b08867ecef2faaede16
M4 canary commit 6a9491359795840ec9e79c9edc0ea82f595e9784: deactivated
exact rollback target: 2f0f02769dbdf2e8240e6b08867ecef2faaede16
```

The configured branch head is not the exact known-good live commit. Promotion and rollback therefore require exact-commit identity; generic branch-head deployment is not sufficient evidence.

Exact R2-C promotion plan is recorded in VoiceBridge:

`docs/planning/2026-09-04_KRC_MEDIA_R2C_PUBLIC_PRIVACY_RENDER_PROMOTION_PLAN.md`

## Retained invariant

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC               -> remains usable
```

## Safe continuation

The next state-changing gate is the bounded R2 permanent backend promotion/canary using the exact candidate and rollback plan.

That operation requires fresh explicit owner authorization.

R3 must not be inferred from R2 authorization. Even after an R2 promotion/canary PASS, updating the existing published K-Research & Critic GPT through Builder remains a separate owner gate.

No Render deployment, Render environment mutation, Neon mutation, VoiceBridge main merge, provider cutover, ChatGPT Builder Update, or public rollout was performed by R2-C.

Recovery must start from checkpoint 80.
