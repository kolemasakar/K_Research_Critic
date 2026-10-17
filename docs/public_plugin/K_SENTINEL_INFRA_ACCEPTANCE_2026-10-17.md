# K_Sentinel — KRC Public MCP infrastructure acceptance — 2026-10-17

**Verdict: PARTIAL / public release NO-GO until access-security gate passes.** FREE_ONLY. Read-only inspection, no Caddy/Docker/MEDIA/OCI changes.

## Evidence
- KRC report: `docs/public_plugin/KRC_COBALT_STABILITY_2026-10-17.md`: 120/120 MCP flows PASS, 10 concurrent clients × 12 rounds, 74.01 sec, MemoryPeak 43,028,480 B, 110 throttled CPU periods, 0 OOM and 0 service restarts, Cobalt 12/12 HTTP 200. Owner deferred longer soak, large documents and FIFO accumulation; these are *not release blockers by owner decision*.
- Independent read-only device check on `krc-cobalt`: systemd krc-public-mcp active, User/Group=krcmcp, MemoryMax=201326592 (192 MiB), CPUQuotaPerSecUSec=500ms (50%), TasksMax=32, NRestarts=0, MemoryPeak=43028480 (~41.03 MiB).
- Disk `/dev/sda1` available 37,959,656 KiB / total 46,212,176 KiB (~82.14% free) — 10% minimum PASS.
- Permissions: `/opt/krc-public-mcp` root:root 0755; `server.py` root:root 0644; `/var/lib/krc-public-mcp` krcmcp:krcmcp 0700. Strong separation by file permissions.
- Services docker/caddy/krc-public-mcp all active. Cobalt loopback `127.0.0.1:9000/` HTTP 200. On disk Caddyfile host `89-168-65-88.sslip.io` routes `/krc-wake/v1` -> `127.0.0.1:9012`, fallback -> `127.0.0.1:9000`; **no route to 9013**. Listening sockets include MCP `127.0.0.1:9013`, Cobalt `127.0.0.1:9000`, Caddy :80/:443. No Caddy reload or change.
- Production SQLite: access denied indirectly by directory mode to remote `krcops`. **No PRAGMA integrity_check, WAL metadata, or journald review possible from this identity.** Offline SQLite recovery/integrity PASS from earlier isolated DB tests, not production. Do not conflate.
- Active Caddy config (in-memory) and OCI ingress rules were not independently retrieved; on-disk config alone insufficient proof.
- No public path auth, rate limit, concurrency cap, request caps or ChatGPT client handshake verified. **10 simultaneously tested clients are not an enforced 10-user admission cap.** No account identity binding in guest sessions per SDK README.

## Matrix
| Criterion | Verdict |
|---|---|
| Cobalt / Docker / Caddy | PASS limited: service/HTTP health, container status from previous operator script |
| Production SQLite / WAL | PARTIAL: offline PASS, production unread |
| Service permissions / isolation | PASS for checked user and filesystem ACL; journal unread |
| CPU / RAM / disk | PASS for actual cgroup settings, observed load, free disk |
| HTTPS network infrastructure | PARTIAL: Caddy TLS listeners/on-disk routes, active route and OCI ingress not verified |
| Public access security | PARTIAL / blocking: no authenticated rate limiting or 10-user cap evidence |
| Infrastructure for initial public release | **PARTIAL / NO-GO** |

## Required final gates (within owner scope)
1. Authorized Ubuntu root read-only production SQLite check: stat `/var/lib/krc-public-mcp/queue.sqlite3{,-wal,-shm}`, `sqlite3` URI `mode=ro` with `PRAGMA integrity_check;` and `PRAGMA journal_mode;`. SQLite's `mode=ro` can still need WAL/SHM handling in some environments; prefer a consistent backup snapshot into separate private temporary storage to avoid interacting with live DB or write to it, then inspect snapshot. No destructive SQL, service restart or checkpoint.
2. Read journals and Cobalt container status from approved admin session, record critical errors and OOM cgroup counters.
3. Verify live Caddy admin config and OCI NSG/security list ingress, public TLS functioning. No existing MEDIA route modification.
4. Before public activation implement and test admission **cap 10 users**, authentication or documented bounded anonymous access, rate limits, body size bounds, abuse controls; establish ChatGPT MCP handshake and security review. Grant separate explicit public release approval.

No long soak, large-document or FIFO accumulation test required for initial limited launch per owner's decision. **This audit neither enables nor publishes HTTPS MCP endpoint.**
