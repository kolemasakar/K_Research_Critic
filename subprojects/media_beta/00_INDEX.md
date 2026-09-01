# MEDIA BETA Documentation Index
Канонічний індекс документації приватного K-Research & Critic MEDIA BETA.

Version: 4.6
Status: ACTIVE / RELEASE_HOLD_OWNER_TESTING / M3_ACTIVE
Updated: 2026-09-01

## Purpose

This directory is the self-contained documentation root for the isolated private MEDIA BETA work. Historical numbered records preserve phase evidence; the current documents below define the active accepted state.

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product. `K_Research_Critic` remains the product/roadmap authority. VoiceBridge provides media/backend technology, implementation, and validation evidence.

## Canonical Reading Order

1. `63_M3_REFERENCE_REVIEW_CHECKPOINT_2026_09_01.md` - current recovery checkpoint after accepted asset byte capture and candidate reference hashing; current gate is independent listening review plus final reference SHA-256.
2. `62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md` - complete cross-repository baseline across KRC Core, MEDIA BETA, VoiceBridge, runtime/provider boundaries, release gates, and pre-capture M3 state.
3. `README.md` - current scope and release hold.
4. `61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md` - interpretation of the completed VoiceBridge live Gemini migration and its bounded impact on KRC prerecorded MEDIA BETA.
5. `60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md` - product hierarchy, active VoiceBridge KRC migration branch, and M3 roadmap overlay.
6. `03_CURRENT_STATE.md` - accepted operational baseline through the 2026-08-29 hardening state.
7. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` - owner release decision and recovery boundary.
8. `54_PROJECT_DOCUMENTATION_AUDIT_2026_08_27.md` - previous A9/A10 documentation synchronization record.
9. `01_ARCHITECTURE.md` - current architecture including separate VoiceBridge live and KRC prerecorded STT domains.
10. `02_ROADMAP.md` - current roadmap including the active KRC prerecorded M3 provider-evidence track.
11. `04_OPERATIONS_RUNBOOK.md` - owner testing/defect operations.
12. `05_TEST_PLAN.md` - current regressions and hold testing.
13. `06_DECISION_LOG.md` - compact decision authority.
14. `08_CHAT_HANDOFF.md` - fresh-chat recovery.
15. `09_WORK_LOG.md` - material chronology.
16. `07_FREE_MODE_TARGET.md` - optional future sustainability direction only.

## Current Acceptance Records

Key accepted late A9/A10 and current cross-project records:

```text
44_A9_7_I_PRIVATE_GPT_FACEBOOK_POLICY_E2E_ACCEPTANCE.md
45_A9_9_TELEGRAM_PUBLIC_ADAPTER_AUDIT.md
46_A9_9_PRIVATE_GPT_TELEGRAM_E2E_ACCEPTANCE.md
47_A9_10_LOCAL_UPLOAD_TRANSPORT_AUDIT.md
49_A9_10_ATTACHMENT_TRANSPORT_RUNTIME_ACCEPTANCE.md
50_A9_10_PRIVATE_GPT_LOCAL_ATTACHMENT_E2E_ACCEPTANCE.md
51_A10_STABILIZATION_AND_RELEASE_BOUNDARY.md
52_A10_SAFE_TABLE_RUNTIME_ACCEPTANCE.md
53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md
54_PROJECT_DOCUMENTATION_AUDIT_2026_08_27.md
55_STATE_CONTINUATION_NEGATIVE_MATRIX_ACCEPTED.md
56_CONSENT_CREDIT_QUOTA_NEGATIVE_MATRIX_ACCEPTED.md
57_DURABLE_FAIL_CLOSED_NEGATIVE_MATRIX_ACCEPTED.md
58_PRIVACY_CLEANUP_NEGATIVE_MATRIX_ACCEPTED.md
59_RETENTION_LOG_REDACTION_NEGATIVE_MATRIX_ACCEPTED.md
60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md
61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md
62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md
63_M3_REFERENCE_REVIEW_CHECKPOINT_2026_09_01.md
```

VoiceBridge provides detailed implementation/evidence records for both its accepted live Gemini baseline and the separate KRC prerecorded M0-M3 migration track.

Earlier numbered files remain historical evidence and should be read only when their phase details are needed.

## Source-of-Truth Precedence

When documents disagree:
1. current code, exact-head CI, and verified current runtime evidence;
2. `63_M3_REFERENCE_REVIEW_CHECKPOINT_2026_09_01.md` for the current M3 recovery position and accepted clean-public evidence state;
3. `62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md` for the complete 2026-09-01 cross-repository baseline;
4. `61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md` for interpretation of VoiceBridge live-provider changes versus KRC prerecorded state;
5. `60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md` for the cross-repository KRC migration overlay;
6. `03_CURRENT_STATE.md` for the accepted operational runtime baseline;
7. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` for release decisions;
8. latest accepted phase/capability record for the specific capability;
9. `06_DECISION_LOG.md` for policy decisions;
10. older phase/transition records.

VoiceBridge technical evidence is authoritative for the implementation it validates, but it cannot independently authorize KRC product release gates.

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
REFERENCE_SOURCE_CANDIDATES_LOCKED_3_OF_3
REFERENCE_ARTIFACT_CANDIDATE_SHA256_CREATED_3_OF_3
REFERENCE_AUDIO_RECONCILIATION_COMPLETE_FALSE
REFERENCE_SHA256_ACCEPTED_FALSE
READY_FOR_AB_FALSE
M3_LIVE_PRERECORDED_AB_NOT_RUN
M3_INDEPENDENT_LISTENING_REVIEW_NEXT
RELEASE_HOLD_OWNER_TESTING
```

## Active Engineering Branches

```text
KRC public Core: kolemasakar/K_Research_Critic / main
KRC MEDIA BETA: kolemasakar/K_Research_Critic / agent/video-url-research / draft PR #8
VoiceBridge current project baseline: kolemasakar/VoiceBridge / main
VoiceBridge active KRC prerecorded migration: agent/krc-media-gemini-migration
VoiceBridge migration head: c98c77521c919611b735971451e72366dedd2750
VoiceBridge migration draft PR: #45
VoiceBridge exact-head Validate: 33521717978 SUCCESS
legacy VoiceBridge KRC Media branch: agent/krc-media-transcript (historical/runtime lineage)
```

KRC PR #8 and VoiceBridge PR #45 remain integration/evidence mechanisms only; neither draft PR state authorizes a product release gate.

## Accepted Owner Media Inputs

```text
YouTube
Instagram Reel
Facebook Video/Reel via free Cobalt
supported public Telegram video post
one local current-conversation audio/video attachment
```

## Current Package

Accepted private runtime baseline:

```text
Builder package: 0.9.1-beta-a10
Action schema: 0.6.0-a9.10
Builder runtime applied: true
active KRC prerecorded provider: AssemblyAI universal-2
Gemini prerecorded candidate active: false
```

The completed VoiceBridge streaming provider migration does not alter these package/runtime values.

## Current Roadmap Position

```text
M3 INDEPENDENT LISTENING REVIEW + FINAL REFERENCE SHA-256
```

Asset byte evidence is accepted for the first three clean-public cases. Candidate reference artifacts and candidate hashes exist outside GitHub. They must now be reconciled against the exact accepted audio before any reference digest can be accepted or any case can reach `READY_FOR_AB`.

No AssemblyAI/Gemini M3 corpus call is authorized before this review gate completes.

## Recovery Command

```text
recover KRC MEDIA BETA M3 reference review checkpoint 2026-09-01
```

Always read `63_M3_REFERENCE_REVIEW_CHECKPOINT_2026_09_01.md` first, then `62_FULL_PROJECT_STATE_CHECKPOINT_2026_09_01.md`, and verify live GitHub heads/CI before any write or provider-consuming action.

## Non-Negotiable Hold Boundary

Do not merge MEDIA BETA into public Core, change the public KRC Builder, promote/replace the beta backend, enable external testers, publish/share MEDIA publicly, activate Gemini prerecorded for normal KRC jobs, enable automatic paid fallback, or weaken credit/privacy/traceability gates without a separate explicit owner decision.

VoiceBridge Phase 2 completion and KRC M3 provider-evidence work do not themselves approve any release gate.

## Documentation Naming Exception

This subproject predates the repository-wide preference against numeric-prefix ordering. Existing numbered phase/acceptance files are retained as stable historical references. New numbered records are added only when they are distinct immutable phase/checkpoint/audit artifacts, not as revisions of stable documents.
