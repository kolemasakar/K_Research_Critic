# KRC signed Artifact GET isolated boundary checkpoint — 2026-10-31

Status: SOURCE_ONLY_PARTIAL / GET_OFF / SIGNER_OFF / Production NO-GO.

Source implementation:
- `src/krc_research/stage131_signed_artifact_boundary.py` introduces a **disabled-by-default in-process** boundary. It is NOT registered as `POST /v1/artifacts/read` on any UDS handler and has no deployed services.
- Calls previous signed verifier with trusted identity derived externally by authenticated UID; uses durable atomic nonce registry, read-only `RequestLedger` lookup for an existing COMPLETE science request, then `HardenedExchange.read_stream` for scope, TTL and full SHA256/size checks.
- Fully assembles <=1 MiB bytes before returning; no byte is returned on known errors. 200 bytes; 403 signature/peer/replay; 404 route OFF or no completed ledger/unknown; 410 owner-scoped expiry; 413 >1MiB; 502 corruption. **These are in-process result fixtures, not observed HTTP response codes.**
- Do not interpret this as support for large up-to-200MiB blobs. Existing stream generator after complete hash preflight still has race/late-errors concerns and needs verified immutable spool or sealed descriptor before HTTP headers. API field `request_id` selectors never authorize by themselves.
- Security debt: registered UDS handler with actual SO_PEERCRED, server-owned identity derivation, true retrieval key lifecycle/rotation, no replay across restart (isolated nonce storage tests only), precise ledger/object owner binding and installed-binary parity; no real signed HTTP response fixtures.
- Profiled unit test suite `tests/test_stage131_signed_artifact_boundary.py`, `test_stage131_artifact_nonce_registry.py`, `test_stage131_signed_artifact_read.py`: **16/16 PASS** on krc-cobalt source checkout. The four new isolated boundary tests cover disabled 404, exact signed success bytes, replay 403, wrong UID, no completed ledger, expired 410, corrupt 502 and altered MAC.
- No claim that Sentinel 40 external GET negatives or Science 48 E2E ran.

Next: reviewed server handler factory+in-memory UDS server with real signed POST and synthetic key, then independent Sentinel 40-case adapter. Do not change Stage127, installed Stage131, secrets, consent or science signer without distinct owner authorization.
