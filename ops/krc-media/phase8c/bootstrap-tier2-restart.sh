#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
  echo "ERROR: run as root" >&2
  exit 1
fi
if [[ "$#" -ne 0 ]]; then
  echo "ERROR: arguments are not accepted" >&2
  exit 64
fi

SOURCE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
HELPER_SRC="$SOURCE_DIR/krc-tier2-cobalt-restart"
SUDOERS_SRC="$SOURCE_DIR/92-krcops-tier2-cobalt-restart"
HELPER_DST='/usr/local/sbin/krc-tier2-cobalt-restart'
SUDOERS_DST='/etc/sudoers.d/92-krcops-tier2-cobalt-restart'
EXPECTED_SHA256='9ef17650c6eb0e94a55e80cac77b03c0eb0c98f37a913d1a9f38702c47acf27f'

id krcops >/dev/null 2>&1
command -v visudo >/dev/null 2>&1
command -v sha256sum >/dev/null 2>&1
[[ "$(sha256sum "$HELPER_SRC" | awk '{print $1}')" == "$EXPECTED_SHA256" ]]

tmp_sudoers="$(mktemp /tmp/92-krcops-tier2-cobalt-restart.XXXXXX)"
trap 'rm -f "$tmp_sudoers"' EXIT
install -o root -g root -m 0440 "$SUDOERS_SRC" "$tmp_sudoers"
visudo -cf "$tmp_sudoers" >/dev/null

install -o root -g root -m 0755 "$HELPER_SRC" "$HELPER_DST"
[[ "$(sha256sum "$HELPER_DST" | awk '{print $1}')" == "$EXPECTED_SHA256" ]]
install -o root -g root -m 0440 "$tmp_sudoers" "$SUDOERS_DST"
visudo -c >/dev/null

if sudo -u krcops sudo -n "$HELPER_DST" unexpected-argument >/dev/null 2>&1; then
  echo "ERROR: Tier-2 helper unexpectedly accepts arguments through sudoers" >&2
  exit 80
fi
if sudo -u krcops sudo -n /usr/bin/id -u >/dev/null 2>&1; then
  echo "ERROR: arbitrary root unexpectedly allowed" >&2
  exit 81
fi

echo 'KRC_PHASE_8_P8_C_HOST_BOOTSTRAP=APPLIED'
echo "helper=$HELPER_DST"
echo "sudoers=$SUDOERS_DST"
echo 'NEXT=merge approved repository implementation, then run operation=tier2-restart'
