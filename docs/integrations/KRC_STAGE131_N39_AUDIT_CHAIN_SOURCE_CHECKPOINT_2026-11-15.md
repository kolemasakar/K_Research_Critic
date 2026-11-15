# KRC Stage131 N39 — isolated protected audit journal checkpoint (2026-11-15)

**Code/test pin:** `8c9fdaf05bdc3b577fcbc8b50162113e89ba4020`. Draft PR #29.
**Scope:** SOURCE ONLY; no real authorization, no privileged installation, no running-service changes. GET/signer OFF, Production NO-GO.

## Delivered

- `src/krc_research/stage131_n39_audit_journal.py` implements a canonical SHA-256 linked event journal in restricted SQLite, using `BEGIN IMMEDIATE`, `synchronous=FULL` and a supplied **independent** anchor validation callback.
- For out-of-band issuance, revocation or explicit regrant, an `INTENT` event records scoped principal/request/artifact/grant, operator reference, ticket SHA-256, event ID and timestamp. Intent MUST be independently anchored before any privileged receipt installation. An unanchored intent cannot pass `check_anchored_intent`.
- `OUTCOME` event captures disposition and installed receipt SHA-256, references the original intent, and must be independently anchored before passing `check_anchored_outcome`. A failed/denied outcome is never equivalent to an installed grant.
- Verification detects missing/modified/reordered chain records and an independently anchored head mismatch. On absent, stale or unavailable independent anchor, all checks fail closed.
- `tests/test_stage131_n39_audit_journal.py` covers intentional tampering, removal/rollback, bad ticket, unavailable anchor, restart, unanchored intent, unanchored outcome, mismatched receipt SHA and denied outcome.

## Explicitly not solved by code alone

- The anchor checker is a dependency injection contract, **not** an implemented off-host WORM audit service. It must be implemented with independently authenticated read access and immutable, durable anchor storage; caller-controlled callbacks are not trustworthy issuance evidence.
- Neither owner identity verification nor real consent ticket signing is implemented or validated. Root-owned files alone do not establish human authorization.
- The existing `N39RootRetrievalReceipts` authorizer is **not yet wired** to this audit journal. The audit module cannot itself issue or revoke root-owned receipts. Operational integration with independently enforced audit-before-install and audit-after-install remains a release HOLD.
- No authoritative owner issuance SOP was approved; `KRC_STAGE131_N39_OWNER_ISSUANCE_AUDIT_SOP_DRAFT_2026-11-15.md` remains DRAFT.
- No installed source parity or external N01–N40 full tests. Previous Sentinel independent root-owned synthetic N39 ACK remains valid only for its exact earlier source pin; this new audit component requires separate review.
- Near-200MiB load: OWNER_WAIVED / NOT_TESTED. No new scientific research and no real grants.

## Acceptance prerequisites
1. Human owner expressly approves the scoped ticket/identity procedure and operator responsibilities.
2. Independent off-host tamper-evident anchor implementation, audited access, and crash/recovery validation.
3. Trusted root-only installer integration that verifies anchored INTENT before installation and independently anchored OUTCOME after installation, with rejection on any audit failure.
4. Independent Sentinel N39 ACK/MISMATCH on this audit source and K_Science consumer/provenance verification.

**Status:** AUDIT_SOURCE_TESTED / OPERATIONAL_ISSUER_AND_EXTERNAL_ANCHOR_HOLD / Production NO-GO.
