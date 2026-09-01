# K-Research & Critic MEDIA BETA - M3 Reference Review Checkpoint
Канонічний recovery-checkpoint після прийняття byte-capture evidence та підготовки reference transcript candidates.

Version: 1.0
Status: CANONICAL_RECOVERY_CHECKPOINT / RELEASE_HOLD_OWNER_TESTING / M3_ACTIVE
Snapshot date: 2026-09-01

## 1. Inherited full project baseline

This checkpoint advances and supersedes the M3 continuation point recorded in:

`62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md`

All product hierarchy, Core invariants, accepted MEDIA BETA runtime behavior, Neon/durable-state baseline, route policies, privacy/safety boundaries, provider separation, and release gates from checkpoint 62 remain in force unless explicitly changed below.

Product hierarchy remains:

```text
K-Research & Critic
|
+-- public Core
|   repo: kolemasakar/K_Research_Critic
|   branch: main
|   state: PUBLISHED / MAINTENANCE
|
+-- K-Research & Critic - MEDIA BETA
    role: CLOSED BETA MODULE
    product/roadmap authority: K_Research_Critic
    branch: agent/video-url-research
    release state: RELEASE_HOLD_OWNER_TESTING
    |
    +-- VoiceBridge
        role: technology/backend implementation and validation source
        KRC migration branch: agent/krc-media-gemini-migration
```

VoiceBridge does not independently authorize KRC product release gates.

## 2. Exact KRC MEDIA BETA state before checkpoint write

```text
repo: kolemasakar/K_Research_Critic
branch: agent/video-url-research
pre-checkpoint head: fe6c56aae6208527bba0cddfdeac5a55ff3ef357
roadmap: subprojects/media_beta/02_ROADMAP.md version 3.9
CI workflow: Tests
CI run: 33521649491
CI result: SUCCESS
Python 3.13 tests: PASS
Python 3.14 tests: PASS
quality gates: PASS
```

No product runtime, Builder, Action schema, provider setting, Render environment, Neon data, or release gate was changed by the roadmap/checkpoint work.

## 3. Exact VoiceBridge M3 state

```text
repo: kolemasakar/VoiceBridge
branch: agent/krc-media-gemini-migration
head: c98c77521c919611b735971451e72366dedd2750
head message: M3: Hash reference transcript candidates pending listening review
PR: #45
PR state: OPEN / DRAFT / UNMERGED
Validate run: 33521717978
Validate result: SUCCESS
cloud: PASS
browser-extension: PASS
repository-docs: PASS
cloud regression: 224/224 PASS
```

The normal KRC prerecorded provider remains:

```text
provider: AssemblyAI
model: universal-2
```

The candidate remains:

```text
provider: Gemini
model: gemini-3.5-transcribe
normal activation: FALSE
```

VoiceBridge live Gemini acceptance remains separate from KRC prerecorded M3 evidence.

## 4. M3 byte capture - accepted

Workflow run `33490716248` successfully captured exact version-pinned public speech fixture bytes, verified expected byte sizes, computed SHA-256, deleted temporary media, and uploaded no raw-media artifact.

Accepted clean-public assets:

```text
ua-clean-public-001
asset SHA-256: 98e29c2276533699c67454de16b713d9846f668b6cc32b7591a0b2eb8a275a8c

ru-clean-public-001
asset SHA-256: d066239503c4e7406ebeb47423334b5109aa6b30d62046d0338a04e41b4c52f5

en-clean-public-001
asset SHA-256: 63a4b1e4c1dc655ac70961ffbf518acd249df237e5a0152faae9a4a836949715
```

Canonical VoiceBridge record:

`docs/history/2026-09-01_KRC_MEDIA_M3_BYTE_CAPTURE_ACCEPTANCE.md`

The byte-capture workflow is now manual-only via `workflow_dispatch`.

## 5. Reference transcript candidate artifacts - prepared, not accepted

Independent reference-source candidates are locked for all three accepted assets.

Candidate transcript bytes were prepared outside GitHub using this exact byte convention:

```text
encoding: UTF-8
line_endings: LF
terminal_newline: exactly one
normalization_before_hash: NONE
```

Candidate reference SHA-256 values:

```text
ua-clean-public-001
d9a6dbf5f2d0d1f8c200b11736982f3c9b2c02741d2303c96a359fe30015e461

ru-clean-public-001
1c7ac3953951270a56bf5927c86a26d28281ca9b958981c9ab56776837faaadf

en-clean-public-001
044267656cd78db47edd50fead3ae70f8f7240f3c1f3523cc53b94594de5ecfa
```

These are `CANDIDATE` hashes only. They are not final accepted reference digests and do not prove audio/text identity.

Canonical VoiceBridge record:

`docs/history/2026-09-01_KRC_MEDIA_M3_REFERENCE_TRANSCRIPT_PREPARATION.md`

## 6. Evidence state

```text
M3_BYTE_CAPTURE: ACCEPTED
REAL_ASSET_BYTES_CAPTURED: TRUE
REAL_ASSETS_SELECTED: TRUE
ASSET_SHA256_ACCEPTED: TRUE / 3 OF 3

REFERENCE_SOURCE_CANDIDATES_LOCKED: TRUE / 3 OF 3
REFERENCE_ARTIFACT_CANDIDATE_BYTES_CREATED: TRUE
REFERENCE_ARTIFACT_CANDIDATE_SHA256_CREATED: TRUE / 3 OF 3
REFERENCE_AUDIO_RECONCILIATION_COMPLETE: FALSE
REFERENCE_SHA256_ACCEPTED: FALSE
REFERENCE_REVIEW_STATE: LISTENING_REVIEW_PENDING

READY_FOR_AB: FALSE
M3_LIVE_PRERECORDED_AB: NOT_RUN
ASSEMBLYAI_M3_CORPUS_CALLS: NONE
GEMINI_M3_CORPUS_CALLS: NONE
PAID_RETRIEVAL_FOR_M3: NONE
```

## 7. Exact current roadmap position

```text
CURRENT_MILESTONE = M3 INDEPENDENT LISTENING REVIEW + FINAL REFERENCE SHA-256
```

Required transition:

```text
CANDIDATE_BYTES_HASHED
 -> independently listen to each exact accepted audio asset end-to-end
 -> reconcile every spoken token and clipping boundary
 -> correct candidate transcript bytes if required
 -> recompute final reference transcript SHA-256 after any edit
 -> set reference_review_state=independent_reviewed
 -> READY_FOR_AB
 -> controlled same-asset AssemblyAI universal-2 vs Gemini gemini-3.5-transcribe A/B
 -> deterministic metrics plus manual factual/hallucination review
 -> M3 closure decision
```

Do not mark `independent_reviewed` based only on upstream transcript metadata, another STT model, or candidate-provider output.

## 8. Local review package

A temporary review package was prepared outside the repositories for the listening gate. It contains candidate transcript artifacts, their hashes, and a checklist. It does not change canonical repository state.

Package name:

`KRC_MEDIA_BETA_M3_REFERENCE_REVIEW_2026_09_01.zip`

The exact public audio assets remain version-pinned at their source repositories; raw media was not committed to KRC or VoiceBridge and was not uploaded as an Actions artifact.

## 9. Release and safety gates

Unchanged:

```text
RELEASE_HOLD_OWNER_TESTING: ACTIVE
R1 merge MEDIA BETA toward KRC main: HOLD
R2 backend/production promotion: HOLD
R3 external testers: HOLD
R4 public/Store rollout: HOLD
M4 canary: NOT_STARTED
M5 cutover: NOT_AUTHORIZED
```

Also unchanged:

```text
Facebook Cobalt failure -> unavailable
NO automatic paid Facebook fallback
Telegram public-only / zero-credit retrieval
Gemini prerecorded normal activation = FALSE
AssemblyAI prerecorded active provider = TRUE
```

## 10. Recovery order

For a fresh chat, use:

```text
recover KRC MEDIA BETA M3 reference review checkpoint 2026-09-01
```

Read in this order:

```text
1. 63_M3_REFERENCE_REVIEW_CHECKPOINT_2026_09_01.md
2. 62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md
3. 00_INDEX.md
4. 02_ROADMAP.md
5. 61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md
6. 60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md
7. 03_CURRENT_STATE.md
8. 53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
```

Then re-check exact GitHub heads/CI before any write or provider-consuming action.

## 11. Marker

```text
KRC_MEDIA_BETA_M3_REFERENCE_REVIEW_CHECKPOINT_2026_09_01
BYTE_CAPTURE_ACCEPTED
ASSET_SHA256_ACCEPTED_3_OF_3
REFERENCE_CANDIDATES_HASHED_3_OF_3
INDEPENDENT_LISTENING_REVIEW_PENDING
READY_FOR_AB_FALSE
M3_PROVIDER_CALLS_NONE
RELEASE_HOLD_OWNER_TESTING
```
