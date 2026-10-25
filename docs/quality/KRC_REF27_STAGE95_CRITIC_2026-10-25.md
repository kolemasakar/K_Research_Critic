# KRC №95 — REF-27 automated Critic and regression boundary (2026-10-25)

## Verified execution
- Canonical owner-uploaded PDF SHA256 `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`: PASS.
- Local `pytest -q test_stage93_audit.py test_stage94_metrology.py test_stage95_critic.py`: **11/11 PASS**, 0 failures.
- Deterministic local Critic checklist: `REVISE`; publication gate `NO_GO`.
- Previous full KRC isolated 249/249 baseline is historical (№85), **not re-executed in №95**. The repository was not remotely cloned into the local container (DNS unavailable); remote execution was blocked in earlier calls.

## Gate matrix
- Source byte custody/hash: PASS.
- Raster sha and coordinate formula checks: PASS.
- Independent second inspection of chart tick and mark coordinates: SHORTFALL.
- Mapping of Figure 1 curves to the nine Table I specimens or established group aggregation: SHORTFALL.
- Full metrological uncertainty (axes, curve, source ±1% instrument bound, original data) SHORTFALL.
- Independent test of author's 270 m/s decrease in the first two hours from Figure 2: SHORTFALL (source-reported only).
- Independent human scientific review: PENDING until final owner-approved gate.
- Current full KRC regression: NOT_RUN.

## Source interpretation
Figure 2's y-axis is “Decrease of the UPV” with tick labels from 200 to 400 m/s; it cannot be treated as raw UPV or a 0-origin graphic. A plotted cumulative decrease near time zero is not itself an interval difference of 270m/s. Nominal speed/device accuracy ≤±1% is manufacturer-reported on source PDF page 2, not evidence of unrounded measurements or a combined confidence interval. Do not interpret approximate chart points as separate confirmed experiments.

## Artefacts
Locally produced `stage95_critic.py`, `test_stage95_critic.py`, and `stage95_critic.json`. No source raster or PDF modified.

## Result
Internal engineering arithmetic PASS; scientific claims and publication **NO_GO**. FREE_ONLY upheld. Production, MEDIA and public endpoints untouched.
