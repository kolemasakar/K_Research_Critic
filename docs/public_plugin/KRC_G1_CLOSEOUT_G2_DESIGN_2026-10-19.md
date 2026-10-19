# KRC G1 Closeout / G2 Design — 2026-10-19
Status: G1 SDK/SCHEMAS PASS; RUNTIME CODE PROVENANCE PARTIAL; G2 DESIGN ONLY.

## Observed
- RDC krc-cobalt under krcops; krc-public-mcp.service active (PID 82373).
- SDK streamable-HTTP initialize PASS protocol 2025-11-25; tools/list PASS, seven schemas.
- SHA256 on-disk server.py: 7fc66008429682f87dc04d2c6f1138b55e4a667ed5124a4c7f1b91a013db5c54; file mtime matches process-start second, but no Git checkout and no privileged live-code attestation; loaded bytecode parity cannot be proved read-only.
- /proc process fd denied to krcops. Do not infer that disk SHA equals running code SHA.
- Systemd: restricted krcmcp user; localhost:9013, CPU 50%, RAM 192M, tasks 32, ProtectSystem=strict, NoNewPrivileges.
- Existing research validation limited to CriticProfile risk floors, asserted-origin deduplication and report structure; no internet fact checking.
- FIFO queue=256, ten-hour expiry, >=10% disk free guard, bounded doc/chunk/payload and in-process rate limits.
- Production unchanged, no media started.

## G2 proposed minimal useful MCP (no deploy yet)
1. ChatGPT handles research, sources, citations, approval gating and critique. MCP provides strictly deterministic validation; never claims to establish truth.
2. Prefer just three bounded tools for public review: research_profile_validate; claim_evidence_audit; research_report_validate. Retain job/guest/upload tools only if validated as necessary for the end-user flow.
3. Preserve no KRC login, FREE_ONLY, no MEDIA, no remote paid providers. Data minimization; no payload or guest-token logs.
4. Before publication review TLS public endpoint separately from Cobalt, request limits and reverse-proxy rate controls, Origin/Host checks, abuse risks, queue exhaustion, sensitive payload handling, state cleanup, SSRF/no external fetching.
5. Keep PRIVATE NO_MCP 0.19.8 intact. Create separate With MCP publication package, 5 positive and 3 negative cases, user-access trial only after approval.
6. Verify live code provenance with authorized deployment manifest or controlled service restart in a distinct approved phase, not by speculative parity assumptions.

## Status
G1 critical protocol controls PASS; loaded-code provenance recorded PARTIAL.
G2 design drafted; no authorization for external endpoint, config changes or submission.