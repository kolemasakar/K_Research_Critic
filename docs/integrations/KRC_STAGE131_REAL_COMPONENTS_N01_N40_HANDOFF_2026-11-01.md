# KRC Stage131 real isolated component fixture handoff — 2026-11-01

## Immutable source checkpoint
- Real-component fixture and regression commit: `08536070f51d6e38debed26741e6a560b5f0073b`.
- Repository: `kolemasakar/K_Research_Critic`, draft PR #29, branch `security/stage131-uds-bounds-20261101`.
- Reusable fixture: `tools/stage131_isolated_real_components.py`.
- Test: `tests/test_stage131_reusable_real_components.py` (4 combined integrated targeted tests PASS with `tests/test_stage131_real_store_ledger_authorization.py`).
- Dependencies: `src/krc_research/request_ledger119.py`, `artifact_exchange.py`, `stage131_artifact_nonce_registry.py`, `stage131_signed_artifact_read.py`, `stage131_signed_artifact_boundary.py`, `stage131_signed_artifact_uds.py`.

## Consumer contract (K_Sentinel)
1. Import `isolated_real_components` from the fixture module after placing KRC `src` and `tools` on the Python import path, or vendor exact pinned KRC modules in an isolated temporary checkout.
2. Within `with isolated_real_components() as fixture:`, use `str(fixture.socket_path)`, `fixture.signed_request(nonce="unique-value-at-least-16-chars")` and `fixture.descriptor()`.
3. The signed AF_UNIX client MUST call `shutdown(SHUT_WR)` after exactly declared Content-Length bytes and before receiving HTTP.
4. Fixture uses actual KRC SQLite RequestLedger (COMPLETE row), durable SQLite nonce registry, real ArtifactExchange metadata and content verification, real signed boundary and real UDS HTTP.
5. Synthetic identity is `K_Science / kolemasakar/K_Science / refs/heads/main`, scoped to current host process UID; synthetic key exists solely in source tests. No live credentials, science signer or deployed endpoints.
6. Negative cases can mutate isolated fixture instance: `fixture.ledger`, `fixture.exchange`, `fixture.nonce` and `fixture.boundary`; each context starts in a new temporary directory with independent state.
7. Descriptor SHA is derived from actual stored bytes and index metadata, NOT a claim from the HTTP response. K_Science must independently attest descriptor provenance before declaring consumer E2E success.

## Acceptance limits
- KRC source-only tests do not establish Stage127 external ingress OIDC/JWKS trust, Tailnet ACL, deployed key parity, external N01–N40 FULL PASS, or K_Science independent final ACK.
- K_Sentinel should replace only synthetic KRC backend in its isolated joined harness, run N01–N40 against real components and publish exact per-case PASS/PARTIAL/NOT_RUN with immutable pins.
- 200 MiB performance workload explicitly OWNER_WAIVED/NOT_TESTED. Production NO-GO; Stage127 GET OFF, signer OFF; no installed service changes.
