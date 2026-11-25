# Stage135 joint review disposition - 2026-11-25

KRC decision for source implementation, subject to Sentinel ACK and owner
approval of actual credential installation and disclosure.

1. Retain independent randomly generated 32-byte key, stage135-prepared-read-v1.
No derivation from existing artifact key. Root provisions only after approval;
root-owned directory and separate root-owned 0440 key readable only by the
two approved service identities through a dedicated restricted group or
equivalent service-specific credential mechanism. No broadening existing
group access without membership audit. Rotation uses coordinated disable,
replace, verify, re-enable; revoke by disabling route and key acceptance.
Exact live UID/GID and custody to be verified by Sentinel before install.
No actual key created.

2. Existing projected branch identity is not sufficient by itself for a
disclosure grant. Require exact signed OIDC workflow_ref, run_id and
run_attempt=1 at Sentinel; bind approved workflow file and run to disclosure
registry. Propose a versioned contract amendment with these three fields
included in the HMAC-covered identity (workflow_file_ref, run_id,
run_attempt). Do not silently alter v1 envelope or deployed identity policy.
KRC and Sentinel must ACK exact field types and workflow allowlist before
implementing this amendment. No wildcard main admission.

3. Preserve v1 408 REQUEST_TIMEOUT for client request framing/deadline,
503 BACKEND_UNAVAILABLE for unavailable backend or capacity; propose
504 GATEWAY_TIMEOUT for upstream response deadline and 429 TOO_MANY_REQUESTS
only for explicit ingress rate limiter. Existing POST/result GET mappings
unchanged. Sentinel to ACK mapping before shared wire freeze.

Science reports 34/34 mock tests PASS; Sentinel reports 20/20 synthetic
prepared GET and 27/27 workflow regression PASS. Neither demonstrates
actual KRC UDS authority. Next KRC implementation: isolated registry,
revocation, canonical HMAC verifier, exact byte reader and UDS fixtures.
No real disclosure, consent activation, service changes or production GO.
