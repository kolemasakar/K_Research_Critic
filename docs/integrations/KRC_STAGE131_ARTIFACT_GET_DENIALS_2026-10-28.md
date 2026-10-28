# KRC Stage131 — private Artifact GET denial checkpoint (2026-10-28)

STAGING ONLY / FREE_ONLY / Production NO-GO.

## Implemented
Added `tests/test_stage131_artifact_get_denials.py` commit `85e211c12ceaf2ce8c6782d6ebffb6bb9f8f4daf` covering private HardenedExchange negative access:
- wrong principal and wrong request_id -> NOT_FOUND
- malformed/traversal artifact ID -> NOT_FOUND
- oversized read chunk -> INVALID_REQUEST
- altered on-disk bytes -> ARTIFACT_CORRUPTED
- expired object -> ARTIFACT_EXPIRED

## Evidence
On krc-cobalt using SHA-verified checkout HEAD `85e211c12ceaf2ce8c6782d6ebffb6bb9f8f4daf`, `pytest -q tests/test_stage131_artifact_get_denials.py tests/test_artifact_stage117.py tests/test_stage131_actual_uds_response_schema.py` returned **10 passed in 0.83s**. No services restarted or newly installed.

## Scope / limitations
This confirms private artifact storage and read checks, not authenticated HTTP GET integration via Sentinel Stage127. Separate HTTP-level SO_PEERCRED and route authorization negative tests and end-to-end content-length/digest contract remain mandatory. Stage131 still has no real owner grant, no deployed backend and no scientific E2E. Existing :19015/:19016 services preserved, Stage127 :19017 sole canonical external transport staging candidate.

## Next
- Explicitly verify local HTTP GET response statuses and headers under synthetic peer identities without modifying active socket.
- Sentinel review method/path allowlist, OIDC->UDS identity scope and response byte caps.
- Freeze T5 wire schema only after joint reconciliation.
