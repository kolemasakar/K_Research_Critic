# Core Traceability Runtime Acceptance

Version: 1.0
Date: 2026-08-23
Status: PASS / RUNTIME_ACCEPTED_MAIN_CORE

## Scope

This record captures the final NEW-chat runtime regression of the manually synchronized main `K-Research & Critic` after the traceability hardening in `prompts/GPT_STORE_CORE_BUILDER_INSTRUCTIONS.md`.

The regression query was the CRITICAL medical research request about whether cold showers improve immunity. The profile was approved through the direct-run gate with option `1`.

## Acceptance result

`CORE_TRACEABILITY_HARDENING_RUNTIME = ACCEPTED`

Observed runtime behavior:
- `risk_level=CRITICAL`;
- `required_cross_checks=3`;
- material claims exposed claim-level `Cross-check: achieved/required - PASS|SHORTFALL`;
- a real `1/3 - SHORTFALL` was retained rather than inflated to PASS;
- evidence counted in `achieved_independent` was made user-visible and attributable to named/cited evidence origins;
- derivative repetition of the 2016 Buijze result by a later systematic review was explicitly NOT counted as a second independent origin;
- the mandatory claim-level protocol summary table was present with Required, Achieved independent, and Exception values;
- Critic ran `REVISE -> PASS`;
- final reliability score was `0.88`;
- final status was `COMPLETED` with the remaining evidence limitation stated explicitly.

## Traceability evidence

### Claim 1

Claim: cold showers have not been shown to reduce infection frequency/duration in a clinically meaningful way.

Runtime value:
`Cross-check: 3/3 - PASS`

Visible counted independent evidence origins:
1. Buijze et al., 2016 - randomized cold-shower trial, 3018 adults;
2. Collier et al., 2015 - cold-water swimming / upper-respiratory infection comparison;
3. El-Ansary et al., 2024 - randomized cold-vs-warm shower immune-marker study.

Result: traceable `3/3` PASS.

### Claim 2

Claim: cold exposure can alter laboratory immune markers.

Runtime value:
`Cross-check: 3/3 - PASS`

Visible counted independent evidence origins:
1. El-Ansary et al., 2024;
2. Janský et al., 1996;
3. Brenner et al., 1999.

Result: traceable `3/3` PASS.

### Claim 3

Claim: the 2016 cold-shower trial reported approximately 29% fewer sick-leave absence days.

Runtime value:
`Cross-check: 1/3 - SHORTFALL`

The later systematic review repeating the same Buijze result was explicitly recognized as derivative and did not increase `achieved_independent`.

Result: independence/deduplication rule PASS; shortfall remained visible and qualified.

## Protocol table

The runtime output included a claim-level summary table covering all material claims with:

```text
Claim | Required | Achieved independent | Exception
```

Observed rows were consistent with the claim blocks:
- infection-frequency/duration claim: `3 / 3 / NONE`;
- immune-marker claim: `3 / 3 / NONE`;
- 29% sick-leave claim: `3 / 1 / SHORTFALL`.

The ChatGPT renderer visually collapsed the Markdown header text in the pasted result (`ClaimRequiredAchieved independentException`), but the four logical columns and all row values were present. This is recorded as a non-blocking presentation defect, not a workflow or evidence-accounting failure.

## Acceptance matrix

- CRITICAL risk floor -> PASS
- required_cross_checks=3 -> PASS
- claim-level PASS/SHORTFALL -> PASS
- visible evidence-origin traceability -> PASS
- achieved count bounded by traceable origins -> PASS
- derivative/duplicate evidence not double-counted -> PASS
- mandatory claim-level protocol summary -> PASS
- shortfall transparency -> PASS
- Ukrainian report language and localized verdicts -> PASS
- ISO-8601 approval metadata -> PASS

## Disposition

The main `K-Research & Critic` Core workflow is runtime-accepted for:
- two-stage CriticProfile gate;
- risk-based cross-check floors;
- claim-level evidence accounting;
- visible evidence-origin traceability;
- explicit SHORTFALL handling;
- mandatory claim-level Review Protocol summary.

This acceptance does NOT authorize repository merge to `main`, MEDIA BETA public rollout, production VoiceBridge changes, external tester rollout, or any previously unaccepted media adapter.

Canonical hardening record: `35_CORE_RUNTIME_TRACEABILITY_HARDENING.md`.
