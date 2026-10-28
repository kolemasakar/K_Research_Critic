# Stage131 SHA-pinned regression checkpoint — 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO.**

## Immutable checkout
On krc-cobalt cloned GitHub branch to `/home/krcops/stage131-verified-source`, git HEAD verified `acb0e4e09b73e18de7351b7cedb5460d95d9c266` at first run, then fast-forward updated to `8d3067f75e18245dd472ef48d7d723ee9d442948`. Unprivileged isolated venv is `/home/krcops/stage131-test-venv`; no active services changed.

## Stage131 compatibility correction
One test failed when explicit consent approvals_dir was made mandatory: `test_stage128_internal_signer_live_uds.py` still used old implicit directory interface. Updated fixture to pass a synthetic isolated `consent_approvals_dir` and verify it is forwarded (no loosening of production guard). Targeted pytest: **11/11 PASS**, HEAD `8d3067f75e18245dd472ef48d7d723ee9d442948`.

## Full pinned source run
`PYTHONPATH=src /home/krcops/stage131-test-venv/bin/python -m pytest -q --disable-warnings tests`, from exact HEAD `8d3067f75e18245dd472ef48d7d723ee9d442948`: **971 passed, 10 failed, 17 skipped in 39.40 s**. Test process exit 1; NOT full PASS.
Remaining failures:
- 3 GPT Store package tests
- 1 MCP Core Skill exact snapshot
- 1 Media R3 public integration Builder limit
- 1 Plugin migration canonical snapshot
- 1 Unified R39 Builder artifact
- 2 PDF embedded figure inventory tests
- 1 Request Log Builder public instruction length.
The repository-static-policy failure seen in a non-git directory disappeared with the real Git checkout; the consent integration failure was fixed. Do not silently edit public Builder/Core skill or PDF validators to force green. Private KRC science/backend acceptance remains separate.

## Unperformed
No privileged root install/start of Stage131, no real human owner consent issuance, no Crossref/Europe PMC live provider calls, no approved final schema, no actual authenticated scientific E2E. Sentinel Stage127 is sole canonical external transport candidate, separate T1/T2 responsibilities. Production remains NO-GO.
