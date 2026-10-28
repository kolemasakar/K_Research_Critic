# KRC Stage131 — UID/GID and Sentinel T4 incident boundary (2026-10-28)
**STAGING ONLY / FREE_ONLY / Production NO-GO.**

## Independent observation (krc-cobalt)
- `krcresearch` UID 988, `krcsentinel` UID 987, both GID 984 `krc-sentinel-ipc`.
- Stage126 `krc-research-v2.service` ACTIVE PID37979 NRestarts0; runtime dir `/run/krc-research-v2` ownership krcresearch:krc-sentinel-ipc mode0750.
- Unprivileged krcops stat of Stage126 socket returned Permission denied, **not** proof of socket failure; don't change perms or keys.
- Stage131 unit is absent; no privileged Stage131 install or start.
- **Sentinel Stage127 currently FAILED MainPID0**, corroborates Sentinel PR #38 T4 restart incident. The GitHub run passing outside actual restart window is NOT T4 live PASS. Incident belongs to K_Sentinel operator; do not restart Sentinel from KRC, purge replay ledger or change transport.

## KRC work allowed during incident
1. Continue isolated local Stage131 science/consent/bibliography/schema/Artifact GET tests on SHA-pinned checkout.
2. Prepare minimal reviewed Stage131 operator install checklist (root-owned code, dedicated state/config/approvals, strictly controlled socket group), but no activation or network changes.
3. Freeze no remote artifact GET route while Sentinel Stage127 failed and authenticated external GET policy unresolved.
4. After Sentinel restores own service and documents actual restart/replay evidence, repeat peer/identity and T2–T5 integration gates independently.

## Installation gate
Stage131 `/run/krc-stage131` should be owned by service UID988 and group984 with mode0750, private socket at most0660, private state UID988 mode0700; secret config and approvals separately operator-controlled, no cross-read from Stage126. Real owner consent is a separate evidence-based, one-use gate, never synthesized from transported booleans.

No scientific E2E and no production approval are claimed.
