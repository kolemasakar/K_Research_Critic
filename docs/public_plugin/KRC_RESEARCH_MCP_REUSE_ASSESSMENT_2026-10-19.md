# KRC Research MCP Reuse Assessment — 2026-10-19
Decision: REUSE WITH GATES. No production change.

## Live evidence
- Inspected /opt/krc-public-mcp/server.py and deploy/Caddyfile.review-only on krc-cobalt through authorized RDC as krcops.
- Existing MCP streamable HTTP initialize/tools-list protocol PASS from preceding live audit; seven tools; only loopback:9013.
- Existing functional tools: guest_session, research_submit, research_status, research_document_upload, research_profile_validate, claim_evidence_audit, research_report_validate.
- Guest capability created with secrets.token_urlsafe(32); owner stored as token digest. Job IDs are uuid4 hex. SQL uses parameterized queries.
- Queue FIFO max 256; 10-hour result/document expiry; disk reserve at least 10%; 16 MiB document, 160 KiB chunks, 256 KiB payload; in-process per-guest/global rate limits.
- Systemd sandbox uses dedicated krcmcp, ProtectSystem=strict, NoNewPrivileges, CPU 50%, MemoryMax 192M.
- Proposed Caddy path /krc-public/mcp strips prefix to localhost 9013, but this is a commented review-only file and not installed.

## Reuse verdict
Reusable now as an isolated internal deterministic validation backend; NOT yet approved as public internet-facing MCP.
Provides meaningful but narrowly scoped deterministic profile checks, identifier de-duplication and report structure; no independent source verification or general web research. Core Skill and ChatGPT own fact checking and critique.
No need for new VM, paid services, media pipelines or wholesale rewrite.

## Required before public routing
1. Test security and auth-free abuse posture; proxy-wide rate limits and body/request/concurrency ceilings; Host/Origin, CORS/session and TLS tests.
2. Assess privacy implications of queued research payloads and document uploads; restrict logging; 10-hour retention; verify cleanup and disk consumption on multi-user load.
3. Check error handling, queue exhaustion, restart semantics, state limits and redirection/path routing; run isolated tests, not public production jobs.
4. Attest deployed runtime code via authorized controlled deployment SHA/restart or immutable release evidence; disk hash alone insufficient.
5. Prepare independent With MCP plugin submission, five positive and three negative end-to-end cases, release/demo video, website/support/privacy/terms; verify Plus user installation post-review.
6. Preserve private NO_MCP 0.19.8 and all MEDIA systems; FREE_ONLY. Owner approval required before proxy/network changes.

## Observation cautions
Rate limiter is Python in-memory and resets on restart; not a substitute for ingress protection.
Unexpired queued jobs intentionally have no time deadline; potential resource starvation must be bounded by max queue and public controls.
Claim-origin equality check is syntactic, not actual evidence independence.
Request tool schema and SDK initialization PASS; complete tool workflows have not been re-run in this audit.