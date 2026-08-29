# MEDIA BETA Consent / Credit / Quota Negative Matrix Checkpoint

Date: 2026-08-29
Status: ACCEPTED
Release state: RELEASE_HOLD_OWNER_TESTING
KRC canonical state: Version 7.4

VoiceBridge implementation:
`30d71868987b4ffba3f0ed52e3860f6751242cf7`

VoiceBridge acceptance record:
`docs/history/KRC_MEDIA_CONSENT_CREDIT_QUOTA_NEGATIVE_MATRIX_2026-08-29.md`

Accepted evidence:
- native, metadata, AI-generate, and Facebook reserve consent substitutions fail before billable provider work;
- invalid quota durations and exhausted/stale consent states fail closed;
- isolated live no-spend consent smoke run `33263832119`: SUCCESS;
- Neon managed/client/STT counters remained unchanged during that live smoke;
- active managed KRCM routes reserve daily STT quota durably before AssemblyAI;
- legacy client-assisted KRCC audio now shares the same PostgreSQL daily STT ledger;
- PostgreSQL 18 shared-quota workflow run `33264731836`: SUCCESS;
- full cloud suite after final repair: 153/153 PASS;
- concurrent KRCM 40s + KRCC 40s against a 60s limit allows exactly one request;
- same-job replay does not double-charge quota;
- shared schema initialization is serialized to avoid concurrent DDL races;
- quota serialization acquires a transaction advisory lock before the quota-reading statement so a waiter receives a fresh MVCC snapshot;
- paid Facebook/ScrapeCreators activation: NONE;
- Render environment mutation from acceptance smoke: NONE;
- release-gate transition: NONE.

Neon PostgreSQL 18 remains the active durable store. Original Render PostgreSQL remains retained and deletion is not authorized. PR #8 and VoiceBridge PR #28 remain release-gated. This checkpoint does not authorize merge, production promotion, external testing, public rollout, original database deletion, or paid Facebook activation.
