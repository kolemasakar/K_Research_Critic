# KRC №82 — REF-27 Table I arithmetic audit and publication-date screening
Date: 2026-10-25

## Authorization and scope
Internal research engineering only, FREE_ONLY. No changes to KRC production, public plugin, MEDIA, reviewer credentials or payment services. Independent human scientific review is deferred under approved combined policy.

## Primary experimental source
Lencis, Udris, Korjakins (2013), *Moisture Effect on the Ultrasonic Pulse Velocity in Concrete Cured under Normal Conditions and at Elevated Temperature*, Construction Science 14, 71–78, DOI **10.2478/cons-2013-0011**.
RTU publisher/institution original PDF: https://ortus.rtu.lv/science/en/publications/16677/fulltext
Original PDF SHA256: `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`
Table I located on **physical PDF p3** (printed p73).

## Structured UPV-series recalculation
Transcribed nine rows into `tests/fixtures/ref27_upv_table_i.json`, checked all nine specimen IDs and all four UPV stage values against source's extracted p3 Table I text. Source printed delta columns were mapped to three explicit difference comparisons, avoiding their presentation order ambiguity:
- max-saturation UPV minus dry UPV
- max-saturation UPV minus air-dry UPV
- air-dry UPV minus dry UPV.

Implemented `src/krc_research/upv_series_recalc.py`: decimal arithmetic, strict exact match by default, explicit optional tolerance with per-delta residuals; never infer raw instrument precision or experimental validity. Six basic tests plus two actual-source fixture tests.

**Actual RTU source results:** 9 specimens × 3 reported differences = **27 arithmetic comparisons**; **19 exact matches**, **8 residuals of ±1 m/s**, **0 residuals larger than 1 m/s**. All 27 would pass *only if* an explicit ±1 m/s tolerance were applied. Such a tolerance was used only as a sensitivity analysis: there is **no independent confirmation** from unrounded raw data whether differences reflect publication rounding, transcription, or another issue. Strict default still records eight deviations. Three specimen rows are strictly exact in all three differences. Numerical summary output: `/tmp/krc-ext-s04-acceptance/ref27_table_i_recalculation.json`.

### Per-row delta residuals (calculated minus source printed; m/s)
| ID | Saturated−dry | Saturated−air-dry | Air-dry−dry |
|---|---:|---:|---:|
| N-1.28 | +1 | 0 | 0 |
| N-2.28 | 0 | −1 | 0 |
| N-7.28 | −1 | 0 | −1 |
| K-9.28 | 0 | +1 | 0 |
| K-11.28 | 0 | 0 | 0 |
| K-12.28 | +1 | +1 | 0 |
| KV-19.28 | +1 | 0 | 0 |
| KV-21.28 | 0 | 0 | 0 |
| KV-24.28 | 0 | 0 | 0 |

REF-27 uses nine reused concrete cubes from predecessor REF-26: **do not count these as independent physical specimen cohorts**. Calculating from source-printed rounded UPV values is an internal arithmetic consistency check, **not independent experiment replication**. No original raw UPV measurements, uncertainty propagation, instrument calibration records or independent reviewer signature obtained.

## P3 source publication date screen
Implemented `src/krc_research/publication_date_screen.py` with 7 tests: exact ISO day, inclusive period bounds, mandatory provider origin, missing dates UNRESOLVED rather than silently accepted, duplicate source rejection, deterministic manifest digest. It does not prove the first day of public dissemination or novelty.

Live Crossref DOI metadata consulted:
- EXT-S04 DOI 10.3390/buildings14030720: `published.date-parts = [2024,3,7]`
- REF-27 DOI 10.2478/cons-2013-0011: `published.date-parts = [2013,1,1]` — **the 1 January day may be a default/placeholder** and is **not independently checked against print issue release date**.
- REF-26: precise ISO day unknown and stored as `UNRESOLVED_DATE`, rather than inferring a day from publication year.

Example bounded 2013-01-01..2024-12-31 filter: 2 `IN_PERIOD`, 1 `UNRESOLVED_DATE`. Output `/tmp/krc-ext-s04-acceptance/publication_period_20261025.json`.

## Engineering acceptance
Isolated `krc-cobalt` full `PYTHONPATH=src .venv/bin/python -m pytest -q tests/`: **237/237 PASS, zero failures, 1.61 s**, exit 0. Previous baseline 222 PASS.

## Important limitations and Critic
The nine manual transcribed rows are supported by literal text in original PDF, but **no visual inspection of print table cells or original raw experimental data was performed in this run**. Numeric discrepancies are **not proof of erroneous original scientific measurements**. Figure curves were not digitized; no interval/statistical uncertainty was independently recalculated. The date screening relies on publisher/index metadata and cannot certify date authenticity. No independent human review at this phase. **Scientific acceptance: NO_GO**.

## Next execution priorities
Recompute published group averages and percentages from printed table with explicit denominator / rounding assumptions; verify table to figure concordance only with inspectable original figure data; improve publication date precision handling for Crossref YYYY-only metadata and uncertainty. Keep results fail-closed and internal.
