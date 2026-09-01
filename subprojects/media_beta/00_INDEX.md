# MEDIA BETA Documentation Index
Канонічний індекс документації приватного K-Research & Critic MEDIA BETA.

Version: 4.3
Status: ACTIVE / RELEASE_HOLD_OWNER_TESTING / M3_ACTIVE
Updated: 2026-09-01

## Purpose

This directory is the self-contained documentation root for the isolated private MEDIA BETA work. Historical numbered records preserve phase evidence; the current documents below define the active accepted state.

`K-Research & Critic - MEDIA BETA` is a closed-beta module of the published `K-Research & Critic` product. `K_Research_Critic` remains the product/roadmap authority. VoiceBridge provides media/backend technology, implementation, and validation evidence.

## Canonical Reading Order

1. `README.md` - current scope and release hold.
2. `60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md` - current product hierarchy, active VoiceBridge migration branch, and exact M3 roadmap overlay.
3. `03_CURRENT_STATE.md` - accepted operational baseline through the 2026-08-29 hardening state.
4. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` - owner release decision and recovery boundary.
5. `54_PROJECT_DOCUMENTATION_AUDIT_2026_08_27.md` - previous A9/A10 documentation synchronization record.
6. `01_ARCHITECTURE.md` - accepted private runtime architecture baseline.
7. `02_ROADMAP.md` - current roadmap including the active M3 provider-evidence track.
8. `04_OPERATIONS_RUNBOOK.md` - owner testing/defect operations.
9. `05_TEST_PLAN.md` - current regressions and hold testing.
10. `06_DECISION_LOG.md` - compact decision authority.
11. `08_CHAT_HANDOFF.md` - fresh-chat recovery.
12. `09_WORK_LOG.md` - material chronology.
13. `07_FREE_MODE_TARGET.md` - optional future sustainability direction only.

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
```

VoiceBridge provides the detailed M0-M3 implementation/evidence records for the active provider-migration track, including the 2026-09-01 real-corpus source-selection checkpoint.

Earlier numbered files remain historical evidence and should be read only when their phase details are needed.

## Source-of-Truth Precedence

When documents disagree:
1. current code, exact-head CI, and verified current runtime evidence;
2. `60_PROJECT_DOCUMENTATION_AUDIT_AND_M3_ROADMAP_SYNC_2026_09_01.md` for the current cross-repository engineering overlay;
3. `03_CURRENT_STATE.md` for the accepted operational runtime baseline;
4. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` for release decisions;
5. latest accepted phase/capability record for the specific capability;
6. `06_DECISION_LOG.md` for policy decisions;
7. older phase/transition records.

VoiceBridge technical evidence is authoritative for the implementation it validates, but it cannot independently authorize KRC product release gates.

## Current Phase Marker

```text
A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED
A9_10_LOCAL_ATTACHMENT_ACCEPTED
A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED
KRC_MEDIA_GEMINI_M0_COMPLETE
KRC_MEDIA_GEMINI_M1_PASS
KRC_MEDIA_GEMINI_M2_PASS_INACTIVE
KRC_MEDIA_GEMINI_M3_ACTIVE
FIRST_PUBLIC_SOURCE_TRANCHE_LOCKED
REAL_ASSET_BYTES_CAPTURED_FALSE
READY_FOR_AB_FALSE
M3_LIVE_AB_NOT_RUN
M3_BYTE_CAPTURE_SHA256_NEXT
RELEASE_HOLD_OWNER_TESTING
```

## Active Engineering Branches

```text
KRC product/beta docs: kolemasakar/K_Research_Critic / agent/video-url-research
VoiceBridge active forward migration: kolemasakar/VoiceBridge / agent/krc-media-gemini-migration
VoiceBridge migration draft PR: #45
legacy VoiceBridge KRC Media branch: agent/krc-media-transcript (historical/runtime lineage)
```

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

## Current Roadmap Position

```text
M3 BYTE CAPTURE + SHA-256
```

This is evidence preparation for the first locked public corpus tranche. It must hash exact media bytes without retaining raw media as a GitHub artifact and without invoking AssemblyAI or Gemini. Reference transcript hashing/review and `READY_FOR_AB` follow before any same-asset provider A/B run.

## Non-Negotiable Hold Boundary

Do not merge MEDIA BETA into public Core, change the public KRC Builder, promote/replace the beta backend, enable external testers, publish/share MEDIA publicly, enable automatic paid fallback, or weaken credit/privacy/traceability gates without a separate explicit owner decision.

M3 provider-evidence work does not itself approve any release gate.

## Documentation Naming Exception

This subproject predates the repository-wide preference against numeric-prefix ordering. Existing numbered phase/acceptance files are retained as stable historical references. New numbered records are added only when they are distinct immutable phase/checkpoint/audit artifacts, not as revisions of stable documents.
