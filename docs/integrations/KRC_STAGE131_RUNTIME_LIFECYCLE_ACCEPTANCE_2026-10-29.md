# Stage131 controlled staging runtime acceptance — 2026-10-29

## Scope and release
STAGING ONLY / FREE_ONLY / Production NO-GO. Operator explicitly approved controlled installation, manual start, rollback and NO real science requests. Installed pinned source commit `49f8b857b46ebdf45636deffe90f8a4ee578bddf`, isolated Python3.12, installed focused suite 11/11 PASS; source Git archive diff 0:0, root-owned non-group-writable files. Provisioner SHA256 `4b5ec858f0ecf100c921ab2be42eaab95ec206d4264ea33163b51eed5b99d1cb`, reported INSTALL_PREFLIGHT=PASS, STAGE131_PROVISIONED=PASS.

## Runtime observations
1. First start: Stage131 `active`, PID46265, restarts0; Unix socket /run/krc-stage131/backend.sock owner krcresearch:krc-sentinel-ipc mode660.
2. Operator config inspection: SCIENCE_SIGNER_DISABLED=True; WORKFLOW_DISABLED=True.
3. Controlled stop: Stage131 inactive, socket removed (SOCKET_REMOVED_RC=0). Existing Stage126 active PID37979, Stage127 active PID45059.
4. Controlled **restart after stop**: Stage131 active PID46327 NRestarts0; Unix socket owner krcresearch:krc-sentinel-ipc mode660.
5. Independent read-only Remote Desktop Commander systemd snapshot after restart: Stage131 active PID46327, Stage126 active PID37979 NRestarts0, Stage127 active PID45059 NRestarts1. `UnitFileState=static` Stage131; `Restart=no` verified earlier.
**Verdict:** STAGE131_INSTALL_AND_LIFECYCLE=PASS, controlled runtime rollback/recovery=PASS. No change to Stage126/Stage127 observed.

## Still explicitly not accepted
Real owner consent and backend signer; K_Science/Sentinel formal scientific request/UDS schema ACK; bibliography provider dispatcher, full text/license provenance; signed live scientific E2E-01..05, independent gate acceptance. Do not equate Unix socket ready with scientific feature ready. Never share secret bytes. No automatic service enable, public exposure or production change.
