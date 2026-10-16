# KRC Public MCP — local security iteration 2026-10-16

Status: PROTOTYPE ONLY / NO DEPLOYMENT / NOT PUBLIC READY.

Baseline: KRC_PUBLIC_MCP_OFFLINE_PROTOTYPE_2026-10-16.zip.
Output local artifact: KRC_PUBLIC_MCP_SECURITY_ITERATION_2026-10-16.zip (available as conversation attachment; source files have NOT yet been committed to GitHub).

## Changes
- Job status now checks opaque owner token against stored SHA-256 hash and does not reveal records to a different supplied token.
- Document ownership checked at submission.
- Explicit acknowledgement on job status starts result expiration at ACK +10 hours, and document expiration for linked documents at ACK+10h; document expiry is not initialized on upload.
- MCP call arguments include owner_token and optional acknowledge_delivery.

## Local validation
12/12 unittest PASS on isolated execution environment. No external services used.

## Security and acceptance gaps
- This is *not* strong end-to-end user authentication. Tokens are caller-supplied rather than cryptographically bound to a platform-authenticated user. HTTP OAuth/Bearer scheme and per-user authorization still needed.
- Unclaimed documents and undelivered results can persist without limit, conflicting with data minimization; define fallback TTL.
- Raw payload currently stored in SQLite; audit persistence/retention and strict access control.
- ResourceWarning: some sqlite connections not closed on interpreter test run.
- MCP Streamable HTTP protocol/security/interoperability incomplete. No actual OCI Cobalt concurrent workload test.
- FIFO fairness and idempotency between owners require additional tests; one worker and 3 simultaneous operations wording must be reconciled.

## Deployment state
No OCI changes; no production service created, no domain/TLS altered. RELEASE HOLD.
