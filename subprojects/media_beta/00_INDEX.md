# MEDIA BETA Documentation Index
Канонічний індекс документації приватного K-Research & Critic MEDIA BETA.

Version: 4.2
Status: ACTIVE / RELEASE_HOLD_OWNER_TESTING
Updated: 2026-08-27

## Purpose

This directory is the self-contained documentation root for the isolated private MEDIA BETA work. Historical numbered records preserve phase evidence; the current documents below define the active accepted state.

## Canonical Reading Order

1. `README.md` - current scope and release hold.
2. `03_CURRENT_STATE.md` - exact current functional state.
3. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` - owner release decision and recovery boundary.
4. `54_PROJECT_DOCUMENTATION_AUDIT_2026_08_27.md` - audit/synchronization record.
5. `01_ARCHITECTURE.md` - current accepted architecture.
6. `02_ROADMAP.md` - completed A9/A10 and release-gate roadmap.
7. `04_OPERATIONS_RUNBOOK.md` - owner testing/defect operations.
8. `05_TEST_PLAN.md` - current regressions and hold testing.
9. `06_DECISION_LOG.md` - compact decision authority.
10. `08_CHAT_HANDOFF.md` - fresh-chat recovery.
11. `09_WORK_LOG.md` - material chronology.
12. `07_FREE_MODE_TARGET.md` - optional future sustainability direction only.

## Current Acceptance Records

Key late-stage evidence:

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
```

Earlier numbered files remain historical evidence and should be read only when their phase details are needed.

## Source-of-Truth Precedence

When documents disagree:
1. current code, exact-head CI, and verified current runtime evidence;
2. `03_CURRENT_STATE.md`;
3. `53_RELEASE_HOLD_OWNER_TESTING_CHECKPOINT.md` for release decision;
4. latest accepted phase record for the specific capability;
5. `06_DECISION_LOG.md` for policy decisions;
6. older phase/transition records.

`54_PROJECT_DOCUMENTATION_AUDIT_2026_08_27.md` records which stale descriptions were corrected; it does not override newer live evidence.

## Current Phase Marker

```text
A9_OWNER_ZERO_CLIENT_MEDIA_INPUT_ACCEPTED
A9_10_LOCAL_ATTACHMENT_ACCEPTED
A10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED
RELEASE_HOLD_OWNER_TESTING
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

```text
Builder package: 0.9.1-beta-a10
Action schema: 0.6.0-a9.10
Builder runtime applied: true
```

## Non-Negotiable Hold Boundary

Do not merge PR #8/#28, change KRC public `main`, promote production VoiceBridge, enable external testers, publish/share MEDIA publicly, enable ScrapeCreators, introduce paid Telegram retrieval, or weaken credit/privacy/traceability gates without a separate explicit owner decision.

## Documentation Naming Exception

This subproject predates the repository-wide preference against numeric-prefix ordering. Existing numbered phase/acceptance files are retained as stable historical references. New numbered records are added only when they are distinct immutable phase/checkpoint/audit artifacts, not as revisions of stable documents.
