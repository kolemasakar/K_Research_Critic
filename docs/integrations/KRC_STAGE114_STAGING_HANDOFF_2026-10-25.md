# KRC №114 — staging backend handoff for K_Sentinel

Date: 2026-10-25. Isolated KRC checkout on krc-cobalt. No production/public/MEDIA changes.

Implemented `src/krc_research/staging_backend114.py`, pure in-process staging entrypoints `execute_staging_request` and `staging_capabilities`; no HTTP or MCP listener. Four allowed private operations: `research.profile.validate`, `research.evidence.preflight`, `research.bibliography.audit`, `research.inspection.review`. Uses existing signed envelope validation/ACL/TTL, draft JSON schema checks, sanitized error mapping, passed-in replay registry. External bibliography provider disabled by default: staging caller must inject explicitly approved no-network bibliography function for offline acceptance. Synthetic tests never contact outside providers. Inventory endpoint is a pure function that does not create jobs.

Seven new tests; full isolated suite **341/341 PASS** (2.79s, exit 0) using `PYTHONPATH=src:/tmp/krc-mcp-sdk-isolated .venv/bin/python -m pytest -q tests/`. Code and tests committed to KRC branch.

K_Sentinel responsibilities: create separate staging-only authorized adapter or bridge (not simply add four operations to existing `LIVE_ALLOWED`), preserve OIDC/Tailscale/ACL, isolate loopback service/network if needed, map four operation schemas, require durable replay registry, keep bibliography network disabled until separately approved, implement independent principal-to-CriticProfile consent binding and stable machine errors; test zero request and negative cases. Current production `kscience-krc-gateway` only permits `krc_capabilities`, `krc_tools_list`. Do not change public MCP or private production allowlist without separate acceptance.

Open blockers: no active private network listener for these research operations, no live K_Sentinel 4/4 mapping, schema drafts not final, authenticated human author approval not established. Research integration network acceptance **NO_GO**. FREE_ONLY.
