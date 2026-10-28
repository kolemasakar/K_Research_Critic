# KRC Stage131 — complete local regression inventory 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO**

## Scope and environment
Host: krc-cobalt, unprivileged venv /home/krcops/stage131-test-venv, local working tree /home/krcops/krc-stage128-test. Source is not a Git working tree and **cannot be attested as the current GitHub branch HEAD**. Tests were performed using system-independent venv, with pytest, pydantic, python-dotenv, jsonschema and pypdf available. Active Stage126 and Sentinel Stage127 remained PID37979/PID40306, NRestarts0. No new backend installation.

## Full test result
Command: `PYTHONPATH=src /home/krcops/stage131-test-venv/bin/python -m pytest -q --disable-warnings tests`
Result: **960 passed, 11 failed, 17 skipped** in 37.97 s. Exit nonzero. Counts refer to one complete run.

Failing test identifiers:
1. `tests/test_gpt_store_package.py::test_manifest_preserves_store_first_invariants`
2. `tests/test_gpt_store_package.py::test_instruction_package_matches_accepted_public_core_runtime`
3. `tests/test_gpt_store_package.py::test_store_package_validation_cli_passes`
4. `tests/test_krc_mcp_canary.py::test_existing_core_skill_snapshot_remains_exact`
5. `tests/test_krc_media_r3_public_integration_candidate.py::test_core_plus_media_addendum_fits_builder_limit_and_keeps_isolation`
6. `tests/test_krc_plugin_migration_candidate.py::test_core_skill_snapshot_is_exact_canonical_core`
7. `tests/test_krc_unified_r39.py::test_r39_builder_artifact_is_exact_core_plus_media_addendum`
8. `tests/test_p0_figure_asset_inventory.py::test_pdf_blank_inventory_not_graph_pass`
9. `tests/test_p0_figure_asset_inventory.py::test_invalid_page_denied`
10. `tests/test_phase12_quality_gates.py::test_repository_static_policy_passes`
11. `tests/test_request_log_builder_integration.py::test_public_core_instructions_keep_request_logging_disabled`

Observed causes or categories (not all fully root-caused): GPT Store Builder public instructions 21793 >8000 character limit; Core Skill exact-snapshot disagreement; PDF asset test failures require detailed traceback investigation; repository static policy calls git ls-files and fails because local test directory lacks .git. The failing public package tests do **not** automatically imply new Stage131 backend failures.

## Positive focused tests from prior same-host isolated venv
Science signer / Consent / Metadata / Bibliography / contract inventory: 29 passed. UDS / Research Boundary / Artifact / Science Adapter: 23 passed. They are subsets, not additive to 960.

## Nonclaims
This is **not** a full Stage131 immutable-SHA verification. Tests of current KRC Stage131 entrypoint must be rerun in an attested code checkout. No live user grant, no external bibliography, no scientific E2E acceptance, no production changes.

## Next gates
- Attest source from exact Git commit SHA, verify digest and run complete suite in isolated filesystem.
- Investigate PDF fixture failures and immutable Core Skill snapshot mismatch separately. Do not bypass guards merely to achieve green.
- Finish local backend with exact Stage131 approval directory, science authorization and separate replay; no root install/start until reviewed.
- Preserve owner-approved Sentinel Stage127 :19017 as canonical external transport candidate. Keep old ports/services unchanged.
