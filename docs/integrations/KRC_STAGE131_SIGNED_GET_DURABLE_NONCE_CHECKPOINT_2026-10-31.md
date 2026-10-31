# KRC signed Artifact GET — durable nonce checkpoint (2026-10-31)

Sentinel independent MAC vector report: `18cd0f208aed9d76630bfa1439503ed183fcac08`. Its independently computed digest `906b7f4511634fc2b5fc65a539563304c579b1dbee4775aa85a7bd26965975fa` is recorded as partner-reported source-only evidence, NOT a KRC independently executed vector comparison this turn.

Implemented `src/krc_research/stage131_artifact_nonce_registry.py`: separate SQLite WAL/FULL durable nonce store with atomic BEGIN IMMEDIATE and unique (key_id, nonce, principal) key; deny replay after re-instantiation/restart, concurrent duplicate wins once, bounded TTL. This is a source-only building block and not yet installed/attached to a UDS handler.

- Test file: `tests/test_stage131_artifact_nonce_registry.py`.
- Tests executed in unprivileged krc-cobalt checkout: nonce+signature focused suite **12/12 PASS** (3 new durable registry tests + 9 existing signature tests).
- GET source-only verifier `stage131_signed_artifact_read.py` still takes injected nonce_claim and trusted_identity; no production trusted SO_PEERCRED/OIDC binding, retrieval-only provisioned secret or full owner+RequestLedger authorization.
- Separate signed endpoint `POST /v1/artifacts/read` remains NOT REGISTERED. No signed HTTP bytes/headers/actual server fixtures and no signed GET streaming tests. Artifact GET OFF, signer OFF; 40 external negative GET scenarios NOT_RUN, 48 science E2E NOT_RUN.

Security review debt: nonce TTL requires authorization timestamp replay-window coherence and server clock review; storage path must be deployed private under separately approved service UID; long-lived restarted nonce anti-replay claims should be tested with explicit service restart in disposable staging. SQL replay after TTL expires is acceptable ONLY when timestamp freshness rejects the old message.

Next KRC gate: implement and independently test isolated authenticated UDS request handler with trusted peer identity, scoped secret, ledger/owner/TTL/size/digest validation and all-or-nothing byte release, then send exact server-produced positive/negative fixture pin to Sentinel. Stage127 stays unchanged.

STAGING ONLY / FREE_ONLY / Production NO-GO.
