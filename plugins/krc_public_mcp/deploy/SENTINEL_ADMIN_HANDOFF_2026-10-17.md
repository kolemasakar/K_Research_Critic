# KRC Public MCP — administrator handoff — 2026-10-17

Status: **BLOCKED / NOT INSTALLED**. Executed read-only checks on `krc-cobalt`: Desktop Commander online, `caddy` and `docker` active, `krc-public-mcp` inactive, `sudo -n true` rejected by remote command policy. No changes to the host or public routes.

## Scope
Target `krc-cobalt` exclusively. Never touch K-Trader or KGM. No upgrade, Docker restart, Caddy reload, existing route modification, broad sudo permission, or public listener.

## Approved administrator session: prerequisites
- Obtain a normal, audited admin session on `krc-cobalt` via its existing OCI management/SSH mechanism, not a privilege bypass via `krcops`.
- Inspect `id krcmcp`, `getent group krcmcp`, `systemctl status docker caddy`, `ss -ltn`, `free -m`, `df -h /opt`, `journalctl -u caddy -n 40 --no-pager`, and authorized Docker/Cobalt health. Record the baseline.
- Review source and dependency hashes, and attest the target commit before activation. SDK version pinned in README: `mcp==1.30.0`. Keep Python dependencies inside `/opt/krc-public-mcp/venv`.

## Provisioning checklist (administrator-only; not executed)
1. Create system-only identity, if absent: `useradd --system --user-group --home-dir /var/lib/krc-public-mcp --shell /usr/sbin/nologin krcmcp`. Do not add to docker/sudo groups.
2. Install approved source at `/opt/krc-public-mcp`, service code root-owned and non-writable by `krcmcp`. Place an isolated virtual environment there using a locally validated, pinned set of dependencies. Verify imports under service user.
3. Provision `/var/lib/krc-public-mcp` as `krcmcp:krcmcp` mode `0700`; ensure no other state write locations. Verify state persistence and SQLite WAL lifecycle.
4. Install the **already reviewed** unit from `plugins/krc_public_mcp/deploy/krc-public-mcp.service` to `/etc/systemd/system/krc-public-mcp.service`. Confirm the full sandbox compatibility. `systemctl daemon-reload`, then `systemctl enable --now krc-public-mcp` only after all checks.
5. Verify `systemctl show krc-public-mcp -p User -p MemoryMax -p CPUQuotaPerSecUSec -p TasksMax -p ActiveState -p NRestarts`; `ss -ltnp` must show exactly `127.0.0.1:9013` for this app. Check logs without leaking credentials.
6. Run SDK handshake/integration via loopback, Cobalt coexistence under actual concurrent load, `memory.events` / `memory.peak` / CPU throttling, restart and SQLite recovery. Record PASS/FAIL and rollback steps.
7. No `Caddyfile` installation/reload or public security list/NSG change. Perform negative external exposure checks and compare baseline Docker/Caddy/Cobalt.
8. Send final evidence to KRC, and report PASS only after every acceptance gate succeeds.

## Report to KRC
- Admin access status: blocked by Remote Desktop Commander command policy.
- User: not provisioned by Sentinel.
- Unit: inactive; not deployed.
- Cgroup limits: present in GitHub unit, not applied/tested on host.
- Caddy: active and unchanged; Docker: active and unchanged by this effort. Container application-level health not verified.
- Endpoint: no listener on `9013` in previous inspection, no public route enabled.
- Release decision: **NO-GO until administrator provisioning and constrained coexistence test**.
