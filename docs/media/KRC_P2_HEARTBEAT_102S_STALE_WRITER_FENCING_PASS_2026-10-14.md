# KRC P2 — Long heartbeat and stale-owner fencing independent acceptance (2026-10-14)

## Objective
After private VoiceBridge commit 16186fd5 deployed to Render and a short Instagram LIVE reel passed, independently validate 90s+ heartbeat longevity and rejection of a late write from a worker whose PostgreSQL lease was taken by another process. This is an isolated controlled fault-injection study, not a production MEDIA run.

## Test environment and safety
- Authorized `krc-cobalt`, nonprivileged `krcops`.
- Actual PostgreSQL 16.15 Linux server, local UNIX socket only at `/tmp/krc_p2_realpg_20261014/socket`, no TCP listener. Separate disposable databases `p2_fencing` and `p2_heartbeat`.
- Original compiled VoiceBridge `ManagedMediaService` and original `ManagedMediaPersistentStore` with spawned `psql`; lease patch and production-equivalent private branch source from previous acceptance. All media providers faked with deterministic counters; no provider or Render production changes.
- Reproducible script committed at `docs/media/tests/p2_heartbeat_fencing.mjs`. It assumes precreated disposable databases and private psql PATH + PGHOST, PGPORT and PGUSER.
- After test local PostgreSQL stopped cleanly with pg_ctl stop -m fast.

## Test 1 — delayed owner write fenced after reconciliation
- One service started a PROCESSING reservation and blocked in mock provider (provider call counter 1).
- Direct SQL in **disposable database only** shifted the lease heartbeat to now minus 121 s. A distinct `ManagedMediaPersistentStore`/service instance reconciled the expired lease into `FAILED` error `MANAGED_PROVIDER_RESULT_UNCERTAIN_RETRY_BLOCKED`.
- Original worker was then allowed to return. Its database `put` was rejected with `Managed media fenced write rejected: lease owner changed`. Independent SQL verified FAILED retained, reconciler owner remained, and mock provider calls stayed at 1.
- Trace: `FENCING_OLD_WORKER_PASS {"final":"FAILED","provider_calls":1,"old_write_rejected":true}`.
- **PASS** — no obsolete worker overwrite or false successful acknowledgment.

## Test 2 — long-running active lease and remote read
- Separate active provider job remained in PROCESSING for 102 real seconds (intentionally longer than 90 s grace threshold).
- Database heartbeat value advanced **90 s** across observation points while original `lease_owner` and job identity remained stable.
- After 102 seconds, an independent new service instance using same Postgres database called same-key start. It received `PROCESSING`, `reused=true`, not falsely FAILED; mock external provider count still 1. On releasing first mock provider, final status COMPLETED. No paid/external provider work.
- Trace: `HEARTBEAT_102S_PASS {"elapsed_s":102,"heartbeat_advance_s":90,"other_status":"PROCESSING","provider_calls":1,"final":"COMPLETED"}`.
- **PASS** — active lease survives beyond expiry grace with continuously refreshed heartbeat and permits safe idempotent status.

## Regression context and exact boundaries
- Earlier after-patch independent full VoiceBridge suite: **278/278 PASS**, zero FAIL/SKIP; integration exact psql server cases completed/lost response, concurrent start, SIGKILL with simulated expired lease, Facebook FREE_ONLY retry and two-process overlap PASS.
- Render already deployed commit `16186fd5fdc2cb6c890e7ec1a6e964ccc355345d` as `dep-db7do3dg1s2s73a543v0`, status live 2026-10-14 01:34:38 UTC.
- Connected Neon read-only verification confirmed lazy migration `lease_owner` and `lease_heartbeat_at`; short Instagram reel new job `KRCM_24813ae3-1762-4ca7-8e4b-568c3fe98b52` completed; 331 transcript chars, 1 segment, 0 reported credits, 42 STT seconds and matching PostgreSQL row. See prior deployment report.
- These latest 102s provider hold and force-expiry tests were on the local isolated PG server, **not live Render during PROCESSING**.
- Not proven: exact provider external billing/idempotence after ambiguous transport failure, actual Render crash mid-external provider execution, operational long-term multiple replicas. Do not overstate production full acceptance or enable Telegram LIVE.
- P2 technical correctness: **PASS for isolated heartbeat + fencing**, prior deployed smoke PASS; remaining production-wide/financial acceptance gates tracked separately. Overall KRC MEDIA release stays HOLD pending remaining E1/E4 gates and owner release decision.

## Logs and references
Remote test host log `/tmp/krc_p2_realpg_20261014/heartbeat_fencing.log`, exit RC 0, completed in 103.61 seconds. Test script is at `docs/media/tests/p2_heartbeat_fencing.mjs` commit `516867a232f6a52f4a49eb23f3b5e133de65c6bc`.
