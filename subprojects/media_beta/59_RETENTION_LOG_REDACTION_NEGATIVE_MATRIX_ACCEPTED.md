# MEDIA BETA Retention / Log-Redaction Negative Matrix Checkpoint

Date: 2026-08-29
Status: ACCEPTED
Release state: RELEASE_HOLD_OWNER_TESTING
KRC canonical state: Version 7.7

VoiceBridge acceptance record:
`docs/history/KRC_MEDIA_RETENTION_LOG_REDACTION_NEGATIVE_MATRIX_2026-08-29.md`

VoiceBridge initial regression commit:
`5faa93bfced213c3be82dd71362fc775f3eb0a94`

VoiceBridge corrected regression commit:
`43bd757b541f9dcbffa40041228466a6eaa38c7d`

VoiceBridge acceptance-record commit:
`a0d1d5a380d0d90a42510c3b28f6221385578d52`

KRC canonical-state sync commit:
`2805a3084c80cbd7e472523317aee3feaa606715`

Accepted evidence:
- zero-credit/certain managed jobs use the configured normal TTL;
- charged or charge-uncertain jobs retain at least a 24-hour recovery window;
- uncertain provider failure is non-retryable and not automatically replayed;
- expired durable jobs are purged and expired records are excluded from reads;
- durable STT quota-ledger records older than two UTC days are pruned;
- structured managed-media warning output is metadata-only and excludes sensitive payload fields;
- PostgreSQL command stderr is suppressed and generic durable-store errors are exposed;
- managed-media HTTP responses are `cache-control: no-store` and no console request-body logging is present;
- initial VoiceBridge run `33267727322`: 167/168 PASS; the one failure was an overbroad test-harness assertion that confused response serialization with logging;
- corrected VoiceBridge run `33267869660`: SUCCESS, 168/168 PASS;
- KRC state-sync run `33268042699`: SUCCESS;
- temporary KRC state-sync workflow removed after successful canonical-state commit;
- provider-consuming work: NONE;
- Render environment mutation: NONE;
- Neon data mutation requested: NONE;
- paid Facebook/ScrapeCreators activation: NONE;
- release-gate transition: NONE.

This checkpoint does not activate the separately pending Gemini 3.5 Transcribe transition plan and does not authorize merge, production promotion, external testing, public rollout, original Render PostgreSQL deletion, or paid Facebook activation.