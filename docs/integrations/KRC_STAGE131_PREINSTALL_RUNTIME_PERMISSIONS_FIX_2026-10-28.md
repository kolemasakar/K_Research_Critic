# Stage131 operator preinstall permissions correction — 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO**

## Blocking bug found and resolved in source only
The review-only systemd unit declares `RuntimeDirectoryMode=0750`, but `staging_entrypoint131._private_dir()` formerly rejected any group bit, including necessary group traversal. This made the approved sample configuration incompatible with its own boot validator.

Commit `aa0078e03ef232af44ce50a12353f81d23885d2e` makes explicit `allow_group_traverse=True` only for the socket parent runtime directory, permitting group read/traverse (0750) but rejecting group write/other; state directory remains private 0700. Commit `6a6d9c42fe76a572cd24a60da9b899c1c8e732a5` adds isolated negative mode checks. Pinned SHA tests: **18/18 PASS** for permissions, Stage131 config, consent, schemas and private GET.

## Verified prerequisites
krcresearch UID988; krcsentinel UID987; shared group krc-sentinel-ipc GID984. Stage131 unit absent, source checkout unprivileged. Existing Stage126 should not be changed. Sentinel Stage127 had FAILED status at previous observation; do not claim recovery or T4 PASS.

## Remaining operator go/no-go checklist
1. Review exact immutable release SHA and dependencies, root-owned code directory; no symlinks or mutable source execution.
2. root-controlled `/etc/krc-stage131/staging.json` and secret files mode0600 **but ensure service UID988 is permitted to read config/key files without granting other UIDs**; root ownership alone does not grant service read rights. Consent grants remain absent and signer disabled.
3. `RuntimeDirectory=krc-stage131` group GID984, mode0750, socket 0660; `StateDirectory=krc-stage131` UID988 mode0700.
4. Confirm exact expected Sentinel Stage127 peer UID987 and claim allowlist; do not expose external artifact GET without Sentinel authorization.
5. Inspect and dry-check final systemd unit and config as operator, no auto-enable; do not start until Sentinel incident and security review are resolved.
6. Preserve Stage126/114/legacy ports, replay ledgers, service units and secrets.

No service install/start, owner grant, external GET or scientific E2E performed.
