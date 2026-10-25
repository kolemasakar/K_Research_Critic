#!/bin/sh
# Owner-authorized KRC private scientific MCP, user-only supervisor.
# No public endpoint; no privileged writes; never touches existing :9013.
set -eu
BASE=/home/krcops/krc-research-private
LOCK="$BASE/.private-mcp-supervisor.lock"
LOG="$BASE/private-mcp.log"
PY="$BASE/.venv/bin/python"
export PYTHONPATH="$BASE/src"
export KRC_PRIVATE_RESEARCH_PORT=19014
cd "$BASE"
exec 9>"$LOCK"
flock -n 9 || exit 0
if /usr/bin/ss -ltn | /usr/bin/grep -q '127.0.0.1:19014 '; then exit 0; fi
if /usr/bin/pgrep -f '[p]ython -m krc_research.mcp_private_server' >/dev/null 2>&1; then exit 0; fi
umask 077
/usr/bin/nohup "$PY" -m krc_research.mcp_private_server >>"$LOG" 2>&1 </dev/null &
echo "PRIVATE_MCP_SUPERVISOR_STARTED_PID=$!"
