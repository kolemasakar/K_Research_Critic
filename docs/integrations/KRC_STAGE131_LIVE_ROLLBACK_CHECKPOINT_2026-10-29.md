# Stage131 live runtime and rollback checkpoint — 2026-10-29

## Scope
STAGING ONLY; FREE_ONLY; Production NO-GO. Owner approved manual Stage131 launch, rollback, and no real scientific operations. Source SHA `49f8b857b46ebdf45636deffe90f8a4ee578bddf`.

## Observed operator execution
- Provision script SHA256 `4b5ec858f0ecf100c921ab2be42eaab95ec206d4264ea33163b51eed5b99d1cb`, `INSTALL_PREFLIGHT=PASS`, `STAGE131_PROVISIONED=PASS`, `NOT_STARTED=TRUE`.
- `sudo systemctl start krc-research-stage131.service` success, `MainPID=46265`, `NRestarts=0`, active/running.
- `/run/krc-stage131/backend.sock`: socket `krcresearch:krc-sentinel-ipc` mode `660`.
- Runtime configured `User=krcresearch`, `RestrictAddressFamilies=AF_UNIX`, `Restart=no`.
- Operator inspected JSON flags: `SCIENCE_SIGNER_DISABLED=True`, `WORKFLOW_DISABLED=True` (`staging-disabled`).
- Controlled `systemctl stop krc-research-stage131.service`: `inactive`. `test ! -e /run/krc-stage131/backend.sock`: `SOCKET_REMOVED_RC=0`. **RUNTIME_ROLLBACK_PASS**.
- Independent subsequent RD snapshot after stop: Stage131 inactive PID0, Stage126 active PID37979 NRestarts0, Sentinel Stage127 active PID45059 NRestarts1. No evidence of change to Stage126/127.
- No requests dispatched, no science signer, no bibliographic provider.

## Remaining gate
A controlled manual *restart* and socket ownership/state check is outstanding; do not claim restart PASS. Need operator `sudo -n systemctl start krc-research-stage131.service`, inspect active/PID and socket, read-only RD confirmation, then mark runtime recovery PASS. No real E2E, no external research authorization. Never show keys.
