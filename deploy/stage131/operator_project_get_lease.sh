#!/bin/bash
# Temporary STAGING GET lease. Run only root-held, SHA-verified copy.
# No new ports, no science dispatch. 20-minute independent rollback timer.
set -Eeuo pipefail
umask 077
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
cd /
[[ $(id -u) = 0 ]] || { echo OPERATOR_ROOT_REQUIRED; exit 77; }
SELF=/var/backups/krc-stage127-get-lease.sh
[[ "$0" = "$SELF" && $(stat -c '%u:%a' "$SELF") = 0:600 ]]
MODE=${1:-}
[[ "$MODE" = on || "$MODE" = off ]]
CONF=/etc/krc-sentinel-v2/stage127.json
STATE=/var/backups/krc-stage127-get-lease-20261118
MARKER=/etc/krc-project-n39-read/enable-reviewed-staging
SOCK=/run/krc-project-n39-read/backend.sock
READ=krc-project-n39-read.service
SENT=krc-sentinel-stage127.service
TIMER=krc-stage127-get-lease-expiry
SP=/opt/krc-sentinel-v2/releases/stage127-get-963540fe08055b65f0b25a5a6484a61712c282f8
KP=/opt/krc-project-n39-read/46aebfcd52117d564624fd708709a097bb533362
PY=/opt/krc-sentinel-v2/venv/bin/python
URL=http://100.118.132.8:19017/staging/v2/artifacts/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
exec 9>/run/lock/krc-stage127-get-lease.lock
flock -w 90 9
flag() {
  runuser -u krcsentinel -g krc-sentinel-ipc -- env PYTHONPATH="$SP" PYTHONNOUSERSITE=1 "$PY" -s -c 'import sys;from stage127_ingress_entrypoint import load_config;assert load_config(sys.argv[1])["artifact_get_enabled"] is (sys.argv[2]=="on")' "$CONF" "$1"
}
status_code() {
  curl --noproxy '*' -sS -m 8 -H 'X-KRC-Request-ID: KS-00000000000000000000000000000000' -o /dev/null -w '%{http_code}' "$URL"
}
atomic_config() {
  local tmp
  tmp="$(mktemp /etc/krc-sentinel-v2/.stage127-get-XXXXXX)"
  install -o 987 -g 984 -m "$CONFIG_MODE" "$1" "$tmp" || { rm -f -- "$tmp"; return 1; }
  mv -T "$tmp" "$CONF" || { rm -f -- "$tmp"; return 1; }
}
off() {
  # Restore exact pre-lease config, NOT an example. Preserve all other services.
  if [[ -f "$STATE/original.json" ]]; then
    CONFIG_MODE="$(cat "$STATE/config-mode")" || return 1
    [[ "$CONFIG_MODE" = 400 || "$CONFIG_MODE" = 600 ]] || return 1
    (cd "$STATE" && sha256sum -c original.sha256 >/dev/null) || { systemctl stop "$SENT"; return 1; }
    if ! cmp -s "$CONF" "$STATE/original.json" || ! flag off || [[ "$(status_code 2>/dev/null || true)" != 404 ]]; then
      atomic_config "$STATE/original.json" || { systemctl stop "$SENT"; return 1; }
      flag off || { systemctl stop "$SENT"; return 1; }
      systemctl restart "$SENT" || { systemctl stop "$SENT"; return 1; }
    fi
  else
    flag off || return 1
  fi
  systemctl stop "$READ" || return 1
  rm -f -- "$MARKER" || return 1
  test ! -S "$SOCK" || return 1
  if [[ "$(status_code 2>/dev/null || true)" != 404 ]]; then
    systemctl stop "$SENT"
    echo ROLLBACK_NOT_VERIFIED_SENTINEL_STOPPED
    return 1
  fi
  systemctl is-active --quiet "$SENT" || return 1
  systemctl is-active --quiet krc-research-stage131.service || return 1
  systemctl is-active --quiet krc-research-v2.service || return 1
  systemctl stop "$TIMER.timer" || true
  if [[ -d "$STATE" ]]; then
    date -u +%FT%TZ > "$STATE/closed-at" || return 1
  fi
  echo STAGING_GET_OFF_VERIFIED
}
if [[ "$MODE" = off ]]; then
  off
  exit 0
fi
# Must be executed only after the approved main workflow is ready to dispatch.
[[ ! -e "$STATE" && ! -L "$STATE" && ! -e "$MARKER" && ! -S "$SOCK" ]]
test "$(systemctl show "$READ" -p ActiveState --value)" = inactive
test "$(systemctl show "$READ" -p LoadState --value)" = loaded
test "$(systemctl show "$SENT" -p WorkingDirectory --value)" = "$SP"
test "$(readlink -f /opt/krc-project-n39-read/current)" = "$KP"
test "$(stat -c '%u:%g:%a:%s:%h' /etc/krc-project-n39-read/retrieval.key)" = 0:984:440:32:1
test "$(stat -c '%u:%g:%a' /etc/krc-project-n39-read)" = 0:984:750
test "$(stat -c '%u:%g' "$CONF")" = 987:984
test ! -L "$CONF"
CONFIG_MODE="$(stat -c '%a' "$CONF")"
test "$CONFIG_MODE" = 400 -o "$CONFIG_MODE" = 600
flag off
test "$(status_code)" = 404
for s in "$SENT" krc-research-stage131.service krc-research-v2.service; do systemctl is-active --quiet "$s"; done
install -d -o root -g root -m 0700 "$STATE"
install -o root -g root -m 0600 "$CONF" "$STATE/original.json"
echo "$CONFIG_MODE" > "$STATE/config-mode"
(cd "$STATE" && sha256sum original.json > original.sha256)
python3 - "$STATE/original.json" "$STATE/enabled.json" <<'PY'
import json,sys
def unique(items):
 d={}
 for k,v in items:
  assert k not in d
  d[k]=v
 return d
with open(sys.argv[1]) as f:c=json.load(f,object_pairs_hook=unique)
assert c.get("artifact_get_enabled",False) is False
c["artifact_get_enabled"]=True
with open(sys.argv[2],"x") as f:json.dump(c,f,sort_keys=True);f.write("\n")
PY
# Arm independent rollback BEFORE any change. It invokes the same verified root copy.
systemd-run --unit="$TIMER" --on-active=20min --timer-property=AccuracySec=1s --property=Type=oneshot /bin/bash "$SELF" off
systemctl is-active --quiet "$TIMER.timer"
# If activation fails, immediate rollback; timer remains a separate fallback.
trap 'rc=$?; trap - EXIT; if ((rc!=0)); then if ! off; then echo ROLLBACK_REQUIRES_OPERATOR; fi; fi; exit "$rc"' EXIT
install -o root -g root -m 0600 /dev/null "$MARKER"
systemctl start "$READ"
for i in {1..50}; do [[ -S "$SOCK" ]] && break; sleep .1; done
systemctl is-active --quiet "$READ"
test "$(stat -c '%u:%g:%a' "$SOCK")" = 1002:984:660
atomic_config "$STATE/enabled.json"
flag on
systemctl restart "$SENT"
for i in {1..30}; do [[ "$(status_code 2>/dev/null || true)" = 401 ]] && break; sleep .5; done
test "$(status_code)" = 401
systemctl is-active --quiet "$TIMER.timer"
date -u +%FT%TZ > "$STATE/opened-at"
echo STAGING_GET_ON_LEASE_20MIN
echo NO_BEARER_401_PASS
echo 'Run approved main workflow enabled phase; manually run this script off after completion.'
trap - EXIT
