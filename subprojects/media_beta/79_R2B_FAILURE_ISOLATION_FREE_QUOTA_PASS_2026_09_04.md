# K-Research & Critic / MEDIA BETA - R2-B Failure Isolation and Free-Quota Checkpoint 79

Date: 2026-09-04
Status: R2-B_CODE_AND_CI_PASS / ACCOUNT_EVIDENCE_REQUIRED / R2_NOT_READY / NO_DEPLOYMENT

## Purpose

Record completion of repository/CI R2-B work for the future public MEDIA capability while preserving the existing published Core KRC and the release hold.

No Render deployment, Render environment mutation, Neon mutation, provider-consuming validation, VoiceBridge main merge, ChatGPT Builder Update, or public rollout occurred in this step.

## VoiceBridge candidate

Repository:

`kolemasakar/VoiceBridge`

Release branch:

`agent/krc-media-gemini-migration`

R2-B head:

`0757a00dccaa1c938e2dd454c8369e8e067a3e7b`

PR:

`#45 / OPEN / DRAFT / UNMERGED / mergeable=true`

Canonical Validate:

`33885047366 / SUCCESS`

Validated jobs:

```text
cloud               SUCCESS
krc-image-parity     SUCCESS
browser-extension    SUCCESS
repository-docs      SUCCESS
```

## Supported public MEDIA boundary

```text
youtube
telegram
instagram
facebook
```

Free-only route policy remains:

```text
YouTube   -> Supadata Free native transcript
Instagram -> Supadata Free native transcript; optional generated transcript only inside remaining Free credits and explicit consent
Facebook  -> Cobalt self-hosted retrieval -> AssemblyAI Universal-2
Telegram  -> public Telegram web retrieval -> AssemblyAI Universal-2
```

Paid retrieval/STT continuation remains forbidden. Gemini prerecorded activation remains false.

## Runtime failure-isolation matrix

R2-B added:

`src/cloud/tests/r2b_failure_isolation_runtime_matrix.test.ts`

The matrix validates an actual HTTP handler/server boundary and verifies:

```text
invalid Action bearer
  -> MEDIA 401 / no provider work
  -> Core health remains available

Supadata Free credits exhausted on YouTube/Instagram
  -> MEDIA 429 / no paid continuation
  -> Core health remains available

Telegram public retrieval unavailable
  -> MEDIA unavailable
  -> Core health remains available

Facebook Cobalt unavailable
  -> MEDIA unavailable
  -> no paid fallback
  -> Core health remains available

durable MEDIA state unavailable
  -> MEDIA fails closed
  -> Core health remains available

unsupported external media URL
  -> rejected before provider work
  -> Core health remains available
```

Existing durable-store regression coverage continues to verify that deterministic persistence/quota failures stop before provider work when the charge boundary is knowable.

## Verified current provider free-tier terms

### Supadata

Official current pricing verified on 2026-09-04:

```text
Free plan: 100 credits/month
Free rate: 1 request/second
native transcript: 1 credit
generated transcript: 2 credits/minute
Free Auto Recharge: none
```

The R2-A wrapper already enforces `Free` account state and an accepted maximum plan ceiling of 100 credits before a credit-consuming Supadata request.

### AssemblyAI

Official current free-tier documentation verified on 2026-09-04:

```text
Free/trial allowance: finite $50 credit pool
Universal-2 current list price: $0.15/hour
billing granularity: per second
free allowance is NOT a daily seconds quota
```

Therefore the existing public KRC limit:

`MEDIA_DAILY_STT_SECONDS <= 7200`

is a project safety ceiling only. It must not be represented as the AssemblyAI provider free-tier quota.

## Remaining account-specific blocker

Repository code cannot prove the current KRC AssemblyAI account's live remaining balance, payment-method state, or autopay state from the documented public provider API surface.

`KRC_MEDIA_ASSEMBLYAI_FREE_TRIAL_ONLY=true` remains an operator/deployment attestation, not provider-side billing evidence.

Before any permanent R2 backend promotion, owner/operator evidence is required that:

- the KRC AssemblyAI account remains Free/trial-only;
- sufficient free balance remains for the intended bounded validation;
- no card-funded/autopay path can automatically turn public MEDIA usage into paid usage without fresh owner authorization.

Supadata live account state must also report Free and no more than the accepted 100-credit monthly ceiling; this is rechecked by the runtime wrapper before provider use.

## R2-B disposition

```text
R2-B repository implementation     PASS
R2-B canonical VoiceBridge CI       PASS
R2-B failure-isolation matrix       PASS
R2-B provider public terms          VERIFIED
R2-B AssemblyAI live account proof  REQUIRED
R2 permanent backend promotion      HOLD
```

## Gate state

```text
R0   PASS
R1   COMPLETE
R2-A PASS
R2-B CODE + CI PASS / ACCOUNT EVIDENCE REQUIRED
R2   NOT READY / NO DEPLOYMENT
R3   HOLD
R4   HOLD
```

Next safe work item:

`R2-C account/billing evidence + public privacy policy + explicit Render promotion plan, still without deployment unless separately authorized.`
