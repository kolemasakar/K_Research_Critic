# KRC Stage131 N39 — provenance issuance and crash-recovery repair checkpoint
Date: 2026-11-14

STATUS: SOURCE-ONLY TESTED; INDEPENDENT ROOT-OWNED RECEIPT AND EXTERNAL ACCEPTANCE PENDING; Production NO-GO.
No changes to installed Stage127, Stage131, Research v2, GET activation, signer, keys, ACL, or actual grants.
Near-200-MiB load test OWNER_WAIVED/NOT_TESTED.

## Independent review addressed
K_Sentinel ACK_SOURCE_ISOLATED / MISMATCH_PROVENANCE_RELEASE_GATE:
https://github.com/kolemasakar/Sentinel-Remote/blob/1fb989b2a65f25e05764ca9bef26ee0223824228/docs/STAGE127_N39_FORMAL_INDEPENDENT_ACK_MISMATCH_2026-11-14.md
The two reproduced release gaps were (a) consumed original consent with missing historical origin row after the second SQLite insert fails, and (b) caller-controlled regrant via the source-only operator API.

## Implemented source-only
- `ConsentCustody128.inspect_consumed(context)`: non-consuming verification of both the durable consumed nonce/ref row and original root-owned grant, matching canonical context digest, original valid consumed-at time, owner/mode and exact grant schema. Returns receipt SHA256, original approver, consumed time; DOES NOT accept caller boolean as owner consent.
- `N39ProvenanceJournal`: durable `PENDING` intent written before single-use ConsentCustody consumption; finalize `COMMITTED` only after verifying root-owned consumed evidence. If a fault occurs after durable consumption and before historical record finalize, `reconcile` may promote PENDING to COMMITTED using real custody evidence. If evidence missing or altered, remains `HOLD_UNVERIFIED`. Recovery does not invoke consent again, trigger science, issue a receipt, or authorize resubmission. A pre-dispatch attempt against an existing journal row never reruns science.
- `execute_with_durable_n39_custody`: alternative isolated source-only pre-dispatch helper binding principal/request/operation/task to the journal. No installed dispatch integration.
- `N39RootRetrievalReceipts`: read-only protected receipt reader; uses open directory FD + `O_NOFOLLOW` on directory/file, root owner/mode check, bounded file sizes, explicit retrieval scope, original root-receipt SHA, issuer, validity interval, revocation tombstone. No HTTP/UDS grant issuance API. Files are provisioned only out-of-band by authorized root operator.
- `N39ProtectedReadAuthorizer`: checks current attestation against root-owned original receipt and consumed evidence again at read time; reads a root-owned scope-hash index and root-issued active retrieval grant. A revoked grant cannot be reused; regrant must have new ref plus explicit supersedes referencing a matching root-owned revocation receipt. Nonmatching principal/request/artifact denied.
- Previous `N39ConsentPolicy` mutating operator helpers and read authorization now fail closed by default; synthetic tests must explicitly set `synthetic_test_mode=True`. This is a BREAKING SOURCE CONTRACT and partner clients must use protected authorizer for release testing.

## Fixture schema for independent root-owned acceptance
- Original grant: existing `ConsentCustody128` exactly `consent_ref/context_sha256/approver/approved_at/expires_at`, root-owned.
- Retrieval grant `<grant_ref>.json`: `version=1`, `action=grant`, `grant_ref`, `principal`, `request_id`, `artifact_id`, `issuer`, integer `issued_at`, integer `expires_at`, `origin_receipt_sha256`, nullable `supersedes`.
- Scope selector `<sha256(canonical({principal,request_id,artifact_id}))>.index.json`: `version=1`, exact scope, `active_grant_ref`, nullable `previous_grant_ref`. Root-owned and not group/world writable.
- Revocation receipt `<grant_ref>.revoked.json`: `version=1`, `action=revoke`, exact `grant_ref/principal/request_id/artifact_id`, `issuer`, integer `revoked_at`. A malformed pre-existing tombstone also blocks access. Regrant requires root-owned selector's previous ref, verified revocation and new grant `supersedes`.
- Original root-issued receipt MUST remain preserved as immutable history when the original execution consent is revoked. Revocation is recorded separately; removal or modification of the original receipt fails closed at read time.
- Root-owned receipt metadata proves controlled filesystem provenance, NOT that a particular human owner authorized the action; out-of-band owner ticket, operator identity, privilege/ACL, issuance and tamper-evident operational audit are still a separate release gate. In-memory or caller-provided issuer values are not authority.

## Recovery / race policy
- `PENDING` + consumed custody evidence = `RECOVERED` provenance ONLY; **never science replay**. No consumed evidence or missing root receipt = `HOLD_UNVERIFIED`.
- Previously signed and completed research is not a current retrieval grant. Read authorization is checked before bytes; revocation committed first denies subsequent reads. A transfer already authorized before revocation may finish (no retroactive cancellation).
- Missing or invalid original provenance/retrieval grant returns sanitized 403 FORBIDDEN; missing completed owner ledger 404 NOT_FOUND; authorized expired artifact 410 GONE; no retry or science rerun.
- Actual full external GET N01–N40, installed source-to-runtime parity and privileged root-custody tests remain separate.

## Verification evidence
Immutable code+tests pin: `4d477704a05b5a530ccfdbe6131cf659abf05fda`.
Targeted N39 provenance+policy+pre-dispatch: **16 PASS / 1 SKIP / 0 FAIL** (unprivileged isolated KRC krc-cobalt).
Complete KRC pytest regression on isolated krc-cobalt: **1146 PASS / 18 SKIP / 0 FAIL in 51.83 s**.
Tests intentionally mock root ownership for protected retrieval receipt logic; an independent actual root-owned retrieval fixture is NOT_RUN. Earlier Sentinel root-owned original ConsentCustody synthetic fixture is prior evidence, not acceptance of this NEW code. No real owner grants were created or revoked.

## Next independent gates
1. K_Sentinel: review exact pinned source, independently reproduce crash after real-root consent consumption and before history commit (no replay), malformed root receipt, unauthorized issuer, regrant/rollback, and root-owned retrieval-gate 403->200->403; publish ACK/MISMATCH for N39. Do not mark external N39 full PASS from these unit tests.
2. K_Science: independently attest actual owner approval/issuer provenance, source descriptor SHA, consumer HTTP 200/403/410, no retry, revocation and retention.
3. Owner/ops: review separately privileged issuance, immutable root receipts, independent audit and installed parity before any activation.

Production NO-GO. Signed GET OFF. Stage127/131/Research v2 installed services untouched.
