# N39 external enabled GET technical acceptance evidence
Date: 2026-11-18
Status: EXTERNAL BASELINE AND CLIENT SUBSET PASS / JOINT MATRIX PARTIAL / CONTINUOUS RELEASE PENDING.

Actual K_Science main workflow_dispatch run 44397533267, job 135131351796,
attempt 1, head b32de96449d9e307ad50767dd61a0465848d8586,
completed success at 21:05:16 UTC. Logs independently inspected by KRC.
https://github.com/kolemasakar/K_Science/actions/runs/44397533267/job/135131351796

Observed enabled-phase response checks (17 log markers):
- N02 401; N04_BAD_SIGNATURE 401; N06 403.
- N14/N16/N17 400; N38_HEAD/N38_POST 405.
- N15/N19_UNKNOWN_SELECTOR 404.
- OWNER_FIXTURE_BASELINE 200, SHA/size PASS, scientific_approval=false.
- N09_SAME_JTI 403 (immediate replay, not restart).
- N35_FRESH_JTI, N11_OVERRIDE_IGNORED, N12_CLIENT_CONSENT_IGNORED,
  N13_CLIENT_SCIENCE_MAC_IGNORED each 200 with SHA/size PASS,
  scientific_approval=false.
- N34 429 with bounded Retry-After.
Five successful reads of the same prior owner-approved 398-byte technical
artifact. This is actual external consumer evidence, not a scientific study.
OIDC diagnostic, Tailnet join and reviewed main/exclusive guard passed;
all POST probe steps skipped. Prior disabled run 44396037112 supplies N01
client evidence. Full N01-N40 not accepted by these logs alone:
N09 restart, N19 cross-request scope, override denial variants,
expired/revoked/corrupt fixtures and server audit/correlation remain pending.

KRC post-run actual read-only host verification 21:06:40 UTC:
reader PID159498 active, Sentinel PID159524 active, original Stage131 PID46327
and Research v2 PID37979 unchanged. Producer science replay count still 1.
Read nonce registry 12 rows, quick_check ok. Row count is not a per-request
audit accounting proof. No new dispatch or consent mutation observed.
Temporary lease timer active, scheduled 21:21:26 UTC (23:21:26 Kyiv).
No manual OFF or timer cancellation by KRC. Owner clarified normal target
continuous GET ON; permanent lifecycle acceptance and controlled deployment
remain pending. Temporary timer still automatically restores OFF unless a
reviewed permanent transition is separately executed. Do not simply cancel
the lease timer on the current non-boot-ready installed unit.

Sentinel: correlate actual server admission, zero-dispatch and per-case
matrix evidence, report ACK/MISMATCH; complete nonfatal lifecycle candidate.
Science: confirm independent receiver and remaining external test coverage.
KRC: coordinate durable lifecycle deployment after joint acceptance. No
production release or 48 science E2E claimed.
