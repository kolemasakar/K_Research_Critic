# KRC Public Research MCP — SDK candidate

**Status:** Staging-tested on OCI loopback. **Not authorized for public traffic.**

This is a separate research-only MCP implementation (no media providers, no paid API), following the V5 design but using the official Python `mcp` SDK for Streamable HTTP.

## Tools

- `guest_session`: short-lived opaque guest capability. No extra end-user login.
- `research_submit`: FIFO submit for one of the three validators.
- `research_status`: queue position, result and optional delivery acknowledgment.
- `research_document_upload`: bounded base64 chunk upload to temporary server-side document.
- `research_profile_validate`, `claim_evidence_audit`, `research_report_validate`: enqueue via FIFO and return job ID and guest capability.

One background worker processes requests in arrival order. SQLite WAL persists the queue across restarts. Result retention is 10h after completion, or 10h after explicit delivery ACK. Up to 32 documents of up to 16 MiB are admitted; the oldest eligible document can be displaced. Documents linked to queued/running jobs are protected. Filesystem admission guard preserves at least 10% space for the current write, **not a global guarantee**.

## Local test on OCI Cobalt

```bash
git clone --branch agent/krc-public-media-r3-integration https://github.com/kolemasakar/K_Research_Critic.git
# SDK isolated (operator-managed Python environment recommended):
python3 -m pip install --target /tmp/krc-mcp-sdk-isolated 'mcp==1.30.0'
cd K_Research_Critic/plugins/krc_public_mcp
PYTHONPATH=/tmp/krc-mcp-sdk-isolated:. python3 -W error::ResourceWarning -m unittest -q test_server
KRC_HOST=127.0.0.1 KRC_PORT=19015 KRC_STATE=/tmp/krc-mcp-stage35/state3 PYTHONPATH=/tmp/krc-mcp-sdk-isolated python3 server.py
# another terminal:
KRC_TEST_URL=http://127.0.0.1:19015/mcp PYTHONPATH=/tmp/krc-mcp-sdk-isolated:. python3 sdk_live_test.py
```

## Known release blockers

- No verified native ChatGPT Plugin Directory MCP handshake; testing used official Python MCP SDK only.
- Current SDK version and protocol support must be aligned with production client capabilities.
- Cobalt MEDIA simultaneous peak workload, 192 MiB memory ceiling and 0.5 CPU quota not yet exercised under actual enforced cgroups.
- No Internet exposure/rate-limit/security audit; anonymous requests must not exhaust queue/disk. Token capability is not bound to ChatGPT account identity.
- Unclaimed and delivered result TTL covered by unit tests; 10-hour disk eviction and crash recovery under system pressure need longer endurance testing.
- Documents processed as UTF-8 text (report) or JSON object (other validators), not arbitrary PDF/DOCX; added document storage is not a full document parser.
- Production service account and Caddy configuration require authorized Sentinel provisioning. KRC Cobalt not currently connected to SentinelX.

Do not connect this prototype to a public Plugin Directory listing until acceptance checks pass.
