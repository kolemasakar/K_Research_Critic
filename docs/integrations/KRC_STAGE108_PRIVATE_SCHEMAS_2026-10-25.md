# KRC №108 — private contract schema draft verification

Isolated `krc-cobalt` regression of entire `/tmp/krc-p0-offline-20261025` research checkout: **302/302 passed**, 0 failures, 3.85 s, exit 0 (2026-10-25).

Created and synchronized:
- `src/krc_research/private_contract_schemas.py` — DRAFT JSON schema representations for four `krc-science/1` operations, common response envelope, proposed error codes. Not wired into live network dispatcher and NOT an MCP tools/list output.
- `tests/test_p0_private_contract_schemas.py` — seven new tests confirming four operations, fail-closed output, error code enumeration, and conservative approval-receipt handling.

`approval_receipt_status` can only return `PRESENT_UNVERIFIED` for a well-shaped claimed approval; no external cryptographic/author approval attestation yet. Schemas are intentionally incomplete for nested scientific objects; cannot be declared final strict input/output schemas. No production or public MCP change.

Next: specify nested source/evidence/receipt schema, formalize error mapping in an isolated adapter, bind approval to verified signed principal + immutable profile digest, then run clean checkout and acceptance tests. K_Sentinel route still WAITING_FOR_SENTINEL_READY; FREE_ONLY; scientific NO_GO.