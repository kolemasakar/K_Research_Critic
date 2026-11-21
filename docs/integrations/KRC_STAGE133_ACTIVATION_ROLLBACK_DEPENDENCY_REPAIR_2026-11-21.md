# Stage133 live activation / Stage127 dependency failure and operator fix
Date: 2026-11-21. STAGING ONLY. LIVE STAGE133 NOT ACCEPTED. SCIENCE NO_SEND.

## Observed actual state
The user (root SSH operator) installed the operator script from KRC PR35 as /var/backups/krc-stage133-operator-20261121.sh with root:root 0600 and invoked stage (PASS):
- Archive manifest PASS.
- Broker imported as UID1002, default-off PASS.
- Gateway imported as UID988, default-off PASS.
- STAGE133_ROOT_STAGED_DEFAULT_OFF_NO_SERVICE_CHANGE_PASS.

The user next explicitly activated Stage133. Two in-role checks succeeded:
- BROKER_UID1002_STAGE133_OPTIN_PASS
- GATEWAY_UID988_STAGE133_OPTIN_PASS
Then the operator printed STAGE133_ACTIVATION_FAILED_CODE=3 and initiated STAGE133_ROLLBACK_BEGIN. Its GET401 recovery probe failed repeatedly with curl connection refused (port 19017).

Independent read-only inspection of the host established:
- Stage132 broker and gateway unit contents are restored to the exact old source/command and both services ACTIVE (new PIDs 19171 and 19181).
- Artifact reader ACTIVE (PID5267), no restart.
- Stage127 Sentinel INACTIVE/dead (MainPID0, ExecMainStatus15 SIGTERM, Result=success). Port 19017 is unreachable.
- Stage133 immutable files remain under /opt/krc-stage133-offline/<SHA>, but current live Stage132 units no longer request Stage133.
- Stage127 actual unit: Requires=tailscaled.service krc-research-v2.service and After=... krc-research-v2.service; Restart=on-failure. Stopping gateway during Stage133 switching caused dependent Stage127 stop. A normal SIGTERM stop is not a failure, so systemd does not restart Sentinel just because gateway subsequently restarts.
- Therefore the original operator performed incomplete dependency recovery: it assumed Sentinel would remain active / independently restart, then read_health returned code 3 and subsequent wait_ingress_401 could never pass.
- Existing release did not modify nonce or science grant files. No new Science E2E observed. The earlier activation-success marker may still exist under root-owned BACK because rollback failed before cleanup; only the recover phase checks and cleans this up.

## Operator script fix (root-controlled, source-only until installed)
tools/stage133_root_operator_20261121.sh updated to:
1. restore_transport() checks whether krc-sentinel-stage127 is active, explicitly starts it after gateway if necessary, and requires an active result.
2. Activation and rollback both call restore_transport before final read_health and GET401 ingress smoke. Rollback continues to restore exact original units, not leave Stage133 enabled.
3. New non-disruptive recover phase for this specific partially completed rollback: checks exact old systemd unit hashes + root backup parity, Stage133 marker absent, broker/gateway/reader active, staged-release integrity, restarts Sentinel only if inactive, confirms all four active and external negative GET401, moves stale activated marker to a preserved first-attempt record and marks recovered. It does not stop or restart any KRC scientific service.
4. Release tar and live service paths unchanged. No bypass of UID/ACL, HMAC, consent, or Stage133 install gate.

Static acceptance: Bash parse PASS; extracted allowlisted immutable package 16 files PASS; exact file parity PASS; dependency assertions for Sentinel in activation/rollback/recover PASS. Actual root recover and independent cross-UID Stage133 E2E still NOT_RUN.

## Required operator actions (SSH with root via sudo)
Before continuing deployment restore Stage127 immediately:
  sudo systemctl start krc-sentinel-stage127.service

The updated operator script must be copied from pinned KRC source onto root-owned operator location, with SHA256 verified against checkpoint after final source hash is recorded. Preserve original failed version in root-only backups if available.

Then perform recovery:
  sudo bash /var/backups/krc-stage133-operator-20261121.sh recover

Only after STAGE133_RECOVERY_STAGE132_FOUR_SERVICES_AND_GET401_PASS (and checked runtime status) can a subsequent separately operator-approved activate be attempted. No automatic retry; NO_SEND throughout. If recovery fails, leave Stage132 unchanged and collect error text.

## Scientific / production impact
Two internal Python opt-in allowlist checks PASS; this does not establish installed cross-UID relay acceptance. K_Sentinel role remains transparent transport only. External research operation E2E count unchanged at 2/48. Production NO-GO.
