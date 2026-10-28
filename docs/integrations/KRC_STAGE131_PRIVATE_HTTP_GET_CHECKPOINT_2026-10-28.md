# Stage131 HTTP-over-UDS Artifact GET test checkpoint — 2026-10-28
**STAGING ONLY / FREE_ONLY / Production NO-GO.**

On krc-cobalt verified source SHA `0d182b24e8660e8fabeed56a418ad3e4ce9d593d`, executed isolated HTTP-over-Unix-domain socket test in temporary directory with current process UID as synthetic allowed peer. No active service or existing socket changed.

`tests/test_stage131_private_get_http.py` verifies:
- valid GET /v1/artifacts/{artifact_id} -> HTTP 200;
- response body equals synthetic bytes;
- Content-Length and X-Content-SHA256 match actual bytes;
- wrong X-KRC-Request-ID and malformed ID -> HTTP 404.
Together with `tests/test_stage131_artifact_get_denials.py`: **4/4 passed in 0.72s**.

Limitations: The synthetic server trusts only test UID; it does not establish real Sentinel UID/claim mapping, OIDC, Tailnet, authenticated Stage127 remote GET or human approval. Wrong-principal HTTP-level testing requires a separate OS UID and is not covered by this suite, although lower-level scoped exchange negatives exist. Real owner consent, K2 deployment and E2E are NOT_RUN.

Next: reconcile Sentinel Stage127 allowed request methods, response size caps, exact authenticated GET authorization and replay handling; separately test with real isolated service identity after audited setup. Do not expose new ports.
