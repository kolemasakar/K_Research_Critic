#!/bin/bash
# REVIEW ONLY. Joint STAGING candidate. Use a root-held hash-verified copy.
# stage: immutable files only, may run during temporary lease.
# switch: after lease closure and joint release approval; GET stays OFF.
# on: after default-off POST acceptance, exercises real local outage/recovery.
# rollback: restore exact prior units/config and OFF, preserve producer/keys/nonce.
set -Eeuo pipefail
umask 077
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
cd /
[[ $(id -u) = 0 ]] || { echo OPERATOR_ROOT_REQUIRED; exit 77; }
SELF=/var/backups/krc-n39-continuous.sh
[[ "$0" = "$SELF" && $(stat -c '%u:%a' "$SELF") = 0:600 ]]
MODE=${1:-}
KPIN=549d44868f188c6f6715bd9224c6fa4de29b05cf
SPIN=b2a8064027c887065522b4b96f846c3d0540194f
KBASE=/opt/krc-project-n39-read
KREL=$KBASE/$KPIN
SBASE=/opt/krc-sentinel-v2/releases
SREL=$SBASE/stage127-get-$SPIN
OLDK=$KBASE/46aebfcd52117d564624fd708709a097bb533362
OLDS=$SBASE/stage127-get-963540fe08055b65f0b25a5a6484a61712c282f8
B=/var/backups/krc-n39-continuous-20261118
KUNIT=/etc/systemd/system/krc-project-n39-read.service
SUNIT=/etc/systemd/system/krc-sentinel-stage127.service
DROP=$SUNIT.d/20-artifact-get-release.conf
RECOVERY=$SUNIT.d/10-bounded-recovery.conf
CONF=/etc/krc-sentinel-v2/stage127.json
READ=krc-project-n39-read.service
SENT=krc-sentinel-stage127.service
MARKER=/etc/krc-project-n39-read/enable-reviewed-continuous
TEMP=/etc/krc-project-n39-read/enable-reviewed-staging
SOCK=/run/krc-project-n39-read/backend.sock
WANTS=/etc/systemd/system/multi-user.target.wants
PY=/opt/krc-sentinel-v2/venv/bin/python
URL=http://100.118.132.8:19017/staging/v2/artifacts/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
KSH=b2d993847b103561323e914ecb1a08ca96f762be77b9af1ebf924e6cb09edbae
SSHASH=97318fb098a8b683e68ea938eda58594dc957b630c60a8e19117ada378618e55
LOCKDIR=/run/krc-n39-continuous-lock
[[ ! -L "$LOCKDIR" ]]
install -d -o root -g root -m 0700 "$LOCKDIR"
[[ $(stat -c '%u:%g:%a' "$LOCKDIR") = 0:0:700 ]]
exec 9>"$LOCKDIR/lock"
flock -w 60 9
hash_eq(){ echo "$1  $2" | sha256sum -c -; }
safe_tree(){
 [[ -d "$1" && ! -L "$1" ]]
 [[ -z $(find "$1" ! -user root -o ! -group root) ]]
 [[ -z $(find "$1" -perm /022 -o -type l) ]]
}
status(){ curl --noproxy '*' -sS -m 5 -H 'X-KRC-Request-ID: KS-00000000000000000000000000000000' -o /dev/null -w '%{http_code}' "$URL"; }
wait_status(){
 local v
 for i in {1..25}; do v=$(status 2>/dev/null || true); [[ "$v" = "$1" ]] && return 0; sleep .4; done
 return 1
}
flag(){
 runuser -u krcsentinel -g krc-sentinel-ipc -- env PYTHONPATH="$1:$KREL/src" PYTHONNOUSERSITE=1 "$PY" -s -c 'import sys;from stage127_ingress_entrypoint import load_config;assert load_config(sys.argv[1])["artifact_get_enabled"] is (sys.argv[2]=="on")' "$CONF" "$2"
}
no_lease(){
 ! systemctl is-active --quiet krc-stage127-get-lease-expiry.timer
 ! systemctl is-active --quiet krc-stage127-get-lease-expiry.service
 [[ ! -e "$TEMP" ]]
}
atomic_config(){
 local tmp
 tmp=$(mktemp /etc/krc-sentinel-v2/.continuous-XXXXXX) || return 1
 install -o 987 -g 984 -m "$(cat "$B/config-mode")" "$1" "$tmp" || { rm -f "$tmp"; return 1; }
 mv -T "$tmp" "$CONF" || { rm -f "$tmp"; return 1; }
}
verify_baseline_units(){
 hash_eq ec212137efb8801f6ca8df19ec9805f3bcbd9be77990cfe912c4d3efa4b56f44 "$SUNIT"
 hash_eq 8e6cc4b2ba1fd324c301d66fb1b6c79f4790bdb280b864e4bce485a33dabf5d6 "$RECOVERY"
}
verify_staged(){
 [[ -f "$B/staged" ]]
 hash_eq "$KSH" "$B/krc.tar"
 hash_eq "$SSHASH" "$B/sentinel.tar"
 safe_tree "$KREL"; safe_tree "$SREL"
 hash_eq b1965cc2a05da77b9e69e3b328854242398e19127975d8af7937c77ad757dd99 "$KREL/src/krc_research/stage131_project_read_lifecycle.py"
 hash_eq 93016f92e056b981203266348d6b8d59d7726a54b6e1b46e3f7eb46d56f3b408 "$KREL/deploy/stage131/krc-project-n39-read-continuous.service.example"
 (cd "$SREL" && sha256sum -c SHA256SUMS)
 # Compare all installed files to the authenticated archive (not only a few hashes).
 python3 - "$B/krc.tar" "$KREL" "$B/sentinel.tar" "$SREL" <<'PY'
import pathlib,sys,tarfile
for archive,root in zip(sys.argv[1::2],sys.argv[2::2]):
 root=pathlib.Path(root);expected=set()
 with tarfile.open(archive) as t:
  for m in t.getmembers():
   if m.isfile():
    expected.add(m.name);assert (root/m.name).read_bytes()==t.extractfile(m).read()
 assert {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()}==expected
print("ALL_INSTALLED_ARCHIVE_BYTES_MATCH")
PY
}
rollback(){
 # Preconditions checked explicitly; failure must not leave uncontrolled GET.
 no_lease || { echo ACTIVE_LEASE_DO_NOT_INTERFERE; return 1; }
 [[ -f "$B/baseline.sha256" ]] || return 1
 (cd "$B" && sha256sum -c baseline.sha256) || { systemctl stop "$SENT"; return 1; }
 atomic_config "$B/original.json" || { systemctl stop "$SENT"; return 1; }
 systemctl stop "$SENT" || return 1
 systemctl stop "$READ" || return 1
 rm -f "$MARKER" || return 1
 # Remove only links created by this exact transaction.
 for n in "$READ" "$SENT"; do
   if [[ -f "$B/bootlink-$n" ]]; then
     [[ ! -e "$WANTS/$n" && ! -L "$WANTS/$n" ]] || {
       [[ $(readlink "$WANTS/$n") = "/etc/systemd/system/$n" ]] || return 1
       rm "$WANTS/$n" || return 1
     }
   fi
 done
 install -o root -g root -m 0644 "$B/original-read.service" "$KUNIT" || return 1
 install -o root -g root -m 0644 "$B/original-drop.conf" "$DROP" || return 1
 systemctl daemon-reload || return 1
 systemctl start "$SENT" || return 1
 if ! wait_status 404; then systemctl stop "$SENT"; echo ROLLBACK_NOT_VERIFIED; return 1; fi
 [[ ! -S "$SOCK" ]] || return 1
 echo CONTINUOUS_ROLLBACK_GET_OFF_VERIFIED
}
case "$MODE" in
stage)
 [[ ! -e "$B" && ! -L "$B" && ! -e "$KREL" && ! -L "$KREL" && ! -e "$SREL" && ! -L "$SREL" ]]
 verify_baseline_units
 install -d -o root -g root -m 0700 "$B"
 install -o root -g root -m 0600 /home/krcops/krc-project-n39-read-release-20261118/continuous-candidate.tar "$B/krc.tar"
 install -o root -g root -m 0600 /home/krcops/stage127-get-continuous-20261118/stage127-continuous.tar "$B/sentinel.tar"
 hash_eq "$KSH" "$B/krc.tar"; hash_eq "$SSHASH" "$B/sentinel.tar"
 python3 - "$B/krc.tar" "$B/sentinel.tar" <<'PY'
import pathlib,tarfile,sys
for i,path in enumerate(sys.argv[1:]):
 with tarfile.open(path) as t:
  names=set()
  for m in t.getmembers():
   p=pathlib.PurePosixPath(m.name)
   assert not p.is_absolute() and ".." not in p.parts and (m.isfile() or m.isdir()) and m.name not in names
   names.add(m.name)
   if i==0:
    assert m.name in ("src","src/krc_research","deploy","deploy/stage131") or m.name.startswith("src/krc_research/") or m.name in ("deploy/stage131/krc-project-n39-read-continuous.service.example","deploy/stage131/project_read_contract.schema.json")
   else:
    assert len(p.parts)==1 and m.isfile() and (p.suffix==".py" or p.name in ("manifest.json","SHA256SUMS","20-artifact-get-release.conf"))
  assert len(names)==(101 if i==0 else 19)
print("BOTH_ARCHIVE_ALLOWLISTS_PASS")
PY
 for pair in krc sentinel; do
   if [[ "$pair" = krc ]]; then rel=$KREL; else rel=$SREL; fi
   install -d -o root -g root -m 0755 "$rel"
   tar -xf "$B/$pair.tar" -C "$rel" --no-same-owner --no-same-permissions
   find "$rel" -type d -exec chmod 0755 {} +
   find "$rel" -type f -exec chmod 0644 {} +
 done
 touch "$B/staged"
 verify_staged
 runuser -u krcsentinel -g krc-sentinel-ipc -- env PYTHONPATH="$SREL:$KREL/src" PYTHONNOUSERSITE=1 "$PY" -s -B -c 'import stage127_get_runtime,artifact_get_project_adapter127,krc_research.stage131_project_read_lifecycle; print("CANDIDATE_IMPORT_PASS")'
 echo CONTINUOUS_FILES_STAGED_NO_RUNTIME_CHANGE
 ;;
switch)
 no_lease
 verify_staged; verify_baseline_units
 [[ ! -e "$B/baseline.sha256" && ! -e "$MARKER" && ! -S "$SOCK" && ! -e "$KBASE/continuous" && ! -L "$KBASE/continuous" ]]
 [[ $(systemctl show "$READ" -p ActiveState --value) = inactive ]]
 [[ $(systemctl show "$SENT" -p WorkingDirectory --value) = "$OLDS" ]]
 hash_eq e46d43f62b1b2bfd45dd4a81c86656fb6a4d963db9365045bdf87c104b84c571 "$KUNIT"
 hash_eq 77a8952a29c8c92f66fd20ef54070940704e3efa58700ea13da35030c67f6d54 "$DROP"
 flag "$OLDS" off; wait_status 404
 [[ $(stat -c '%u:%g:%a' "$CONF") = 987:984:400 || $(stat -c '%u:%g:%a' "$CONF") = 987:984:600 ]]
 for n in "$READ" "$SENT"; do [[ ! -e "$WANTS/$n" && ! -L "$WANTS/$n" ]]; done
 cp -- "$CONF" "$B/original.json"; stat -c '%a' "$CONF" > "$B/config-mode"
 cp -- "$KUNIT" "$B/original-read.service"; cp -- "$DROP" "$B/original-drop.conf"
 (cd "$B" && sha256sum original.json original-read.service original-drop.conf config-mode > baseline.sha256)
 trap 'rc=$?; trap - EXIT; if ((rc!=0)); then rollback || echo ROLLBACK_REQUIRES_OPERATOR; fi; exit "$rc"' EXIT
 ln -s "$KREL" "$KBASE/continuous"
 install -o root -g root -m 0644 "$KREL/deploy/stage131/krc-project-n39-read-continuous.service.example" "$KUNIT"
 install -o root -g root -m 0644 "$SREL/20-artifact-get-release.conf" "$DROP"
 systemd-analyze verify "$KUNIT" "$SUNIT"
 systemctl daemon-reload
 systemctl restart "$SENT"
 wait_status 404
 flag "$SREL" off
 [[ $(systemctl show "$SENT" -p WorkingDirectory --value) = "$SREL" ]]
 [[ ! -S "$SOCK" ]]
 touch "$B/switched"
 echo CONTINUOUS_CANDIDATE_SWITCHED_GET_OFF
 echo REQUIRE_REAL_POST_T3_BEFORE_ON
 trap - EXIT
 ;;
on)
 no_lease
 verify_staged; verify_baseline_units
 [[ -f "$B/switched" && ! -f "$B/on" && ! -e "$MARKER" ]]
 [[ $(systemctl show "$SENT" -p WorkingDirectory --value) = "$SREL" ]]
 flag "$SREL" off; wait_status 404
 [[ $(readlink -f "$KBASE/continuous") = "$KREL" ]]
 # Invocation is conditional on prior externally verified POST T3 and joint release decision.
 trap 'rc=$?; trap - EXIT; if ((rc!=0)); then rollback || echo ROLLBACK_REQUIRES_OPERATOR; fi; exit "$rc"' EXIT
 install -o root -g root -m 0600 /dev/null "$MARKER"
 systemctl start "$READ"
 [[ $(systemctl show "$READ" -p Type --value) = notify ]]
 systemctl is-active --quiet "$READ"
 [[ $(stat -c '%u:%g:%a' "$SOCK") = 1002:984:660 ]]
 [[ $(stat -c '%u:%g:%a' "$(dirname "$SOCK")") = 1002:984:750 ]]
 python3 - "$B/original.json" "$B/enabled.json" <<'PY'
import json,sys
with open(sys.argv[1]) as f:c=json.load(f)
assert c.get("artifact_get_enabled",False) is False
c["artifact_get_enabled"]=True
with open(sys.argv[2],"x") as f:json.dump(c,f,sort_keys=True);f.write("\n")
PY
 atomic_config "$B/enabled.json"; flag "$SREL" on
 systemctl restart "$SENT"; wait_status 401
 old=$(systemctl show "$SENT" -p MainPID --value)
 # Controlled reader outage; verify same ingress survives (external authenticated
 # GET503 and POST T3 still require runner evidence).
 systemctl stop "$READ"; [[ ! -S "$SOCK" ]]; wait_status 401
 [[ $(systemctl show "$SENT" -p MainPID --value) = "$old" ]]
 systemctl start "$READ"; [[ $(stat -c '%u:%g:%a' "$SOCK") = 1002:984:660 ]]
 wait_status 401
 [[ $(systemctl show "$SENT" -p MainPID --value) = "$old" ]]
 # No reboot, no extra dependency on reader. Explicit boot links for static Sentinel
 # and independently managed read service; existing POST Requires remains intact.
 for n in "$READ" "$SENT"; do
   [[ ! -e "$WANTS/$n" && ! -L "$WANTS/$n" ]]
   touch "$B/bootlink-$n"
   ln -s "/etc/systemd/system/$n" "$WANTS/$n"
 done
 systemctl daemon-reload
 systemctl is-active --quiet "$READ"; systemctl is-active --quiet "$SENT"
 touch "$B/on"
 echo CONTINUOUS_GET_ON_LOCAL_LIFECYCLE_PASS
 echo EXTERNAL_AUTHENTICATED_RECOVERY_AND_BOOT_ACCEPTANCE_PENDING
 trap - EXIT
 ;;
rollback) rollback ;;
*) echo 'Usage: stage | switch | on | rollback'; exit 64 ;;
esac
