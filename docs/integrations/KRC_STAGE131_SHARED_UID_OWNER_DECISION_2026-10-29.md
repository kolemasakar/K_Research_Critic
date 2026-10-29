# Stage131 owner decision — shared service UID, 2026-10-29

**Owner-approved architecture choice:** use existing `krcresearch` (UID988), group `krc-sentinel-ipc` (GID984), for the isolated internal Stage131 backend. **Do not create `krcstage131` or another service user.** Keep Sentinel **Stage127** as the only external Tailnet transport candidate (`100.118.132.8:19017`). Stage131 is a local Unix-domain-socket backend, not a second external transport.

This decision supersedes the earlier recommendation to move Stage131 to a dedicated Unix user. It does **not** imply that Stage126 and Stage131 are distinct Unix security principals, nor that their key material can be shared. The shared-UID visibility limitation is an explicitly accepted architectural tradeoff, not a claim of hard process isolation.

## Required compensating controls
- Separate paths: Stage131 `/run/krc-stage131/backend.sock`, `/var/lib/krc-stage131`, `/etc/krc-stage131`; keep Stage126 files, services and ports unchanged.
- Stage131-only generated transport/science secrets; **never reuse or copy Stage126 keys**. 0600 file owner UID988; private config owned UID988 and 0600; state 0700; runtime 0750 and socket 0660 under reviewed group.
- Signer remains explicitly disabled; no real owner grant is inferred.
- Pinned release SHA, hash-locked dependencies, no auto-enable, operator-controlled deployment, positive and negative auth/replay tests before any science E2E.
- No external GET until separately authorized and tested through Sentinel. Do not claim Stage127 availability alone proves T4/E2E.

## Current acceptance status
Review-only systemd template already specifies `User=krcresearch` and `Group=krc-sentinel-ipc`; no unit edit is necessary. Stage131 root-owned release and real config/secrets remain absent. Read-only UID audit 6 NOT_READY, synthetic custody and mode regressions 6/6 PASS. No service installation or restart occurred as part of this decision.
