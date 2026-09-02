# K-Research & Critic - MEDIA BETA
## Post-AssemblyAI Free-Credit Hybrid STT Plan

Date: 2026-09-02
Status: PLANNED / NOT_IMPLEMENTED / DEFERRED_UNTIL_ASSEMBLYAI_FREE_CREDITS_EXHAUSTED
Authority: product/roadmap plan only; no runtime authorization

## Owner decision

The owner approved recording a future free-first STT architecture for `K-Research & Critic - MEDIA BETA` after the remaining AssemblyAI free credits are exhausted.

This document records a planned implementation only.

```text
CURRENT ACTIVE PROVIDER: AssemblyAI universal-2
CURRENT BEHAVIOR CHANGE: NONE
GEMINI PRERECORDED NORMAL ACTIVATION: FALSE
POST-CREDIT HYBRID IMPLEMENTATION: PLANNED
IMPLEMENT NOW: FALSE
TRIGGER: AssemblyAI free credits exhausted / effectively unavailable as a free path
```

The preferred future direction is the combined **Hybrid C/D** option discussed after M3/M3B evidence and free-tier analysis.

## Planned target architecture - Hybrid C/D

### C - Gemini free-first functional split

After the trigger, the intended free-first KRC prerecorded routing is:

```text
media job
  -> capability / quota router
      -> Gemini 3.5 Transcribe Live
         primary free path for eligible jobs that do not require
         word-level timestamps or speaker diarization

      -> Gemini 3.5 Transcribe unary
         feature path when word-level timestamps and/or speaker diarization
         are required and current free-tier quota permits the request
```

The Live path is not assumed to be a drop-in prerecorded API replacement. Implementation will require a dedicated prerecorded-to-live streaming adapter, chunk/session handling, transcript assembly, ordering guarantees, timeout handling, and equivalence testing.

### D - AssemblyAI retained as controlled fallback

AssemblyAI `universal-2` remains the accepted rollback/fallback technology, but after free credits are exhausted it becomes potentially billable.

Therefore the planned rule is:

```text
Gemini free path unavailable / unsuitable
  -> DO NOT silently spend AssemblyAI credits or paid balance
  -> fail closed or hold the job
  -> AssemblyAI paid fallback only after separate explicit owner authorization
```

No automatic paid provider fallback is authorized by this plan.

## Why this plan is preferred

The current evidence does not establish a decisive quality winner between AssemblyAI and Gemini across the seven-case M3/M3B corpus.

The free-tier economics create a separate architectural reason to preserve Gemini as the future first-line candidate:

- AssemblyAI free use is credit-balance based and therefore finite;
- Gemini 3.5 Transcribe currently exposes a continuing free tier subject to project rate limits;
- Gemini 3.5 Transcribe Live currently exposes a materially more permissive free quota profile than unary Transcribe in the owner `VoiceBridge` project;
- the owner explicitly accepts the Free Tier data-use condition for model/product improvement;
- Gemini's advertised language coverage is lower numerically than AssemblyAI Universal-2, but it includes the core KRC geopolitical language set reviewed so far;
- language quantity alone is not accepted as a quality proxy.

## Current observed Gemini quota snapshot

Owner-observed Google AI Studio project: `VoiceBridge`.

Observed on 2026-09-01/02:

```text
Gemini 3.5 Transcribe
RPM: 3
TPM: 10,000
RPD: 25

Gemini 3.5 Transcribe Live
RPM: Unlimited
TPM: 20,000
RPD: Unlimited
```

These values are a planning snapshot, not a permanent contract. They MUST be re-read from the active Google project immediately before implementation or cutover.

## Language planning boundary

Current planning assumptions:

```text
AssemblyAI Universal-2: broader advertised language count (99)
Gemini 3.5 Transcribe: 85+ advertised locales/languages
```

For KRC, the decision criterion is not the headline count but tested support for the actual geopolitical source set.

At implementation time, the minimum language verification matrix must include:

- Ukrainian;
- Russian;
- English;
- Polish;
- Belarusian;
- Turkish;
- Arabic;
- Persian/Farsi;
- Hebrew;
- Mandarin Chinese;
- key South Caucasus and Central Asian languages used by KRC sources.

Targeted code-switching verification must include at least:

```text
UA <-> RU
UA <-> EN
RU <-> EN
PL <-> UA
```

## Deferred implementation path

No stage below is authorized for implementation now.

### H0 - Trigger confirmation

- verify that usable AssemblyAI free credits are exhausted or no longer economically relevant;
- record the exact remaining balance/state;
- do not enable paid AssemblyAI fallback implicitly.

### H1 - Fresh provider/quota/privacy preflight

- re-check current Gemini Free Tier pricing and rate limits;
- re-check model names and lifecycle status;
- re-check language coverage;
- re-check Live session limits and feature restrictions;
- re-confirm owner data-use policy;
- if the product audience has expanded beyond private owner testing, perform a fresh privacy/consent review before using a provider tier that may use data for model improvement.

### H2 - Capability-aware provider router

Introduce an explicit routing contract based on:

- required language;
- audio duration;
- timestamps required/not required;
- diarization required/not required;
- free quota availability;
- provider health;
- explicit paid-fallback authorization state.

The router must be deterministic, observable, and fail closed.

### H3 - Prerecorded-to-Gemini-Live adapter

Implement a separate adapter that can feed prerecorded media through the Live transcription interface without changing the existing accepted KRC job contract.

Requirements:

- bounded chunk/session strategy;
- deterministic segment ordering;
- no duplicate transcript segments on reconnect;
- explicit partial-session failure state;
- cancellation and timeout cleanup;
- quota accounting;
- no silent switch to a paid provider.

### H4 - Gemini unary feature route

Use unary `gemini-3.5-transcribe` for jobs whose accepted KRC output requires capabilities not supplied by the Live path, especially word-level timestamps and/or speaker diarization, subject to current free quota.

Long media must be chunked only under a tested deterministic strategy that preserves segment order and provenance.

### H5 - Free-quota ledger and admission control

Before each Gemini job:

- evaluate current local quota budget;
- reserve capacity atomically where practical;
- avoid burst patterns that exceed RPM/TPM;
- queue or reject cleanly when free quota is unavailable;
- never convert free-tier exhaustion into an automatic paid-provider call.

### H6 - Controlled AssemblyAI fallback gate

Retain AssemblyAI `universal-2` adapter and rollback tests.

After its free credits are exhausted:

```text
fallback default: DISABLED_FOR_BILLABLE_USE
```

Billable AssemblyAI use requires a separately recorded owner approval/budget policy before activation.

### H7 - Targeted acceptance corpus before cutover

Before making the hybrid route normal, execute a targeted acceptance tranche covering the remaining M3 evidence gaps:

- real multi-speaker conversation;
- UA/RU and UA/EN code-switching;
- noisy Ukrainian;
- noisy Russian;
- telephone-bandwidth speech;
- 10-30 minute real-world media;
- numeric/date/name fidelity;
- one exact-asset comparison of Gemini unary versus Gemini Live where both are technically applicable.

Provider output must not become ground truth. References require independent review.

### H8 - Owner-only canary

Only after H0-H7 acceptance:

- enable the hybrid route for private owner canary traffic;
- preserve immediate rollback to the accepted AssemblyAI implementation where explicitly authorized and economically available;
- verify quotas, latency, transcript ordering, error handling, retention cleanup, and KRC provenance behavior.

### H9 - Separate activation decision

A successful implementation/canary still does not authorize:

- provider cutover for all KRC jobs;
- merge to public Core;
- backend production promotion;
- external tester onboarding;
- public rollout.

Each remains a separate owner decision.

## Non-goals now

This plan does NOT authorize any current change to:

```text
KRC_MEDIA_STT_PROVIDER
AssemblyAI credentials
Gemini credentials
Render environment
Neon state
Builder package
Action schema / URL
normal KRC runtime routing
PR merge state
R1 / R2 / R3 / R4 release gates
```

No provider-consuming validation run is authorized by this planning document.

## Current operational rule

Until the trigger is reached:

```text
USE CURRENT ACCEPTED ASSEMBLYAI UNIVERSAL-2 PATH
DO NOT IMPLEMENT HYBRID C/D YET
DO NOT ACTIVATE GEMINI FOR NORMAL KRC PRERECORDED JOBS
```

## Future implementation authority

When AssemblyAI free credits are exhausted, recover this document and the then-current KRC/VoiceBridge state, revalidate all mutable external assumptions, and request a fresh explicit implementation authorization before making code/runtime changes.
