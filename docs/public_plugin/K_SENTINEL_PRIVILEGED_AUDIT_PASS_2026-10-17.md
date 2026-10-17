# KRC Public MCP — privileged read-only audit (2026-10-17)

Evidence: owner ran `/usr/local/sbin/krc-sentinel-inspect` as `sudo` on `krc-cobalt`.

- MCP active, user/group krcmcp, MemoryMax 201326592 B, CPU quota 500ms/sec, TasksMax 32, NRestarts 0, MemoryPeak 43028480 B.
- Docker and Caddy active; Cobalt backend running, restarts 0, HTTP 200, loopback 9000.
- Code `/opt/krc-public-mcp` root:root mode 755; state `/var/lib/krc-public-mcp` UID 994/GID 987 mode 700; SQLite DB UID 994/GID 987 mode 600.
- Online read-only SQLite snapshot: PRAGMA integrity_check = ok; source journal_mode = wal; WAL file present.
- Disk free 82.14% (>10%).
- journalctl error counts for MCP/Caddy/Docker = 0 for the script's 1h window (summary count only).
- Active Caddy admin API accessible: reverse proxy to 9000 found, no literal 127.0.0.1:9013 in active routes. This does not replace external network/OCI ingress review.
- Public release NOT authorized until explicit max-10-user admission/rate limit and external reachability/security checks. Owner deliberately postponed long soak, large document and FIFO accumulation tests.

**Infrastructure local health PASS. Public exposure NO-GO pending security gates.**
