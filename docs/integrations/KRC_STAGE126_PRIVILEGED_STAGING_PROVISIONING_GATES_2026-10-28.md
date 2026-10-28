# KRC staging v2 — guarded provisioning checklist (NOT an executable installer)

## Verified before activation
- A dedicated `krcresearch` unprivileged account and a dedicated `krc-sentinel-ipc` group do not yet exist on krc-cobalt (read-only getent).
- Proposed `/run/krc-research-v2/backend.sock` is absent. No persistent staging service is enabled.
- Existing KRC isolation tests: 4 signed real operations via verified UDS PASS; selected artifact, quota, replay and local restart tests 33/33 PASS on 2026-10-28. This is not live Sentinel E2E.
- `gh auth status` on krc-cobalt reports no logged-in GitHub hosts; do not copy a PAT or any secret into chat.

## Privileged staging prerequisites (operator-reviewed, not yet executed)
1. Agree exact Unix username, group members and peer UID with K_Sentinel; have an authorized host administrator create a locked-down **system** account and exclusive IPC group (no login shell), recording numeric UID/GID in the deployment manifest.
2. Provision protected `/run/krc-research-v2` and `/var/lib/krc-research-v2`. The runtime parent must prevent untrusted socket replacement. Check parent path symlinks, owner, mode and effective systemd restrictions.
3. Use per-staging random transport HMAC key and science HMAC key, separately stored under `/etc/krc-research-v2`, readable only by `krcresearch` (0400/0600), never committed, transmitted in issues or printed. Provision key IDs, an allowlist for signed principal/repository/workflow, key rotation and revocation separately. The current entrypoint requires keys >=32 bytes and exact private owner.
4. Audit the non-installed `krc-research-v2.staging.service.example`: Python interpreter/dependencies, WorkingDirectory and `PYTHONPATH` must match the deployed pinned commit. The configured `Group=krc-sentinel-ipc` and `UMask=0007` aim to create 0660 socket; verify numeric GID/mode at runtime, not just unit syntax. Run under separate unprivileged identity and ensure SQLite/WAL and artifact directories are private.
5. **Before enabling**, review known blockers: 20/25s deadline and capacity, immutable artifact read vs uncooperative changes, cleanup races, fail-safe connection-abort, 200MiB limit/2GiB aggregate, TTL, error mapping, restart reconciliation and upstream OIDC claims. No automatic production cutover.

## Acceptance commands (for authorized administrator to execute independently; do not execute automatically)
- `getent passwd krcresearch`, `getent group krc-sentinel-ipc`
- `stat -c '%U %G %a %n' /run/krc-research-v2 /var/lib/krc-research-v2 /run/krc-research-v2/backend.sock`
- `systemctl status krc-research-v2.service --no-pager`, `systemctl is-enabled krc-research-v2.service`
- `ss -xl | grep /run/krc-research-v2/backend.sock`
- Review logs only with secret redaction, document service restart and socket removal without touching Stage114 v1.

## K_Science workflow
In GitHub `kolemasakar/K_Science` → **Actions** → **kscience-krc-research** → **Run workflow**, choose `main` and `probe_gateway=true`. Run this only after the approved private endpoint is active and K_Sentinel confirms connected OIDC/Tailscale signed identity. Do not run as proof of v2 while its socket is absent.

**Status:** source tests PASS / provisioning NOT DONE / live staging E2E NO-GO / production NO-GO. FREE_ONLY.
