# MEDIA BETA Durable Fail-Closed Negative Matrix Checkpoint

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
