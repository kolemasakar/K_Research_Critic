# KRC №109 — nested evidence schemas, read-only isolated QA

October 25, 2026. Parallel processes previously caused remote execution and GitHub operations to be blocked. Retried successfully on isolated `krc-cobalt`; no production code or service configuration changed.

Added `src/krc_research/private_contract_details.py` (draft nested `EVIDENCE`, `CLAIM`, `RECEIPT`, and `ERROR_SCHEMA`, plus a sanitized pure error formatter and a fail-closed owner approval receipt check). Added `tests/test_p0_private_contract_details.py` with 11 tests.

First full test collection failed (`ModuleNotFoundError: No module named 'jsonschema'`) in the research `.venv`. Reused existing isolated `/tmp/krc-mcp-sdk-isolated` dependency path without installation, resulting in **313/313 PASS** in 2.51 seconds, exit 0:

```bash
cd /tmp/krc-p0-offline-20261025
PYTHONPATH=src:/tmp/krc-mcp-sdk-isolated .venv/bin/python -m pytest -q tests/
```

Limitations: these Draft 2020-12 schemas are prototypes; nested schema validators and structured errors are not yet wired into private dispatcher, and `PRESENT_UNVERIFIED` is not an attested owner approval. Existing public MCP tools/list remains unchanged. Full live K_Science→KRC route WAITING_FOR_SENTINEL_READY. Scientific approval NO_GO; FREE_ONLY and production/MEDIA/public freeze maintained.
