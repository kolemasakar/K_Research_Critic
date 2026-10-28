# KRC Stage118 continued — full regression triage (2026-10-28)

Reproduced the suite on krc-cobalt in isolated checkout `/home/krcops/krc-stage118-sandbox/repo` with dedicated `test-venv`, installing repository `requirements.txt` and `requirements-dev.txt`, plus optional PDF-test dependencies `pypdf` and `Pillow`. No production/Stage114 changes.

Before Pillow: **882 passed, 10 failed, 17 skipped** in 31.16s. Two failures were missing `PIL` import; after installing Pillow, focused run `tests/test_p0_figure_asset_inventory.py` plus the three artifact test modules: **32/32 PASS** in 1.87s. This does not constitute rerun of the entire suite after dependency repair.

Remaining 8 observed failures are in legacy package/Builder/Core Skill snapshot and instruction-length tests, independent of the three artifact modules: `test_gpt_store_package` (3), `test_krc_mcp_canary` (1), `test_krc_media_r3_public_integration_candidate` (1), `test_krc_plugin_migration_candidate` (1), `test_krc_unified_r39` (1), `test_request_log_builder_integration` (1). They include canonical-snapshot mismatch and 8,000-character instruction cap checks against ~21,793 or ~22,626 chars. **Do not edit accepted Core Skill or public MEDIA packages merely to force tests green**; requires separate approval/triage.

Current artifact subset on server **28/28 PASS**; focused artifact + PDF tests **32/32 PASS** after Pillow. Whole suite remains **NOT PASS**, final post-Pillow total not yet verified. Remaining Stage117/118 work: crash-safe filesystem/SQLite recovery, immutable snapshot, authenticated UDS principal, idempotence, full-stage E2E. FREE_ONLY, no production/public/MEDIA/Stage114 v1 changes.
