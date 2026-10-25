# KRC №84 — REF-27 percentage methods and Figure 1–2 evidence limitations
Date: 2026-10-25.

## Source custody
2013 Lencis/Udris/Korjakins, DOI 10.2478/cons-2013-0011, official RTU original PDF https://ortus.rtu.lv/science/en/publications/16677/fulltext.
SHA256 `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`. Printed Table I on physical PDF page 3; Figure 1 and Figure 2 captions on physical page 4.

## P4 executable result: alternative percentage calculations
New module `src/krc_research/ref27_percent_alternatives.py` and three tests `tests/test_p0_ref27_percent_alternatives.py`.
Using published stage velocities of nine original specimen rows, group N/K/KV:
1. Percent calculated as a ratio of corresponding group mean velocities, rounded HALF_UP: matches all published group percentage summaries.
2. Mean of individual **unrounded** specimen percentage ratios, rounded at the end: **also matches all published summaries**.
3. Mean of **already-rounded** individual percentages, rounded at the end: does **not** match group K, where computed [18,11,6] vs publisher [18,12,5].

**Therefore the publisher's precise original aggregation formula cannot be uniquely inferred from displayed group numbers.** Previous report №83 stating ratio-of-group-means reproduces values is correct, but does not establish it as the unique formula. New module explicitly returns both consistent methods and `authors_original_rounding_method_proven=False`.

## Figure 1 and Figure 2
Literal source inspection of the original hashed PDF confirms:
- Physical page 4 has caption `Fig. 1. Relationships between ultrasonic pulse velocity and water absorption by weight`.
- Physical page 4 has caption `Fig. 2. Decrease in the UPV in concrete after the specimens are taken out from water.`
- Physical page 3 contains author-written report that the UPV velocity `has decreased by 270 m/s` in first two hours across groups. Extraction splits **ve locity** and `270\nm/s`; first literal check failed due a line-break mismatch, a second strict check using the actual extracted line break PASS.
- The PDF figures have not been independently digitized; the captions and cited prose **do not establish** that the shape and coordinate data of graph curves agree quantitatively with Table I.
- `figure_numeric_consistency_verified=False`, graph curves remain SHORTFALL.
- The source states nine measurements in diagonal directions on each specimen face, but the searched text inspection does not establish original instrument metrological accuracy/resolution or the precision of unrounded experimental raw readings. Do not invent an uncertainty value.

Isolated source evidence saved as `/tmp/krc-ext-s04-acceptance/ref27_figure_percent_20261025.json`, with a supplementary corrected quote validation performed separately. This artifact's first failed quote row was a **literal text-line issue**, not a falsified source.

## QA
KRC isolated `krc-cobalt` full regression: **243/243 PASS**, 0 failures, 1.70 s (previous 240). Automated rule Critic and source evidence checks are not independent human scientific peer review. Scientific acceptance remains NO_GO.

## Follow-up
Digitize Figure 1/2 only with a defensible reproducible pixel-to-axis calibration protocol and clear uncertainty estimates. Avoid claiming plotted numerical validation without verified axes/labels and source image coordinates. Obtain independently verified raw readings or instrument precision before attributing eight one-meter-per-second residuals to rounding.

## Owner constraints
FREE_ONLY; no production, MEDIA, public-plugin deployment or external human reviewer signature. KRC and K_Science code/doc updates on existing branches only.
