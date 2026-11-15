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

## GitHub audit witness created — 2026-11-15

A separate branch `audit/n39-anchor-ledger` now contains `audit/n39/README.md`, `GENESIS.json` and `ANCHOR_FORMAT.json`. Genesis is EMPTY: seq=0 and a 64-zero digest. Commit `179a4429747e5ee5718ec42db61ebe280a5626da` records the storage structure, not a real grant or even an operating anchor.

This repository is public. Publish ONLY nonidentifying sequence/digest/commit references; keep the real owner's identity, private ticket, consent/grant documents and sensitive request details OUT of GitHub.

**NOT IMMUTABLE YET**: GitHub rulesets currently return `[]`. The connected GitHub app cannot configure branch rulesets or access admin-only branch protection settings. The owner must configure deletion/force-push restrictions and independent reviewed changes, ensure no admin bypass where supported, and appoint an independent checkpoint witness. Same-repository Git objects are not legal WORM storage and can be made unreachable by a repo admin.

### Concrete approval and issuance sequence
1. Approve *this procedure only* by explicit owner instruction, identify owner verifier and independent root operator, and approve allowed retention period and identity verification channel. Approval of the procedure itself does not approve ANY scientific task or artifact read.
2. For each operation, owner authorizes its exact action, principal, request ID, artifact ID (for read/revoke), expiry and reason through the agreed authenticated channel; trusted operator creates a private ticket and its SHA-256.
3. Authorizer prepares a local N39 audit `INTENT`; publish its chain-head digest and sequence as a NEW GitHub anchor file; verify GitHub commit ancestry and capture an independent witness of commit SHA. Fail closed if either write/verification fails.
4. Independently privileged operator installs one root-owned receipt in the isolated authorized environment; never place real consent or ticket content in this public repo. Validate UID/mode/scope/expiry and fsync; rollback/deny on mismatch.
5. Operator records `OUTCOME` and installed receipt SHA-256 in local audit; publish another NEW GitHub checkpoint, independently verify and witness it before treating the operation as audit accepted.
6. When revoking, preserve historic root-owned original consent evidence, create a separate root-owned revocation tombstone, anchor before/after, and deny new reads. A regrant needs a distinct reference, an independently approved new ticket and explicit supersedes.
7. During restart or recovery, reconcile local N39 journal with root-owned evidence AND the independent GitHub-witnessed chain; never re-consume consent or re-dispatch science; ambiguous cases remain `HOLD_UNVERIFIED`.
8. Partner Sentinel and Science must independently verify issuance/recovery evidence and final client status before deployment approval.

**No real issuance without separate action-scoped owner consent and verified controls.**
