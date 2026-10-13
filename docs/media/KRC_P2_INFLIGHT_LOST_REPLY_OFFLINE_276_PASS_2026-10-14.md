# KRC P2 — In-flight PROCESSING recovery and duplicate-start offline acceptance
Date: 2026-10-14. Owner instruction: execute next P2 stage. Scope is offline no-provider regression and static production-path review. State **OFFLINE PASS; LIVE IN-FLIGHT OPEN**.

## Reproducible environment
- Authorized Oracle test host `krc-cobalt`, isolated checkout `/tmp/krc_p2_offline_20261014`, tracked VoiceBridge branch `agent/krc-media-gemini-migration`.
- Frozen checked-out Git commit `48354ded605a6c703342678695bdce8cabe6d692` (short `48354de`), separate from the Render-deployed earlier source SHA `072658ff512802262cef00ff424b87eedde1f934`. The offline result does not prove that the Render deploy has this code.
- No production service restart or deploy, no production Neon mutation, no provider STT/retrieval execution; dependencies installed in the isolated checkout with `npm ci --ignore-scripts --no-audit --no-fund`.
- TypeScript `npm run build` PASS.

## Targeted tests executed
Command from `src/cloud`:
```sh
node --test dist/tests/managed_media_durability.test.js \
 dist/tests/managed_media_durable_fail_closed.test.js \
 dist/tests/managed_media_persistence_contract.test.js \
 dist/tests/managed_media_state_continuation_negative_matrix.test.js
```
Observed **14 tests, 14 PASS, 0 FAIL, 0 SKIP**, exit code 0. Tests include:
- Completed job/segments survive a new service instance and duplicate start reuses exact job ID with one provider call.
- Two concurrent starts have exactly one mock provider winner; second returns reused PROCESSING.
- Previously persisted PROCESSING reservation with uncertain charge becomes FAILED `MANAGED_PROVIDER_RESULT_UNCERTAIN_RETRY_BLOCKED` on simulated service restart; no provider reexecution (0 quote, 0 transcript calls), no silent free replay.
- Durable initialization/quota failures fail closed before provider execution.
- Platform isolation and state/continuation invalid inputs are rejected before any provider operation.

## Full VoiceBridge offline regression
From the same checkout, `npm test` output **276 tests, 276 PASS, 0 FAIL, 0 SKIP, exit code 0**, approximately 87 s. `node --test` runs compiled `dist/tests/**/*.test.js`. Logs retained at `/tmp/krc_p2_all_results_20261014.log` on the isolated test host; targeted log `/tmp/krc_p2_suite_results_20261014.txt`.

## Source audit/limitations
- `src/cloud/src/managed_media_service.ts`: `interruptedRecord()` maps orphan PROCESSING to FAILED with `credit_charge_uncertain=true` and `retryable=false`; `reusableRecord()` calls it when no local inFlight exists.
- `freeRouteStartReservation()` uses a *different* explicit retry-chain rule for free Facebook/Telegram: orphan PROCESSING becomes FAILED with `FREE_MEDIA_REQUEST_INTERRUPTED`, `credit_charge_uncertain=false` and a derived retry key. This policy must be documented as a distinct case; never generalize paid/uncertain native route guard to all providers. Real provider billing and lost-response edge cases remain unverified.
- `lookupFreeRoute()` itself performs only read operations, without retries/provider work.
- The targeted durability test uses `SharedStore` in memory, not a real Neon-backed database; it verifies business logic and mocks, not PostgreSQL durability under a crash.
- The prior live P2 test proved **completed** Instagram reel job surviving real Render sleep/restart, using Neon + R3C parity and zero credits. It did not include an interrupted PROCESSING job.
- These source routes include legacy optional paid-provider code; FREE_ONLY control must remain enforced at configured live exposure and consent boundaries. No user authorized spending or Telegram LIVE.

## Verdict
- Build: PASS.
- Offline targeted in-flight/duplicate/fail-closed suite: **PASS 14/14**.
- Full compiled offline VoiceBridge suite: **PASS 276/276**.
- Live in-flight job process-kill recovery / live lost reply exactly-once external side effects: **NOT RUN**, requires a specially isolated test route or explicit fault-injection instrumentation; do not kill production while live provider work may occur, fabricate a PROCESSING job in production, or start duplicate provider calls.
- General MEDIA acceptance remains HOLD. Next focus: implement or use a deterministic fault-injection integration harness with production-like PostgreSQL on a disposable isolated branch/database, two service instances, and fake provider with a durable call counter; cover both credit-uncertain and free-only retry policies. Keep public main and paid paths unchanged.
