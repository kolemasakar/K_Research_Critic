# KRC Stage131 signed GET HTTP hardening checkpoint — 2026-11-01

**SOURCE-ONLY / GET OFF / SIGNER OFF / STAGING ONLY / FREE_ONLY / Production NO-GO.**

Source change in `src/krc_research/stage131_signed_artifact_uds.py`:
- Reject ambiguous framing with `400 INVALID_REQUEST`: Transfer-Encoding present, duplicate Content-Length, nondecimal/comma-delimited Content-Length.
- Bounded connection socket inactivity timeout 5 seconds and fail-closed socket exceptions.
- `ThreadingMixIn` UnixStreamServer for concurrency; daemon threads and backlog 16. **No bound on simultaneous threads yet**; resource-exhaustion acceptance remains BLOCKED.
- Unhandled boundary exceptions map to sanitized 503 BACKEND_UNAVAILABLE. No exception detail leaks.
- Existing success and replay semantics preserved.

Isolated server tests in `tests/test_stage131_signed_get_http_hardening.py` plus `tests/test_stage131_signed_artifact_real_uds.py`: **3/3 PASS** on krc-cobalt, including CL/TE ambiguity, duplicated and comma Content-Length, backend failure, concurrent valid response with another incomplete client, and signed response/replay.

**Security gaps that remain**: the socket timeout is an *inactivity timeout*, not an absolute full-request deadline; unbounded ThreadingMixIn may allow many slow clients; extra body bytes after declared Content-Length are not yet explicitly denied; response-writing disconnect+spool closure not independently tested on actual server; near-200MiB, store quota/TTL edge, trusted installed ACL/retrieval key, restart replay and Sentinel 40 cases NOT_RUN. No full repository suite run claimed for this checkpoint.

Request K_Sentinel independent source ACK/MISMATCH for framing, 503 mapping, concurrency plus further negative scenarios. K_Science client integrity remains separate. No installed service changes.
