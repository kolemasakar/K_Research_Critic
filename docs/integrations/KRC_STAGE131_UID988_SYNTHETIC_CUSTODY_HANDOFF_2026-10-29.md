# KRC Stage131 — scoped UID988 configuration and secret custody, 2026-10-29

**STAGING ONLY / FREE_ONLY / PRODUCTION NO-GO**

## Contract verified
- `staging_entrypoint131.load_stage131_config` requires a regular owned-by-service-UID configuration mode0600, exact fields, socket `/run/krc-stage131/backend.sock`, state `/var/lib/krc-stage131`, distinct `peer_uid`, and paths for two dedicated secrets directly under `/etc/krc-stage131`. The signing flag **must be false**.
- `staging_entrypoint124.secret` requires owner == effective service UID, a regular file with no group/other mode bits, and at least 32 key bytes.
- Review-only unit runs as UID `krcresearch` (observed UID988), group `krc-sentinel-ipc` (GID984). Shared UID988 with Stage126 weakens process-identity separation. Dedicated UID for Stage131 would require changing and re-reviewing the operator design; **no claim of hard inter-service UID isolation**.
- `/etc/krc-stage131` must be service-UID-owned mode0700 (the preinstall metadata audit checks this), runtime /run/krc-stage131 UID988 mode0750, state /var/lib/krc-stage131 UID988 mode0700. Config and two key paths are mode0600. UID988 ownership is required by current code, not just root ownership.

## Test evidence
Synthetic test file `tests/test_stage131_synthetic_secret_custody.py` uses only in-memory/test temporary dummy values. Confirmed secret mode0600 permits read; group-readable mode0640 denied; absent file denied; signing=true denied; config mode0644 denied. Combined synthetic/preinstall/runtime tests **6/6 PASS** in 0.70s, on krc-cobalt unprivileged checkout.
The prior actual read-only preinstall probe yielded six `NOT_READY` paths, deliberately exit2. This is **not** real UID988 secret access attestation.

## Secure operator handoff — review only
1. Obtain a reviewed immutable release SHA and separate Stage131-only secret material via operator-approved secure channel; do not reuse Stage126 transport keys or copy them through GitHub.
2. Provision dedicated staging directories and owner-private config/secrets as privileged admin **only after approval**; no command that prints secret contents or includes key bytes in shell history. Ensure config values bind specifically to canonical Sentinel Stage127 identities and allowlist.
3. With controlled authorization, independently confirm effective UID988 `stat` plus file access without displaying bytes, followed by read-only config validation. Do not start a process that serves requests at this gate.
4. Recheck risk: shared service UID988 can access Stage126-owned files despite distinct filesystem paths. Consider dedicated `krcstage131` UID and group-access socket ACL, or formally accept limitation; do not pretend file modes alone solve UID isolation.
5. Check T4 Sentinel evidence, OIDC/replay and real consent separately, and require rollback acceptance before any Stage131 start.

No privileged filesystem changes, no real secrets created, no new port, no service restart/enable, no owner grant or scientific E2E.
