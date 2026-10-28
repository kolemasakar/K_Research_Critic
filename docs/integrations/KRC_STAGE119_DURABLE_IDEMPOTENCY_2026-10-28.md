# KRC Stage119 — durable request idempotency, 2026-10-28

Implemented in development branch: `src/krc_research/request_ledger119.py`, `tests/test_request_ledger119.py`. Server isolated checkout: `/home/krcops/krc-stage118-sandbox/repo` on krc-cobalt. Full code review and isolated test subset: **36/36 PASS, 1.60 s**, composed of 8 new ledger tests + 28 prior artifact tests. No production changes.

Ledger uses SQLite WAL and `BEGIN IMMEDIATE` to atomically admit one `(principal,request_id)` with canonical operation/payload SHA-256. Decisions: EXECUTE (new), REPLAY (completed identical), AMBIGUOUS (same in-progress after timeout/reboot), error IDEMPOTENCY_CONFLICT (same key with different digest). Refuses invalid client identities. Completion persists the return JSON. Replay after restart verified; concurrency 8 callers: exactly one EXECUTE.

Important: the ledger is separate staging library, NOT yet wired into gateway dispatch or Artifact Exchange writes. The `principal` argument is supplied by caller; no UDS peer authentication established. `AMBIGUOUS` requires reconciliation; cannot assume completion or retry. Durable result and external scientific side effects are NOT atomic. The protocol currently has no cancellation/status endpoint or retention/GC policy for ledger. Therefore not production safe, not E2E PASS.

Prior full isolated KRC suite as of Stage118: 884 PASS, 8 FAIL, 17 SKIP (legacy Core Skill / GPT package snapshot or 8000-character cap). No complete suite rerun after adding ledger; 36 focused tests passed. No public/production/MEDIA or Stage114 v1 modifications; FREE_ONLY.

Next: crash recovery/reconciliation journal for artifacts and request status; staging-only UDS authenticated peer binding; complete E2E transport v2 contract; immutable-file reads under concurrency and disk reserve stress. Separate owner decision needed for legacy eight test failures.