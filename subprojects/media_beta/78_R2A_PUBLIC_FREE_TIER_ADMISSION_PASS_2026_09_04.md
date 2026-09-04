# K-Research & Critic / MEDIA BETA - R2-A Public Free-Tier Admission Checkpoint 78

Date: 2026-09-04
Status: R2-A_CODE_AND_TESTS_PASS / R2_NOT_READY / NO_DEPLOYMENT

## Purpose

Record completion of repository-only R2-A work for future public MEDIA access while preserving the existing published Core KRC and the release hold.

No Render deployment, Render environment mutation, Neon mutation, provider-consuming validation, VoiceBridge main merge, ChatGPT Builder Update, or public rollout occurred in this step.

## VoiceBridge candidate

Repository:

`kolemasakar/VoiceBridge`

Outer release branch:

`agent/krc-media-gemini-migration`

R2-A integrated head:

`c85d0dc8777629993d4556cd00ed470159ae1700`

Outer PR:

`#45 / OPEN / DRAFT / UNMERGED / mergeable=true`

Canonical Validate after R2-A integration:

`33881935054 / SUCCESS`

Validated jobs:

```text
cloud               SUCCESS
krc-image-parity     SUCCESS
browser-extension    SUCCESS
repository-docs      SUCCESS
```

## Public MEDIA support boundary

The repository candidate supports public HTTPS video/media URLs for:

```text
youtube
telegram
instagram
facebook
```

Platform-specific active policy remains:

```text
YouTube/Instagram -> Supadata managed transcript path
Facebook          -> Cobalt free retrieval -> AssemblyAI STT
Telegram          -> public web retrieval -> AssemblyAI STT
```

Unsupported/private/auth-required resources continue to fail closed.

## Authentication and admission

Future public MEDIA mode uses the GPT Action server-to-server Bearer token as the external authentication boundary.

Public users do not receive or submit the previous owner beta access codes. In public mode the backend derives an internal admission principal from the Action token and injects it server-side.

This is anonymous/shared public GPT admission, not per-user OAuth identity. Therefore quota enforcement is intentionally global/shared across public MEDIA traffic rather than account-specific.

## Free-tier-only guardrails

The user requirement for this phase is free-use-only operation.

Implemented repository guardrails:

```text
KRC_MEDIA_PUBLIC_MODE=true
  requires KRC_MEDIA_FREE_TIER_ONLY=true
  requires KRC_MEDIA_ASSEMBLYAI_FREE_TRIAL_ONLY=true
  requires SUPADATA_API_KEY
  requires ASSEMBLYAI_API_KEY
  requires KRC_MEDIA_COBALT_ENDPOINT
  forbids SCRAPECREATORS_API_KEY
```

Supadata public boundary:

```text
plan must be Free
max plan credits accepted: 100/month
request-rate boundary: 1 request/second
paid Supadata plan -> fail closed
credit exhaustion -> fail closed
```

Public MEDIA backend protection:

```text
request cap: <=60/minute
minimum request interval: 1 second
concurrency: 1
project AssemblyAI STT daily cap: <=7200 seconds
```

AssemblyAI remains the KRC prerecorded provider. R2-A does not enable Gemini prerecorded for normal KRC jobs and does not add any paid STT fallback.

The AssemblyAI `free-trial-only` flag is a deployment attestation/guard. The current AssemblyAI account balance, payment method/autopay state, and remaining free credit were not directly read in this phase and remain a deployment-readiness blocker.

## Facebook paid fallback policy

Public free-tier mode forbids ScrapeCreators credentials in configuration and the factory suppresses the paid Facebook retriever when free-tier-only mode is active.

Retained invariant:

```text
Cobalt success -> continue
Cobalt failure -> unavailable
NO automatic paid fallback
```

## Failure isolation

The new public MEDIA admission controller only handles the managed MEDIA route prefix.

Legacy/Core-adjacent VoiceBridge routes bypass the public MEDIA admission guard. Regression coverage verifies that a MEDIA rate/concurrency rejection does not intercept the health/Core route boundary.

This is repository/CI evidence. A full live public failure-injection matrix is still required before permanent backend promotion.

## Remaining R2 blockers

R2 is not ready for permanent backend promotion until the following are closed:

- current AssemblyAI account free/trial balance and no-paid/autopay state are verified;
- public MEDIA privacy/release policy replaces the current private-owner scope;
- Render promotion plan maps the current live rollback commit to the new VoiceBridge candidate explicitly;
- required Render public-mode environment keys/flags are prepared without enabling paid fallback;
- live failure-isolation matrix is executed on an isolated/bounded target;
- final provider/account free-tier assumptions are rechecked immediately before promotion.

## Gate state

```text
R0  PASS
R1  COMPLETE
R2-A CODE + TESTS PASS
R2  NOT READY / NO DEPLOYMENT
R3  HOLD
R4  HOLD
```

Next safe work item:

`R2-B Free-tier deployment-readiness closure: provider account verification, public privacy policy, explicit Render promotion plan, and bounded live failure-isolation preflight.`
