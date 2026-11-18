#!/bin/bash
# Owner-only STAGING install and internal Unix smoke test. External GET stays OFF.
# Execute a root-held copy only after verifying its separately published SHA256.
set -Eeuo pipefail
umask 077
if [[ $(id -u) != 0 ]]; then echo OPERATOR_ROOT_REQUIRED; exit 77; fi
PIN=46aebfcd52117d564624fd708709a097bb533362
ARCHIVE_SHA=75895401f582d65868109a7c3d5d7510aa9303090429a1e37eb2ae6bd104795b
IN=/home/krcops/krc-project-n39-read-release-20261118/release.tar
BACKUP=/var/backups/krc-project-n39-read-20261118
BASE=/opt/krc-project-n39-read
REL="$BASE/$PIN"
SERVICE=krc-project-n39-read.service
UNIT=/etc/systemd/system/$SERVICE
CONF=/etc/krc-project-n39-read
MARKER="$CONF/enable-reviewed-staging"
STATE=/home/krcops/krc-project-n39-staging/state
SOCK=/run/krc-project-n39-read/backend.sock
SENT=/opt/krc-sentinel-v2/releases/stage127-get-963540fe08055b65f0b25a5a6484a61712c282f8
SCONF=/etc/krc-sentinel-v2/stage127.json
SENTPY=/opt/krc-sentinel-v2/venv/bin/python
GET_URL=http://100.118.132.8:19017/staging/v2/artifacts/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
RID=KS-b190d3c43f52c07516170ecebbcd7641
EXPECTED_SHA=840fcb4faf75519d8a55b0569720e9912d35d969c6ea2165b82086d66225042e
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
# Do not import modules from the operator's working directory.
cd /
test "$(stat -c '%u:%a' "$0")" = 0:600
test "$(id -u krcops):$(id -u krcsentinel):$(getent group krc-sentinel-ipc | cut -d: -f3)" = 1002:987:984
test "$(id -g krcsentinel)" = 984
test "$(stat -c '%u:%a' "$STATE")" = 1002:700
for p in "$STATE/consent.sqlite" "$STATE/requests.sqlite" "$STATE/artifacts/index.sqlite3"; do
    test ! -L "$p"; test "$(stat -c '%u:%a' "$p")" = 1002:600
done
test "$(stat -c '%u:%a' "$STATE/artifacts/objects")" = 1002:700
test "$(cat /home/krcops/krc-project-n39-staging/SOURCE_COMMIT)" = 1de17e2dda51a2fbb155632778c425d86fe152d9
for p in "$BASE" "$CONF" "$UNIT" "$BACKUP" /run/krc-project-n39-read /var/lib/krc-project-n39-read; do
    test ! -e "$p"; test ! -L "$p"
done
test "$(systemctl show "$SERVICE" -p LoadState --value)" = not-found
test "$(systemctl show krc-sentinel-stage127.service -p WorkingDirectory --value)" = "$SENT"
for s in krc-sentinel-stage127.service krc-research-stage131.service krc-research-v2.service; do systemctl is-active --quiet "$s"; done
# Read only the reviewed Sentinel configuration through its actual loader.
runuser -u krcsentinel -g krc-sentinel-ipc -- env PYTHONPATH="$SENT" PYTHONNOUSERSITE=1 "$SENTPY" -s -c 'from stage127_ingress_entrypoint import load_config; assert load_config("/etc/krc-sentinel-v2/stage127.json")["artifact_get_enabled"] is False; print("GET_FLAG_OFF=PASS")'
test "$(curl --noproxy '*' -sS -m 5 -o /dev/null -w '%{http_code}' "$GET_URL")" = 404
baseline="$(systemctl show krc-sentinel-stage127.service krc-research-stage131.service krc-research-v2.service -p Id -p MainPID -p WorkingDirectory)"
config_sha="$(sha256sum "$SCONF")"
install -d -o root -g root -m 0700 "$BACKUP"
install -o root -g root -m 0600 "$IN" "$BACKUP/release.tar"
echo "$ARCHIVE_SHA  $BACKUP/release.tar" | sha256sum -c -
# No root interpreter executes repository code. Archive is verified first.
python3 - "$BACKUP/release.tar" <<'PY'
import pathlib,sys,tarfile
with tarfile.open(sys.argv[1]) as t:
 for m in t.getmembers():
  p=pathlib.PurePosixPath(m.name)
  assert not p.is_absolute() and ".." not in p.parts and (m.isfile() or m.isdir())
  assert (m.name in ("src","src/krc_research","deploy","deploy/stage131") or
          m.name.startswith("src/krc_research/") or m.name in (
          "deploy/stage131/krc-project-n39-read.service.example",
          "deploy/stage131/project_read_release_config.example.json",
          "deploy/stage131/project_read_contract.schema.json"))
print("ARCHIVE_ALLOWLIST=PASS")
PY
install -d -o root -g root -m 0755 "$BASE" "$REL"
tar -xf "$BACKUP/release.tar" -C "$REL" --no-same-owner --no-same-permissions
find "$REL" -type d -exec chmod 0755 {} +
find "$REL" -type f -exec chmod 0644 {} +
test -z "$(find "$REL" ! -user root -o ! -group root)"
test -z "$(find "$REL" -perm /022 -print)"
(cd "$REL" && sha256sum -c <<'SUMS'
e0300c8a948916b0b54117cb74275f9d5e1738adbe031acf7f3f7cc678516614  src/krc_research/stage131_project_signed_read.py
377c1c986af8e44138d0a70d417bcff79056156fef3d00fab3344aa90436c4f0  src/krc_research/stage131_project_descriptor_client.py
834cb3934d7c7ec5b6d2b2933dc4a59a3709be11f2c118be5b924530f7c6f7f2  src/krc_research/stage131_signed_artifact_read.py
c8db333d289bb90aa90b9a1c064752570917490c59a2541699bf5b74d78df375  src/krc_research/stage131_signed_artifact_uds.py
c3b9f9e3d26792fdef61f1cc74dd106aea3e799b7340fc06ed6f752bf46cb1ec  src/krc_research/stage131_artifact_nonce_registry.py
e46d43f62b1b2bfd45dd4a81c86656fb6a4d963db9365045bdf87c104b84c571  deploy/stage131/krc-project-n39-read.service.example
0d4e486df67f5922bac9a3707a29d66834333bc11706885d8700475a097835fb  deploy/stage131/project_read_release_config.example.json
b8cd7bf82ba76bcce08ddb41d27bac4fd521bcbd209de7ce37403564e91880b2  deploy/stage131/project_read_contract.schema.json
SUMS
)
ln -s "$REL" "$BASE/current"
install -o root -g root -m 0644 "$REL/deploy/stage131/krc-project-n39-read.service.example" "$UNIT"
install -d -o root -g krc-sentinel-ipc -m 0750 "$CONF"
# Compare to existing execution/POST keys privately. Never print secrets.
python3 - "$CONF/retrieval.key" <<'PY'
import hmac,json,os,pathlib,secrets,stat,sys
def read_regular(p):
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK|os.O_CLOEXEC)
 with os.fdopen(fd,"rb") as f:
  s=os.fstat(f.fileno());assert stat.S_ISREG(s.st_mode) and 32<=s.st_size<=4096
  return f.read(4097)
paths={pathlib.Path("/etc/krc-sentinel-v2/transport.key")}
for root in (pathlib.Path("/etc/krc-stage131"),pathlib.Path("/etc/krc-research-v2")):
 c=json.loads((root/"staging.json").read_text())
 for name in ("transport_key_file","science_key_file"):
  p=pathlib.Path(c[name]);assert p.is_absolute() and p.parent==root
  paths.add(p)
keys=[read_regular(p) for p in paths]
key=secrets.token_bytes(32)
assert not any(hmac.compare_digest(key,x) for x in keys)
fd=os.open(sys.argv[1],os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW|os.O_CLOEXEC,0o400)
with os.fdopen(fd,"wb") as f:
 os.fchown(f.fileno(),0,984);os.fchmod(f.fileno(),0o440)
 f.write(key);f.flush();os.fsync(f.fileno())
print("RETRIEVAL_KEY_SEPARATION=PASS")
PY
test "$(stat -c '%u:%g:%a:%s:%h' "$CONF/retrieval.key")" = 0:984:440:32:1
runuser -u krcops -g krc-sentinel-ipc -- env PYTHONPATH="$REL/src" PYTHONNOUSERSITE=1 /usr/bin/python3 -s -c 'from krc_research.stage131_project_signed_read import ProjectArtifactAuthority,STATE; ProjectArtifactAuthority(STATE); print("KRC_DEPENDENCY_AND_AUTHORITY_IMPORT=PASS")'
runuser -u krcsentinel -g krc-sentinel-ipc -- env PYTHONPATH="$SENT:$REL/src" PYTHONNOUSERSITE=1 "$SENTPY" -s -c 'from artifact_get_project_adapter127 import ProjectReadAdapter; from stage127_get_runtime import load_retrieval_key; from staging_keyring123d import load_local_key; load_retrieval_key(load_local_key("/etc/krc-sentinel-v2/transport.key",expected_uid=987)); print("SENTINEL_DEPENDENCY_AND_KEY=PASS")'
runuser -u krcsentinel -g krc-sentinel-ipc -- test ! -r "$STATE/consent.sqlite"
echo SENTINEL_NO_PRIVATE_STATE_ACCESS=PASS
systemd-analyze verify "$UNIT"
systemctl daemon-reload
test ! -e "$MARKER"; test ! -e "$SOCK"
# Internal test only. Marker and socket are removed at end, even on failure.
cleanup() {
  systemctl stop "$SERVICE" || true
  rm -f -- "$MARKER"
}
trap cleanup EXIT
# Obtain a read-only exact descriptor for the already approved technical result.
META="$(runuser -u krcops -- env PYTHONPATH="$REL/src" PYTHONNOUSERSITE=1 /usr/bin/python3 -s - "$RID" "$EXPECTED_SHA" <<'PY'
import json,sys,sqlite3
from krc_research.stage131_project_signed_read import STATE,ro,ProjectArtifactAuthority
rid,sha=sys.argv[1:]
with ro(STATE/"requests.sqlite") as db:
 row=db.execute("SELECT state,result FROM requests WHERE principal=? AND request_id=?",("K_Science",rid)).fetchone()
 assert row and row[0]=="COMPLETE";a=json.loads(row[1])["artifact"]
scope={"request_id":rid,"artifact_id":a["artifact_id"],"principal":"K_Science"}
d=ProjectArtifactAuthority(STATE).descriptor(scope)
assert d["size_bytes"]==398 and d["sha256"]==sha
print(json.dumps(d))
PY
)"
# Snapshot logical producer state, not mutable WAL sidecar bytes.
snapshot() {
 runuser -u krcops -- env PYTHONPATH="$REL/src" PYTHONNOUSERSITE=1 /usr/bin/python3 -s - <<'PY'
import hashlib,json,sqlite3
from krc_research.stage131_project_signed_read import STATE,ro
with ro(STATE/"consent.sqlite") as c,ro(STATE/"requests.sqlite") as r,ro(STATE/"artifacts"/"index.sqlite3") as a,ro(STATE/"science-replay.sqlite") as s:
 tables=[c.execute("SELECT * FROM approvals ORDER BY request_id").fetchall(),
         c.execute("SELECT * FROM artifacts ORDER BY artifact_id").fetchall(),
         r.execute("SELECT * FROM requests ORDER BY principal,request_id").fetchall(),
         a.execute("SELECT * FROM objects ORDER BY id").fetchall(),
         s.execute("SELECT * FROM requests ORDER BY task_id").fetchall()]
 print(hashlib.sha256(json.dumps(tables,default=str,sort_keys=True).encode()).hexdigest())
PY
}
before="$(snapshot)"
install -o root -g root -m 0600 /dev/null "$MARKER"
systemctl start "$SERVICE"
for i in {1..50}; do [[ -S "$SOCK" ]] && break; sleep .1; done
systemctl is-active --quiet "$SERVICE"
test "$(stat -c '%u:%g:%a' "$SOCK")" = 1002:984:660
test "$(stat -c '%u:%g:%a' "$(dirname "$SOCK")")" = 1002:984:750
pid="$(systemctl show "$SERVICE" -p MainPID --value)"
test "$pid" -gt 1
test "$(ps -o euid= -p "$pid" | tr -d ' ')" = 1002
test "$(ps -o egid= -p "$pid" | tr -d ' ')" = 984
for p in "$STATE/consent.sqlite" "$STATE/requests.sqlite" "$STATE/artifacts/index.sqlite3" "$STATE/artifacts/objects"; do
    findmnt --task "$pid" --target "$p" --noheadings --output OPTIONS | grep -Eq '(^|,)ro(,|$)'
done
echo ACTUAL_UID_GID_SOCKET_READONLY_MOUNTS=PASS
# UID987 uses the actual deployed Sentinel adapter and exact pinned KRC dependency.
runuser -u krcsentinel -g krc-sentinel-ipc -- env PYTHONPATH="$SENT:$REL/src" PYTHONNOUSERSITE=1 "$SENTPY" -s - "$META" <<'PY'
import hashlib,json,os,secrets,socket,sys,time
from artifact_get_project_adapter127 import ProjectReadAdapter
from artifact_get_uds_client127 import RetrievalDenied
from krc_research.stage131_signed_artifact_read import sign_fixture
from krc_research.stage131_project_signed_read import IDENTITY,KEY_ID,KEY_PATH,SOCKET
d=json.loads(sys.argv[1]);key=KEY_PATH.read_bytes()
assert os.getuid()==987 and os.getgid()==984
def message(aid=d["artifact_id"]):
 return sign_fixture({"version":"krc-artifact-get/1","operation":"artifact.read","request_id":d["request_id"],
 "artifact_id":aid,"identity":IDENTITY,"auth":{"key_id":KEY_ID,"issued_at_epoch":int(time.time()),
 "nonce":secrets.token_hex(24),"mac_sha256":"0"*64}},key)
def wire(m):
 body=json.dumps(m,separators=(",",":")).encode()
 with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
  s.settimeout(5);s.connect(str(SOCKET))
  s.sendall(b"POST /v1/artifacts/read HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nContent-Length: "+str(len(body)).encode()+b"\r\nConnection: close\r\n\r\n"+body)
  s.shutdown(socket.SHUT_WR);data=b""
  while True:
   part=s.recv(65536)
   if not part:break
   data+=part
 head,payload=data.split(b"\r\n\r\n",1);return int(head.split()[1]),payload
adapter=ProjectReadAdapter(socket_path=SOCKET,key=key,expected_uid=1002,expected_gid=984,enabled=True)
m=message();f,descriptor=adapter(m)
with f: raw=f.read()
assert descriptor==d and len(raw)==398 and hashlib.sha256(raw).hexdigest()==d["sha256"]
print("LIVE_UID987_DESCRIBE_READ_SHA_EOF=PASS")
try:adapter(m)
except RetrievalDenied as e:assert e.code=="UPSTREAM_DENIED_403"
else:raise AssertionError("REPLAY_ACCEPTED")
print("DURABLE_NONCE_REPLAY=PASS")
bad=message();bad["auth"]["mac_sha256"]="0"*64
assert wire(bad)[0]==403
assert wire(message("a"*48))[0]==404
print("BAD_MAC_AND_WRONG_SCOPE_DENIED=PASS")
PY
# A valid HMAC from a different UID, with access to the IPC group, must fail.
runuser -u krcops -g krc-sentinel-ipc -- env PYTHONPATH="$REL/src" PYTHONNOUSERSITE=1 /usr/bin/python3 -s - "$META" <<'PY'
import json,os,secrets,sys,time
from krc_research.stage131_project_signed_read import IDENTITY,KEY_ID,KEY_PATH,SOCKET
from krc_research.stage131_signed_artifact_read import sign_fixture
from krc_research.stage131_project_descriptor_client import fetch_descriptor,DescriptorDenied
assert os.getuid()==1002
d=json.loads(sys.argv[1]);key=KEY_PATH.read_bytes()
m=sign_fixture({"version":"krc-artifact-get/1","operation":"artifact.read","request_id":d["request_id"],"artifact_id":d["artifact_id"],
 "identity":IDENTITY,"auth":{"key_id":KEY_ID,"issued_at_epoch":int(time.time()),"nonce":secrets.token_hex(24),"mac_sha256":"0"*64}},key)
try:fetch_descriptor(SOCKET,m,key=key)
except DescriptorDenied as e:assert e.status==403
else:raise AssertionError("WRONG_PEER_ACCEPTED")
print("ACTUAL_WRONG_UID_DENIED=PASS")
PY
test "$(stat -c '%u:%g:%a' /var/lib/krc-project-n39-read)" = 1002:984:700
test "$(stat -c '%u:%a' /var/lib/krc-project-n39-read/nonce.sqlite)" = 1002:600
test "$before" = "$(snapshot)"
echo PRODUCER_STATE_UNCHANGED=PASS
cleanup
trap - EXIT
test ! -e "$MARKER"; test ! -e "$SOCK"
test "$(systemctl show "$SERVICE" -p ActiveState --value)" = inactive
test "$baseline" = "$(systemctl show krc-sentinel-stage127.service krc-research-stage131.service krc-research-v2.service -p Id -p MainPID -p WorkingDirectory)"
test "$config_sha" = "$(sha256sum "$SCONF")"
test "$(curl --noproxy '*' -sS -m 5 -o /dev/null -w '%{http_code}' "$GET_URL")" = 404
echo KRC_READ_INSTALLED_INTERNAL_SMOKE_PASS_GET_OFF
echo PRODUCTION_UNCHANGED
