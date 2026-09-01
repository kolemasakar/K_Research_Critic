# MEDIA BETA Roadmap
Поточний roadmap приватного MEDIA BETA після завершення A9-A10 та під час M3 prerecorded provider-evidence migration track.

Version: 3.8
Status: RELEASE_HOLD_OWNER_TESTING / M3_ACTIVE
Updated: 2026-09-01

## Product Position

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product.

```text
product/roadmap authority: kolemasakar/K_Research_Critic
public Core: main
closed-beta product branch: agent/video-url-research
technology/backend implementation source: kolemasakar/VoiceBridge
active KRC provider-migration branch: agent/krc-media-gemini-migration
```

VoiceBridge supplies reusable technology, backend implementation, and validation evidence. It is not the parent product and does not independently authorize KRC MEDIA BETA release decisions.

## Completed Historical Baseline

```text
A4-A7 closed-beta infrastructure and provider validation   COMPLETE/HISTORICAL
A8 browser-assisted owner baseline                        COMPLETE/FALLBACK_ONLY
```

The A8 Helper remains evidence/fallback only and is not normal owner UX.

## A9 Owner Zero-Client Media Input

Status: COMPLETE / ACCEPTED.

```text
YouTube managed route                       ACCEPTED
Instagram managed route                     ACCEPTED
Facebook free Cobalt route                  ACCEPTED
Facebook Cobalt failure -> unavailable      ACCEPTED
Telegram public route                       ACCEPTED
local attachment transport + ingestion      ACCEPTED
CriticProfile integration                   ACCEPTED
claim-level cross-check enforcement         ACCEPTED
```

## A9.10 Local Attachment

Status: COMPLETE / ACCEPTED.

Accepted flow:

```text
current-conversation audio/video attachment
 -> openaiFileIdRefs
 -> trusted OpenAI temporary delivery
 -> bounded ingestion
 -> AssemblyAI
 -> durable KRCM
 -> CriticProfile
 -> Research/Critic
```

Retrieval credits are zero. Accepted max attachment size is 32 MiB.

## A10 Stabilization

Status: COMPLETE / ACCEPTED.

Delivered:
- strict visible four-column claim-summary table;
- mandatory fenced copy-safe duplicate;
- runtime preservation of real SHORTFALL;
- external ChatGPT Copy defect documented rather than hidden.

Builder package: `0.9.1-beta-a10`.
Action schema: `0.6.0-a9.10`.

## VoiceBridge Gemini Migration - Accepted Shared Baseline

VoiceBridge has already completed its own real-time STT migration to Gemini and subsequently closed Phase 2 Universal Cloud Audio.

```text
VoiceBridge main                               a426ae331721dd36291874e45380faf603d854cf
VoiceBridge streaming STT default              Gemini gemini-3.5-transcribe-live
VoiceBridge streaming rollback                 AssemblyAI universal-streaming-english
VoiceBridge Phase 2                            COMPLETE / CONTROLLED E2E VALIDATED
VoiceBridge main Validate                      SUCCESS
```

This completed migration changes the shared VoiceBridge technology baseline used by future KRC forward-port work, but it does not change the accepted KRC prerecorded provider in the current private runtime.

Provider separation is explicit:

```text
VoiceBridge live streaming STT
  selector: STT_PROVIDER
  default: gemini
  model: gemini-3.5-transcribe-live
  state: ACCEPTED DEFAULT

KRC MEDIA BETA prerecorded STT
  selector: KRC_MEDIA_STT_PROVIDER
  active provider: assemblyai
  active model: universal-2
  Gemini candidate model: gemini-3.5-transcribe
  state: ASSEMBLYAI ACTIVE / GEMINI INACTIVE
```

The current KRC migration implementation enforces `KRC_MEDIA_STT_PROVIDER=assemblyai` as the only normal provider value until the explicit Gemini activation gate. The Gemini prerecorded adapter is available only through the controlled candidate path.

The KRC migration branch is based on VoiceBridge main commit `eba77183bee29621aa6c7cb859737a10edb6e4d4`. Current VoiceBridge main is 13 commits ahead of that base. The compared delta contains Phase 2 documentation and closure synchronization only; no additional runtime-code re-port is required solely because of those 13 commits.

Impact classification:

```text
current owner MEDIA BETA behavior             UNCHANGED
current prerecorded STT provider              UNCHANGED / ASSEMBLYAI
provider-neutral architecture                 IMPROVED
Gemini candidate implementation               AVAILABLE / INACTIVE
VoiceBridge project baseline                  ADVANCED / PHASE 2 COMPLETE
KRC M3 evidence requirement                   STILL REQUIRED
release state                                 UNCHANGED / HOLD
```

The accepted VoiceBridge Live A/B result is useful technology evidence but is not equivalent to KRC prerecorded evidence and cannot close M3.

## Active Track: KRC Gemini Prerecorded Forward Migration

This KRC-specific engineering track is additive to the accepted private runtime. It does not activate Gemini for normal KRC MEDIA BETA jobs and does not authorize a release gate.

Technical authority for the current forward-port implementation/evidence:

```text
VoiceBridge branch: agent/krc-media-gemini-migration
current verified head: 7c2cac849d9322a8b532815ac3be44e87bd52e27
VoiceBridge draft PR: #45
exact-head Validate run: 33480804395 SUCCESS
cloud tests: 224/224 PASS
```

### M0 - Recovery / Migration Preflight

Status: COMPLETE.

### M1 - Provider Abstraction

Status: PASS.

AssemblyAI remains the active KRC prerecorded provider behind the provider-neutral boundary.

### M2 - Gemini Prerecorded Adapter

Status: PASS / INACTIVE.

```text
candidate: gemini-3.5-transcribe
normal KRC activation: FALSE
active KRC prerecorded provider: AssemblyAI universal-2
```

### M3 - Evidence and Same-Asset A/B Gate

Status: ACTIVE.

Completed:

```text
offline A/B evaluator                        PASS
same-asset execution contract                PASS
corpus manifest/readiness contract            PASS
byte-exact evidence preparation helper        PASS
first public source tranche                   LOCKED
```

First locked cases:

```text
ua-clean-public-001
ru-clean-public-001
en-clean-public-001
```

Current evidence state:

```text
FIRST_PUBLIC_SOURCE_TRANCHE_LOCKED            TRUE
REAL_ASSET_BYTES_CAPTURED                     FALSE
ASSET_SHA256                                  NOT_CREATED
REFERENCE_TRANSCRIPT_SHA256                   NOT_CREATED
READY_FOR_AB                                  FALSE
M3_LIVE_AB                                    NOT_RUN
```

### CURRENT ROADMAP POSITION

```text
M3 BYTE CAPTURE + SHA-256
```

Required transition:

```text
SOURCE_LOCKED_PENDING_BYTE_CAPTURE
 -> capture exact media bytes
 -> compute byte-exact asset SHA-256
 -> do not retain raw media as GitHub artifact
 -> delete temporary media after hashing
 -> prepare/reconcile independent reference transcript
 -> compute reference transcript SHA-256
 -> independent review
 -> READY_FOR_AB
 -> same-asset AssemblyAI vs Gemini prerecorded A/B
 -> manual factual/hallucination review
 -> M3 closure decision
```

The byte-capture step must not itself call AssemblyAI or Gemini.

The VoiceBridge live provider acceptance must not be substituted for this gate. KRC uses a different model (`gemini-3.5-transcribe`), prerecorded/file semantics, different duration/timestamp constraints, and an evidence-oriented fidelity standard.

### M4 - New-Infrastructure Canary

Status: NOT STARTED.

Prerequisite: deployment-image parity audit for the target VoiceBridge runtime, including KRC media/runtime dependencies.

Current VoiceBridge main Phase 2 completion is positive evidence for the target cloud baseline, but it does not prove KRC-specific deployment-image parity for media retrieval, probing/transcoding, PostgreSQL tooling, durable state, or KRC Action routes.

### M5 - Cutover Decision

Status: NOT AUTHORIZED.

Any KRC prerecorded provider or infrastructure cutover requires separate explicit owner approval and verified rollback to the accepted AssemblyAI path.

## Current Phase: Release Hold Owner Testing

Status: ACTIVE.

Canonical release checkpoint:

```text
53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
```

Current decisions:

```text
merge to KRC main = HOLD
production/backend promotion = HOLD
external tester onboarding = HOLD
public sharing/Store rollout = HOLD
```

During this phase, owner testing, defect correction, regression hardening, documentation maintenance, and the explicitly activated M3 evidence track are in scope. None of these activities automatically advances a release gate.

## Future Release Gates

R1 Merge: accept selected MEDIA BETA product changes toward `main`.
R2 Production promotion: deploy/promote the media backend to approved production infrastructure.
R3 External testers: enable a controlled non-owner group.
R4 Public rollout: public sharing/Store availability.

Each requires a separate explicit decision. No gate inherits approval from another.

## Optional Future Sustainability Work

Cloudflare/local Whisper or other provider-neutral cost reductions remain a future optional architecture track. They are not a prerequisite for continued private owner testing and must not silently replace the accepted beta route.
