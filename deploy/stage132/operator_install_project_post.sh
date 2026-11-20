#!/bin/bash
# Explicit owner STAGING deployment. Never execute a scientific task.
set -Eeuo pipefail
umask 077
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
SELF=/var/backups/krc-stage132-operator.sh
[[ $(id -u) = 0 ]] || { echo OPERATOR_ROOT_REQUIRED; exit 77; }
[[ "$0" = "$SELF" && $(stat -c '%u:%g:%a' "$SELF") = 0:0:600 && ! -L "$SELF" ]]
SRC=/home/krcops/stage132-post-candidate-20261120/stage132-post-release-candidate-v2.tar
HASH=e1e03b5afd04d22f033711c02272e9c4b3160fc1c8c642a73988bc5c5c750993
P=/var/backups/krc-stage132-post-20261120
BASE=/opt/krc-stage132-post
REL=$BASE/b77c237c850a8ce9382d1abda05637b4f9f86b85
CONF=/etc/krc-stage132-post
STATE=/var/lib/krc-project-n39-post
BROKER=krc-project-n39-post.service
GATE=krc-research-v2.service
SENT=krc-sentinel-stage127.service
READ=krc-project-n39-read.service
LEG=krc-research-stage131.service
UNIT=/etc/systemd/system/$BROKER
DIR=/etc/systemd/system/$GATE.d
DROP=$DIR/20-project-pilot-post.conf
DRAFT=/home/krcops/krc-project-n39-staging/state
SOCK=/run/krc-project-n39-post/backend.sock
OLD=/run/krc-research-v2/backend.sock
MARK=$CONF/enable-reviewed-staging-post
[[ ! -L "$P" ]]
install -d -o root -g root -m 0700 "$P"
[[ $(stat -c '%u:%g:%a' "$P") = 0:0:700 ]]
exec 9>"$P/lock"
flock -w 5 9
pid(){ systemctl show "$1" -p MainPID --value; }
active(){ systemctl is-active --quiet "$1"; }
check_hash(){ echo "$1  $2" | sha256sum -c -; }
static_units(){
 check_hash bf6cc891ddf5598fa5454d396f5cdcd9458915a665cf4c4c9b7f6482593cd78c /etc/systemd/system/$GATE
 check_hash 93016f92e056b981203266348d6b8d59d7726a54b6e1b46e3f7eb46d56f3b408 /etc/systemd/system/$READ
 check_hash ec212137efb8801f6ca8df19ec9805f3bcbd9be77990cfe912c4d3efa4b56f44 /etc/systemd/system/$SENT
 check_hash 8e6cc4b2ba1fd324c301d66fb1b6c79f4790bdb280b864e4bce485a33dabf5d6 /etc/systemd/system/$SENT.d/10-bounded-recovery.conf
 check_hash 4fb63880d5b5ba47ad4e7d73d79cd30a34a9984388eb50ecd7e2b2d94fc7f504 /etc/systemd/system/$SENT.d/20-artifact-get-release.conf
}
get401(){
 [[ $(curl --noproxy '*' -sS -m 4 -H 'X-KRC-Request-ID: KS-00000000000000000000000000000000' -o /dev/null -w '%{http_code}' 'http://100.118.132.8:19017/staging/v2/artifacts/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') = 401 ]]
}
wait_sock(){
 local unit="$1" path="$2" ownership="$3"
 for i in {1..45}; do
   if active "$unit" && [[ -S "$path" && $(stat -c '%u:%g:%a' "$path") = "$ownership" ]]; then return 0; fi
   sleep 1
 done
 return 1
}
wait_ingress(){
 for i in {1..45}; do
   if active "$SENT" && get401; then return 0; fi
   sleep 1
 done
 return 1
}
snapshot(){
 runuser -u krcops -- /usr/bin/python3 -s - <<'PY'
import sqlite3,json
from pathlib import Path
root=Path("/home/krcops/krc-project-n39-staging/state")
out={}
for name,table in (("science-replay.sqlite","requests"),("requests.sqlite","requests"),("consent.sqlite","approvals")):
 with sqlite3.connect((root/name).as_uri()+"?mode=ro",uri=True) as c:
  assert c.execute("pragma quick_check").fetchone()[0]=="ok"
  out[name]=c.execute("select count(*) from "+table).fetchone()[0]
print(json.dumps(out,sort_keys=True))
PY
}
verify_release(){
 [[ $(readlink -f "$BASE/current") = "$REL" ]]
 [[ $(stat -c '%u:%g:%a' "$BASE" "$REL") = $'0:0:755\n0:0:755' ]]
 [[ -z $(find "$REL" ! -user root -o ! -group root -o -type l -o -perm /022) ]]
 (cd "$REL"; sha256sum -c SHA256SUMS)
 cmp "$UNIT" "$REL/deploy/krc-project-n39-post.service.example"
 [[ $(stat -c '%u:%g:%a' "$CONF" "$STATE" "$CONF/gateway.key" "$CONF/broker.key" "$STATE/relay.sqlite") = $'0:984:750\n1002:984:700\n988:984:400\n1002:984:400\n1002:984:600' ]]
 cmp -s "$CONF/gateway.key" "$CONF/broker.key"
}
rollback(){
 trap - EXIT
 echo STAGE132_ROLLBACK_BEGIN
 if [[ ! -e "$P/cutover-started" ]]; then
   rm -f "$MARK"
   systemctl disable --now "$BROKER" || return 1
   systemctl daemon-reload || return 1
   active "$GATE" && active "$SENT" && active "$READ" && get401 || return 1
   touch "$P/rolled-back"
   echo STAGE132_ROLLBACK_PRE_CUTOVER_NO_INGRESS_RESTART
   return 0
 fi
 systemctl stop "$SENT" || return 1
 systemctl stop "$GATE" || return 1
 if [[ -e "$DROP" ]]; then
   cmp -s "$DROP" "$REL/deploy/20-project-pilot-post.conf.example" || return 1
   rm "$DROP"
 fi
 rm -f "$MARK"
 systemctl disable --now "$BROKER" || return 1
 systemctl daemon-reload || return 1
 static_units || return 1
 systemctl start "$GATE" || return 1
 wait_sock "$GATE" "$OLD" 988:984:660 || return 1
 systemctl start "$SENT" || return 1
 wait_ingress || return 1
 touch "$P/rolled-back"
 echo STAGE132_ROLLBACK_RESTORED
}
case "${1:-}" in
stage)
 static_units
 active "$GATE"; active "$READ"; active "$SENT"; active "$LEG"; get401
 [[ ! -e "$BASE" && ! -e "$CONF" && ! -e "$STATE" && ! -e "$UNIT" && ! -e "$DIR" && ! -e "$P/staged" ]]
 [[ ! -L "$BASE" && ! -L "$CONF" && ! -L "$STATE" && ! -L "$UNIT" && ! -L "$DIR" ]]
 snapshot > "$P/stage-before.json"
 install -o root -g root -m 0600 "$SRC" "$P/release.tar"
 check_hash "$HASH" "$P/release.tar"
 # Exact archive allowlist; no extractall, links, special files or traversal.
 /usr/bin/python3 - "$P/release.tar" "$REL" <<'PY'
import os,sys,tarfile,pathlib,hashlib
archive,release=sys.argv[1:];root=pathlib.Path(release)
files={"SHA256SUMS","deploy/20-project-pilot-post.conf.example","deploy/krc-project-n39-post.service.example","schemas/external_project_pilot_post_v1.schema.json"}
files|={"src/krc_research/stage132_project_post_"+n+".py" for n in ("wire","contract","relay","runtime")}
files|={"gateway-src/krc_research/stage132_project_post_"+n+".py" for n in ("wire","relay","runtime")}
dirs={".","deploy","schemas","src","src/krc_research","gateway-src","gateway-src/krc_research"}
with tarfile.open(archive,"r:") as t:
 seen=set();blobs={}
 for m in t.getmembers():
  n=m.name.removeprefix("./").rstrip("/") or "."
  assert n not in seen;seen.add(n)
  if n in dirs:assert m.isdir()
  else:
   assert n in files and m.isfile() and 0<m.size<=65536
   blobs[n]=t.extractfile(m).read()
 assert seen==dirs|files and set(blobs)==files
 sums={}
 for line in blobs["SHA256SUMS"].decode("ascii").splitlines():
  h,n=line.split("  ",1);n=n.removeprefix("./");assert n not in sums;sums[n]=h
 assert set(sums)==files-{"SHA256SUMS"}
 for n,h in sums.items():assert hashlib.sha256(blobs[n]).hexdigest()==h
 root.mkdir(parents=True,mode=0o755)
 os.chmod(root.parent,0o755)
 for n in sorted(dirs-{"."},key=lambda n:(n.count("/"),n)):
  p=root/n;p.mkdir(mode=0o755);p.chmod(0o755)
 root.chmod(0o755)
 for n,data in blobs.items():
  p=root/n
  with p.open("xb") as f:f.write(data)
  p.chmod(0o644)
print("ARCHIVE_ALLOWLIST_AND_HASHES_PASS")
PY
 ln -s "$REL" "$BASE/current"
 install -d -o root -g 984 -m 0750 "$CONF"
 install -d -o 1002 -g 984 -m 0700 "$STATE"
 # No secret bytes in command arguments, stdout, or temporary untrusted files.
 /usr/bin/python3 - "$CONF" <<'PY'
import os,secrets,sys,pathlib
p=pathlib.Path(sys.argv[1]);key=secrets.token_bytes(32)
for name,uid in (("gateway.key",988),("broker.key",1002)):
 fd=os.open(p/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o400)
 with os.fdopen(fd,"wb") as f:
  f.write(key);f.flush();os.fchown(f.fileno(),uid,984);os.fsync(f.fileno())
PY
 runuser -u krcops -g krc-sentinel-ipc -- env PYTHONPATH="$REL/src:/opt/krc-project-n39-read/549d44868f188c6f6715bd9224c6fa4de29b05cf/src" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -s - <<'PY'
from krc_research.stage131_artifact_nonce_registry import ArtifactNonceRegistry
from pathlib import Path
import os
p=Path("/var/lib/krc-project-n39-post/relay.sqlite")
assert not p.exists()
os.umask(0o077)
ArtifactNonceRegistry(p)
os.chmod(p,0o600)
PY
 install -o root -g root -m 0644 "$REL/deploy/krc-project-n39-post.service.example" "$UNIT"
 verify_release
 # Verify actual old configuration and role-separated imports before any stop.
 runuser -u krcresearch -g krc-sentinel-ipc -- env PYTHONPATH="$REL/gateway-src:/opt/krc-research-v2/src" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /opt/krc-research-v2/.venv/bin/python -s - <<'PY'
from krc_research.stage132_project_post_runtime import OLD_CONFIG,OLD_SOCKET,OLD_STATE,CONF,read_key
from krc_research.staging_entrypoint124 import load_config,secret
import krc_research.staging_service123c as legacy
from pathlib import Path
assert Path(legacy.__file__).is_relative_to("/opt/krc-research-v2/src")
c=load_config(OLD_CONFIG)
assert (c["socket_path"],c["state_root"],c["peer_uid"],c["principal"],c["client"],c["repository"],c["workflow_ref"],c["key_id"])==(str(OLD_SOCKET),str(OLD_STATE),987,"K_Science","K_Science","kolemasakar/K_Science","refs/heads/main","stage126-v1")
k=read_key(CONF/"gateway.key",988)
assert k!=secret(c["transport_key_file"]) and k!=secret(c["science_key_file"])
print("LEGACY_CONFIG_AND_GATEWAY_ROLE_IMPORT_PASS")
PY
 runuser -u krcops -g krc-sentinel-ipc -- env PYTHONPATH="$REL/src:/opt/krc-project-n39-read/549d44868f188c6f6715bd9224c6fa4de29b05cf/src" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -s - <<'PY'
from krc_research.stage132_project_post_runtime import CONF,read_key,OWNER_STATE,NONCE
from krc_research.stage131_project_read_lifecycle import retrieval_key,producer_preflight,existing_nonce
from krc_research.stage131_project_signed_read import KEY_PATH
assert read_key(CONF/"broker.key",1002)!=retrieval_key(KEY_PATH)
producer_preflight(OWNER_STATE)
existing_nonce(NONCE)
print("BROKER_ROLE_IMPORT_STATE_AND_KEY_SEPARATION_PASS")
PY
 systemd-analyze verify "$UNIT"
 snapshot > "$P/stage-after.json"
 cmp "$P/stage-before.json" "$P/stage-after.json"
 active "$GATE"; active "$READ"; active "$SENT"; get401
 touch "$P/staged"
 echo STAGE132_ROOT_STAGED_NO_RUNTIME_CHANGE
 ;;
switch)
 [[ -f "$P/staged" && ! -e "$P/switched" && ! -e "$P/rolled-back" && ! -e "$MARK" && ! -e "$DIR" ]]
 verify_release; static_units
 active "$GATE"; active "$READ"; active "$SENT"; active "$LEG"; get401
 r=$(pid "$READ"); l=$(pid "$LEG"); g=$(pid "$GATE"); s=$(pid "$SENT")
 snapshot > "$P/switch-before.json"
 # Rollback is armed before any changes to the running services.
 trap 'rc=$?; if [[ $rc != 0 ]]; then rollback || echo STAGE132_ROLLBACK_FAILED; fi; exit $rc' EXIT
 trap 'exit 130' INT TERM
 install -o root -g root -m 0600 /dev/null "$MARK"
 systemctl daemon-reload
 systemctl start "$BROKER"
 wait_sock "$BROKER" "$SOCK" 1002:984:660
 # Real role-separated broker denial before touching the existing gateway.
 runuser -u krcresearch -g krc-sentinel-ipc -- env PYTHONPATH="$REL/gateway-src:/opt/krc-research-v2/src" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /opt/krc-research-v2/.venv/bin/python -s - <<'PY'
from krc_research.stage132_project_post_runtime import read_key,CONF,RELAY
from krc_research.stage132_project_post_relay import RelayClient
from krc_research.stage132_project_post_wire import IDENTITY,OP
import secrets
e={"version":"krc-transport/2","identity":IDENTITY,"request_id":"KS-"+secrets.token_hex(16),"operation":OP,"payload":{"critic_profile":{"profile_id":"stage132-no-approval-probe","version":"v1","protocol":"KRC Core","topic":"Technical denial only"}}}
c=RelayClient(RELAY,key=read_key(CONF/"gateway.key",988),expected_uid=1002,expected_gid=984)
assert c.execute(e)==(403,{"error":"OPERATION_DENIED"})
print("BROKER_CROSS_UID_MISSING_APPROVAL_403_PASS")
PY
 runuser -u krcsentinel -g krc-sentinel-ipc -- test ! -r "$CONF/gateway.key"
 runuser -u krcsentinel -g krc-sentinel-ipc -- test ! -r "$CONF/broker.key"
 runuser -u krcresearch -g krc-sentinel-ipc -- test ! -r "$DRAFT/consent.sqlite"
 [[ $(pid "$GATE") = "$g" && $(pid "$SENT") = "$s" && $(pid "$READ") = "$r" ]]
 # Planned brief ingress interruption ONLY for gateway cutover.
 touch "$P/cutover-started"
 systemctl stop "$SENT"
 systemctl stop "$GATE"
 install -d -o root -g root -m 0755 "$DIR"
 install -o root -g root -m 0644 "$REL/deploy/20-project-pilot-post.conf.example" "$DROP"
 systemd-analyze verify "$GATE" "$BROKER"
 systemctl daemon-reload
 systemctl start "$GATE"
 wait_sock "$GATE" "$OLD" 988:984:660
 systemctl start "$SENT"
 wait_ingress
 [[ $(pid "$GATE") != "$g" && $(pid "$SENT") != "$s" && $(pid "$READ") = "$r" && $(pid "$LEG") = "$l" ]]
 active "$BROKER"
 # Actual role-pinned signed legacy gateway path, never using the owner grant.
 runuser -u krcsentinel -g krc-sentinel-ipc -- env PYTHONPATH="/opt/krc-sentinel-v2/releases/stage127-get-b2a8064027c887065522b4b96f846c3d0540194f" PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /opt/krc-sentinel-v2/venv/bin/python -s - <<'PY'
import secrets
from identity_assertion import sign_assertion
from staging_keyring123d import load_local_key
from krc_uds_client import create_pinned_staging_client,IPCError
key=load_local_key("/etc/krc-sentinel-v2/transport.key",expected_uid=987)
identity={"client":"K_Science","principal":"K_Science","repository":"kolemasakar/K_Science","workflow_ref":"refs/heads/main"}
client=create_pinned_staging_client("/run/krc-research-v2/backend.sock",expected_uid=988,expected_gid=984,expected_socket_gid=984)
payload={"critic_profile":{"profile_id":"stage132-no-approval-probe","version":"v1","protocol":"KRC Core","topic":"Technical denial only"}}
for op,p in (("research.profile.validate",payload),("transport.probe",{})):
 e={"version":"krc-transport/2","identity":identity,"operation":op,"request_id":"KS-"+secrets.token_hex(16),"payload":p}
 try:client.execute(sign_assertion(e,key=key,key_id="stage126-v1"))
 except IPCError as exc:assert exc.code=="OPERATION_DENIED"
 else:raise AssertionError("UNEXPECTED_DISPATCH")
print("ACTUAL_SIGNED_GATEWAY_PILOT_AND_TRANSPORT_DENIAL_PASS")
PY
 systemctl enable "$BROKER"
 snapshot > "$P/switch-after.json"
 cmp "$P/switch-before.json" "$P/switch-after.json"
 static_units
 touch "$P/switched"
 trap - EXIT INT TERM
 echo STAGE132_SWITCH_LOCAL_PASS_EXTERNAL_ACCEPTANCE_PENDING
 ;;
rollback)
 [[ -f "$P/staged" && ! -e "$P/rolled-back" ]]
 rollback
 ;;
*) echo 'Usage: stage | switch | rollback'; exit 64;;
esac
