# KRC P2 — Exact psql/PostgreSQL adapter integration + cross-process race audit
2026-10-14 UTC. Status: **4 recovery/replay scenarios PASS; one cross-process concurrency defect CONFIRMED. Gate: PARTIAL / HOLD.**

## Environment and safety
- Remote test machine: authorized `krc-cobalt`, nonprivileged Unix user `krcops` (UID 1002), x86_64 Ubuntu, ~647 MB RAM available at audit.
- PostgreSQL **16.15**, official Ubuntu binary packages extracted directly as `krcops` into `/tmp/krc_p2_realpg_20261014/root`. No sudo, Docker, service install, firewall/production config, or paid resource. Private PostgreSQL cluster and durable database located under `/tmp/krc_p2_realpg_20261014/data`.
- Isolated UNIX socket `/tmp/krc_p2_realpg_20261014/socket`, port number 55479 **unix-only**, TCP host disabled (`-h ''`); `ss -ltn` returned no TCP listener on 55479. Databases `p2_completed`, `p2_concurrent`, `p2_crash`, `p2_facebook`, `p2_cross`. Real server shut down after test: **PG_STOPPED**.
- Original compiled VoiceBridge `ManagedMediaService` and **unchanged original `ManagedMediaPersistentStore` class**, including spawned `psql`, SQL schema and atomic reservations. VoiceBridge checkout HEAD `48354ded605a6c703342678695bdce8cabe6d692`, not deployed by test.
- Fake-only provider operations, file-backed mock call counters. No real MEDIA starts, no actual paid providers, no production Neon writes, no Render/production restarts, no public/main changes.
- Harness version committed in private KRC repository under `docs/media/tests/p2_real_postgres_harness.mjs`. Requires compilation of isolated VoiceBridge and environment `PATH` pointing at private 16/bin, `LD_LIBRARY_PATH` to extracted libpq, `PGHOST` private socket, `PGPORT=55479`, `PGUSER=krcops`. Use an independent new fixture data directory/databases for reruns.

## Passed live local real-Postgres adapter scenarios
1. **Lost client response after successful job**: New service instance and original Postgres tables returned same COMPLETED ID/segments; reused=true; one mock provider call. Trace `LOST_REPLY_COMPLETED_REUSE_PASS provider_calls=1 job_same=true`. SQL table `p2_completed`: COMPLETED=1.
2. **Two starts inside one service process**: Single mock provider despite concurrent calls. Trace `CONCURRENT_SINGLE_WINNER_PASS provider_calls=1`. SQL `p2_concurrent`: COMPLETED=1.
3. **Actual child SIGKILL during legacy native PROCESSING**: Test child blocked inside mock provider after durable reservation; forced SIGKILL; independent new Node process used same live Postgres adapter and converted record to FAILED `MANAGED_PROVIDER_RESULT_UNCERTAIN_RETRY_BLOCKED`, `credit_charge_uncertain=true`, no second mock provider call. SQL `p2_crash`: FAILED=1; mock counter=1. Traces `CRASH_IN_PROCESSING_INJECTED provider_calls_before=1`, `CRASH_RECOVERY_FAIL_CLOSED_PASS provider_calls=1 status=FAILED`.
4. **Actual child SIGKILL during Facebook FREE_ONLY PROCESSING**: Old record FAILED, controlled fresh key record COMPLETED. SQL `p2_facebook`: FAILED=1, COMPLETED=1; mock counters **free retrieval=2, STT=1, paid retrieval=0**. Trace `FREE_FACEBOOK_CRASH_CONTROLLED_RETRY_PASS free_retrieval_calls=2 fake_stt_calls=1 paid_calls=0 two_job_states=FAILED_COMPLETED`. Note this is two *free* retrieval attempts, not at-most-once.

## NEW defect: cross-process active PROCESSING marked orphan incorrectly
5. **Cross-process overlap (two independent Node processes, same real PostgreSQL)**:
  - Process A acquired durable job reservation in `p2_cross` and was actively inside blocked fake provider (confirmed ready marker; counter 1).
  - While A remained alive and blocked, process B (separate local `inFlight` set) called `startNative` with the same canonical request key.
  - B did **not** make a duplicate provider call (counter remained 1), but returned `FAILED`, `reused=true`, error `MANAGED_PROVIDER_RESULT_UNCERTAIN_RETRY_BLOCKED`.
  - SQL while A was still running showed `FAILED|1`. After terminating the test holder, SQL yielded `FAILED|MANAGED_PROVIDER_RESULT_UNCERTAIN_RETRY_BLOCKED`; count=1. This is **false orphan classification / premature mutation of an active job**, a concurrency defect rather than a PostgreSQL failure.
  - Code path: `ManagedMediaService.reusableRecord()`: `if (this.inFlight.has(requestKey)) return existing; return this.interruptedRecord(existing);`. `inFlight` is process-local, not distributed. Free route `freeRouteStartReservation()` uses a related local-only check. This logic is present in **currently Render-deployed exact VoiceBridge commit `072658ff512802262cef00ff424b87eedde1f934`**, confirmed by direct source read.
  - Render currently reports a single instance but overlap can occur with concurrent workers, rolling deployments or stale processes. This test establishes defect in multi-process conditions; it does NOT prove that an actual user production job suffered it.

## Acceptance classification and required fix
- Real PostgreSQL `psql` adapter operational, persistence, SIGKILL/reopen, lost-reply reuse: **PASS**.
- Cross-process concurrent correctness: **FAIL**, cannot certify universal exactly-once job state safety.
- Production external provider calls/billing and Render in-flight fault injection: **NOT RUN**.
- Recommended patch design for VoiceBridge private development branch: persisted lease/worker epoch + owner token/heartbeat, atomic compare-and-swap state transition for confirmed stale workers only. Readers and independent processes should return active PROCESSING unchanged during a valid lease, not mark FAILED solely because their local inFlight lacks a key. Preserve fail-closed on uncertain charges and protect against old worker overwriting a reconciled state. Cover free routes separately; free-only controlled retries must not silently invoke paid providers.
- After patch: re-run exact real-Postgres harness with cross-process overlapping A/B, actual SIGKILL orphan recovery, tests 14/14 and full 276+ suite, no production deploy until separate owner authorization.
- **Global KRC MEDIA acceptance remains HOLD**, no paid fallback enabled.

## Audit artifacts
- `docs/media/tests/p2_real_postgres_harness.mjs` code committed.
- Original standalone PGlite test report and harness also retained, but this is the first completed actual PostgreSQL server + unchanged `psql` adapter execution.
