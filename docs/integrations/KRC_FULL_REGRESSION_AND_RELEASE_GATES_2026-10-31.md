# KRC 2026-10-31 full regression checkpoint and release gates

## Verified source checkpoint
- Working branch: `agent/krc-public-media-r3-integration`, HEAD `93342d308cc32c32058b32353798ebba9629190b`; local checkout clean after fast-forward.
- Full repository regression: `PYTHONPATH=src /home/krcops/stage131-remediation-hash-venv/bin/python -m pytest -q tests --disable-warnings` => **1050 passed, 17 skipped, 0 failed** in 40.49 seconds.
- Remediated 3 CORE/R39 exact snapshot mismatches by regenerating embedded Core Skill snapshot and unified R39 from the shortened canonical public GPT Builder instructions. Builder package tests 10/10 PASS; canonical file 6943 characters <= 8000. Historic binary assets and live public GPT not modified.
- Remediated 3 staging test failures by failing closed on inaccessible UDS path in staging_entrypoint131 instead of leaking PermissionError; isolated entrypoint regression PASS.
- Source file SHA256: `prompts/GPT_STORE_INSTRUCTIONS.md` = `663a66f91de5efdae36aa9e36396811c01f756ab403078f6da5491c0f3332fbc`, `stage131_correlated_dispatch.py` = `6126efe5907886aca4c6344dc9385dc1bdc0ebf55bd0c9d93569c87f1d2d06a6`; `staging_entrypoint131.py` = `ec2bcb80d5fbaf88e9e618e4110fe69beae49da6256be33b25ea0b019e9a07f2`.

## Remaining implementation and acceptance (not done by green regression)
- Stage131 deployed immutable source still previously pinned to `49f8b857b46ebdf45636deffe90f8a4ee578bddf`. Existing services active: Stage131 PID 46327; Stage126 PID 37979; Stage127 PID 45059. No restart/install or permissions changed.
- Correlation, source-only custody gate, artifact descriptor TTL and provider adapter tests pass, but no reviewed enablement of real science signer and no genuine owner grant.
- Full inner-science result/error schema and operation-specific engine_result validation still need joint K_Science acceptance. K_Science M1+M2 32/32 source tests ACK at old RC, not this rebuilt HEAD.
- Crossref and Europe PMC provider adapter is metadata-only source code, network-off by default. Need final endpoint/redirect/timeout/rate/provider security review and explicit permitted integration before enabling any real provider calls.
- External Artifact GET is a disabled Sentinel design; 40 live GET negative cases NOT_RUN, 48 real science E2E NOT_RUN.
- No release deployment before immutable source pin, independently tested update/rollback procedure, user approval for staging installation, source-to-installed parity and partner ACK. Production NO-GO.

## Next handoff
1. K_Science: retest new exact pin for inner schema and results/correlation; return field-level ACK/MISMATCH and fixtures.
2. K_Sentinel: approve or reject signed UDS/HTTP GET/identity/consent mapping; keep GET disabled.
3. KRC: prepare verified signer-entrypoint and offline bibliography integration, then offer separate staging rollout for approval; no real science dispatch yet.
