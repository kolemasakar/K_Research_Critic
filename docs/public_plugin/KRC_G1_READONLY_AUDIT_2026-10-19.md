# KRC G1 Read-Only Architecture and Protocol Audit
Date: 2026-10-19
Status: PARTIAL_PASS — protocol and schemas verified, runtime code identity not fully established

## Access/evidence
- Authorized RDC krc-cobalt device 71b80124-ac49-4899-828f-930b2249c509, local user krcops.
- Service krc-public-mcp.service ActiveState=active, MainPID=82373, ExecStart=/opt/krc-public-mcp/venv/bin/python /opt/krc-public-mcp/server.py
- Source /opt/krc-public-mcp/server.py SHA256=7fc66008429682f87dc04d2c6f1138b55e4a667ed5124a4c7f1b91a013db5c54; directory has no .git, so this hash is disk artifact evidence, not git commit hash.
- Process started 2026-10-19 13:47:13 UTC, server.py mtime 13:47:13.636 UTC; disk source and loaded bytecode equality not established merely from timestamps.
- Local handshake through official mcp Python SDK ClientSession / streamablehttp_client on 127.0.0.1:9013/mcp PASS; protocolVersion=2025-11-25; server=KRC Public Research.
- tools/list PASS; seven schemas:
 guest_session({})
 research_submit({guest_token,tool,payload,document_id?})
 research_status({guest_token,job_id,acknowledge_delivery?})
 research_document_upload({guest_token,chunk_base64,document_id?,final?})
 research_profile_validate({payload,guest_token?})
 claim_evidence_audit({payload,guest_token?})
 research_report_validate({payload,guest_token?})
- No MEDIA tools exposed by Research MCP.
- Source has one FIFO queue, MAX_QUEUE=256, TEN_HOURS=36000, MIN_FREE=.10, payload/doc limits, guest token + rate limits.
- Source code explicitly says do not expose directly to the internet before operational-controls review.

## Constraints and blockers before G2 deployment / publication
- Currently only localhost:9013 verified. No public HTTPS MCP transport/domain/TLS exposure or internet-facing abuse posture verified.
- Guest and tools return queued jobs, with result polling; test tool calls on live service could add durable jobs, so only initialize/list_tools was exercised during G1.
- Code reports ability to validate profile risk floors, deduplicate asserted evidence origins, and check structure, **not** perform web research, verify independence of source content, or factual truth. Core Skill retains responsibility for evidence and citation verification.
- Need verify process loaded-code provenance (service restart log/reproducible deployment checksum), input and SSRF/abuse review, privacy/legal URLs and portal readiness.
- Production not changed. No media processing started.

## Next G2
Define minimal useful research MCP function, preserve stateless no-user-login design where possible, and evaluate whether existing tools qualify as functional MCP utilities for ChatGPT Plus. Security threat model and 5 positive + 3 negative tests in isolated environment. Avoid Cobalt/media changes; seek separate approval for routing or production modifications.
