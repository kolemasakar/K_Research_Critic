# Continuous GET installed-code fault regression and operator acceptance
Date: 2026-11-19
Disposition: INSTALLED_CODE_TARGETED_PASS / OPERATOR_CRASH_AND_BOOT_PROCEDURE_READY / EXTERNAL_FINAL_ACCEPTANCE_PENDING.

## Actual completed KRC work
- Host krc-cobalt; installed immutable KRC 549d44868f188c6f6715bd9224c6fa4de29b05cf used directly through PYTHONPATH; no testing against a substituted checkout implementation.
- Lifecycle and joint fault tests 24/24 passed (15.29s). Repeated matrix tests with synthetic wire capture: 21/21 passed (14.55s), 23 response observations.
- KRC-owned matrix evidence, isolated real signed UDS with synthetic databases and artifacts:
  N12 400; N15/N18/N19 404; N20 missing404/conflict502; N21 410; N22/N23/N24 502; N25 stable verified spool200, next corrupted read502; N26 413 using reduced test limit; N27/N28/N29/N30 403; N39 cancel403/missing association403. Backend DB unavailable503. Descriptor/read200 hash/size correct; durable nonce restart403. Timeout503/504 assertions in descriptor client test also passed. These do not constitute live external cases.
- Actual host read-only check: existing owner-approved descriptor matches 398 bytes, exact expected retained SHA, not expired; nonce rows12 and science replay count1; both DB quick checks ok. Reader PID162911 and Sentinel PID162881 active, no failed systemd units. GET remained ON; no attempted live crash or boot in this turn.
- No new execution/provider; synthetic fixture runs offline and isolated. No original state mutation.

## Operator acceptance script
Source deploy/stage131/operator_continuous_get_acceptance.sh at b006e3940e2f6a97731a0d94ca47daa5fc6b14ef, blob 1af54a959b1a3891d060bfa689f362952a158861, SHA256 1990e8842e210c206d15c008dbb3ff66554820a8125b04f8bf7e512aef04635a.
Actual staged file /home/krcops/krc-project-n39-read-release-20261118/operator_continuous_get_acceptance.sh. SHA, bash -n, three embedded Python compiles, unprivileged refusal77, live read-only snapshot and authoritative descriptor verification PASS. Actual host supports --kill-whom=main. Privileged action not yet tested. Use root-owned hash-verified copy, no alternative auth or privilege bypass.

- crash: preflight exact units/paths, active services, marker and boot links, no lease; actual approved technical file signed read as UID987, SHA/size200; root-only short-lived signed envelope never logged; snapshot nonce registry and science dispatch count; issue exactly one SIGKILL to reader main process, wait bounded 45s for systemd auto-restart; verify new PID and NRestarts, unchanged Sentinel/Stage131/Research v2 PIDs, GET401 and socket custody; compare nonce digest and science count across restart, actual same signed message403 then fresh signed read200 SHA. No config edits, no reboot, root-only replay message removed on exit. If test fails, stop progression and inspect service; do not repeatedly kill or reset start limits.
- boot-before: preflight, retain old actual kernel boot_id and nonce digest/science count; no reboot automatic. Avoid other signed traffic between checkpoints, because legitimate nonce admission/pruning changes digest.
- boot-after: require changed kernel boot_id, automatic read/Sentinel/Research v2 activation and exact runtime checks, restore Stage131 if prior manual service is inactive, compare state fingerprint/count. Important host finding: Stage131 is intentionally static manual-only, no boot dependency. Preserve policy; restore only its pre-existing active state after reboot. No new boot link for legacy Stage131. A host reboot interrupts other services; operator action only in a maintenance window. Actual restart across kernel reboot is not yet proven.
- No external workflow during local crash and checkpoint/reboot interval. External test after both local tests.

## Exact operator commands
```bash
sudo install -o root -g root -m 0600 \
 /home/krcops/krc-project-n39-read-release-20261118/operator_continuous_get_acceptance.sh \
 /var/backups/krc-n39-continuous-acceptance.sh &&
echo '1990e8842e210c206d15c008dbb3ff66554820a8125b04f8bf7e512aef04635a  /var/backups/krc-n39-continuous-acceptance.sh' |
 sudo sha256sum -c - &&
sudo bash /var/backups/krc-n39-continuous-acceptance.sh crash
```
After PASS, execute boot-before, then operator reboot if maintenance conditions allow, then boot-after on reconnected SSH. Never blindly re-run one-shot test with existing snapshot files.

## Joint remaining evidence
Science external GET enabled run on continuous pin not yet observed at last Actions check. Current connector cannot dispatch new inputs; authorized UI runner required. Sentinel external 503/200 outage and POST concurrency correlation need coordinated runner; local direct UDS nonce test is not OIDC JTI restart or external admission proof. Last accepted external matrix 2/40 full,15 partial,23 isolated only; no artificial promotion. KRC source evidence supplied; partner review and full matrix closure remain. Continuous GET remains ON; no routine OFF, production NO-GO.
