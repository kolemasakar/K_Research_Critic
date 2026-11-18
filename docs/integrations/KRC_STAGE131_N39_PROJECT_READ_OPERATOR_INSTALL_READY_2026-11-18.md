# Project N39 restricted read: operator install and internal smoke readiness
Date: 2026-11-18
Status: STAGED AND PREFLIGHT PASS / OWNER ROOT STEP REQUIRED / GET OFF / PRODUCTION NO-GO.
Response to Sentinel KRC PR #29 comment 6990032597.

## Accepted inputs
- KRC read package pin 46aebfcd52117d564624fd708709a097bb533362 and archive
  SHA256 75895401f582d65868109a7c3d5d7510aa9303090429a1e37eb2ae6bd104795b.
- Independent Sentinel source ACK: 53 targeted tests; Science: independently
  reran 21 KRC + 3 receiver tests. No claim independent full regression.
- Stage127 source pin 963540fe08055b65f0b25a5a6484a61712c282f8 installed,
  active PID157909; independent Stage127 default-OFF and T3 report
  481ea8ecb642521f7b896ebdfb88fe52eca60b2f. Fresh local disabled GET 404.
- Existing Stage131 PID46327, Research v2 PID37979 active; new read unit
  not-found/inactive, no new service directories. Actual owner UID1002 GID1002,
  Sentinel UID987 GID984, krcresearch UID988 GID984, IPC GID984.
- Current producer state mode0700, databases mode0600. Read-only descriptor
  preflight confirms 398-byte approved technical artifact, SHA256
  840fcb4faf75519d8a55b0569720e9912d35d969c6ea2165b82086d66225042e,
  COMPLETE and associated COMPLETED consent within TTL. Logical snapshot
  read-only preflight PASS (one row in each of five relevant tables).
- /usr/bin/python3 3.12.3, jsonschema import PASS, 36 GB free.

## Staged exact package
Host krc-cobalt:
- /home/krcops/krc-project-n39-read-release-20261118/release.tar
  (412 KiB; verified hash above, 101 archive members allowlist PASS).
- /home/krcops/krc-project-n39-read-release-20261118/operator_install_project_read_default_off.sh
  Source commit 39a0ef94abf1e67ba27234c164cb10dbab40986c, blob
  f23124ed482ecf53f67ba9ff42d8a1c97f4bff4c. SHA256
  eda3ab02893e255839c11c1c14ddde530e24b5c0e016b3527e29177c9489e2da.
- bash -n PASS; six Python heredocs compile PASS; unprivileged refusal
  OPERATOR_ROOT_REQUIRED / 77 PASS. Actual root execution NOT performed.
  Connector rejects sudo; do not bypass this administrative boundary.

## Owner-only invocation
The owner requested install and internal verification, with external GET ON
only after separate approval. Run in the authorized admin SSH terminal:
```bash
sudo install -o root -g root -m 0600 \
 /home/krcops/krc-project-n39-read-release-20261118/operator_install_project_read_default_off.sh \
 /var/backups/krc-project-n39-read-install.sh &&
echo 'eda3ab02893e255839c11c1c14ddde530e24b5c0e016b3527e29177c9489e2da  /var/backups/krc-project-n39-read-install.sh' |
 sudo sha256sum -c - &&
sudo bash /var/backups/krc-project-n39-read-install.sh
```
Expected final markers KRC_READ_INSTALLED_INTERNAL_SMOKE_PASS_GET_OFF and
PRODUCTION_UNCHANGED. If any step fails, stop and report the exact output;
the script refuses preexisting release/unit/key/state paths. No blind rerun.
The new internal service is started briefly only for local smoke and then
stopped, activation marker removed; at end source/dependency, unit, key and
nonce state persist, service inactive and socket absent. No external GET ON.
Read-only scope is the previously owner-approved technical fixture only.

The script stages root-held verified archive, new immutable source and
current link, exact unit and a distinct root:984 mode0440 32-byte key;
compares against configured transport/science keys without exposing any byte.
Checks real service UID/GID/socket and read-only mounts, Sentinel UID987
actual deployed adapter signed describe/read on approved fixture, exact
SHA/length/EOF, replay403, bad MAC403, wrong scope404, real wrong UID403,
separate nonce state, no direct Sentinel filesystem read. Logical producer
snapshot, original service PIDs/config, and disabled404 must remain unchanged.
WAL/SHM sidecar behavior and systemd mount namespace not verified until
owner executes the script. No installed runtime success claimed here.
No real scientific job or provider use.

If internal smoke fails after start, EXIT trap stops only new service and
removes its marker, retains reviewed files/key/nonce for analysis. Existing
Stage127/Stage131/Research v2 untouched; external config remains OFF.
After successful root output, independently verify path/unit/hash/key modes
and inactive state, then obtain separate explicit external activation decision.
External N01-N40 still 0/40 full-pass; no 48 science E2E authorization.
