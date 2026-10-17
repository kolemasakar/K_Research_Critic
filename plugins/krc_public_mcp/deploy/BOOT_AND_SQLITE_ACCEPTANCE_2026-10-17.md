# KRC Public MCP — SQLite Recovery and Boot Enable Acceptance — 2026-10-17

Owner-supplied SSH outputs from krc-cobalt:

- `SQLITE_RECOVERY=PASS` and `SQLITE_INTEGRITY=PASS` from an isolated temporary SQLite QueueStore test exercising `running → queued`, completion and `PRAGMA integrity_check`. This did NOT crash/restart the production instance.
- `sudo systemctl enable krc-public-mcp.service`: created symlink under `/etc/systemd/system/multi-user.target.wants/`.
- `systemctl is-enabled krc-public-mcp.service`: `enabled`.
- `systemctl is-active krc-public-mcp.service`: `active`.
- Existing local bind `127.0.0.1:9013`, verified SDK tests and 192 MiB RAM/50% CPU cgroup settings recorded in LOCAL_RUNTIME_ACCEPTANCE_2026-10-17.md.
- Adapted Caddyfile (owner-provided): reverse proxies `/krc-wake/v1` → `127.0.0.1:9012`, default Cobalt → `127.0.0.1:9000`; no route to `9013` in disk Caddyfile. Caddy active runtime/config divergence and OCI ingress still require separate verification.

**LOCAL DEPLOYMENT PASS**. **PUBLIC RELEASE NO-GO** pending KRC sustained simultaneous load, active Caddy/OCI ingress audit, security and rate-limit controls, and explicit release approval. Never claim full production endurance validation based on this isolated test.
