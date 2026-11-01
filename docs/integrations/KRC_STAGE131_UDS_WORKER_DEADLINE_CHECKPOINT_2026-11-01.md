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

## Owner decision, 2026-11-01
- Actual 200 MiB artifact load/transfer test explicitly waived by owner: `NOT_TESTED / OWNER_WAIVED`. Do not run it. Configured file limit remains 200 MiB; no performance acceptance is implied.
- Continue small synthetic negative tests for TTL equality/expiry, quota boundary, SHA256 tampering, cleanup, and HTTP/UDS semantics. Existing coverage added in `tests/test_artifact_exchange.py`; 25/25 targeted storage+HTTP tests PASS at `bb972aabc2e4c3efe309e01c12959c6a00d361d8`.
- Full source regression after these added tests must be separately recorded; partner acceptance and production release remain NO-GO.

## Actual isolated HTTP fixture acceptance and regression — 2026-11-01 (subsequent)

- Code/test pinned SHA: `5a5fa6db5787c4edeecf99d95ad0093d49c86590`.
- Actual AF_UNIX synthetic HTTP checks: `tests/test_stage131_signed_get_http_hardening.py` **7/7 PASS**.
- Scenarios: small 200 response with SHA-256/Content-Length, denied 403, malformed CL+TE 400, disconnect causing spool closure, worker exhaustion, slow header and exception sanitization.
- Full repository source regression after these tests: **1125 passed, 17 skipped, 0 failed in 47.60 s**, isolated `krc-cobalt` checkout.
- Small synthetic artifact only. No 200 MiB workload performed (**OWNER_WAIVED**).
- The fixture test validates actual wire response invariants but does not yet publish an independent captured byte-for-byte fixture bundle. It uses synthetic stub for the 200/403 cases and separate signed-boundary positive/replay test.
- Open blocking gates: delayed post-check request bytes; source/storage mutation race and installed ACL/keys; immutable wire capture bundle; partner independent ACK/MISMATCH; Sentinel 40 and Science 48 real E2E (NOT_RUN). No deployment or activation.

## Stage131 isolated protocol closure candidate, 2026-11-01

- **New source-only wire requirement:** the trusted AF_UNIX client MUST call `shutdown(SHUT_WR)` after transmitting exactly the declared request bytes, then read the response. The server now waits for EOF before calling the signed artifact boundary. Any undeclared extra bytes, including bytes delayed after the body, yield 400. Without EOF no dispatch occurs; deadline-driven EOF has a separate expired flag and is never accepted as peer confirmation. This is a **breaking internal wire contract** requiring Sentinel independent ACK/client update prior to any integration.
- Source regression negative tests include delayed extra bytes with zero boundary calls, missing write-half-close/deadline, incomplete body, CL+TE ambiguity, worker exhaustion.
- Artifact Exchange source race tests: same-size mutation before open is rejected by trusted SHA; atomic path replacement after open retains verified original open descriptor; subsequent corrupt path is rejected.
- Versioned reproducible **actual AF_UNIX HTTP captures (synthetic boundary)** in `tests/fixtures/stage131_uds_http_wire_capture_v1.json`, produced by `tools/capture_stage131_uds_fixtures.py` and independently compared by `tests/test_stage131_wire_capture_fixture.py`: success 200 with length/hash, denied 403, undeclared-trailer 400. These are normalized captures (volatile Date and Server headers removed), NOT raw complete packets or deployed ingress evidence.
- Focused combined tests **33/33 PASS** at `ab2e4bf3a9038e27e1aca96ca571d741c89baf4a`.
- 200 MiB performance test remains **OWNER_WAIVED / NOT_TESTED**; configured maximum unchanged.
- **Pending independent acceptance:** Sentinel needs to ACK the mandatory request write-half-close, error status/headers, source-to-client interoperability, disabled external adapter and 40 negatives. Science needs independent semantic 23-case review and end-to-end receiver acceptance. Installed runtime parity and consent gates remain separate. Production NO-GO.

## Final source validation record for isolated hardening (2026-11-01)

- Code, captured fixture and tests at immutable commit `ab2e4bf3a9038e27e1aca96ca571d741c89baf4a`.
- Focused tests: **33 PASS / 0 FAIL**.
- Entire KRC source pytest suite on isolated `krc-cobalt`: **1130 PASS / 17 SKIP / 0 FAIL, 48.16 s**.
- Handoff dispatched to Sentinel PR #38 comment `6554195420`, K_Science PR #7 comment `6554195755`, KRC Draft PR #29 comment `6554196169`.
- Partner review is a distinct gate: **ACK/MISMATCH not implied by comment publication**. The new write-half-close contract must be implemented/approved by an independent client owner before external adapter integration.
- Actual 200 MiB load test remains **OWNER_WAIVED / NOT_TESTED**, not an acceptance assertion.
- Production remains **NO-GO**, installed Stage127 and Stage131 unchanged, science signer OFF, external GET OFF.

## K_Science receiver policy alignment — latest source pin

- K_Science independently reported missing `X-Content-Type-Options: nosniff` header in KRC success responses. KRC added it to success and JSON error responses and refreshed the normalized observed capture bundle.
- Latest KRC source+fixture SHA: `54a6fbbeb3bf610d8a8f67ebf7bbb14b9211a72c`.
- On `krc-cobalt`, focused tests **33/33 PASS**; complete source pytest regression **1130 PASS / 17 SKIP / 0 FAIL in 48.04 s** after this header fix.
- K_Science consumer must still independently require equality of HTTP `X-Content-SHA256` and trusted descriptor SHA-256. This client-side remedy is outside KRC source and is NOT acknowledged as completed.
- Independent K_Sentinel and K_Science final ACK/MISMATCH remains pending. Production NO-GO, GET OFF, signer OFF, Stage127 unchanged, 200 MiB load test OWNER_WAIVED.
