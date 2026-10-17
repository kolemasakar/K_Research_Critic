# Sentinel access audit — KRC Public MCP — 2026-10-17

Status: **PARTIAL / NOT DEPLOYED**. Read-only inspection only. No public endpoint activated.

## Target and execution identity
- Host: `krc-cobalt`; existing Remote Desktop Commander connection confirmed.
- Executing identity: `uid=1002(krcops)`, group `krcops`.
- SentinelX Free account: one operational slot occupied by `k-trader-prod-vnic`; `krc-cobalt` is not enrolled/operational there. No changes to that host or KGM.
- `sudo -n -l` denied by Remote Desktop Commander command policy. Docker API via `docker ps` reported `permission denied`. No authorized root provisioning available in this channel.

## Read-only observations
| Check | Observation | Gate |
|---|---|---|
| Remote connection | hostname `krc-cobalt` confirmed | PASS |
| Current identity | `krcops` | PASS |
| `krcmcp` user | `getent passwd krcmcp` yielded no entry | NOT DONE |
| App path | `/opt/krc-public-mcp` absent | NOT DONE |
| Data path | `/var/lib/krc-public-mcp` absent | NOT DONE |
| MCP service | `krc-public-mcp.service` inactive | NOT DONE |
| Port 9013 | not listening | PASS: not exposed |
| Docker service | active | PASS: baseline only |
| Caddy service | active | PASS: baseline only |
| Cobalt port | `127.0.0.1:9000` listening | PASS: baseline only |
| Disk | 37 GiB free of 45 GiB | PASS: baseline |
| RAM | 952 MiB total; 599 MiB available; swap 2 GiB | CAPACITY RISK |
| Existing caddy MemoryCurrent | 18,870,272 bytes | informational |
| Existing docker MemoryCurrent | 24,481,792 bytes | informational |

Cobalt application health, Docker container status and simultaneous load **not proven** by this audit. No post-change checks are possible because no deployment was made.

## Existing release assets
- `plugins/krc_public_mcp/deploy/krc-public-mcp.service` already sets `User=krcmcp`, `Group=krcmcp`, loopback `127.0.0.1:9013`, `MemoryMax=192M`, `CPUQuota=50%`, `Restart=on-failure`, private working directory and restrictive systemd sandbox.
- `plugins/krc_public_mcp/deploy/Caddyfile.review-only` remains intentionally **uninstalled**.
- SDK dependency `mcp==1.30.0` should be installed into a dedicated venv, not global Python.

## Required administrator provisioning and acceptance
1. Provide approved least-privilege provisioning path for `krc-cobalt` only; do not add `krcops` to Docker group or grant general sudo.
2. Confirm a baseline for Cobalt (container state/health, logs, current memory/CPU peak, Caddy config checksum and existing routes). No modifications to current Cobalt or MEDIA workload.
3. Provision system user `krcmcp` without login, application directory root-owned (service read/execute), state directory `krcmcp`-owned mode 0700, isolated Python venv. Verify source revision/hash before copying.
4. Install the reviewed systemd unit. Confirm `systemd-analyze security` when available, `systemctl show` limits, exact process identity and listening socket only on `127.0.0.1:9013`.
5. Run SDK loopback test and sustained constrained-memory coexistence test with Cobalt. Capture cgroup MemoryPeak, CPU throttling, OOM events and container health, including restart/recovery.
6. Confirm no open inbound firewall/security-list/NSG route to port 9013. Leave Caddy public route disabled pending a separate release sign-off. Recompare Cobalt/Docker/Caddy health and route checksums.
7. Record evidence, test outputs and release gate in a new deployment audit commit; declare PASS only after all gates succeed.

**Result: BLOCKED ON ADMINISTRATIVE ACCESS; NO PROD CHANGES.** FREE_ONLY preserved.
