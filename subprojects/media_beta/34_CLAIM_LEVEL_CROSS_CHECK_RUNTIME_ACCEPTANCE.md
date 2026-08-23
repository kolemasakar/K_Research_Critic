# Claim-Level Cross-Check Runtime Acceptance

Version: 1.0
Date: 2026-08-23
Status: PASS / RUNTIME_ACCEPTED_PRIVATE_OWNER_BETA

## Scope

Acceptance test for claim-level enforcement of `required_cross_checks` in the actual private `K-Research & Critic - MEDIA BETA` Custom GPT after Builder synchronization.

This test is non-billable text research; media transcript Actions were not used and managed media credits remained 0.

## Test query

`Досліди, чи справді холодний душ покращує імунітет.`

The first CriticProfile gate used direct execution option `1`.

## Expected contract

For a medical task:
- `risk_level=CRITICAL`;
- `required_cross_checks>=3`;
- every material factual claim exposes its own `achieved/required` state;
- `achieved<required` produces `SHORTFALL` plus an explicit reason and qualified conclusion;
- hidden/unqualified shortfall cannot end in unconditional `PASS`.

## Observed result

The final report recorded:
- `risk_level: CRITICAL`;
- `required_cross_checks: 3 independent evidence sources for each material claim`;
- user-visible claim-level lines in the form `Cross-check: achieved/required - PASS|SHORTFALL`;
- multiple claims with `3/3 - PASS`;
- the claim interpreting `29% fewer sick-leave days` with `Cross-check: 1/3 - SHORTFALL`;
- explicit limitation: no three independent high-quality replications of that specific cold-shower result;
- the shortfall was not misrepresented as satisfied;
- final status `COMPLETED_WITH_LIMITATIONS`;
- approved profile metadata included ISO-8601 `approved_at`.

## Acceptance verdict

PASS.

The previous aggregate-only defect is resolved at the behavioral contract level: the actual private GPT now surfaces claim-level cross-check shortfalls and prevents an unconditional successful completion from concealing them.

## Quality notes

Two non-blocking follow-ups remain:
- where a claim reports `3/3 - PASS`, the final presentation should ideally make all three independent evidence streams directly traceable to the reader;
- bibliographic/source accuracy remains a separate quality dimension and should be independently validated by Critic rather than inferred from cross-check counts alone.

These notes do not invalidate claim-level enforcement acceptance.

## Production boundary

This acceptance applies only to the private owner `K-Research & Critic - MEDIA BETA` and branch `agent/video-url-research` / draft PR #8.

It does not authorize merge to `main`, public GPT promotion, external tester rollout, or production VoiceBridge changes.
