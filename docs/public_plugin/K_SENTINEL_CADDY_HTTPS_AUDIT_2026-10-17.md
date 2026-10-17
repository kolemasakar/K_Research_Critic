# Sentinel KRC HTTPS/Caddy read-only audit — 2026-10-17

Target: OCI krc-cobalt; FREE_ONLY; no configuration changes.

Checks through Remote Desktop Commander:
- systemctl is-active caddy/docker/krc-public-mcp: all active.
- listeners: Caddy :80/:443, MCP 127.0.0.1:9013, Cobalt 127.0.0.1:9000, wake 127.0.0.1:9012.
- HTTPS https://89-168-65-88.sslip.io/ returned HTTP/2 200; curl performed from VM (not independently external).
- /krc-wake/v1: HEAD 501 and GET 405, showing path routed, but endpoint method semantics untested.
- /krc-public/mcp: GET 302 from existing Cobalt fallback, **not** proof of MCP public availability.
- /etc/caddy/Caddyfile: wake path to 9012, fallback to 9000; no 9013 upstream in file. Earlier active Caddy API audit also no 9013 upstream.
- OCI ingress rules NOT inspected: no authorized OCI console/API connector for this check. Need owner to inspect security lists and NSGs for VNIC and screenshot/output, including TCP 80/443 and potential unintended TCP 9013 exposure. Also inspect IPv6 if configured.
- External independent TLS/public reachability NOT tested beyond VM's own HTTPS request.
- NO-GO for enabling MCP public route until 10-user admission enforcement, rate limiting, request-size limits, relevant abuse/security gates, and explicit owner release authorization.

Verdict: Caddy/TLS internal path PASS; overall external network gate PARTIAL. All MEDIA/Caddy/MCP configs unchanged.
