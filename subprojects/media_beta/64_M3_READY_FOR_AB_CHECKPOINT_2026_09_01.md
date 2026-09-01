# K-Research & Critic MEDIA BETA - M3 READY_FOR_AB Checkpoint
Канонічний checkpoint переходу першої M3 clean-public tranche до READY_FOR_AB після незалежної перевірки reference transcript.

Version: 1.0
Status: CANONICAL_RECOVERY_CHECKPOINT / M3_READY_FOR_AB / RELEASE_HOLD_OWNER_TESTING
Date: 2026-09-01

## Purpose

Preserve the exact M3 evidence state after byte capture, independent listening review, Ukrainian reference correction, final reference hashing, and readiness derivation for the first three clean-public cases.

This checkpoint does not authorize provider-consuming AssemblyAI/Gemini A/B execution and does not change normal KRC prerecorded provider activation.

## Cross-Repository State

```text
K_Research_Critic
  public Core: main / maintenance
  MEDIA BETA branch: agent/video-url-research
  roadmap authority: K_Research_Critic

VoiceBridge
  shared project baseline: main
  KRC prerecorded migration: agent/krc-media-gemini-migration
  draft PR: #45
```

VoiceBridge remains technology/backend implementation and validation evidence. It does not independently authorize KRC release gates.

## VoiceBridge Exact Evidence Head

```text
branch: agent/krc-media-gemini-migration
head: 90ca4f354a466f7f5ffdba20de246eb033b369a8
commit: M3: Accept final reference evidence and mark clean tranche READY_FOR_AB
Validate run: 33527873644
Validate result: SUCCESS
```

The acceptance record is:

```text
docs/history/2026-09-01_KRC_MEDIA_M3_REFERENCE_REVIEW_ACCEPTANCE.md
```

## Accepted Asset Evidence

### ua-clean-public-001

```text
asset SHA-256:
98e29c2276533699c67454de16b713d9846f668b6cc32b7591a0b2eb8a275a8c

original candidate reference: REJECTED AFTER LISTENING REVIEW
corrected final reference SHA-256:
2ec614c71321a8747b6bb50fb57a7c341bcad9150a09c5cb2a1825ebfc0f828e
reference_review_state: independent_reviewed
readiness: READY_FOR_AB
```

### ru-clean-public-001

```text
asset SHA-256:
d066239503c4e7406ebeb47423334b5109aa6b30d62046d0338a04e41b4c52f5

final reference SHA-256:
1c7ac3953951270a56bf5927c86a26d28281ca9b958981c9ab56776837faaadf
reference_review_state: independent_reviewed
readiness: READY_FOR_AB
```

### en-clean-public-001

```text
asset SHA-256:
63a4b1e4c1dc655ac70961ffbf518acd249df237e5a0152faae9a4a836949715

final reference SHA-256:
044267656cd78db47edd50fead3ae70f8f7240f3c1f3523cc53b94594de5ecfa
reference_review_state: independent_reviewed
readiness: READY_FOR_AB
```

Reference transcript bytes remain outside GitHub. GitHub stores only accepted digests, provenance metadata, review state, and readiness state.

## Ukrainian Reference Correction

The original upstream Ukrainian reference candidate was materially inconsistent with the exact accepted audio during full manual listening review.

The original candidate digest is therefore not accepted as final evidence.

A corrected local reference artifact was created outside GitHub with:

```text
encoding: UTF-8
line endings: LF
terminal newline: exactly one
normalization before hash: NONE
```

The corrected final SHA-256 is:

```text
2ec614c71321a8747b6bb50fb57a7c341bcad9150a09c5cb2a1825ebfc0f828e
```

## Derived M3 Readiness

```text
REAL_ASSET_BYTES_CAPTURED: TRUE
REAL_ASSETS_SELECTED: TRUE
ASSET_SHA256_ACCEPTED: TRUE 3/3
REFERENCE_LISTENING_REVIEW_COMPLETED: TRUE 3/3
FINAL_REFERENCE_SHA256_ACCEPTED: TRUE 3/3
REFERENCE_REVIEW_STATE: independent_reviewed 3/3
READY_FOR_AB: TRUE 3/3
M3_PROVIDER_AB: NOT_RUN
ASSEMBLYAI_M3_CALLS: NONE
GEMINI_M3_MEDIA_CALLS: NONE
GEMINI_PRERECORDED_ACTIVE: FALSE
```

The accepted manifest contract derives `READY_FOR_AB`; this is not a caller-supplied state.

## Current Roadmap Position

```text
M3 READY_FOR_AB / PROVIDER-CONSUMING A/B AUTHORIZATION GATE
```

Next valid transition:

```text
explicit provider-consuming test authorization
 -> exact same asset to AssemblyAI universal-2
 -> exact same asset to Gemini gemini-3.5-transcribe
 -> capture provider output and execution metadata
 -> deterministic comparison against final reference
 -> manual factual/hallucination review
 -> M3 closure decision
```

## Provider Boundary

Reaching READY_FOR_AB does not itself authorize provider spend.

Current normal KRC prerecorded state remains:

```text
active provider: AssemblyAI
active model: universal-2
Gemini prerecorded candidate: gemini-3.5-transcribe
Gemini normal activation: FALSE
```

No provider-consuming M3 A/B call has been made at this checkpoint.

## Release Boundary

```text
R1 merge toward KRC main: HOLD
R2 production/backend promotion: HOLD
R3 external testers: HOLD
R4 public/Store rollout: HOLD
```

M3 readiness or a later favorable A/B result does not automatically authorize any release gate.

## Recovery Command

```text
recover KRC MEDIA BETA M3 READY_FOR_AB checkpoint 2026-09-01
```

After recovery, verify current GitHub heads and CI before provider-consuming work.

## Marker

```text
KRC_MEDIA_M3_ASSET_SHA256_ACCEPTED_3_OF_3
KRC_MEDIA_M3_REFERENCE_REVIEW_ACCEPTED_3_OF_3
KRC_MEDIA_M3_FINAL_REFERENCE_SHA256_ACCEPTED_3_OF_3
KRC_MEDIA_M3_READY_FOR_AB_3_OF_3
KRC_MEDIA_M3_PROVIDER_AB_NOT_RUN
KRC_GEMINI_PRERECORDED_INACTIVE
RELEASE_HOLD_OWNER_TESTING
```
