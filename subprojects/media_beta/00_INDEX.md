# MEDIA BETA Documentation Index
Канонічний індекс документації приватного K-Research & Critic MEDIA BETA.

Version: 4.7
Status: ACTIVE / RELEASE_HOLD_OWNER_TESTING / M3_READY_FOR_AB
Updated: 2026-09-01

## Purpose

This directory is the self-contained documentation root for the isolated private MEDIA BETA work. Historical numbered records preserve phase evidence; the current documents below define the active accepted state.

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product. `K_Research_Critic` remains the product/roadmap authority. VoiceBridge provides media/backend technology, implementation, and validation evidence.

## Canonical Reading Order

1. `64_M3_READY_FOR_AB_CHECKPOINT_2026_09_01.md` - current recovery checkpoint after independent listening review and final reference hashing; the first three clean-public cases are READY_FOR_AB and provider-consuming A/B is not yet run.
2. `63_M3_REFERENCE_REVIEW_CHECKPOINT_2026_09_01.md` - historical checkpoint immediately before final listening-review closure.
3. `62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md` - complete cross-repository baseline across KRC Core, MEDIA BETA, VoiceBridge, runtime/provider boundaries, release gates, and pre-capture M3 state.
4. `README.md` - current scope and release hold.
5. `61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md` - interpretation of the completed VoiceBridge live Gemini migration and its bounded impact on KRC prerecorded MEDIA BETA.
6. `60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md` - product hierarchy, active VoiceBridge KRC migration branch, and M3 roadmap overlay.
7. `03_CURRENT_STATE.md` - accepted operational baseline through the 2026-08-29 hardening state.
8. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` - owner release decision and recovery boundary.
9. `01_ARCHITECTURE.md` - current architecture including separate VoiceBridge live and KRC prerecorded STT domains.
10. `02_ROADMAP.md` - current roadmap including M3 READY_FOR_AB state.
11. `04_OPERATIONS_RUNBOOK.md` - owner testing/defect operations.
12. `05_TEST_PLAN.md` - current regressions and hold testing.
13. `06_DECISION_LOG.md` - compact decision authority.
14. `08_CHAT_HANDOFF.md` - fresh-chat recovery.
15. `09_WORK_LOG.md` - material chronology.
16. `07_FREE_MODE_TARGET.md` - optional future sustainability direction only.

## Current Acceptance Records

```text
53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md
61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md
62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md
63_M3_REFERENCE_REVIEW_CHECKPOINT_2026_09_01.md
64_M3_READY_FOR_AB_CHECKPOINT_2026_09_01.md
```

VoiceBridge detailed M3 evidence authority includes:

```text
docs/history/2026-09-01_KRC_MEDIA_M3_BYTE_CAPTURE_ACCEPTANCE.md
docs/history/2026-09-01_KRC_MEDIA_M3_REFERENCE_TRANSCRIPT_PREPARATION.md
docs/history/2026-09-01_KRC_MEDIA_M3_REFERENCE_LISTENING_REVIEW_PARTIAL.md
docs/history/2026-09-01_KRC_MEDIA_M3_REFERENCE_REVIEW_ACCEPTANCE.md
```

## Source-of-Truth Precedence

When documents disagree:

1. current code, exact-head CI, and verified current runtime evidence;
2. `64_M3_READY_FOR_AB_CHECKPOINT_2026_09_01.md` for current M3 readiness and final reference evidence;
3. `62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md` for the complete 2026-09-01 cross-repository baseline;
4. `61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md` for VoiceBridge live versus KRC prerecorded interpretation;
5. `60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md` for the cross-repository migration overlay;
6. `03_CURRENT_STATE.md` for accepted operational runtime baseline;
7. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` for release authority;
8. latest accepted phase/capability record;
9. `06_DECISION_LOG.md` for policy decisions;
10. older phase/transition records.

VoiceBridge implementation evidence is authoritative for what it validates, but it cannot independently authorize KRC product release gates.

## Current Phase Marker

```text
A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED
A9_10_LOCAL_ATTACHMENT_ACCEPTED
A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED
VOICEBRIDGE_LIVE_GEMINI_DEFAULT_ACCEPTED
VOICEBRIDGE_PHASE_2_COMPLETE
KRC_PRERECORDED_ASSEMBLYAI_ACTIVE
KRC_GEMINI_PRERECORDED_IMPLEMENTED_INACTIVE
KRC_MEDIA_GEMINI_M0_COMPLETE
KRC_MEDIA_GEMINI_M1_PASS
KRC_MEDIA_GEMINI_M2_PASS_INACTIVE
KRC_MEDIA_GEMINI_M3_ACTIVE
M3_BYTE_CAPTURE_ACCEPTED
REAL_ASSET_BYTES_CAPTURED_TRUE
ASSET_SHA256_ACCEPTED_3_OF_3
REFERENCE_LISTENING_REVIEW_COMPLETED_3_OF_3
FINAL_REFERENCE_SHA256_ACCEPTED_3_OF_3
REFERENCE_REVIEW_STATE_INDEPENDENT_REVIEWED_3_OF_3
READY_FOR_AB_TRUE_3_OF_3
M3_PROVIDER_AB_NOT_RUN
KRC_GEMINI_PRERECORDED_INACTIVE
RELEASE_HOLD_OWNER_TESTING
```

## Current M3 Evidence

```text
ua-clean-public-001
asset: 98e29c2276533699c67454de16b713d9846f668b6cc32b7591a0b2eb8a275a8c
final reference: 2ec614c71321a8747b6bb50fb57a7c341bcad9150a09c5cb2a1825ebfc0f828e
state: READY_FOR_AB

ru-clean-public-001
asset: d066239503c4e7406ebeb47423334b5109aa6b30d62046d0338a04e41b4c52f5
final reference: 1c7ac3953951270a56bf5927c86a26d28281ca9b958981c9ab56776837faaadf
state: READY_FOR_AB

en-clean-public-001
asset: 63a4b1e4c1dc655ac70961ffbf518acd249df237e5a0152faae9a4a836949715
final reference: 044267656cd78db47edd50fead3ae70f8f7240f3c1f3523cc53b94594de5ecfa
state: READY_FOR_AB
```

The Ukrainian original candidate reference was rejected after independent listening and replaced by a corrected outside-GitHub artifact before the final digest was accepted.

## Active Engineering Branches

```text
KRC public Core: kolemasakar/K_Research_Critic / main
KRC MEDIA BETA: kolemasakar/K_Research_Critic / agent/video-url-research / draft PR #8
VoiceBridge current project baseline: kolemasakar/VoiceBridge / main
VoiceBridge active KRC prerecorded migration: agent/krc-media-gemini-migration
VoiceBridge migration head: 90ca4f354a466f7f5ffdba20de246eb033b369a8
VoiceBridge migration draft PR: #45
VoiceBridge exact-head Validate: 33527873644 SUCCESS
legacy VoiceBridge KRC Media branch: agent/krc-media-transcript
```

## Current Package

```text
Builder package: 0.9.1-beta-a10
Action schema: 0.6.0-a9.10
Builder runtime applied: true
active KRC prerecorded provider: AssemblyAI universal-2
Gemini prerecorded candidate active: false
```

## Current Roadmap Position

```text
M3 READY_FOR_AB / PROVIDER-CONSUMING A/B AUTHORIZATION GATE
```

The evidence-readiness gate is complete. The next operation is a controlled same-asset AssemblyAI `universal-2` versus Gemini `gemini-3.5-transcribe` A/B run, but this is provider-consuming work and requires separate authorization.

Reaching READY_FOR_AB does not activate Gemini for normal KRC jobs and does not authorize any release gate.

## Recovery Command

```text
recover KRC MEDIA BETA M3 READY_FOR_AB checkpoint 2026-09-01
```

Always read `64_M3_READY_FOR_AB_CHECKPOINT_2026_09_01.md` first and verify live GitHub heads/CI before provider-consuming work.

## Non-Negotiable Hold Boundary

Do not merge MEDIA BETA into public Core, change the public KRC Builder, promote/replace the beta backend, enable external testers, publish/share MEDIA publicly, activate Gemini prerecorded for normal KRC jobs, enable automatic paid fallback, or weaken credit/privacy/traceability gates without a separate explicit owner decision.

## Documentation Naming Exception

This subproject predates the repository-wide preference against numeric-prefix ordering. Existing numbered phase/acceptance files are retained as stable historical references. New numbered records are added only when they are distinct immutable phase/checkpoint/audit artifacts.
