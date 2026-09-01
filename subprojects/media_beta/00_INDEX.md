# MEDIA BETA Documentation Index
Канонічний індекс документації приватного K-Research & Critic MEDIA BETA.

Version: 4.4
Status: ACTIVE / RELEASE_HOLD_OWNER_TESTING / M3_ACTIVE
Updated: 2026-09-01

## Purpose

This directory is the self-contained documentation root for the isolated private MEDIA BETA work. Historical numbered records preserve phase evidence; the current documents below define the active accepted state.

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product. `K_Research_Critic` remains the product/roadmap authority. VoiceBridge provides media/backend technology, implementation, and validation evidence.

## Canonical Reading Order

1. `README.md` - current scope and release hold.
2. `61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md` - current interpretation of the completed VoiceBridge live Gemini migration and its bounded impact on KRC prerecorded MEDIA BETA.
3. `60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md` - product hierarchy, active VoiceBridge KRC migration branch, and M3 roadmap overlay.
4. `03_CURRENT_STATE.md` - accepted operational baseline through the 2026-08-29 hardening state.
5. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` - owner release decision and recovery boundary.
6. `54_PROJECT_DOCUMENTATION_AUDIT_2026_08_27.md` - previous A9/A10 documentation synchronization record.
7. `01_ARCHITECTURE.md` - current architecture including separate VoiceBridge live and KRC prerecorded STT domains.
8. `02_ROADMAP.md` - current roadmap including the active KRC prerecorded M3 provider-evidence track.
9. `04_OPERATIONS_RUNBOOK.md` - owner testing/defect operations.
10. `05_TEST_PLAN.md` - current regressions and hold testing.
11. `06_DECISION_LOG.md` - compact decision authority.
12. `08_CHAT_HANDOFF.md` - fresh-chat recovery.
13. `09_WORK_LOG.md` - material chronology.
14. `07_FREE_MODE_TARGET.md` - optional future sustainability direction only.

## Current Acceptance Records

Key accepted late A9/A10 evidence remains:

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
```

VoiceBridge provides the detailed implementation/evidence records for both its accepted live Gemini baseline and the separate KRC prerecorded M0-M3 migration track.

Earlier numbered files remain historical evidence and should be read only when their phase details are needed.

## Source-of-Truth Precedence

When documents disagree:
1. current code, exact-head CI, and verified current runtime evidence;
2. `61_VOICEBRIDGE_GEMINI_IMPACT_AUDIT_2026_09_01.md` for interpretation of VoiceBridge live-provider changes versus KRC prerecorded state;
3. `60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md` for the cross-repository KRC migration overlay;
4. `03_CURRENT_STATE.md` for the accepted operational runtime baseline;
5. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` for release decisions;
6. latest accepted phase/capability record for the specific capability;
7. `06_DECISION_LOG.md` for policy decisions;
8. older phase/transition records.

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
FIRST_PUBLIC_SOURCE_TRANCHE_LOCKED
REAL_ASSET_BYTES_CAPTURED_FALSE
READY_FOR_AB_FALSE
M3_LIVE_PRERECORDED_AB_NOT_RUN
M3_BYTE_CAPTURE_SHA256_NEXT
RELEASE_HOLD_OWNER_TESTING
```

## Active Engineering Branches

```text
KRC product/beta docs: kolemasakar/K_Research_Critic / agent/video-url-research
VoiceBridge current project baseline: kolemasakar/VoiceBridge / main
VoiceBridge current main: a426ae331721dd36291874e45380faf603d854cf
VoiceBridge active KRC prerecorded migration: agent/krc-media-gemini-migration
VoiceBridge migration head: 7c2cac849d9322a8b532815ac3be44e87bd52e27
VoiceBridge migration draft PR: #45
legacy VoiceBridge KRC Media branch: agent/krc-media-transcript (historical/runtime lineage)
```

The KRC migration branch base is `eba77183bee29621aa6c7cb859737a10edb6e4d4`. Current VoiceBridge main is 13 commits ahead; the compared delta is documentation/Phase 2 closure synchronization only.

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
M3 BYTE CAPTURE + SHA-256
```

This is evidence preparation for the first locked public corpus tranche. It must hash exact media bytes without retaining raw media as a GitHub artifact and without invoking AssemblyAI or Gemini. Reference transcript hashing/review and `READY_FOR_AB` follow before any same-asset prerecorded provider A/B run.

## Non-Negotiable Hold Boundary

Do not merge MEDIA BETA into public Core, change the public KRC Builder, promote/replace the beta backend, enable external testers, publish/share MEDIA publicly, enable automatic paid fallback, or weaken credit/privacy/traceability gates without a separate explicit owner decision.

VoiceBridge Phase 2 completion and KRC M3 provider-evidence work do not themselves approve any release gate.

## Documentation Naming Exception

This subproject predates the repository-wide preference against numeric-prefix ordering. Existing numbered phase/acceptance files are retained as stable historical references. New numbered records are added only when they are distinct immutable phase/checkpoint/audit artifacts, not as revisions of stable documents.
