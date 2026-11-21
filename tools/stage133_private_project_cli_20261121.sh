#!/bin/sh
# KRC single-owner, Stage133-root-pinned private research proposal CLI.
# No consent generation, no authorization shortcut, no Science send.
set -eu
umask 077
BASE=/home/krcops/krc-project-n39-staging
RELEASE=/opt/krc-stage133-offline/d35541ee1f1b991354f4ddbab08f186abdfb979cc56f096c4747b65d5233bab6
PY=/home/krcops/stage131-test-venv/bin/python
[ "$(id -u)" = 1002 ] || { echo "KRC_PROJECT_DENIED:WRONG_UID" >&2; exit 77; }
[ "$(stat -c '%u:%g:%a' "$BASE")" = '1002:1002:700' ] || { echo "KRC_PROJECT_DENIED:STATE_CUSTODY" >&2; exit 77; }
[ "$(readlink -f /opt/krc-stage133-offline/current)" = "$RELEASE" ] || { echo "KRC_PROJECT_DENIED:STAGE133_RELEASE_DRIFT" >&2; exit 77; }
[ "$(stat -c '%u:%g:%a' "$RELEASE")" = '0:0:755' ] || { echo "KRC_PROJECT_DENIED:RELEASE_CUSTODY" >&2; exit 77; }
(
  cd "$RELEASE"
  sha256sum --status -c SHA256SUMS
) || { echo "KRC_PROJECT_DENIED:RELEASE_MANIFEST" >&2; exit 77; }
[ -x "$PY" ] || { echo "KRC_PROJECT_DENIED:PYTHON_UNAVAILABLE" >&2; exit 77; }
export PYTHONPATH="$RELEASE/src:$BASE/source/src"
export PYTHONNOUSERSITE=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONSAFEPATH=1
exec "$PY" -s -P -m krc_research.stage131_project_research_route --state "$BASE/state" "$@"
