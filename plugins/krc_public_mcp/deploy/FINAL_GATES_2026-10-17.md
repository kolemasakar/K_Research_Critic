# KRC Public MCP — remaining acceptance tasks (2026-10-17)

Owner delegated sustained coexistence stress test to KRC (not Sentinel). Run long-duration MCP/Cobalt concurrent loads without changing live MEDIA/Docker/Caddy; collect cgroups memory peak/events, CPU throttling, FIFO/TTL/WAL correctness and service restart counts, then report PASS/FAIL.

Sentinel read-only follow-up:
- Remote Desktop Commander: krc-cobalt online.
- `systemctl is-active krc-public-mcp caddy docker`: active active active.
- `systemctl is-enabled krc-public-mcp`: disabled (persistent boot start NOT configured).
- `ss -ltn`: MCP bound `127.0.0.1:9013`; Cobalt `127.0.0.1:9000`; Caddy public `*:80`, `*:443`.
- `GET http://127.0.0.1:9013/mcp` without MCP Accept headers yielded 406 (not a health failure; earlier SDK session tests passed).
- server.py includes SQLite WAL (`PRAGMA journal_mode=WAL`), and on Store initialization updates jobs from running to queued. This is code evidence only, NOT restart/recovery validation.

Still blocked for administrator-only verification:
1. Copy SQLite database with `sqlite3.Connection.backup()` into isolated temp path, run integrity check and rehearse restart/requeue on a separate test process and port/state directory. Do not restart live service or mutate live queue.
2. Read `/etc/caddy/Caddyfile` and active Caddy routing (admin access) without changing it; test public URL and OCI ingress. A loopback listener alone does not prove absence of a reverse proxy route.
3. After (1) and (2) PASS, `sudo systemctl enable krc-public-mcp.service` (no restart), verify enabled and running. Reconfirm Cobalt status. Enablement authorization was given, conditioned on checks passing.

No administrative changes to service made by Sentinel in this step. No public route authorized. FINAL status PARTIAL.
