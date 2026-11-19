#!/bin/bash
# Operator-only, bounded STAGING acceptance. No config or boot-link edits.
# Run from root-owned /var/backups copy. No automatic reboot.
set -Eeuo pipefail
umask 077
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
SELF=/var/backups/krc-n39-continuous-acceptance.sh
[[ $(id -u) = 0 ]] || { echo OPERATOR_ROOT_REQUIRED; exit 77; }
[[ "$0" = "$SELF" && $(stat -c '%u:%g:%a' "$SELF") = 0:0:600 ]]
R=krc-project-n39-read.service
S=krc-sentinel-stage127.service
L=krc-research-stage131.service
V=krc-research-v2.service
T=krc-stage127-get-lease-expiry.timer
P=/var/backups/krc-n39-continuous-acceptance-20261119
SOCK=/run/krc-project-n39-read/backend.sock
K=/opt/krc-project-n39-read/549d44868f188c6f6715bd9224c6fa4de29b05cf
D=/opt/krc-sentinel-v2/releases/stage127-get-b2a8064027c887065522b4b96f846c3d0540194f
URL=http://100.118.132.8:19017/staging/v2/artifacts/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
[[ ! -L "$P" ]]
install -d -o root -g root -m 0700 "$P"
[[ $(stat -c '%u:%g:%a' "$P") = 0:0:700 ]]
exec 9>"$P/lock"
flock -w 10 9
pid(){ systemctl show "$1" -p MainPID --value; }
restarts(){ systemctl show "$1" -p NRestarts --value; }
status(){ curl --noproxy '*' -sS -m 3 -H 'X-KRC-Request-ID: KS-00000000000000000000000000000000' -o /dev/null -w '%{http_code}' "$URL"; }
wait_active(){
 local u="$1"
 for i in {1..45}; do
   if systemctl is-active --quiet "$u"; then return 0; fi
   sleep 1
 done
 return 1
}
preflight(){
 systemctl is-active --quiet "$R"
 systemctl is-active --quiet "$S"
 systemctl is-active --quiet "$V"
 [[ $(systemctl show "$R" -p Type --value) = notify ]]
 [[ $(systemctl show "$R" -p Restart --value) = on-failure ]]
 [[ $(systemctl show "$S" -p Restart --value) = on-failure ]]
 [[ $(systemctl show "$R" -p UnitFileState --value) = enabled ]]
 [[ $(systemctl show "$S" -p UnitFileState --value) = enabled ]]
 [[ $(readlink -f /opt/krc-project-n39-read/continuous) = "$K" ]]
 [[ $(systemctl show "$S" -p WorkingDirectory --value) = "$D" ]]
 cmp -s /etc/systemd/system/krc-project-n39-read.service "$K/deploy/stage131/krc-project-n39-read-continuous.service.example"
 cmp -s /etc/systemd/system/krc-sentinel-stage127.service.d/20-artifact-get-release.conf "$D/20-artifact-get-release.conf"
 if systemctl is-active --quiet "$T"; then echo ACTIVE_LEASE_DENIED; return 1; fi
 [[ ! -e /etc/krc-project-n39-read/enable-reviewed-staging ]]
 [[ $(stat -c '%u:%g:%a' /etc/krc-project-n39-read/enable-reviewed-continuous) = 0:0:600 ]]
 [[ -S "$SOCK" && $(stat -c '%u:%g:%a' "$SOCK") = 1002:984:660 ]]
 [[ $(status) = 401 ]]
}
snapshot(){
 # Store only fingerprints and counts, never print nonce rows or secrets.
 [[ ! -e "$1" && ! -L "$1" ]]
 (set -o noclobber; runuser -u krcops -g krc-sentinel-ipc -- /usr/bin/python3 -s - > "$1" <<'PY'
import hashlib,json,sqlite3,sys
from pathlib import Path
def query(p,q):
 with sqlite3.connect(Path(p).as_uri()+"?mode=ro",uri=True,timeout=3) as c:
  assert c.execute("pragma quick_check").fetchone()[0]=="ok"
  return c.execute(q).fetchall()
rows=query("/var/lib/krc-project-n39-read/nonce.sqlite","select key_id,nonce,principal,created from used order by key_id,nonce,principal")
science=query("/home/krcops/krc-project-n39-staging/state/science-replay.sqlite","select count(*) from requests")[0][0]
# Existing nonce TTL may legitimately prune rows after new admission; no live
# signed traffic should run during this short local test.
digest=hashlib.sha256(json.dumps(rows,separators=(",",":")).encode()).hexdigest()
print(json.dumps({"nonce_count":len(rows),"nonce_sha256":digest,"science_count":science},sort_keys=True))
PY
 )
 echo NONCE_AND_SCIENCE_DB_QUICK_CHECK_PASS
}
case "${1:-}" in
crash)
 preflight
 systemctl is-active --quiet "$L"
 [[ ! -e "$P/crash-before.json" && ! -e "$P/crash-after.json" ]]
 r=$(pid "$R"); s=$(pid "$S"); l=$(pid "$L"); v=$(pid "$V"); n=$(restarts "$R")
 [[ "$r" != 0 && "$s" != 0 ]]
 snapshot "$P/crash-before.json"
 # Exactly one deliberate reader crash, no change to configured restart limit.
 systemctl kill --kill-who=main --signal=SIGKILL "$R"
 for i in {1..45}; do
   new=$(pid "$R")
   if [[ "$new" != 0 && "$new" != "$r" ]] && systemctl is-active --quiet "$R"; then break; fi
   [[ $(pid "$S") = "$s" ]] || { echo SENTINEL_PID_CHANGED; exit 1; }
   sleep 1
 done
 preflight
 [[ $(pid "$R") != "$r" && $(restarts "$R") -gt "$n" ]]
 [[ $(pid "$S") = "$s" && $(pid "$L") = "$l" && $(pid "$V") = "$v" ]]
 snapshot "$P/crash-after.json"
 cmp -s "$P/crash-before.json" "$P/crash-after.json"
 echo KRC_CRASH_AUTO_RESTART_PASS
 echo NO_BEARER_401_AND_SENTINEL_PID_STABLE
 echo NONCE_AND_SCIENCE_STATE_UNCHANGED
 ;;
boot-before)
 preflight
 systemctl is-active --quiet "$L"
 [[ ! -e "$P/boot-before.id" && ! -e "$P/boot-before.json" ]]
 cat /proc/sys/kernel/random/boot_id > "$P/boot-before.id"
 snapshot "$P/boot-before.json"
 systemctl list-jobs --no-pager
 echo BOOT_CHECKPOINT_READY
 echo STAGE131_MANUAL_ONLY_RESTORE_AFTER_REBOOT
 ;;
boot-after)
 [[ -f "$P/boot-before.id" && ! -e "$P/boot-after.json" ]]
 [[ $(cat /proc/sys/kernel/random/boot_id) != "$(cat "$P/boot-before.id")" ]]
 wait_active "$S"; wait_active "$R"; wait_active "$V"
 preflight
 snapshot "$P/boot-after.json"
 cmp -s "$P/boot-before.json" "$P/boot-after.json"
 echo CONTINUOUS_BOOT_AUTOSTART_PASS
 echo NONCE_AND_SCIENCE_STATE_UNCHANGED
 # Restore prior manually-started Stage131 only; do not enable it at boot.
 if ! systemctl is-active --quiet "$L"; then
   systemctl start "$L"
   wait_active "$L"
   echo MANUAL_STAGE131_RESTORED
 fi
 echo BOOT_LOCAL_ACCEPTANCE_PASS
 ;;
*) echo 'Usage: crash | boot-before | boot-after'; exit 64 ;;
esac
