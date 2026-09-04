# K-Research & Critic - MEDIA BETA Recovery Pointer
Канонічний покажчик на поточний стан MEDIA BETA після завершення R2-A public free-tier admission/auth/quota code and CI validation.

Status: ACTIVE POINTER / R2-A CODE + TESTS PASS / R2 NOT READY / NO DEPLOYMENT
Updated: 2026-09-04

`K-Research & Critic - MEDIA BETA` remains an additive MEDIA capability planned for the existing published `K-Research & Critic` identity.

## Current canonical checkpoint

Repository:

`kolemasakar/K_Research_Critic`

Branch:

`main`

Path:

`subprojects/media_beta/78_R2A_PUBLIC_FREE_TIER_ADMISSION_PASS_2026_09_04.md`

## Current gate state

```text
R0  PASS
R1  COMPLETE
R2-A CODE + TESTS PASS
R2  NOT READY / NO DEPLOYMENT
R3  HOLD
R4  HOLD
```

## Current verified candidate state

```text
KRC main before checkpoint 78: 3b482cafae8da728fbe1fe8f0c587d6161bd9c9e
VoiceBridge migration branch: agent/krc-media-gemini-migration
VoiceBridge migration head: c85d0dc8777629993d4556cd00ed470159ae1700
VoiceBridge Validate: 33881935054 / SUCCESS
PR #45: OPEN / DRAFT / UNMERGED / mergeable=true

MEDIA public platforms: youtube, telegram, instagram, facebook
Action auth boundary: server-to-server Bearer token
Public beta codes: not exposed / not required
Internal admission principal: derived server-side from Action token
Supadata: Free plan only / <=100 credits per month / 1 request per second
Public MEDIA request cap: <=60 per minute with 1-second minimum interval
Public MEDIA concurrency: 1
Project AssemblyAI STT daily cap: <=7200 seconds
AssemblyAI public deployment attestation: free-trial-only required
Facebook retrieval: Cobalt free path
ScrapeCreators in public free-only mode: forbidden
Automatic paid fallback: none
Core/legacy route boundary: bypasses public MEDIA admission guard
```

Authenticated Render baseline remains:

```text
MEDIA service: voicebridge-krc-media-beta-kolemasakar
Render service branch: agent/krc-media-transcript
autoDeploy: no
current live deploy commit: 2f0f02769dbdf2e8240e6b08867ecef2faaede16
M4 canary commit 6a9491359795840ec9e79c9edc0ea82f595e9784: deactivated
rollback to 2f0f027...: confirmed
startup runtime selector: assemblyai / universal-streaming-english
```

No Render deployment, service-branch change, environment mutation, Neon mutation, provider-consuming call, VoiceBridge main merge, or ChatGPT Builder Update was performed.

## Remaining blockers before permanent backend promotion

- current AssemblyAI account free/trial balance and no-paid/autopay state are not directly verified;
- public MEDIA privacy/release policy is not ready;
- current Render live service is not the R2 candidate and requires an explicit promotion plan;
- required Render public-mode environment flags/keys must be prepared and reviewed without enabling paid fallback;
- full bounded live public MEDIA failure -> Core unaffected matrix is not yet executed;
- final provider free-tier assumptions must be rechecked immediately before promotion.

Therefore permanent R2 promotion is not authorized and must not run.

## Retained invariant

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC              -> remains usable
```

## Safe continuation

Next safe work item:

`R2-B Free-tier deployment-readiness closure: provider account verification, public privacy policy, explicit Render promotion plan, and bounded live failure-isolation preflight.`

Any Render deployment, environment mutation, provider-consuming validation, VoiceBridge main merge, permanent backend promotion, or ChatGPT Builder Update requires a separate explicit owner decision.

Recovery must start from checkpoint 78.
