# KRC Public MCP — observed local runtime acceptance — 2026-10-17

Status: **LOCAL_RUNTIME_PASS / FINAL_RELEASE_PARTIAL**.

Evidence: manual SSH session from owner on OCI `krc-cobalt`, 2026-10-17 UTC. This record contains only operator-returned outputs, not an independent performance benchmark.

- Service: `krc-public-mcp.service` active; main runtime on `127.0.0.1:9013`; running as `krcmcp`; `NRestarts=0`.
- SDK version `mcp==1.30.0`. Python unit tests: 12/12 passed.
- Official SDK live checks: concurrency 1/3/10; success 1/1, 3/3, 10/10, respectively; SDK discovered 7 tools. Times: 0.381s, 0.701s, 2.119s.
- cgroup: `MemoryMax=201326592` bytes (192 MiB), `CPUQuotaPerSecUSec=500ms` (50%), `TasksMax=32`. `MemoryCurrent=42307584` (40.35 MiB), `MemoryPeak=42868736` (40.88 MiB). Enforcement settings confirmed; full CPU saturation/OOM behavior not exercised.
- Cobalt: `krc-tier1-media-status` returned `tier1_backend_status=PASS`, backend running, no restarts, binding loopback port 9000; Docker active; Caddy active. Loopback-only listeners confirmed `127.0.0.1:9000` and `127.0.0.1:9013`.
- `Caddyfile.review-only` not installed; dedicated public route not activated. Public Caddy traffic mapping and OCI ingress rules not independently audited.
- Systemd unit loaded but was reported `disabled` after manual start; persistent boot-enable deliberately withheld until extended validation.

Still required before FULL PASS:
1. Sustained simultaneous load including Cobalt workload, cgroup memory/CPU measurements and service health.
2. SQLite queue restart/crash-recovery and retention tests on persistent data.
3. Confirm Caddy routing + upstream external reachability denial for MCP; external firewall/OCI ingress examination.
4. Decide and test safe persistent enablement; document rollback.
5. Separate authorization for public endpoint after abuse/rate limiting and MCP client acceptance.

No claim of production/public readiness. K-Trader and KGM out of scope.
