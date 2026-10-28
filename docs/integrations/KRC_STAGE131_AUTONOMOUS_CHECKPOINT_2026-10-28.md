# KRC Stage131 autonomous checkpoint — 2026-10-28
**STAGING ONLY / FREE_ONLY / Production NO-GO**.

## Independently observed host
krc-cobalt: Stage126 PID37979, Stage114 PID998, K_Science gateway PID7330, Public MCP PID723, Sentinel Stage127 PID40306: active; each NRestarts=0. No Stage131 privileged installation/start.

## Completed focused tests
On existing isolated /home/krcops/krc-stage128-test source:
- signer tests 5/5 PASS;
- bounded bibliography tests 4/4 PASS;
- `python3 -m compileall -q src/krc_research` PASS.
Earlier new Stage131 negative configuration 9/9 PASS, explicit approvals_dir guard 1/1 PASS. These are separate tests/checkpoints, not a complete immutable-head regression.

## Broad test discovery: blocker
`PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -q` discovered 128 tests, with 82 import/setup errors, mostly due to missing pytest/pydantic/dotenv in system Python. This is **NOT PASS**, and does not by itself demonstrate 82 product defects. Do not install dependencies into a live or shared interpreter. A full pinned SHA isolated virtualenv and proper test runner are prerequisites. Do not sum focused tests into comprehensive acceptance.

## Current scope
- Consent custody defaults fixed to demand explicit approvals_dir for opted-in Science signer; signer stays OFF by default. No owner instruction issued for a real grant.
- Stage131 private UDS source and manual-only unit example exist in GitHub, not deployed.
- Crossref/Europe PMC public DOI metadata live backend NOT RUN; contract still DRAFT; real E2E-01–05 NOT_RUN.
- Sentinel owner-approved external canonical transport remains existing Stage127 :19017; legacy ports unchanged.

## Next unprivileged tasks
1. Obtain immutable full-source checkout/archive (verified SHA) and isolated test venv with pinned dependencies; rerun focused and complete tests via correct runner, record counts and errors.
2. Complete Stage131-only consent path injection, deny tests and manual-issuance audit (no live grant).
3. Build provider callbacks with strict public DOI HTTPS allowlist, pacing, cache and error accounting; run only explicitly scoped public metadata smoke.
4. Freeze four-operation JSON schema and private Artifact Exchange semantics with Sentinel and K_Science.
5. Run Stage131 isolated backend integration/negative tests before any privileged deployment.
