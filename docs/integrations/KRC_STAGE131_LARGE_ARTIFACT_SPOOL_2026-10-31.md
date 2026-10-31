# KRC large Artifact Storage signed retrieval — 2026-10-31

**SOURCE-ONLY / GET OFF / SIGNER OFF / STAGING ONLY / FREE_ONLY / Production NO-GO.**

## Implemented source
- Existing Artifact Storage remains authoritative; **INLINE <=1MiB**, artifact <=200MiB, storage total 2GiB, TTL 7 days as previous policy.
- `src/krc_research/stage131_signed_artifact_boundary.py` now consumes `exchange.read_stream` into a bounded `tempfile.TemporaryFile(mode="w+b")`, which is private and unlinked on POSIX. All bytes arrive and the underlying source integrity check completes BEFORE a successful response is returned. <=1MiB results return `body_bytes`; larger results return `body_file` open at offset 0 plus `size_bytes`, for a future HTTP/UDS adapter to send in bounded chunks.
- Failure from upstream read, corrupted bytes, oversize or incomplete generator closes the spool and returns errors without a partial success payload. The HTTP adapter **MUST close body_file in finally**, including client disconnects; currently no HTTP endpoint exists. This avoids loading <=200MiB fully in RAM.
- Existing `HardenedExchange.read_stream` performs full SHA256/size verification and expiration/owner scope checks; the new spool protects from late source generator errors before any success response. However filesystem authenticity, exact owner ledger parity and concurrent external mutation remain part of end-to-end acceptance.

## Test results
- New `tests/test_stage131_signed_artifact_large_spool.py`: 3MiB spool round trip, stream interruption/corruption before first success byte, oversize limit.
- GET focused source tests: **19/19 PASS**.
- Full repository suite: **1104 passed, 17 skipped, 0 failed** on `krc-cobalt`, PYTHONPATH=src:. with Stage131 venv, 41.71 seconds.

## Remaining blockers
1. Register **separate** authenticated `POST /v1/artifacts/read` in isolated UDS handler (not science POST), bind SO_PEERCRED and OIDC-derived identity, configured retrieval-only key and durable nonce, and check completed RequestLedger and trusted owner.
2. Send `body_file` with bounded copy, exact Content-Length/SHA header, exception-safe close on disconnect, negative leak tests and timeout/size quotas. Current in-process boundary does not create true server HTTP responses.
3. Independently test large files near 200MiB and stored TTL/total quota plus data mutation/cleanup races. No large 200MiB test claims here.
4. Sentinel 40 negative scenarios, KScience final ACK, source/install parity, rollback and explicit authorized staging rollout.

**No Stage127 or Stage131 installed service, secret, external route, science signer, or provider was modified.**
