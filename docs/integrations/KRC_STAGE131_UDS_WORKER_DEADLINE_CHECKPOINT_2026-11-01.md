# KRC Stage131 isolated UDS bounds checkpoint — 2026-11-01

**SOURCE-ONLY / STAGING ONLY / FREE_ONLY / GET OFF / SCIENCE SIGNER OFF / Production NO-GO.**

## Isolation and revision
- Baseline pinned recovery commit: `2168dec979bc528dc5b3e52aeae1d9664160b06a`.
- Work branch: `security/stage131-uds-bounds-20261101`; draft PR #29 targeting `agent/krc-public-media-r3-integration`.
- Isolated runtime checkout on `krc-cobalt`: `/tmp/krc-stage131-bounds-20261101`. No installed Stage131 / Stage127 changes; not merged.

## Implemented
- Bound simultaneous UDS request workers with `threading.BoundedSemaphore(4)` acquired before spawning a thread.
- Over-capacity requests are rejected fail-closed (best-effort 503; AF_UNIX Linux can reset when unread bytes are discarded).
- Per-connection 20-second absolute shutdown deadline independent of slow-client trickle and pre-existing 5-second inactivity timeout.
- Connection timer cancelled in handler finish, semaphore released in worker finally.
- Negative tests for saturation and trickling headers.

## Evidence
- Targeted suite: `PYTHONPATH=src /home/krcops/stage131-test-venv/bin/python -m pytest -q tests/test_stage131_signed_get_http_hardening.py tests/test_stage131_signed_artifact_real_uds.py` -> **5 passed**.
- Complete source suite: `PYTHONPATH=src /home/krcops/stage131-test-venv/bin/python -m pytest -q` -> **1112 passed, 17 skipped, 0 failed in 47.58 s**.
- This test run is for branch HEAD `c8c86c6ff1a3175dea495654b755df8e32003a62` (before this documentation-only commit).
- No actual near-200-MiB performance, external 40-case matrix, or 48 Science E2E claimed.

## Remaining blocking gates
1. Reject extra bytes after declared request body; deterministic response semantics for malformed HTTP and disconnected clients.
2. Isolated actual-UDS resource exhaustion and slow response/slow-reader stress; validate four-worker limit across disconnect/reboot.
3. Artifact storage authoritative hash, expiry boundary, 200-MiB/2-GiB quota/low-disk evidence and cleanup.
4. Versioned positive/negative HTTP wire captures; independent K_Sentinel ACK/MISMATCH.
5. Installed ACL/key/runtime parity, rollout/rollback and explicit owner authorization before activation.

**No source-only PASS implies deployment approval.**
