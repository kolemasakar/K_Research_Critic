# N32 first coordinated outage attempt: local PASS, external timing mismatch
Date: 2026-11-19
Disposition: LOCAL_CONTROLLED_OUTAGE_PASS / EXTERNAL_N32_NOT_ACCEPTED / RETEST_REQUIRES_COORDINATION.

Actual owner root output, verified script SHA:
READER_OUTAGE_STARTED utc=2026-11-19T21:20:25Z reader_old_pid=717 sentinel_pid=1454
READER_RECOVERED utc=2026-11-19T21:21:01Z reader_new_pid=3831 sentinel_pid=1454
READER_CONTROLLED_OUTAGE_PASS_EXTERNAL_RUNNER_EVIDENCE_REQUIRED

Actual independent host check 21:21:47Z: Reader active enabled PID3831, Sentinel active enabled PID1454 unchanged NRestarts1; Stage131 PID2065 and Research v2 PID720 unchanged; rescue timer/service inactive; socket1002:984:0660, unauthenticated GET401, nonce DB58 rows quick_check ok, science replay count1 quick_check ok; zero failed units. No state/config changes or science dispatch observed.

Actual Science main run44617295555 job135889310322 head fc951d7d0d6ea884943d939441e3a65086f1fe00 conclusion failure. OIDC/main/Tailnet/checkout gates PASS. Actual emitted:
21:17:54.8204178Z RECOVERY_BASELINE_GET200_SHA_POST_ADMITTED
21:17:54.8205188Z OPERATOR_READER_ONLY_STOP_WINDOW_READY
21:19:37.0986145Z RECOVERY_PROBE_FAILED; error_type=RuntimeError
21:19:40Z workflow completed.
No outage503 or recovery200 marker. Outage started 48s after runner error, 150s after ready marker. Reviewed exact runner: 100s pre-outage monotonic deadline, 3.2s polling, RuntimeError on no coordinated outage. Timing evidence supports timeout, but generic log did not expose exact RuntimeError message. No proof of externally observed fault or POST during fault. Do not count N32 as FULL. Actual local stop/start successful, not another crash or reboot.

Correction: coordinate a fresh run with SSH pre-staged command ready before dispatch; verify current live runner ready marker and that run remains in progress. Never act on stale marker. Request Science/Sentinel evaluate extending only pre-outage operator window to 300s with rate-aware bounded polling and sanitized explicit timeout reason, retain 35s outage/75s rescue and 100s recovery deadline. Re-run mocked timing/denial checks for changes; no approval of changed code here. No repeat outage until fresh coordinated run and reviewed procedure. Existing technical artifact TTL guard remains. GET remains ON. No scientific execution, no production acceptance.

Evidence:
https://github.com/kolemasakar/K_Science/actions/runs/44617295555/job/135889310322
