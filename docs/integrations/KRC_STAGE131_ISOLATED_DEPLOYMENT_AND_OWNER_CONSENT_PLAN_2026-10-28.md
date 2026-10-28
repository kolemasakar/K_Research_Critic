# Stage131 — isolated backend and consent provenance acceptance plan
Date: 2026-10-28. **STAGING ONLY / FREE_ONLY / Production NO-GO**.

## Independently observed at handoff
GitHub KRC head before this document: `69f135e0b620a71c363dd3cd858201f7230e7cf7`. Sentinel Draft PR #38 head `980e44e92d06c7ac0b9c76e4d691d5eb8979e86c`. K_Science Draft PR #6 head `6229d80c43c3514e4ab5a13e8ac5ae4f087d705a`.
Via read-only Remote Desktop Commander on krc-cobalt: krc-research-v2.service active PID37979; Stage114 PID998; K_Science gateway PID7330; Public MCP PID723; Sentinel Stage127 PID40306 all active with NRestarts=0. Existing Unix socket /run/krc-research-v2/backend.sock; Tailnet listeners :19015/:19016/:19017. This does NOT prove source SHA or external runner OIDC admission.

## Deployment boundary (designed; NOT installed or started)
- Preserve Stage126 executable, systemd unit, existing UDS, config, approvals and state. Do not touch legacy Stage114 or :19015.
- New manual-only name `krc-research-stage131.service`. Dedicated immutable reviewed release root `/opt/krc-stage131/<full-reviewed-KRC-commit-SHA>/` root-owned, non-writable by service. Distinct UDS `/run/krc-stage131/backend.sock` with UID988, shared GID984 and mode 0660; distinct state `/var/lib/krc-stage131` with owner UID988 and mode 0700; distinct private config `/etc/krc-stage131/staging.json` and dedicated root-controlled approvals directory. Reject symlink/unsafe permission paths; do not symlink state to Stage126.
- Stage131 must start with isolated authorization and bibliography OFF; no live grant is minted automatically. Explicit flags must be reviewed before enabling KRC internal Science signer. Keep science HMAC exclusively KRC-side. No secret in GitHub or logs.
- Pin complete code archive and requirements hashes, review entrypoint/config, verify systemd sandboxing, UDS peer credentials, UID/GID, response limits, replay state and rollback. First perform no-start install; separately test start/stop and ensure existing PID/socket/listeners unchanged.
- Stop/disable Stage131 and retain its separate state/evidence on rollback; never restart Stage126 as part of Stage131 rollback.

## Real owner consent: mandatory independent acceptance
1. Owner's explicit out-of-band approval must identify immutable ticket (not a user_profile_approved boolean), exact operation, request_id, task_id, canonical principal, CriticProfile reference, evidence references, exact payload SHA-256, consent_ref, approved_at and expires_at. Scope must be narrowly bound and expire. No silent broad or recurring grant.
2. An independently accountable operator verifies identity, scope and the underlying owner instruction. The operator records audit evidence, reviewed context hash and receipt issuance identity outside the untrusted incoming payload. Explicitly distinguish human approval evidence from root ownership. No unpublished scientific contents may be transmitted without new explicit permission.
3. Root-only issuance writes a strictly validated immutable receipt after approval verification; KRC UID988 can read but cannot issue, replace or delete receipt. Never auto-approve from HTTP or job payload. Keep audit records free of secrets and personal corpus contents.
4. Test: absent approval DENY, wrong principal/operation/task/request/profile/evidence/payload DENY, altered digest DENY, expired DENY, symlink/writable file DENY, one-use PASS, concurrent duplicate DENY, durable replay after restart DENY, rollback and audit. Run against isolated Stage131 only.
5. Acceptance requires immutable approval ticket and evidence that approver and issuer were verified by independent procedure. Stage130 synthetic root grant is consumed and is NOT proof of real consent.

## Sentinel v2 ingress / OIDC / Tailnet
- Keep Stage127 :19017 fail-closed and manual-only; its no-bearer 403 is not E2E-01.
- Validate genuine GitHub issuer RS256/JWKS, exact `urn:kscience:krc:research:v1` audience, immutable owner/repository IDs, exact `repo:kolemasakar/K_Science:ref:refs/heads/main` subject and `workflow_ref` of reviewed default-branch workflow. Require one-use durable issuer+jti admission and tested post-auth principal projection `K_Science`; do not trust caller headers.
- Tailscale whois must check actual TCP peer and required `tag:kscience-krc-research`, record nonempty ephemeral StableID for each run; fixed StableID across GitHub ephemeral runners is not a reliable authorization rule. Verify provider-side federated credential scope and effective ACL, not just screenshot tests.
- Do not merge K_Science Draft PR #6 or repoint legacy :19015 as part of a network-only probe. Genuine positive E2E requires a reviewed workflow promoted to main and controlled activation; currently NOT_RUN.

## Bibliography metadata-only live gate
- Public approved DOI only; read-only HTTPS Crossref and Europe PMC, strict endpoint/host allowlist, HTTP GET, request timeout, response bound and 429 Retry-After bounded fail-closed handling; per-provider pacing and persisted private cache/provenance audit. No paid fallback, no full-text upload, no private science material.
- Before any external calls confirm exact DOI, scope and outbound policy; record provider/version/URL (nonsecret), fetch timestamp, HTTP status, cache hit, normalized DOI and returned metadata digest. Metadata missing ≠ no retraction; scientific_approval must remain false.
- Test invalid DOI, duplicates, 429, 5xx, timeout, malformed/oversized JSON, cache expiry, provider unavailable and interrupted operation without concealing partial results.

## Four-operation contract / E2E-01–05
- Keep machine-readable `research.profile.validate`, `research.evidence.preflight`, `research.bibliography.audit`, `research.inspection.review` input/output/error schemas DRAFT until KRC, Sentinel and K_Science agree exact wire envelope, identity mapping, error semantics, idempotency, artifacts and limits.
- Record 29 individual cases with actual UTC, KRC/Sentinel/K_Science full SHAs, workflow run ID, transport HTTP, schema result, scientific verdict and immutable evidence digest. Never turn NOT_RUN or synthetic PASS into actual E2E PASS.
- Production/public deployment remains NO-GO regardless of staging E2E results until separately approved.

## Next implementation prerequisites
1. Independently review Stage131 Python entrypoint and Stage126 installed immutable source; make a **separate** explicit config and no-start installation candidate; stage any root-only filesystem operations separately.
2. Formalize owner approval ticket issuer/authentication and negative verification without creating a live grant.
3. Finish Sentinel dynamic peer identity and durable one-use OIDC jti validation; test exact post-auth projection.
4. Approve a specific public DOI for provider smoke verification; finalize provider code and schemas.
5. Joint E2E only after 1–4 pass. Never assert unverified live deployment.
