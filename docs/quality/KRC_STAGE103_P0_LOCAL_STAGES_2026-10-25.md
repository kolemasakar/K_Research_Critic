# KRC №103 — P0 local research stages (2026-10-25)

K_Science integration document sync after concurrent GitHub operation succeeded at commit `02e71b69`.

## Source verification
Retrieved latest GitHub branch file contents and blob IDs for `bounded_workflow.py`, its tests, and `workflow_readiness.py`. Source exists on branch; a full clean remote checkout regression was not performed in this stage.

## New isolated implementation
`src/krc_research/local_research_stages.py` with seven tests in `tests/test_p0_local_research_stages.py`, implemented on isolated `krc-cobalt`:
- source_search: validation of preexisting search logs only, **not live discovery**.
- source_verify: source metadata screening with `REVIEW_REQUIRED`, not truth checking.
- critic_review: independently-origin-counted evidence ledger arithmetic, conservative `REVISE`.
- research_export: status/digest receipt, not manuscript PDF/DOCX export.

Seven tests exercise these functions and fail-closed controls. Fresh full research checkout `PYTHONPATH=src .venv/bin/python -m pytest -q tests/`: **274/274 PASS**, 0 failed, 1.98s, exit code 0. Previous 267.

## Real network E2E acceptance plan, not yet executed
1. Confirm exact deployed gateway version, authorized subject/project identity, Tailscale/private listener access, source-sha custody, approved CriticProfile and allowed operation.
2. Extend signed allowlist only for reviewed, bounded new research requests; use durable replay storage, input caps and explicit audit receipts with no raw private scientific upload by default.
3. Send one authorized K_Science workflow with non-sensitive test evidence, require correlated gateway `dispatch_completed` and KRC result with `NO_GO`, trace hashes; repeat identical signed envelope and require `REPLAY_REJECTED`.
4. Inject timeout, bad signature, denied scope and incomplete source evidence; verify fail-closed semantics. Do not assert live research operation accepted before these succeed.

Status: isolated arithmetic/controller PASS; live service integration **NOT TESTED**, nine-operation full scientific workflow **NO_GO**. FREE_ONLY, no production/MEDIA/public changes.