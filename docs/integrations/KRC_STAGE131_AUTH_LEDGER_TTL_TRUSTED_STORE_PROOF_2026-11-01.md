# KRC Stage131 — independent server-side authorization / trusted store proof (2026-11-01)

STATUS: SOURCE-ONLY VERIFIED / STAGING ONLY / GET OFF / SIGNER OFF / Production NO-GO.

Source/test pin: `dccdf677e6418526e0b0a3470fbeb312a9861d40`. Draft PR #29. No production or installed Stage131 changes.

## What is verified in a real integrated source path
- `SignedArtifactUDSServer` receives actual AF_UNIX HTTP, uses kernel `SO_PEERCRED` UID and hands it to `SignedArtifactReadBoundary`.
- `verify_signed_read` checks canonical HMAC-SHA256, exact trusted `principal/repository/workflow_ref`, 300-second skew and durable atomic nonce claim. Invalid UID and replay are denied.
- RequestLedger SQLite row must match exact trusted `principal + request_id` and be `COMPLETE`. Non-completed requests are denied before fetching.
- `ArtifactExchange.read_stream` was added as a narrow adapter over existing `iter_chunks/get_bytes`, thus retaining stored authoritative metadata checks (scope, TTL, size, SHA-256) before output.
- Tested non-owner principal and wrong request_id deny access; modified same-source bytes produce no success payload; equality at expiration time denies access (410).
- End-to-end synthetic small artifact from actual ArtifactExchange through signed UDS HTTP returns exact body, Content-Length, X-Content-SHA256 and nosniff; replay returns 403.

Tests: `tests/test_stage131_real_store_ledger_authorization.py` **3/3 PASS**, isolated krc-cobalt checkout.

## Boundaries
- Isolated source tests are not installed runtime authorization, ACL/key lifecycle proof, source-to-deployed parity, or external Stage127 ingress acceptance.
- 200 MiB performance test expressly OWNER_WAIVED / NOT_TESTED. Limit configuration unchanged.
- Sentinel independent ACK/MISMATCH and 40 external GET negative scenarios remain outstanding; Science 48 E2E remain NOT_RUN.
- No automatic science request created on GET; neither signer nor GET enabled.

## Partner action
Independently review signed UDS + real ArtifactExchange/RequestLedger/nonce integration at immutable pin, confirm exact auth/TTL/descriptor assertions and source-only acceptance. Do not interpret as deployment approval.

## Post-integration full source regression

On isolated `krc-cobalt` checkout, source/test pin `dccdf677e6418526e0b0a3470fbeb312a9861d40`: `PYTHONPATH=src /home/krcops/stage131-test-venv/bin/python -m pytest -q` -> **1133 passed, 17 skipped, 0 failed in 50.06 s**. This run preceded only documentation changes.
