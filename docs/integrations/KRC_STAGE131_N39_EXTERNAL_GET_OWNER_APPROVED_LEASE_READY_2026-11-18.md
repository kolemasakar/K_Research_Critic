# Stage127 external GET: owner approval and joint activation preparation
Date: 2026-11-18
Disposition: OWNER TEMPORARY STAGING ACTIVATION APPROVED / TEST WORKFLOW PR OPEN /
ROOT LEASE SCRIPT STAGED / GET OFF / EXTERNAL 0/40 / PRODUCTION NO-GO.

The owner explicitly approved steps 1-5 including temporary activation and
subsequent disablement in the KRC project chat. Do not request another
human activation approval for this same test scope. No real research,
provider call, identity changes or production authorization.

## Actual baseline and evidence
- KRC installed pin 46aebfcd52117d564624fd708709a097bb533362, Sentinel
  installed pin 963540fe08055b65f0b25a5a6484a61712c282f8, prior internal
  smoke PASS. New read unit inactive / socket absent. Stage127 PID157909,
  Stage131 PID46327, Research v2 PID37979 unchanged.
- Actual local GET/HEAD/POST disabled endpoint HTTP404 all observed using
  candidate Science probe (not external ephemeral runner N01 evidence).
- Authoritative read-only descriptor from already approved technical
  fixture KS-b190d3c43f52c07516170ecebbcd7641: size398, SHA256
  840fcb4faf75519d8a55b0569720e9912d35d969c6ea2165b82086d66225042e;
  TTL valid. Actual installed KRC producer spool passed exact Science
  file receiver and candidate schema checks, local only. No new dispatch.
- Existing approved workflow on Science main ed34dccabe36d611ce35df74b8b27cb7e28f311a
  has POST probes only. New branch test/stage127-external-get-20261118,
  head adb7c00d583be892c5912eae1c13e0ebecbe1c73; Science PR #8 to main.
  Existing exact workflow name/path and main-ref OIDC policy retained;
  new manually dispatched choice none (default), disabled, enabled.
  All previous POST inputs remain; no concurrent flags in GET mode.
  Four independently accepted Science consumer/schema files copied from
  aaa6152504bc1c84840ea27a4203279202b3e9f8; probe uses independently retained
  authoritative descriptor. Syntax/YAML/schema, prior T4 condition,
  actual local file receiver and disabled probes all PASS.
- Planned genuine runner subset: N01 disabled; N02 missing bearer,
  N04 tampered JWT signature, N06 bad audience, N09 same jti immediate,
  N11/12/13 ignored overrides, N14/15/16/17 selectors, N19 unknown
  selector (not distinct actual other request), N34 bounded rate test,
  N35 fresh jti, N38 methods, baseline receiver 200.
  No claim of all 40: e.g. restart replay, expired/revoked synthetic
  distinct fixture, failure paths and real receiver/transport audit
  still require partner evidence. Isolated tests from prior pins do
  not count as completed external cases.
- Science PR #8 requires independent source review and merge to main
  before dispatch; OIDC rejects different workflow/ref. GitHub connector
  here supports rerun of existing jobs, not new workflow_dispatch
  with inputs. It cannot launch this new workflow; use authorized
  Science workflow dispatch UI or independently enabled action.
  Do not open GET before disabled external run and enabled runner ready.

## Root-only temporary lease (staged, NOT executed)
Path /home/krcops/krc-project-n39-read-release-20261118/operator_project_get_lease.sh
Source cc26412f3993ef53910246a5bb185b5d4ced4a8d, blob
fb7c19089bff22121ee03603f528fcf1431e5a1b, SHA256
a609825126fe0a444dabd6a193e2064ab65f46e4107b5959cba8c83bbf74c89e.
Bash syntax, embedded Python compile (previous revision), UID1002
refusal77 and systemd-run/flock availability checked. Final root
activation and rollback timer not exercised. Connector denies sudo.
No activation yet. Do not bypass root-only boundary.

After Science PR #8 reviewed/merged and disabled external probe success,
operator runs root-held hash-verified script:
```bash
sudo install -o root -g root -m 0600 \
 /home/krcops/krc-project-n39-read-release-20261118/operator_project_get_lease.sh \
 /var/backups/krc-stage127-get-lease.sh &&
echo 'a609825126fe0a444dabd6a193e2064ab65f46e4107b5959cba8c83bbf74c89e  /var/backups/krc-stage127-get-lease.sh' |
 sudo sha256sum -c - &&
sudo bash /var/backups/krc-stage127-get-lease.sh on
```
Script preflights installed pins/modes/GET OFF, saves exact original
config privately, arms root transient systemd rollback timer BEFORE
starting only restricted read UDS and changing only GET flag,
restarts only Stage127, requires real local no-bearer401. Expected
STAGING_GET_ON_LEASE_20MIN and NO_BEARER_401_PASS. Immediate rollback
on error; timer fallback on normal host uptime. Transient timer
does not survive a host reboot; no guarantee of automatic config
restoration across reboot. New read unit is not autostarted, and
enabled Sentinel requires this socket. After interruption/reboot,
operator must explicitly restore off, not restart GET blindly.
No external test window until actual operator success.

Dispatch enabled mode exclusively in exact Science main workflow.
Collect actual run/job IDs and status, recipient SHA and server audit
correlation. Coordinate remaining N01-N40 evidence; no live artifact
mutation or unauthorized science execution. Close immediately after
run (or on failure) with:
```bash
sudo bash /var/backups/krc-stage127-get-lease.sh off
```
Expected STAGING_GET_OFF_VERIFIED. Restores exact pre-lease config and
mode, restarts Stage127 only if required, stops read unit/removes
marker, verifies 404 and original services. Preserves key, nonce,
audit and producer. If rollback cannot verify 404, stop Sentinel
rather than leave GET exposed; report failure. Do not blindly rerun
on after a lease closes; one lease directory per reviewed test.

Then independent KRC/Sentinel/Science post-off checks, POST T3 real
regression, dispositions for each N01-N40 and receiver ACK/MISMATCH.
External 0/40 until actual per-case independent acceptance. Recurring
audit publication separately pending. No production activation.
