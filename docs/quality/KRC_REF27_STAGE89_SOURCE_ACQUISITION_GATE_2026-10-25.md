# KRC №89 — REF-27 source acquisition gate (2026-10-25)

## Scope
Isolated research only. FREE_ONLY. No production, MEDIA, public access or scientific approval changes.

## Primary source
Lencis, Udris, Korjakins (2013), DOI 10.2478/cons-2013-0011.
Original institutional PDF: https://ortus.rtu.lv/science/en/publications/16677/fulltext
Required SHA-256: 4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c

## Attempted acquisition
- Web opened the official institutional endpoint, but its binary response was not accessible as original file bytes.
- Container HTTPS request failed at DNS resolution for ortus.rtu.lv.
- No original PDF, verified axes or plotted coordinates have been obtained.

## Test run
The local extraction utility ref27_extract_figures.py and its three synthetic tests were rerun: 3/3 PASS. This is not scientific validation of the real plots. The KRC 249/249 baseline was not rerun in this stage.

## Gate
- Extraction mechanism: synthetic-only PASS.
- Original PDF SHA custody: BLOCKED.
- Figure 1/2 axes, curves, Table I quantitative comparison: SHORTFALL.
- Scientific acceptance: NO_GO.

## Next
Acquire bytes in approved isolated host and compare exact SHA before any extraction. If matched, rasterize physical page 4, capture true graph dimensions and independently verify two ticks per axis, compute pixel-to-value mapping with extraction uncertainty, compare with Table I, rerun Critic and full KRC tests. Never replace actual graph data with synthetic coordinates.