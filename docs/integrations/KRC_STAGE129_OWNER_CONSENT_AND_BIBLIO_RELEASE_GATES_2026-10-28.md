# Stage129 — owner consent issuance and staging release gates (2026-10-28)

**STAGING ONLY / FREE_ONLY / Production NO-GO.**

## Policy
A human owner approval is an out-of-band event. A `user_profile_approved=true` in an inbound JSON message is NEVER evidence. Root-owned approval receipts are a local *authorization control*, not proof that human approval happened. Operator MUST verify an explicit instruction from the authorized owner outside the untrusted research payload, record an immutable approval ticket and its scope, and separately audit who issued the receipt. No auto-approval or bulk grants.

## Consent grant custody
`consent_custody128.py` accepts read-only JSON from `/etc/krc-research-v2/approvals/<consent_ref>.json`. The directory must be owned by root and not writable by group/others. Receipt file must be root-owned, regular, no symlink, and not writable by group/others. The process must NOT receive filesystem write permission to this directory. The receipt JSON has exactly:
```json
{
  "consent_ref":"owner-approval-unique-id",
  "context_sha256":"64-char lowercase SHA-256 of canonical context excluding consent_ref",
  "approver":"OWNER_APPROVAL_RECORD_REFERENCE",
  "approved_at":0,
  "expires_at":0
}
```
This is not a signing certificate; root ownership and out-of-band authorization policy are necessary, but not sufficient to prove a particular human approved. Before deployment, independent review must establish approval ticket identity, principal, consent source, task/request/profile/digest/evidence binding, expiry, grant issuance provenance and rollback. Replay DB stays in the service-owned state root and records consumed grants atomically.

Manual provisioning after explicit owner approval (do not execute without approval): install root-owned approval directory mode 0755 under already protected `/etc/krc-research-v2`; generate receipt JSON in isolated root-only staging using canonical fingerprint from reviewed `context`, `O_EXCL`, `fsync` and `os.replace`; ensure receipt owner root/mode 0644 (safe because parent /etc path remains mode 0700); never include keys/MAC/JWT/secret data. The current KRC process **must NOT** execute this issuance procedure.

### Remaining security gates
- Real UID 988 root-owned approval dir/read test (unit tests mocked ownership)
- Complete independently recorded user-grant workflow and explicit owner acceptance
- Privileged staging-only deployment from reviewed SHA, no writable code
- Negative wrong grant, consent replay after controlled restart, scope mutation and audit
- Operational denial if approval file missing
- Negative bibliography when no provider and no network policy configured
- Staging-only service remains manual/disabled until accepted

## Bibliography
KRC current code contains Crossref DOI, Europe PMC DOI and Crossref editorial updates metadata-only adapters. Stage129 `BoundedBibliography129` requires callback-injected providers, applies per-provider call pacing and bounded response size, rejects invalid batch/duplicate DOI and sets evidence_level=METADATA_ONLY and scientific_approval=False. It is **not wired into running stage126**, and does not itself implement a persistent cache or audit log; its unused internal cache must not be presented as working caching. Requirements before real provider activation: explicit public DOI-only consent, min-interval + rate safety, durable provenance log, cache strategy, 429 errors and responses, URL allowlist and timeout, no paid fallback, and no full-text scientific approval.

## Test checkpoint
On krc-cobalt isolated working copy: 21/21 PASS for bibliography adapter, Stage128 UDS internal signing, consent custody, signer unit tests. Synthetic root metadata fixture does not establish actual filesystem ownership.

**Next decision:** conduct separate privileged host preflight and out-of-band approval workflow review. Keep running services and v1 gateway unchanged.
