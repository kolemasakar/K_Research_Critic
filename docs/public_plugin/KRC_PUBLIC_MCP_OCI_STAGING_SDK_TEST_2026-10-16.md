# KRC Public MCP — owner-requested 1–5 execution checkpoint

Date: 2026-10-16. Status: **1–4 OCI staging PASS / 5 PREPARED, PUBLIC NOT ACTIVATED**.

## 1. Source in GitHub
Source `plugins/krc_public_mcp/server.py`; `test_server.py`; `sdk_live_test.py`, `README.md`; review-only deployment manifests under `deploy/`. All committed to `agent/krc-public-media-r3-integration`. Distinct SDK-based implementation rather than bitwise-identical import of V5 ZIP, to address incomplete custom Streamable HTTP support.

## 2. Official MCP SDK client
Installed `mcp==1.30.0` under `/tmp/krc-mcp-sdk-isolated` on OCI `krc-cobalt` (42 MiB); no system Python/site-packages alteration. The local isolated environment was used for a real `ClientSession` over streamable HTTP. `initialize`, `tools/list` (7 tools), `guest_session`, `research_submit`, `research_status` with delivery ACK all PASS. This does not establish verified compatibility with the native ChatGPT Plugins runtime or latest draft MCP protocol.

## 3. Loopback staging
GitHub branch cloned to `/tmp/krc-mcp-stage35/repo`. Candidate ran on `127.0.0.1:19015` with SQLite state in `/tmp/krc-mcp-stage35/state3`, no public exposure. Cobalt Caddy :443 and existing Cobalt :9000 unchanged.
Software fixes during iteration: no expiry of queued jobs just because they waited >10h; completed jobs expire after 10h unless delivery ACK resets 10h countdown; uploaded document content is now read for report and structured evidence validation; all named public validators submit through FIFO.

## 4. Test results
- 12/12 regression tests PASS under `python3 -W error::ResourceWarning -m unittest -q test_server`: research risk floor, evidence duplicates, report headings, FIFO, guest isolation, 10 parallel submissions, restart preservation, 10h retention, delivery ACK, doc content and cleanup, 10% disk guard.
- Official Python SDK live HTTP scenarios: 1/1 in 0.325s, 3/3 in 0.578s, 10/10 in 2.094s, all PASS. Synthetic short claims, *not* 10 heavy documents or active MEDIA concurrent processing.
- Runtime process RSS ~57,916 KiB, no enforced 192 MiB cgroup in test. OCI 952 MiB total RAM, ~552 MiB available after runs, ~37 GiB disk free of 45 GiB volume, existing Docker/Caddy active.
- Recreated Caddy preview by injecting route `/krc-public/mcp` -> loopback `9013`; `caddy adapt --adapter caddyfile` PASS, with formatting warning. **No live Caddyfile changes**.
- Test server processes shut down; no staging sockets 19013/19014/19015 or 9013 left; production :443 and :9000 remain listening; caddy/docker services active.

## 5. Release gate — HOLD
- Service account provisioning through owner-requested Sentinel control not possible yet: SentinelX lists only K-Trader as connected/operational, KGM offline; KRC Cobalt is NOT enrolled in active SentinelX host list. Free plan has 1 active host slot.
- Real systemd service, enforced CPUQuota=50%/MemoryMax=192M and real peak MEDIA co-load must be tested.
- Public unauthenticated endpoint needs abuse/rate controls and bounded resource risk beyond the 10%-free disk admission guard; guest capability is not a platform-verified ChatGPT identity.
- Native ChatGPT plugin handshake and listing review, official hosting/legal URLs remain untested.
- Caddy route is review-only; no DNS/TLS or external MCP connectivity changes authorized until gates pass.
- No paid provider or API calls.

## Safety note
`mcp==1.30.0` was installed with pip `--target` to isolated /tmp. Pip emitted conflict warnings referring to global OCI CLI dependencies, but no global packages were installed. Confirm isolation prior to production deployment.
