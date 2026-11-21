# KRC Stage133 root operator stage / activate / verify / rollback readiness
Date: 2026-11-21
Scope: explicitly authorized STAGING deployment only; NO SCIENCE EXECUTION; no production approval.

## Access boundary and current result
The connected krc-cobalt Remote Desktop Commander executes as uid1002 krcops, primary gid1002. sudo commands are prohibited by the connected control policy. No root operation can be executed through this connection. SentinelX sees a connected K-Trader host, but not krc-cobalt. Attempting to bypass this boundary is not permitted.
No root installation, root marker, modified systemd units, service restart, or installed cross-UID POST/GET verification has been performed in this turn. An unprivileged current Stage127 unauthorized GET probe returned HTTP401, confirming only that its unauthenticated-denial route was reachable. Stage132 remains operational on all four services, with old PIDs and zero restarts at preflight.

## Source/packaging verification
Staged artifact:
 /home/krcops/stage133-unified-acceptance-20261121/stage133-release-candidate-20261121/stage133-offline-release.tar
 SHA256: d35541ee1f1b991354f4ddbab08f186abdfb979cc56f096c4747b65d5233bab6
 Pinned GitHub KRC Stage133 draft PR35 source. Stage134 bibliography hardening is intentionally separate and not in this release.
- Package contents 16/16 allowlisted files, exact SHA256SUMS PASS, no credentials or databases.
- Using packaged broker files over installed reader source and pinned synthetic KRC test fixtures: 60/60 PASS, no live consent.
- Existing Stage127 unauthorized GET negative probe on host Tailnet IP 100.118.132.8:19017 returned 401 before any new deployment. This is an ingress-denial smoke, NOT proof of authenticated POST/GET or science execution.
- Operator script includes a fail-closed negative HMAC probe from real UID988 (an intentionally invalid MAC must return 403 before nonce claim and scientific dispatch), SO_PEERCRED UID1002/GID984 check, and unprivileged nobody socket ACL denial. These probes are prepared but NOT yet executed with root.
- Using installed broker and gateway Python interpreters with default-off package: both imports and profile-only allowlist PASS.
- Root operator script: tools/stage133_root_operator_20261121.sh. Final staged script SHA256 c509da84bbf914b640393cd7c9398a9bf0fd763388d3682c205ed0a495d7ad40.
- Rootless validator: tools/stage133_operator_static_acceptance.py.
- Script bash -n PASS; unprivileged invocation denied with ROOT_REQUIRED PASS.
- Embedded exact allowlist extractor run independently in a user-owned throwaway directory, all 16 files match tar exactly, SHA256 checked; dir permissions 0755, file permissions 0644 PASS.
- Source regression previously 1184 PASS,17 SKIPPED,0 FAIL in both forward/reverse and in separate pytest9 environment.

## Root operator procedure (requires owner SSH/root)
Stage only:
  sudo install -o root -g root -m 0600 /home/krcops/stage133-unified-acceptance-20261121/tools/stage133_root_operator_20261121.sh /var/backups/krc-stage133-operator-20261121.sh
  sudo bash /var/backups/krc-stage133-operator-20261121.sh stage

The stage command validates pinned archive and exact pre-existing Stage132 unit hashes, snapshots original broker/gateway units under root-owned /var/backups/krc-stage133-20261121, installs the immutable root-owned release under /opt/krc-stage133-offline/<FULL_SHA>, verifies broker/gateway imports under their actual UID/GID and systemd-unit syntax, checks current live services unchanged, and does NOT activate the new operations or alter any service.

After an operator verifies stage output, controlled activation:
  sudo bash /var/backups/krc-stage133-operator-20261121.sh activate

The activate command validates baseline and installed release again, stops only KRC gateway and broker (not reader or Sentinel), installs reviewed Stage133 unit/drop-in, creates root-owned 0600 second opt-in marker, daemon-reload, starts broker then gateway, waits for their expected UID/GID/mode socket ownership, verifies running roles and kernel socket credential UID1002/GID984, tests UID988 gateway broker connectivity, rejects invalid HMAC with 403 before nonce/science dispatch, denies unrelated nobody UID at the socket ACL layer, and requires negative Stage127 GET401 health. If any command fails, the operator script attempts automatic rollback of original units and restarts both services.

Additional read-only post-activation:
  sudo bash /var/backups/krc-stage133-operator-20261121.sh verify

Manual rollback:
  sudo bash /var/backups/krc-stage133-operator-20261121.sh rollback

Rollback restores only the two exact original Stage132 service configurations, removes Stage133 marker, daemon-reloads and restarts broker and gateway. No databases, request IDs, consent records, keys or publication artifacts are modified. A failed rollback must be escalated to the operator immediately.

## Interpretation and residual gates
The root operator does NOT submit scientific jobs or consume owner grants. Its UID and socket checks are actual cross-user runtime checks only WHEN root activation is performed. It does NOT establish authenticated HMAC allow/deny for a real third-party science task, complete issued OIDC token and signed artifact E2E, or independently reviewed production acceptance. Those are separate E2E/acceptance gates.
Current outcome: rootless STATIC/PACKAGE_PRECHECK PASS, ROOT_INSTALL NOT_RUN, CROSS_UID_LIVE NOT_RUN. No claim of live Stage133 activation is authorized.
