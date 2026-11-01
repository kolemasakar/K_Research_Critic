# KRC isolated signed Artifact GET UDS server checkpoint — 2026-11-01

**STAGING ONLY / FREE_ONLY / Production NO-GO. GET OFF in actual deployed Stage127 and Stage131.**

## Source-only isolated server
- Added `src/krc_research/stage131_signed_artifact_uds.py`, new optional `SignedArtifactUDSServer`, no auto-launch or existing service changes.
- Dedicated `POST /v1/artifacts/read` (never `/v1/execute`), JSON size <=256KiB, authenticated SO_PEERCRED-derived UID passed to `SignedArtifactReadBoundary` for HMAC/identity/durable nonce/ledger/verified storage checks.
- On success sends `Content-Length`, `X-Content-SHA256`, `Content-Type: application/octet-stream`, `Cache-Control: no-store`, streams <=256KiB chunks from the completely verified unlinked disk spool and closes body_file in finally. Error JSON and disabled-route 404 are separate.
- Test `tests/test_stage131_signed_artifact_real_uds.py` launches a temporary real AF_UNIX HTTP listener with synthetic key/identity and synthetic 1MiB+3 bytes source. Asserts exact response SHA-256 header and bytes, first 200 and signed replay 403; **1/1 PASS**.
- Full source regression in unprivileged krc-cobalt checkout: **1108 passed, 17 skipped, 0 failed** (41.84 s).
- This is NOT a server fixture of deployed Stage131 and does not imply real GET is enabled. Existing source test does not independently prove full 200MiB, quota/TTL boundary, server restart replay, disconnect, full HTTP negative matrix, real persistent configured SO_PEERCRED ACL, retrieval-scoped secrets or installed source parity.
- Technical audit debt: production-grade response handling of interrupted transfers, timeouts, concurrency, race-safe scoped spool/stream verification and exact reproducible HTTP fixture captures. Sentinel 40 external GET negatives and Science 48 real E2E remain NOT_RUN.

## Partner acceptance actions
K_Sentinel: independently review code and genuine isolated server fixture harness, compare exact signed vector, prepare disabled adapter and 40 independent negative tests AFTER server contract review.
K_Science: verify digest/length and client receiver behavior; no consent from GET.
KRC: extend isolated tests to near-200MiB, failure paths, abort/cleanup and signed endpoint security, then require independent release approval. No deployed Stage127/131 changes without separate authorization.
