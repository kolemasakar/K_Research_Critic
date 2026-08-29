from pathlib import Path

state_path = Path("subprojects/media_beta/03_CURRENT_STATE.md")
checkpoint_path = Path("subprojects/media_beta/56_CONSENT_CREDIT_QUOTA_NEGATIVE_MATRIX_ACCEPTED.md")

state = state_path.read_text(encoding="utf-8")


def once(old: str, new: str) -> None:
    global state
    count = state.count(old)
    if count != 1:
        raise SystemExit(f"expected one match, found {count}: {old[:120]!r}")
    state = state.replace(old, new, 1)


once("Version: 7.3", "Version: 7.4")
once(
    "STATE_CONTINUATION_NEGATIVE_MATRIX_ACCEPTED\nA10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED",
    "STATE_CONTINUATION_NEGATIVE_MATRIX_ACCEPTED\nCONSENT_CREDIT_QUOTA_NEGATIVE_MATRIX_ACCEPTED\nA10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED",
)
once(
    "The later state/job-read/continuation matrix is also accepted: stale and interrupted job reads fail safely, non-completed jobs do not expose segments, AI and Facebook continuation paths enforce state/platform compatibility, and fresh native retries require a native FAILED target. The owner continues private testing before release decisions.",
    "The later state/job-read/continuation matrix is also accepted: stale and interrupted job reads fail safely, non-completed jobs do not expose segments, AI and Facebook continuation paths enforce state/platform compatibility, and fresh native retries require a native FAILED target. The consent/credit/quota negative matrix is now accepted as well: provider-credit substitutions fail before provider work, active managed KRCM routes use a durable PostgreSQL STT quota reservation, and the legacy KRCC audio path now competes against that same concurrency-safe daily ledger. The owner continues private testing before release decisions.",
)
once(
    "state/continuation acceptance record: docs/history/KRC_MEDIA_STATE_CONTINUATION_NEGATIVE_MATRIX_2026-08-29.md\ndraft PR: #28",
    "state/continuation acceptance record: docs/history/KRC_MEDIA_STATE_CONTINUATION_NEGATIVE_MATRIX_2026-08-29.md\nconsent/credit/quota implementation: 30d71868987b4ffba3f0ed52e3860f6751242cf7\nconsent/credit/quota acceptance record: docs/history/KRC_MEDIA_CONSENT_CREDIT_QUOTA_NEGATIVE_MATRIX_2026-08-29.md\ndraft PR: #28",
)

section = """## Consent / Credit / Quota Negative Matrix Acceptance

Accepted owner-testing record in VoiceBridge:

```text
docs/history/KRC_MEDIA_CONSENT_CREDIT_QUOTA_NEGATIVE_MATRIX_2026-08-29.md
```

Implementation and validation:
- VoiceBridge implementation commit `30d71868987b4ffba3f0ed52e3860f6751242cf7`;
- native, metadata, AI-generate, and Facebook reserve consent substitutions fail before provider-consuming work: PASS;
- stale AI caps, exhausted balances, and invalid quota durations fail closed: PASS;
- isolated Render live no-spend consent smoke run `33263832119`: SUCCESS;
- live Neon managed/client/STT counters remained unchanged: PASS;
- active managed KRCM routes reserve STT quota durably before AssemblyAI: PASS;
- legacy client-assisted KRCC audio shares the same PostgreSQL daily STT ledger: PASS;
- KRCM/KRCC same-day concurrent reservations are serialized with a transaction advisory lock acquired before the quota-reading statement: PASS;
- PostgreSQL shared-schema initialization is serialized to avoid concurrent `CREATE TABLE IF NOT EXISTS` races: PASS;
- final PostgreSQL 18 shared-quota workflow run `33264731836`: SUCCESS;
- full VoiceBridge cloud suite after the final repair: 153/153 PASS;
- concurrent KRCM 40s + KRCC 40s against a 60s limit allows exactly one request: PASS;
- same-job replay does not double-charge quota: PASS;
- provider-consuming work in the live no-spend acceptance smoke: NONE;
- Render environment mutation: NONE;
- paid Facebook/ScrapeCreators activation: NONE.

Intermediate workflow failures were contained diagnostics: one TypeScript harness typing defect, one concurrent schema-initialization DDL race, and one PostgreSQL MVCC snapshot flaw when an advisory lock was acquired inside the same quota statement. The final repair moved quota locking into an explicit transaction statement before the quota read, then passed the full concurrency matrix.

"""
once("## Research/Critic Invariants", section + "## Research/Critic Invariants")
once(
    "and the auth/input/replay negative matrix is accepted. Local attachment and Instagram route-boundary audits are accepted.",
    "and the auth/input/replay negative matrix is accepted. The consent/credit/quota negative matrix is accepted, with one shared durable daily STT ledger spanning active managed KRCM routes and legacy KRCC audio. Local attachment and Instagram route-boundary audits are accepted.",
)

state_path.write_text(state, encoding="utf-8")

checkpoint_path.write_text(
    """# MEDIA BETA Consent / Credit / Quota Negative Matrix Checkpoint

Date: 2026-08-29
Status: ACCEPTED
Release state: RELEASE_HOLD_OWNER_TESTING

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
""",
    encoding="utf-8",
)

print("KRC_MEDIA_STATE_SYNC_7_4_PREPARED")
