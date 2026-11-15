# N39 owner-authorized receipt issuance and audit SOP — DRAFT / 2026-11-15

Status: OPERATIONAL OWNER APPROVAL NOT YET OBTAINED. This document is a proposed policy only, not a grant, acknowledgement of human consent, production runbook sign-off or staging activation. GET / signer OFF; Production NO-GO.

## Independent acceptance acknowledged
K_Sentinel's independent report dated 2026-11-14 confirms root-owned **synthetic** N39 acceptance at KRC immutable code `4d477704a05b5a530ccfdbe6131cf659abf05fda`, including ConsentCustody consumption, recovery from PENDING after simulated crash, protected retrieval grant, explicit revoke/regrant, rollback and no scientific redispatch. Report: https://github.com/kolemasakar/Sentinel-Remote/blob/8720faae2513d106bd0f6383a1437a28cc58c391/docs/STAGE127_N39_REAL_ROOT_REPAIR_INDEPENDENT_ACK_2026-11-14.md . This is SOURCE/ROOT-OWNED ISOLATED ACK, not external/deployed authorization.

## Proposed human-authorization protocol
1. An authorized human owner explicitly approves **one** specified operation: science execution, artifact retrieval, retrieval revocation or scoped regrant. A retrieval grant does not follow automatically from original execution permission.
2. Independent operator validates the owner's identity using an approved out-of-band channel and creates a durable approval ticket *before* touching protected files. Record: unique ticket reference, owner identity reference (not secrets), verifier/operator identity, approval timestamp, action, principal, request_id, artifact_id (for retrieval), original consent provenance hash, time limits, reason and confirmation method. Never infer approval from an inbound JSON field, completion of a RequestLedger row, ownership of a Linux file, or a synthetic test.
3. Require separation between owner approver and operator who installs the receipt, or a documented dual-control exception approved by the owner. Do not allow the KRC service UID, its source code or GET handler to issue or amend root-owned grants.
4. Only a reviewed privileged operator may create approval files under a protected root-owned directory with restrictive permissions and unique opaque references. Verify exact schema, owner ticket, subject scope, explicit expiry, approved source digest, no symlinks, file owner/mode, atomic install, fsync of file and directory. Never use a reused revoked grant ref; regrant requires new ref and explicit root-owned revocation evidence/supersedes.
5. Before any mutation, append an independently protected, tamper-evident audit event: event UUID, ticket digest, operator identity, action/scope, UTC time and previous event digest. After mutation, append outcome, file content SHA-256, observed owner/mode, and verification result. Audit failure MUST fail closed; no subsequent permission elevation. Retain an off-host append-only audit copy, verify chain and periodically reconcile filesystem receipts, custody consumed DB and journal. GitHub comments alone are not the protected audit log.
6. For revocation, preserve the immutable original execution-consent receipt for provenance checks; create separately scoped revocation record. On suspected tampering, rollback or missing audit records, deny current reads, quarantine the scope and require an independent owner-reviewed replacement authorization.
7. Crash recovery must NEVER replay scientific execution. Durable journal PENDING with independently verified original grant and consumed record may be reconciled to provenance COMMITTED. Unverified evidence or uncertain audit outcome remains HOLD_UNVERIFIED pending owner/operator investigation.
8. Retain original approval tickets, hashes, revocation/supersede events and audit anchors according to an owner-approved retention period and privacy policy. Do not issue real consent until that retention/audit policy is approved.

## Explicit release-gate evidence required
- A human owner explicitly authorizes this SOP and identifies trusted approval and operator roles (or approved alternatives).
- A real, privacy-preserving operator identity verification record and **non-synthetic** approval ticket for a specifically scoped staging action.
- Independent demonstration of protected append-only audit, cross-record reconciliation, backup and tamper detection under approved permissions; deny on audit outage or mismatch.
- Independent K_Science provenance and HTTP 200/403/410/no-retry/descriptor SHA acceptance.
- K_Sentinel source-to-installed parity, Tailnet/UID/ACL/OIDC and external N01–N40 acceptance only after separate approved staging activation.

**Until independently verified:** OPERATIONAL_HUMAN_ISSUANCE_AND_AUDIT = HOLD. Installed services stay untouched, 200 MiB load test OWNER_WAIVED, 48 science E2E not authorized, external N01–N40 full PASS = 0/40.
