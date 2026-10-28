# KRC Stage118 — isolated server full regression after dependency repair

Date: 2026-10-28; environment krc-cobalt `/home/krcops/krc-stage118-sandbox/repo`, dedicated test venv. Dependency restore from repository requirements plus `pypdf`, `Pillow`.

Command: `PYTHONPATH=src /home/krcops/krc-stage118-sandbox/test-venv/bin/python -m pytest -q tests/`.

**Observed: 884 passed, 8 failed, 17 skipped in 28.11s, exit 1.** Complete suite is NOT PASS. All 8 failures: `tests/test_gpt_store_package.py` (3), `tests/test_krc_mcp_canary.py` (1), `tests/test_krc_media_r3_public_integration_candidate.py` (1), `tests/test_krc_plugin_migration_candidate.py` (1), `tests/test_krc_unified_r39.py` (1), `tests/test_request_log_builder_integration.py` (1). Failures involve canonical Core Skill snapshot mismatch or GPT Builder instruction length 8,000 limit vs 21,793/22,626 char content. None observed in Artifact Exchange test files; separate server artifact subset 28/28 PASS.

Not authorized to modify public accepted Core Skill, MEDIA packages or expected legacy snapshots to fake green. Keep this as independent baseline contract debt and require owner decision about which artifact is canonical and what constraints remain.

Stage119 priorities: durable crash-safe recovery, immutable artifact read, disk reserve and quota acceptance, trusted UDS identity and durable request idempotence. Stage114 v1, production and public MCP untouched; FREE_ONLY. No v2 E2E accepted.