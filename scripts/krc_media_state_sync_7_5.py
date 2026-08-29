from pathlib import Path

state_path = Path("subprojects/media_beta/03_CURRENT_STATE.md")
checkpoint_path = Path("subprojects/media_beta/57_DURABLE_FAIL_CLOSED_NEGATIVE_MATRIX_ACCEPTED.md")
state = state_path.read_text(encoding="utf-8")


def once(old: str, new: str) -> None:
    global state
    count = state.count(old)
    if count != 1:
        raise SystemExit(f"expected one match, found {count}: {old[:140]!r}")
    state = state.replace(old, new, 1)


once("Version: 7.4", "Version: 7.5")
once(
    "CONSENT_CREDIT_QUOTA_NEGATIVE_MATRIX_ACCEPTED\nA10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED",
    "CONSENT_CREDIT_QUOTA_NEGATIVE_MATRIX_ACCEPTED\nDURABLE_FAIL_CLOSED_NEGATIVE_MATRIX_ACCEPTED\nA10_COPY_SAFE_CLAIM_TABLE_RUNTIME_ACCEPTED",
)
once(
    "The consent/credit/quota negative matrix is now accepted as well: provider-credit substitutions fail before provider work, active managed KRCM routes use a durable PostgreSQL STT quota reservation, and the legacy KRCC audio path now competes against that same concurrency-safe daily ledger. The owner continues private testing before release decisions.",
    "The consent/credit/quota negative matrix is now accepted as well: provider-credit substitutions fail before provider work, active managed KRCM routes use a durable PostgreSQL STT quota reservation, and the legacy KRCC audio path now competes against that same concurrency-safe daily ledger. The durable fail-closed negative matrix is also accepted: durable-store initialization and durable quota-ledger outages stop before AssemblyAI provider start, and the retained regression covers both managed KRCM and legacy KRCC quota boundaries. The owner continues private testing before release decisions.",
)
once(
    "consent/credit/quota acceptance record: docs/history/KRC_MEDIA_CONSENT_CREDIT_QUOTA_NEGATIVE_MATRIX_2026-08-29.md\ndraft PR: #28",
    "consent/credit/quota acceptance record: docs/history/KRC_MEDIA_CONSENT_CREDIT_QUOTA_NEGATIVE_MATRIX_2026-08-29.md\ndurable fail-closed regression head: 8a66e610b89a7e1398b5e8cbe4ac59334ffee5d2\ndurable fail-closed acceptance record: docs/history/KRC_MEDIA_DURABLE_FAIL_CLOSED_NEGATIVE_MATRIX_2026-08-29.md\ndraft PR: #28",
)

section = """## Durable Fail-Closed Negative Matrix Acceptance

Accepted owner-testing record in VoiceBridge:

```text
docs/history/KRC_MEDIA_DURABLE_FAIL_CLOSED_NEGATIVE_MATRIX_2026-08-29.md
```

Regression and validation:
- retained regression file `src/cloud/tests/managed_media_durable_fail_closed.test.ts`;
- managed durable-store initialization outage stops before job reservation/provider work: PASS;
- managed durable quota-ledger outage fails before AssemblyAI provider start: PASS;
- failed quota-ledger case retains zero retrieval credits and zero STT seconds: PASS;
- attachment, Telegram, and Facebook managed STT routes share the durable `reserveSttQuota` boundary: PASS;
- legacy KRCC reserves durable quota before AssemblyAI transcriber construction: PASS;
- KRCC durable quota/store errors expose explicit fail-closed 503-class errors: PASS;
- initial matrix run `33265879771` exposed only three static test-harness source-path errors after the two behavioral outage tests had already passed;
- corrected matrix run `33265955398`: SUCCESS;
- temporary feature-branch matrix workflow removed after success: PASS;
- final tested VoiceBridge feature head after cleanup: `8a66e610b89a7e1398b5e8cbe4ac59334ffee5d2`;
- exact-head verification run `33266043667`: SUCCESS;
- provider-consuming media work during this acceptance block: NONE;
- Render environment mutation: NONE;
- Neon data mutation requested by this acceptance block: NONE;
- paid Facebook/ScrapeCreators activation: NONE.

No runtime implementation change was required by this block; the only failed attempt was a static test-harness path defect. Release authorization remains unchanged.

"""
once("## Research/Critic Invariants", section + "## Research/Critic Invariants")

state_path.write_text(state, encoding="utf-8")
checkpoint_path.write_text(
    """# MEDIA BETA Durable Fail-Closed Negative Matrix Checkpoint

Date: 2026-08-29
Status: ACCEPTED
Release state: RELEASE_HOLD_OWNER_TESTING
KRC canonical state: Version 7.5

VoiceBridge acceptance record:
`docs/history/KRC_MEDIA_DURABLE_FAIL_CLOSED_NEGATIVE_MATRIX_2026-08-29.md`

Final tested VoiceBridge feature head after temporary workflow cleanup:
`8a66e610b89a7e1398b5e8cbe4ac59334ffee5d2`

Accepted evidence:
- managed durable-store initialization failure stops before job reservation and provider work;
- managed durable quota-ledger failure stops before AssemblyAI provider start;
- failed durable quota reservation records zero retrieval credits and zero STT seconds;
- active attachment, Telegram, and Facebook AssemblyAI routes share the durable quota callback;
- legacy KRCC durable reservation occurs before AssemblyAI transcriber construction;
- corrected full cloud matrix run `33265955398`: SUCCESS;
- exact feature-head verification run `33266043667`: SUCCESS;
- initial run `33265879771` failed only on three static test source-path fixtures after behavioral outage assertions had passed;
- provider-consuming work: NONE;
- Render environment mutation: NONE;
- Neon data mutation requested: NONE;
- paid Facebook/ScrapeCreators activation: NONE;
- release-gate transition: NONE.

Neon PostgreSQL 18 remains the active durable store. Original Render PostgreSQL remains retained and deletion is not authorized. PR #8 and VoiceBridge PR #28 remain release-gated. This checkpoint does not authorize merge, production promotion, external testing, public rollout, original database deletion, or paid Facebook activation.
""",
    encoding="utf-8",
)
print("KRC_MEDIA_STATE_SYNC_7_5_PREPARED")
