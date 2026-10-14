# KRC P2 — Cross-process PROCESSING ownership fix: private-branch acceptance
Date: 2026-10-14. Status: PRIVATE-BRANCH PATCH VALIDATED, DEPLOY NOT AUTHORIZED.

## Defect and reproduction
Previous exact PostgreSQL 16.15 adapter integration demonstrated that a second Node process incorrectly transitioned a legitimately active first process's PROCESSING job to FAILED because its local inFlight set lacked the key. Old failure: CROSS_PROCESS_PROBE status=FAILED, error MANAGED_PROVIDER_RESULT_UNCERTAIN_RETRY_BLOCKED, provider_calls=1, while owner A was still alive. Same logic was present in the deployed older Render SHA, so it is a genuine code-path risk but not evidence of an actual customer incident.

## Fix committed to VoiceBridge private development branch
Repository: kolemasakar/VoiceBridge, branch agent/krc-media-gemini-migration.
- src/cloud/src/managed_media_service.ts commit 6055394a473330a68fa6feb2320abbc4df493a27.
- src/cloud/src/managed_media_persistence.ts commit 57b46d71deb4f38ab99a7acdc88990ccebe1d0f5.
- src/cloud/tests/managed_media_lease.test.ts commit 16186fd5fdc2cb6c890e7ec1a6e964ccc355345d.
- Implementation: owner UUID per PostgreSQL store instance, lease_owner and lease_heartbeat_at columns, 15-second live heartbeat during provider work, 90-second stale threshold. Atomically transition an expired PROCESSING lease in PostgreSQL; active lease returns reusable PROCESSING unchanged. Successful reconciliation fences out old owner writes. Old process's put is rejected when owner changed; no false success. No new external provider route, no fallback enabling, no production deployment.
- ALTER TABLE IF NOT EXISTS handles existing schema and grants grace on previously live PROCESSING rows without lease heartbeat.
- For legacy/native uncertain charges: stale PROCESSING becomes FAILED/RETRY_BLOCKED, no automatic provider replay. For Facebook free route: stale PROCESSING can follow bounded free-only retry chain; no paid fallback in test.

## Verified tests (actual run, remote unprivileged krc-cobalt)
- Isolated checkout of VoiceBridge git initial SHA 48354ded..., patched with exact files above; built via npm run build successfully.
- Targeted existing suites: 14/14 PASS.
- New managed_media_lease.test.ts: 2/2 PASS, asserting live remote lease remains PROCESSING and stale lease fails closed, mock provider calls zero.
- Complete compiled VoiceBridge suite: 278/278 PASS, 0 failed, 0 skipped, exit code 0, duration 93.36 s; local log /tmp/krc_p2_lease_final_full.log.
- Native PostgreSQL 16.15 server, only Unix socket under /tmp/krc_p2_realpg_20261014/socket, port 55479 (no TCP listener). Original ManagedMediaPersistentStore uses exact spawned psql adapter. Each scenario isolated DB, fake provider counters, no external MEDIA or paid operations.
- FINAL real-postgres integration after patch: LOST_REPLY_COMPLETED_REUSE_PASS provider_calls=1 job_same=true; CONCURRENT_SINGLE_WINNER_PASS provider_calls=1; CRASH_IN_PROCESSING_INJECTED provider_calls_before=1; CRASH_RECOVERY_FAIL_CLOSED_PASS provider_calls=1 status=FAILED.
- Crash test explicitly simulates lease heartbeat expiry in the disposable test DB (lease_heartbeat_at shifted 120 seconds into past) to avoid waiting 90 real seconds; immediate crash is expected to leave lease pending, not fail immediately.
- Facebook test: FREE_FACEBOOK_CRASH_CONTROLLED_RETRY_PASS, free retrieval calls 2, fake STT 1, paid 0, durable FAILED+COMPLETED.
- Crucial cross-process concurrency retest: separate owner A blocked inside fake provider; second process B called same key and returned CROSS_PROCESS_PROBE {"status":"PROCESSING","reused":true,"provider_calls":1}; independent SQL status=PROCESSING and lease_heartbeat_at within grace (TRUE). Old false orphan FAILED no longer reproduced.
- Isolated PostgreSQL shut down with pg_ctl stop -m fast; no Render/Neon/prod modifications.

## Limitations / acceptance
- PASS: original psql persistence adapter, double-process live key non-mutation, simulated expired lease reconciliation, SIGKILL crash with fake provider, lost-reply no duplicate completed, free-only controlled retry and full offline suite.
- OPEN: full real-provider cost accounting and actual Render deploy soak, lease refresh observed across >90s long-running provider work, actual old-worker late-write fencing as runtime injected scenario, abnormal process crash when external charge outcome uncertain; verify separately before whole-system release.
- FREE_ONLY must remain strictly enforced; no paid fallback, Telegram LIVE remains BLOCKED.
- Global KRC MEDIA production release remains HOLD pending owner-approved deployment and follow-on controlled pilot acceptance.
- Reproducible exact psql harness in KRC docs/media/tests/p2_real_postgres_harness.mjs updated for expired-lease simulated clock and cross-process conditions (commit caa21c1718a0f8bbdf9e83a7478175e25f4952a8).
