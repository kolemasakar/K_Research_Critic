#!/usr/bin/env bash
# Reviewed STAGING operator procedure. Install/activation requires explicit
# root execution. Never creates a Science approval or dispatches a study.
set -Eeuo pipefail
umask 077
export PATH=/usr/sbin:/usr/bin:/sbin:/bin

SELF=/var/backups/krc-stage133-operator-20261121.sh
ARCHIVE=/home/krcops/stage133-unified-acceptance-20261121/stage133-release-candidate-20261121/stage133-offline-release.tar
SHA=d35541ee1f1b991354f4ddbab08f186abdfb979cc56f096c4747b65d5233bab6
REL=/opt/krc-stage133-offline/d35541ee1f1b991354f4ddbab08f186abdfb979cc56f096c4747b65d5233bab6
BASE=/opt/krc-stage133-offline
BACK=/var/backups/krc-stage133-20261121
BROKER=krc-project-n39-post.service
GATE=krc-research-v2.service
READER=krc-project-n39-read.service
SENT=krc-sentinel-stage127.service
UNIT=/etc/systemd/system/krc-project-n39-post.service
DROP=/etc/systemd/system/krc-research-v2.service.d/20-project-pilot-post.conf
SOCK=/run/krc-project-n39-post/backend.sock
OLD_SOCK=/run/krc-research-v2/backend.sock
MARK=/etc/krc-stage132-post/enable-reviewed-stage133-offline

die(){ echo "STAGE133_DENIED:$*" >&2; exit 77; }
[[ $(id -u) -eq 0 ]] || die ROOT_REQUIRED
[[ "$0" == "$SELF" && -f "$SELF" && ! -L "$SELF" ]] || die REVIEWED_OPERATOR_LOCATION_REQUIRED
[[ "$(stat -c '%u:%g:%a' "$SELF")" == '0:0:600' ]] || die OPERATOR_CUSTODY
phase=${1:-}
[[ "$phase" == stage || "$phase" == activate || "$phase" == verify || "$phase" == rollback ]] || die UNKNOWN_PHASE

install -d -o root -g root -m 0700 "$BACK"
exec 9>"$BACK/operator.lock"
flock -w 5 9 || die OPERATOR_LOCK_BUSY

is_active(){ systemctl is-active --quiet "$1"; }
expect_active(){
 for _ in $(seq 1 20); do
   if is_active "$1"; then return 0; fi
   sleep 1
 done
 return 1
}
verify_archive(){
 [[ -f "$ARCHIVE" && ! -L "$ARCHIVE" ]] || die ARCHIVE_MISSING_OR_LINK
 echo "$SHA  $ARCHIVE" | sha256sum -c - >/dev/null || die ARCHIVE_SHA_MISMATCH
}
baseline_units(){
 # Exact installed Stage132 immutable unit/droplet snapshots taken before this
 # operator was authored; a drift must be manually reviewed before any switch.
 echo 'd7105b58529913b41a58019f146f76523da100551839659f38a6baf2968eeb1f  /etc/systemd/system/krc-project-n39-post.service' | sha256sum -c - >/dev/null || die BROKER_UNIT_DRIFT
 echo '39be4765bdaf88447d96885dc2050e71e044325bd096ccbf86984f8a3ed12a46  /etc/systemd/system/krc-research-v2.service.d/20-project-pilot-post.conf' | sha256sum -c - >/dev/null || die GATEWAY_DROPIN_DRIFT
}
verify_release(){
 [[ -d "$REL" && ! -L "$REL" && -L "$BASE/current" ]] || die RELEASE_NOT_STAGED
 [[ "$(readlink -f "$BASE/current")" == "$REL" ]] || die RELEASE_SYMLINK_DRIFT
 [[ "$(stat -c '%u:%g:%a' "$BASE" "$REL")" == $'0:0:755\n0:0:755' ]] || die RELEASE_ROOT_CUSTODY
 [[ -z "$(find "$REL" \( ! -user root -o ! -group root -o -type l -o -perm /022 \) -print)" ]] || die RELEASE_PERMISSIONS
 (cd "$REL"; sha256sum -c SHA256SUMS >/dev/null) || die RELEASE_MANIFEST
}
verify_default_imports(){
 runuser -u krcops -g krc-sentinel-ipc -- env PYTHONPATH="$REL/src:/opt/krc-project-n39-read/549d44868f188c6f6715bd9224c6fa4de29b05cf/src" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -s - <<'PY'
from krc_research.stage132_project_post_runtime import reviewed_offline_operations
assert reviewed_offline_operations()==frozenset({'research.profile.validate'})
from krc_research.stage132_project_post_contract import ProjectPostBoundary
print('STAGE133_BROKER_UID1002_DEFAULT_OFF_PASS')
PY
 runuser -u krcresearch -g krc-sentinel-ipc -- env PYTHONPATH="$REL/gateway-src:/opt/krc-research-v2/src" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /opt/krc-research-v2/.venv/bin/python -s - <<'PY'
from krc_research.stage132_project_post_runtime import reviewed_offline_operations
assert reviewed_offline_operations()==frozenset({'research.profile.validate'})
print('STAGE133_GATEWAY_UID988_DEFAULT_OFF_PASS')
PY
}
wait_socket(){
 local unit="$1" path="$2" expected="$3"
 for _ in $(seq 1 30); do
   if is_active "$unit" && [[ -S "$path" ]] && [[ "$(stat -c '%u:%g:%a' "$path")" == "$expected" ]]; then
     return 0
   fi
   sleep 1
 done
 return 1
}
read_health(){
 is_active "$BROKER" && is_active "$GATE" && is_active "$READER" && is_active "$SENT"
 [[ -S "$SOCK" ]] || die BROKER_SOCKET_MISSING
 [[ "$(stat -c '%u:%g:%a' "$SOCK")" == '1002:984:660' ]] || die BROKER_SOCKET_CUSTODY
 [[ -S "$OLD_SOCK" ]] || die GATEWAY_SOCKET_MISSING
 [[ "$(stat -c '%u:%g:%a' "$OLD_SOCK")" == '988:984:660' ]] || die GATEWAY_SOCKET_CUSTODY
}
get_unauthorized_401(){
 local status
 status=$(curl --noproxy '*' -sS -m 4    -H 'X-KRC-Request-ID: KS-00000000000000000000000000000000'    -o /dev/null -w '%{http_code}'    'http://100.118.132.8:19017/staging/v2/artifacts/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') || return 1
 [[ "$status" == '401' ]]
}
wait_ingress_401(){
 for _ in $(seq 1 20); do
   if get_unauthorized_401; then
     echo STAGE127_UNAUTHORIZED_GET_401_PASS
     return 0
   fi
   sleep 1
 done
 return 1
}
check_authorized_role_socket(){
 runuser -u krcresearch -g krc-sentinel-ipc -- /usr/bin/python3 -s - <<'PY'
import os,socket,struct
s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
s.settimeout(2)
try:
 s.connect('/run/krc-project-n39-post/backend.sock')
 pid,uid,gid=struct.unpack('3i',s.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
 assert (uid,gid)==(1002,984),(uid,gid)
finally:
 s.close()
print('GATEWAY_UID988_TO_BROKER_UID1002_SOCKET_PASS')
PY
 # Negative HMAC probe from the authorized kernel UID; no real key is read.
 # Rejected before nonce claim and without scientific dispatch.
 runuser -u krcresearch -g krc-sentinel-ipc -- /usr/bin/python3 -s - <<'PY'
import json,secrets,socket,struct,time
s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
s.settimeout(4)
message={
 "domain":"KRC-PROJECT-PILOT-RELAY/1",
 "key_id":"stage132-project-post-relay-v1",
 "issued_at":int(time.time()),
 "nonce":secrets.token_hex(24),
 "envelope":{"version":"krc-transport/2",
             "identity":{"principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"},
             "request_id":"KS-"+"0"*32,
             "operation":"research.evidence.preflight",
             "payload":{}},
 "mac":"0"*64
}
raw=json.dumps(message,sort_keys=True,separators=(",",":")).encode()
assert len(raw)<262144
try:
 s.connect('/run/krc-project-n39-post/backend.sock')
 s.sendall(struct.pack('!I',len(raw))+raw)
 s.shutdown(socket.SHUT_WR)
 def exact(n):
  out=bytearray()
  while len(out)<n:
   data=s.recv(n-len(out))
   if not data:raise AssertionError('CLOSED_WITHOUT_DENIAL')
   out.extend(data)
  return bytes(out)
 length=struct.unpack('!I',exact(4))[0]
 assert 0<length<16384
 answer=json.loads(exact(length))
 assert answer=={"status":403,"body":{"error":"OPERATION_DENIED"}},answer
finally:
 s.close()
print('UID988_INVALID_MAC_DENIED_BEFORE_NONCE_OR_SCIENCE_DISPATCH_PASS')
PY
 runuser -u nobody -g nogroup -- /usr/bin/python3 -s - <<'PY'
import socket
s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
s.settimeout(2)
try:
 try:s.connect('/run/krc-project-n39-post/backend.sock')
 except PermissionError: print('UNAUTHORIZED_NOBODY_SOCKET_DENIED_PASS')
 else:raise AssertionError('UNAUTHORIZED_SOCKET_ADMITTED')
finally:s.close()
PY
}
verify_enabled_roles(){
 [[ $(stat -c '%u:%g:%a' "$MARK") == '0:0:600' && ! -L "$MARK" ]] || die ENABLE_MARKER_CUSTODY
 [[ -f "$BACK/activated" ]] || die NOT_ACTIVATED
 runuser -u krcops -g krc-sentinel-ipc -- env PYTHONPATH="$REL/src:/opt/krc-project-n39-read/549d44868f188c6f6715bd9224c6fa4de29b05cf/src" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -s - <<'PY'
from krc_research.stage132_project_post_runtime import reviewed_offline_operations
assert reviewed_offline_operations(True)==frozenset({'research.profile.validate','research.evidence.preflight','research.inspection.review'})
print('BROKER_UID1002_STAGE133_OPTIN_PASS')
PY
 runuser -u krcresearch -g krc-sentinel-ipc -- env PYTHONPATH="$REL/gateway-src:/opt/krc-research-v2/src" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /opt/krc-research-v2/.venv/bin/python -s - <<'PY'
from krc_research.stage132_project_post_runtime import reviewed_offline_operations
assert reviewed_offline_operations(True)==frozenset({'research.profile.validate','research.evidence.preflight','research.inspection.review'})
print('GATEWAY_UID988_STAGE133_OPTIN_PASS')
PY
 grep -F -- '--enable-stage133-offline-operations' "$UNIT" >/dev/null || die BROKER_UNIT_NOT_ENABLED
 grep -F -- '--enable-stage133-offline-operations' "$DROP" >/dev/null || die GATEWAY_NOT_ENABLED
 read_health
 check_authorized_role_socket
 wait_ingress_401
}
restore_stage132(){
 # Root-only rollback. State, keys, nonce databases and Science grants untouched.
 trap - ERR
 echo STAGE133_ROLLBACK_BEGIN
 systemctl stop "$GATE" || return 1
 systemctl stop "$BROKER" || return 1
 install -o root -g root -m 0644 "$BACK/original-broker.service" "$UNIT" || return 1
 install -o root -g root -m 0644 "$BACK/original-gateway.conf" "$DROP" || return 1
 rm -f "$MARK"
 systemctl daemon-reload || return 1
 baseline_units || return 1
 systemctl start "$BROKER" || return 1
 wait_socket "$BROKER" "$SOCK" '1002:984:660' || return 1
 systemctl start "$GATE" || return 1
 wait_socket "$GATE" "$OLD_SOCK" '988:984:660' || return 1
 read_health || return 1
 wait_ingress_401 || return 1
 touch "$BACK/rolled-back"
 rm -f "$BACK/activated"
 echo STAGE133_ROLLBACK_STAGE132_RESTORED_PASS
}
case "$phase" in
stage)
 verify_archive
 read_health
 get_unauthorized_401 || die BASELINE_INGRESS_UNHEALTHY
 baseline_units
 [[ ! -e "$BASE" && ! -L "$BASE" && ! -e "$BACK/staged" ]] || die ALREADY_STAGED
 [[ ! -e "$MARK" && ! -L "$MARK" ]] || die STAGE133_MARKER_ALREADY_PRESENT
 install -o root -g root -m 0600 "$UNIT" "$BACK/original-broker.service"
 install -o root -g root -m 0600 "$DROP" "$BACK/original-gateway.conf"
 install -d -o root -g root -m 0755 "$BASE"
 /usr/bin/python3 - "$ARCHIVE" "$REL" <<'PY'
import hashlib,os,pathlib,sys,tarfile
archive,release=sys.argv[1:];root=pathlib.Path(release)
allowed={'SHA256SUMS','schemas/stage133/external_offline_payloads_v1.schema.json'}
allowed|={'deploy/stage133-'+v for v in (
 'broker-default-off.service','gateway-default-off.conf',
 'broker-reviewed-optin.service','gateway-reviewed-optin.conf')}
allowed|={'src/krc_research/'+v+'.py' for v in (
 'stage132_project_post_contract','stage132_project_post_relay','stage132_project_post_runtime',
 'stage132_project_post_wire','stage131_project_research_route',
 'stage131_science_semantic_contract','stage133_science_input')}
allowed|={'gateway-src/krc_research/'+v+'.py' for v in (
 'stage132_project_post_relay','stage132_project_post_runtime','stage132_project_post_wire')}
assert not root.exists()
with tarfile.open(archive,'r:') as t:
 members=t.getmembers()
 assert len(members)==len(allowed)==16
 assert {m.name for m in members}==allowed
 blobs={}
 for m in members:
  assert m.isfile() and m.uid==0 and m.gid==0 and m.mode==0o644 and m.mtime==0
  assert 0<m.size<=65536 and not m.issym() and not m.islnk()
  blobs[m.name]=t.extractfile(m).read()
manifest=blobs['SHA256SUMS'].decode('ascii')
assert manifest==''.join(hashlib.sha256(blobs[p]).hexdigest()+'  '+p+'\n'
                         for p in sorted(allowed-{'SHA256SUMS'}))
root.mkdir(mode=0o755)
for name,data in sorted(blobs.items()):
 p=root/name
 p.parent.mkdir(parents=True,exist_ok=True)
 p.parent.chmod(0o755)
 with p.open('xb') as f:f.write(data)
 p.chmod(0o644)
for directory in root.rglob('*'):
 if directory.is_dir(): directory.chmod(0o755)
os.chmod(root,0o755)
print('STAGE133_ROOT_ARCHIVE_MANIFEST_PASS')
PY
 ln -s "$REL" "$BASE/current"
 verify_release
 verify_default_imports
 systemd-analyze verify "$REL/deploy/stage133-broker-default-off.service"
 systemd-analyze verify "$REL/deploy/stage133-broker-reviewed-optin.service"
 read_health
 touch "$BACK/staged"
 echo STAGE133_ROOT_STAGED_DEFAULT_OFF_NO_SERVICE_CHANGE_PASS
 ;;
activate)
 [[ -f "$BACK/staged" && ! -e "$BACK/activated" && ! -e "$BACK/rolled-back" ]] || die NOT_STAGED_OR_ALREADY_USED
 verify_release
 verify_archive
 baseline_units
 read_health
 [[ ! -e "$MARK" && ! -L "$MARK" ]] || die MARKER_UNEXPECTED
 cmp -s "$BACK/original-broker.service" "$UNIT" || die BROKER_UNIT_DRIFT
 cmp -s "$BACK/original-gateway.conf" "$DROP" || die GATEWAY_DROPIN_DRIFT
 on_activate_error(){
   local code=$?
   echo "STAGE133_ACTIVATION_FAILED_CODE=$code" >&2
   restore_stage132 || echo 'STAGE133_ROLLBACK_FAILED_OPERATOR_INTERVENTION_REQUIRED' >&2
   exit "$code"
 }
 trap on_activate_error ERR
 systemctl stop "$GATE"
 systemctl stop "$BROKER"
 install -o root -g root -m 0644 "$REL/deploy/stage133-broker-reviewed-optin.service" "$UNIT"
 install -o root -g root -m 0644 "$REL/deploy/stage133-gateway-reviewed-optin.conf" "$DROP"
 install -o root -g root -m 0600 /dev/null "$MARK"
 systemctl daemon-reload
 systemctl start "$BROKER"
 wait_socket "$BROKER" "$SOCK" '1002:984:660'
 systemctl start "$GATE"
 wait_socket "$GATE" "$OLD_SOCK" '988:984:660'
 touch "$BACK/activated"
 verify_enabled_roles
 trap - ERR
 echo STAGE133_ACTIVATED_CROSS_UID_SOCKET_AND_AUTHORIZED_ROLE_GATES_PASS
 ;;
verify)
 verify_release
 [[ -f "$BACK/activated" ]] || die NOT_ACTIVATED
 verify_enabled_roles
 echo STAGE133_INSTALLED_STATE_VERIFY_PASS
 ;;
rollback)
 [[ -f "$BACK/staged" && -f "$BACK/original-broker.service" && -f "$BACK/original-gateway.conf" ]] || die NO_REVIEWED_ROLLBACK_SOURCE
 if [[ ! -e "$MARK" && ! -e "$BACK/activated" ]]; then
   baseline_units
   read_health
   echo STAGE133_ONLY_STAGED_NOT_ACTIVATED_NO_RESTART_REQUIRED
 else
   restore_stage132
 fi
 ;;
esac
