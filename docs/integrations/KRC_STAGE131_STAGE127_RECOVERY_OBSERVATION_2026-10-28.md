# KRC Stage131 — Sentinel Stage127 recovery observed 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO.**

User reported Stage127 successfully recovered and independently verified on krc-cobalt. KRC-side independent read-only snapshot:
- `krc-sentinel-stage127.service`: `ActiveState=active`, `SubState=running`, `MainPID=43261`, `NRestarts=0`.
- Tailnet-only listener `100.118.132.8:19017` LISTEN.
- `krc-research-v2.service` unchanged and active: `MainPID=37979`, `NRestarts=0`.

This supersedes previously observed Stage127 FAILED/INACTIVE **service availability state only**. Previous T4 race/restart evidence does not automatically become PASS; T4 actual before/after restart and replay-denial must be checked against separate Sentinel acceptance records. External authenticated Artifact GET, real owner consent and scientific E2E still NOT_RUN/NO-GO. No unit restart, configuration changes or system deployment performed by KRC.

Next KRC work: continue SHA-hash offline dependencies, Stage131 local-only staging candidate and K6/K7 contract tests. Sentinel owns T4 evidence and live transport tests.
