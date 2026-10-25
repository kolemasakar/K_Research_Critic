# KRC №93 — REF-27 raster interpretation and Table I cross-check

Date: 2026-10-25. FREE_ONLY / research only. SHA256 original uploaded PDF `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`: PASS.

## Actual new local verification
Previous two PNG raster SHA values rechecked against stage91 manifest. A deterministic script `stage93_audit.py` recalculated actual group arithmetic of nine original Table I rows; four local source-bound tests `4/4 PASS`. This is **not** the full KRC regression (prior 249/249 not rerun).

Table I, 3-row mean UPV per group:
- N: air-dry 4638.0, saturated 4817.0, drying 4477.3, oven-dry 4093.3 m/s.
- K: air-dry 4483.0, saturated 4725.7, drying 4405.0, oven-dry 4019.0 m/s.
- KV: air-dry 4530.7, saturated 4764.0, drying 4417.3, oven-dry 4011.0 m/s.

Previous stage92 exploratory Fig1 x≈0% points: N 4029.6, K 3931.0, KV 4049.3 m/s. Differences versus Table I oven-dry **group means**: N −63.7, K −88.0, KV +38.3 m/s. This comparison is **diagnostic, not a source contradiction**: the graph lacks verified specimen/aggregation mapping and the exact marker picked per group is not an admitted measurement.

## Figure 2 critical interpretation
The vertical axis is *decrease of UPV*, explicitly ticked 200–400 m/s (truncated baseline), not raw ultrasonic speed and not a scale beginning at 0. The stage92 provisional near-zero-hour plotted marks N 221.2, K 236.2, KV 246.2 m/s. Those are already nonzero *decrease values*; treating 270 m/s at ~2 h as an additional fall from zero would be invalid. The paper text (p3, conclusions p7) reports a 270 m/s decrease in first 2 hours; neither the initial reference condition nor 2h exact sample coordinates are independently established by this preliminary marker list. Authors' assertion retained as **SOURCE_REPORTED**, not independent graph-verified.

## Source limitations and gate
- Initial Figure 1 sample-to-curve map **UNRESOLVED**.
- Figure 2 zero/reference convention and claim-to-point map **UNRESOLVED**.
- No independently verified second-person figure read; automated arithmetic is independent re-computation, not independent primary experimental data.
- UK-1401 stated manufacturer instrument maximum measurement error ±1% (physical p2); not a validated full metrological budget for plotted curves.
- Full scientific claim gate **NO_GO / SHORTFALL**. Do not invent labels for graphs or convert assumed pixel ±5 into an empirically established confidence interval.

## Next
Formal extraction of exact tick geometry and curve marker locations with repeat inspection; identify plotted underlying dataset/aggregation from article or authors before quantitative source correspondence; incorporate source-author instrument accuracy separately from image localization error; execute isolated full KRC regression and Critic. No production, MEDIA or public changes.
