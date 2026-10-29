# Stage131 operator provisioning handoff — 2026-10-29

Owner approved controlled isolated staging deploy, UID988, Stage126/127 unchanged, rollback and no science dispatch.

## Confirmed from operator
- Code installed from commit `49f8b857b46ebdf45636deffe90f8a4ee578bddf`; Git archive compare 0:0, owner root:root, no group/world writable source.
- Isolated .venv Python3.12.3, `pip check` PASS, import as UID988 PASS, installed focused tests 11/11 PASS.
- /etc/krc-stage131 and /var/lib/krc-stage131: `krcresearch:krc-sentinel-ipc 0700`.
- Stage126 PID37979 active, Stage127 PID45059 active (read-only RD recheck).
- RD is UID1002, cannot execute privileged sudo. Operator Ubuntu shell has passwordless sudo `SUDO_RC=0`.

## Prepared local operator script
`/home/krcops/stage131_install_operator_20261029.sh` on `krc-cobalt`; bash syntax check PASS; SHA256 `4b5ec858f0ecf100c921ab2be42eaab95ec206d4264ea33163b51eed5b99d1cb`.

The script preflights current service states, UID/GID and directories, aborts if config, keys or unit exist, generates two distinct 48-byte keys without logging their contents, emits private exact-field Stage131 config with `enable_internal_science_signing=false` and `workflow_ref=staging-disabled`, installs a `Restart=no` no-[Install] unit, runs `systemd-analyze verify` and daemon-reload. **It does NOT start or enable the unit**; preserves secret/config on error and attempts to remove a newly created unit on an error. Operator must inspect the script and its SHA before invoking it. Not yet executed as of this checkpoint.

Controlled operator command **after inspecting**: `sudo -n bash /home/krcops/stage131_install_operator_20261029.sh`. Expected `INSTALL_PREFLIGHT=PASS`, `STAGE131_PROVISIONED=PASS`, `NOT_STARTED=TRUE`. No task dispatch or operation under this script.

Next gates: read-only configuration/mode audit, `systemd-analyze verify`, manual systemctl start; ensure endpoint Unix socket and zero HTTP port, service PID and unchanged Stage126/127; explicitly rollback stop test and service restart only if needed. Real research and provider wiring remain NO-GO.
