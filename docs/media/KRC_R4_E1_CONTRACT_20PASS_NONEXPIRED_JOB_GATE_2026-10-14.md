# KRC R4 Private — E1 contract and retained-job audit (2026-10-14)

## Scope
Owner ordered continuation of R4 acceptance after E2 absent-job 401→404 patch deployed. Performed only read-only queries and offline Python tests. No MEDIA start, provider work, credential updates, plugin mutation or Render deployment.

## Retained-job availability
- Connected production Neon `plain-snow-71973546` read-only query at `2026-10-14T04:14:58.126Z` showed **1 nonexpired job, 0 nonexpired COMPLETED**.
- Read-only grouped status query confirmed the single nonexpired record is **FAILED**.
- Consequently an actual successful nonexpired transcript readback (status+segments) **cannot be performed without a new qualifying MEDIA job or catching another existing live job inside its TTL**. Do not reuse expired job IDs or treat a syntactically valid missing ID's 404 as an end-to-end retrieval pass.

## E1 cross-scope tool-contract inspection
- Current KRC `plugins/krc_migration_candidate/mcp_canary/r3e1.py` defines `R3E1_TOOL_NAMES = R3C_TOOL_NAMES + ("media_youtube_start",)`: **nine accepted read-only tools plus one YouTube start**. Its tool list includes R3C Instagram preflight and lookup as cross-route reads.
- Contract tests `tests/test_krc_mcp_r3e1.py` explicitly assert **10 total / 9 readonly / 1 consequential**, with exact names, and `tests/test_krc_mcp_r3f_local_parity.py` checks surface parity. Removing Instagram descriptors without a versioned migration would break this published contract.
- Backend VoiceBridge `public_cobalt_media.ts` scoped auth accepts general/R3.9/R3E2 credentials for Instagram; it does NOT accept E1's YouTube-only credential. Therefore E1 Instagram preflight/lookup 401 in actual composite plugin is consistent with backend scope isolation, not proof E1 YouTube is broken.
- Do not expand E1 bearer privileges merely to make unsupported cross-scope reads succeed. Retain exact E1 10-tool contract pending owner-approved tool surface versioning or a documented per-app "unsupported cross-scope read" response; do not silently claim 9 read operations are all functional using E1 token.

## Offline tests actually run
On authorized krc-cobalt checkout `/tmp/krc_r4_limited_20261014_checkout`, isolated test dependencies `PYTHONPATH=/tmp/krc_pytest_deps_20261010`:
`python3 -m pytest -q tests/test_krc_mcp_r3e1.py tests/test_krc_mcp_r3f_local_parity.py`
- **20 passed in 0.45 s**, exit code 0.
- These are source-contract and mocked tests, **not a fresh live E1 cross-route acceptance**.

## Decision
- E1 YouTube owner-authenticated capabilities/preflight previously PASS; cross-scope Instagram 401 remains an intentional **authorization mismatch in the advertised tool list**, not corrected by weakening token scope.
- E1 advertised surface should be **versioned/clarified** in a separate approved change, with formal compatibility tests. A safe candidate would preserve only demonstrably authorized E1 read tools, or keep R3C tools marked "call through R3C" without falsely claiming they work on E1 credentials.
- Existing R3C/E2 read-only tests PASS in their demonstrated scope; E3/E4 read-only missing-ID 404 reachability is not full job retrieval.
- Current FULL composite five-app read-after-write gate remains OPEN awaiting nonexpired COMPLETED job.
- R4 private remains operationally limited; E4 Telegram LIVE remains BLOCKED by owner policy; global/public release HOLD.
