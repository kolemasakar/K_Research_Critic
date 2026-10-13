# KRC P0 — implemented, tested, disabled-by-default relay, operational checkpoint
Date 2026-10-13. Owner requested proceed without further confirmations. Scope: private FREE_ONLY, no permanent keepalive, no new paid provider jobs.

## Current state — NOT YET P0 COMPLETE
- KRC R3C source now contains feature-gated one-time external wake when a cold Cloudflare-proxied unattributed 429 is observed during readiness. It deliberately does **not** wake on explicit app upstream_code or Retry-After. Exactly one relay invocation allowed per bounded readiness cycle. After successful wake, read-only health is polled with a bounded startup window. Consequential MEDIA start is never replayed by this mechanism.
- Client module: `plugins/krc_migration_candidate/p0_wake_relay_client.py`; locally runnable standalone relay: `plugins/krc_migration_candidate/p0_wake_relay_server.py`. They reside outside protected MCP canary source tree to honor no-live-endpoint-in-canary policy.
- Relay client configuration: `KRC_WAKE_RELAY_ENABLED=1` (OFF by default), `KRC_WAKE_RELAY_URL=https://<pinned-host>/krc-wake/v1`, `KRC_WAKE_RELAY_HOST=<same-pinned-host>`, `KRC_WAKE_RELAY_TOKEN=<rotatable-token>=32 chars`. The relay accepts only exact POST body `{"action":"wake_voicebridge"}`, HTTPS via pinned host and no redirect, token header only. No MEDIA/provider calls.
- Relay server accepts only bearer auth, exact request body, fixed outbound `GET https://voicebridge-krc-media-beta-kolemasakar.onrender.com/api/v1/health`, no redirect; single wake per 90s; loopback-only listening, no arbitrary user URL, jobs, transcripts or dynamic commands. No keepalive loop.
- GitHub commits of implementation: r3c `8f069917`, relay client `34a2a261` updated `029ff8c5` to 35s timeout, relay server `43150768`, recovery tests `493457cb` updated `541e1a89`, relay-server tests `b7368ba2`.
- Exact GitHub code HEAD `541e1a89a7cc316903500c5b7cd23eafcbb76c93` tested in fresh isolated worktree: **493 passed, 17 skipped, 0 failed** (22.54s). The 17 explicitly opt-in cross-repo fixture tests subsequently **17 passed, 0 failed** (38.31s) with controlled test-only VoiceBridge compatibility overlay. No paid providers used during tests.
- Deployed R3C Render service `srv-dale3r942hec73c5t9hg`, deployment `dep-db6ujp3ncjis73etq130`, exact commit `541e1a89...` status LIVE since 2026-10-13T08:21:33.962317Z. Feature remains off (no relay endpoint/env enabled). A subsequent read-only `media_get_capabilities` when VoiceBridge cold returned 429 with CF-Ray `a49ceea19c818ebb-FRA`, expected until relay is enabled. No provider POST.
- VoiceBridge Render production unchanged.

## krc-cobalt local deployment, SECURE but NOT PUBLIC
- As user `krcops` UID 1002, source staged `/home/krcops/krc-p0-wake/relay_server.py` and protected auth env `/home/krcops/.config/krc-wake/relay.env`, mode `0600`; the bearer value was NOT displayed or sent to this document. One-time generated high-entropy token; must be securely transferred to Render when enabling, never committed to GitHub.
- systemd user service `krc-p0-wake-relay.service` enabled + ACTIVE RUNNING on loopback `127.0.0.1:9012`, via `/run/user/1002` bus; linger=yes. Bounded 64 MiB memory, 16 tasks. An initial systemd sandbox attempt failed 218/CAPABILITIES in unprivileged user manager; `PrivateDevices` and `ProtectSystem=strict` removed, after which it started. Do NOT claim those sandbox options active.
- Current root-owned Caddy still routes `89-168-65-88.sslip.io` → `127.0.0.1:9000` (Cobalt). A least-impact **proposed** route for exact `/krc-wake/v1` → `127.0.0.1:9012`, Cobalt fallback intact, was staged at `/home/krcops/krc-p0-wake/Caddyfile.proposed` and passed `caddy validate`. NOT applied to `/etc/caddy/Caddyfile`, NOT exposed to public TLS. Authorized administrator is required for review/apply/reload; do not bypass privilege controls.
- Attempted local authenticated end-to-end test was blocked by platform safety; did not retry/bypass. Unit and local HTTP mock tests are PASS. Thus relay end-to-end verification is NOT DONE; public exposure, Render-to-relay authentication and 3 independent cold tests pending.

## Render support (SENT)
- Render official support@render.com address independently verified from Render pricing FAQ. Gmail connected user account sent ticket-like email 2026-10-13, subject `Infrastructure investigation: Free-to-Free cold start HTTP 429 — CF-Ray evidence (13 Oct 2026)`. Gmail SENT, thread id `1a1345c51acb026f`. Included both failure CF-Ray `a49ccaf70d1d18cb-FRA`, `a49ccaf77d4d0d18-FRA`, source/target IDs, UTC, external successful wake contrast, and FREE_ONLY request. This is EMAIL SENT, not a confirmed official support ticket number. Response pending.
- No paid browser automation/TinyFish was used.

## Remaining P0 gates (strict order)
1. Obtain authorized Caddy administrative change for exact relay path only, with rollback of original Caddyfile; verify TLS and no unrelated route regression, auth failure 403, no new public arbitrary endpoint.
2. Validate authenticated external client request to relay from Render using securely installed env (no secret in logs), check one fixed outbound health GET, edge failure/retryAfter fail-closed. Enable `KRC_WAKE_RELAY_ENABLED` only after validated security and ownership.
3. Perform at least 3 genuine cold cycles (idle >15min, no keepalive), one user-triggered read per cycle, auto-wakeup without operator GET; capture startup latency, safe IDs, credits=0. Failed / ambiguous POST never repeated.
4. Inspect Render support response to determine 429 origin and whether infrastructure fix can supersede relay workaround.
5. After all P0 gates PASS, decide owner acceptance. Otherwise P0 PARTIAL and feature OFF.

## Render support correspondence update — 2026-10-13
- Initial support email SENT to support@render.com, Gmail thread 1a1345c51acb026f. Received a reply from Render's **AI Agent**, explaining standard Free 15-minute spin-down, Cloudflare transit and Rndr-Id tracing. The reply did NOT trace either failing CF-Ray nor establish the emitting layer of HTTP 429; attribution remains OPEN.
- An escalation requesting a HUMAN Render support engineer and direct tracing of CF-Ray a49ccaf70d1d18cb-FRA / a49ccaf77d4d0d18-FRA was sent as a reply in the same thread (Gmail SENT id 1a13460d51754ced). Awaiting human analysis.
- No Render support ticket number provided; do not claim one.

## krc-cobalt staging detail
- Enabled user systemd unit krc-p0-wake-relay.service with linger=yes; listener 127.0.0.1:9012 only, ActiveState=active, SubState=running; key/server/unit files have 0600 permissions. The relay emits no scheduled health/keepalive requests.
- User systemd sandbox PrivateDevices/ProtectSystem options caused 218/CAPABILITIES, were removed; active service retains NoNewPrivileges, PrivateTmp, RestrictAddressFamilies, UMask, MemoryMax=64M and TasksMax=16. Initial restart counter included failed configuration attempts, not evidence of ongoing failures.
- Proposed Caddy routing file /home/krcops/krc-p0-wake/Caddyfile.proposed successfully validated with caddy validate; **NOT INSTALLED**. Existing /etc/caddy/Caddyfile still forwards entire domain to Cobalt port 9000. A privileged authorized Caddy change is required; avoid editing config as unprivileged krcops or bypassing access controls.
- An attempted local secret-bearing live-test call was blocked by a safety guard; it was NOT retried. Do not mark relay authenticated E2E as verified. All offline unit/integration tests remain PASS; live gate pending.
