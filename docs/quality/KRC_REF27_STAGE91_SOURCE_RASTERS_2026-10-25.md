# KRC №91 — original REF-27 raster admission (2026-10-25)

Canonical PDF uploaded by owner: `pub16677.pdf`, 230806 bytes / 8 pages.
SHA256 `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c` **PASS**, matches archived RTU original of DOI 10.2478/cons-2013-0011.

Original PDF physical page 4 has two embedded raster objects, extracted directly with `pdfimages -f 4 -l 4 -png`:
- Figure 1, 865×526 px: UPV m/s against water absorption % for N/K/KV.
- Figure 2, 865×487 px: decline of UPV m/s against time in hours for N/K/KV.

Single-inspector, approximate axes (NOT scientific plot-point admission):
- Fig1 x 104→829 pixels corresponds to 0→6%; y 410→55 corresponds to 3900→4900 m/s.
- Fig2 x 103→836 corresponds to 0→180 hours; y 77→436 corresponds to 200→400 m/s. Fig2 vertical coordinate increases downward by design.
- Illustrative **only** ±3 px axis tick location translates to ±0.0248 percentage points / ±8.45 m/s (Fig1), ±0.737 h / ±1.67 m/s (Fig2). Excludes plotted point, printing and instrument uncertainty.
- Source PDF physical p2 does explicitly state manufacturer UK-1401 ultrasonic speed/time measuring error ≤±1%; this updates the earlier limited source search that could not establish a declared instrument accuracy. It is not original unrounded readings or a traceable uncertainty budget.

Current gate: PDF SHA PASS; original figure extraction PASS; axes PRELIMINARY_SINGLE_INSPECTOR; independent second-pass axis and per-curve coordinates SHORTFALL; graph↔Table I quantitative validation NO_GO; scientific review NO_GO. Full 249/249 regression **not rerun**. FREE_ONLY and production/MEDIA/public pauses unchanged.
