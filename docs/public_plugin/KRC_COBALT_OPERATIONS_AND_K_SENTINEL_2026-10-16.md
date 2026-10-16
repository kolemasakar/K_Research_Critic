# KRC Cobalt — services and access ownership, 2026-10-16

**Owner correction:** K-Trader is separate and MUST NOT be referenced as an access or deployment dependency for KRC Cobalt. KGM VM is reserved for public KGM plugin.

**Roles**
- KRC: application code, research MCP QA, release and application operations.
- K_Sentinel: provision/manage server connectivity, service accounts, permissions and secure operator access for KRC Cobalt as a separate project; avoid relying on one tool's host roster as evidence that the VM lacks project-approved access.
- K-Trader: independent project, out of scope.

**Read-only runtime observation on krc-cobalt via authorized Desktop Commander:**
- RAM 952 MiB total / 588 MiB MemAvailable, swap 363 MiB used of 2047 MiB.
- Caddy and Docker system services active.
- Listener 127.0.0.1:9000 — Cobalt; 127.0.0.1:9012 — auxiliary P0 wake/diagnostic path (identify owning process before further claims); ports 80/443 — Caddy.
- Tailscale and Remote Desktop Commander processes present and access operational.
- Public KRC research MCP previously ran only during isolated localhost tests; no listener on staging ports 19013/19014/19015 or intended production port 9013 during post-test check. Not installed as permanent service.
- `docker ps` inaccessible to current unprivileged `krcops` terminal, so do not assert active container names/count without authorized K_Sentinel inspection.

**Next access work (for K_Sentinel):** Read-only container/status inventory; establish least-privilege dedicated `krcmcp` service identity and persistent state directory; provision reviewed systemd CPUQuota=50%, MemoryMax=192M and filesystem limitations; check runtime cgroup enforcement; approve staged routing only after abuse protections and real co-load test. No credentials in repository.

State: documentation only; existing production not changed.
