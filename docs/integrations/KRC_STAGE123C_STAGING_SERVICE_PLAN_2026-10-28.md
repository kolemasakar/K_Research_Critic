# KRC Stage123-C — verified UDS science composition and staging deployment gate

Status: **SOURCE READY FOR ISOLATED REVIEW / SERVICE NOT DEPLOYED / PRODUCTION NO-GO**. FREE_ONLY. No production/public/MEDIA/Stage114 v1 changes.

## New code and tests

`src/krc_research/staging_service123c.py` composes verified Stage123-B UDS peer/HMAC handler, `ResearchBoundary120`, durable SQLite `RequestLedger119`, existing persistent `ReplayRegistry` for signed science task IDs, `HardenedExchange117`, and `ScienceAdapter122` invoking the real four-operation scientific dispatcher (operation allowlist). Provider bibliography remains network-disabled unless an explicitly supplied function is configured.

`tests/test_staging_service123c.py` executes an independently signed valid profile operation through real UDS and HMAC, restarts the ephemeral server with the same SQLite state, verifies structurally identical cached response, then submits a different transport request_id with the same signed scientific task_id and confirms rejection. Focused Stage114–123C suite: **67/67 PASS (8.85s)** on isolated krc-cobalt checkout. No daemon or persistent socket installed. This single new integration test does not prove all four operations or crash consistency of external side effects.

## Staging deployment design — NOT YET AUTHORIZED / NOT EXECUTED

- Private service `krc-research-v2.service`, dedicated unprivileged OS user `krcresearch`; configure only after checking service UID/GID, allowed Sentinel peer, root directory permissions and no unrelated writers.
- Proposed UDS `/run/krc-research-v2/backend.sock` with protected parent directory and socket mode 0660, restricted group exclusively for Sentinel transport service. **No existing socket asserted.** Never bind TCP.
- Dedicated state root `/var/lib/krc-research-v2` mode 0700, KRC-owned; independent SQLite WAL ledger and signed-science replay registry; KRC artifact root with cap/quota/disk reserve. Keys and signature secrets in permissions-controlled staging credential files, not repository or journald.
- Systemd hardening proposal: `NoNewPrivileges=yes`, `ProtectSystem=strict`, `ProtectHome=yes`, `PrivateTmp=yes`, `RestrictAddressFamilies=AF_UNIX`, `ReadWritePaths` restricted to staging state and socket directories, `UMask=0077` (socket group mode must be explicitly verified; 0077 alone prevents group access), explicit restart and health check. Actual service command/config loader/socket chmod/ownership and credential ingestion still need implementation.
- **No live service until:** trusted OIDC/Tailscale verified by Sentinel, pinned UID and key rotation, finalized error schema, service entrypoint, file race/immutability proof, quota stress, all four signed science operations, 20s deadline, concurrent writer/cleanup, interrupted stream, restarted reconciliation, and rollback tests.

KRC Stage123-C is a **composition module and local restart proof**, not a complete service deployment or authenticated cross-project E2E. Sentinel PR #38 remains Draft and Stage114 v1 unchanged.