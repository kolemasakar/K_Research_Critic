# KRC Public MCP V5 — 2026-10-16
Status: OFFLINE_CODE_FIX_PASS / NOT_DEPLOYED.

## Direct execution
- Re-opened and verified V4 ZIP from conversation mounted in working container.
- Baseline tests: 27/27 PASS but SQLite ResourceWarning.
- V5 changes in local source: use contextlib.contextmanager with try/finally close() for Store._connect; no intended external API change.
- Strict local tests: python -W error::ResourceWarning -m unittest -q => 27/27 PASS, no observed connection warnings.
- Archive KRC_PUBLIC_MCP_V5_SQLITE_CLOSE_2026-10-16.zip validated with unzip -t; SHA256 531c270cbaf7467285a048992a0f0c0e8db205c8d81e5971a155a500be854647.
- Local Python 'mcp' SDK absent; package index inaccessible due to DNS. Official-client compatibility not tested.
- OCI Cobalt read-only: Python 3.12.3; MCP SDK absent; ~543 MiB RAM available; 37 GiB free disk; Cobalt :9000 and Caddy :443 active; staging :9013 unused.
- No code deployed or source written to the VM.
## Remaining gates
- Commit actual V5 source/test files to repository (ZIP currently conversation artifact only).
- Official MCP Streamable HTTP SDK client end-to-end verification, security abuse handling.
- Isolated OCI staging and 1/3/10 concurrency WITH real Cobalt workload.
- Sentinel permissions, Caddy HTTPS and public readiness checks.

Do not interpret 27 offline tests as production acceptance.
