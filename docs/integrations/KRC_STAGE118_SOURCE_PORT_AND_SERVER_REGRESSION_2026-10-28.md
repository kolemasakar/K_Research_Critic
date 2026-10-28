# Stage118 — source port and isolated server regression, 2026-10-28

Source and six tests for Stage117 were ported to KRC development branch: `src/krc_research/artifact_stage117.py`, `tests/test_artifact_stage117.py`.

Restored isolated GitHub checkout at `/home/krcops/krc-stage118-sandbox/repo` on `krc-cobalt`, commit `98cb5c20f00e3c1262b79583d69d82aa3a2b850c`. No active production checkout or service was changed. Ran artifact subset in existing private testing Python: **28/28 PASS, 1.40 seconds**.

Attempted entire repository suite. First attempt stopped during collection with 34 missing import errors (notably PyYAML and pypdf) in reused Python environment. Created a NEW venv `test-venv` under stage118-sandbox and installed pytest, pyyaml, pypdf, jsonschema. Reran full test suite: collection still blocked by **21 errors** (logged in `/home/krcops/krc-stage118-sandbox/full-regression.log`), no global PASS can be claimed. Next action: inspect missing imports and reproduce complete development dependencies without changing production; rerun. FULL REGRESSION = BLOCKED BY TEST ENVIRONMENT.

**Not complete**: durable crash atomicity, immutable snapshot before streamed bytes leave backend, authenticated UDS peer, idempotency, private network E2E. Stage114 v1, production, public MCP and MEDIA unchanged. Staging remains NO-GO; FREE_ONLY.
