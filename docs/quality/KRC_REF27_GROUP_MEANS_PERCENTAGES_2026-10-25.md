# KRC №83 — REF-27 Table I group means and percentages (2026-10-25)

## Controlled source
Lencis, Udris, Korjakins, *Moisture Effect on the Ultrasonic Pulse Velocity in Concrete Cured under Normal Conditions and at Elevated Temperature*, Construction Science 2013, DOI 10.2478/cons-2013-0011. Official RTU PDF https://ortus.rtu.lv/science/en/publications/16677/fulltext, SHA256 `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`. Physical PDF page 3, Table I. Nine N/K/KV specimens. Reuses physical cohort from REF-26; not an independent sample set.

## New code
`src/krc_research/ref27_group_audit.py` recomputes arithmetic means from the publisher-reported three specimen values per group. Published delta means are rounded HALF_UP in m/s; percent changes are computed as ratios of group mean UPVs for saturated/dry, air-dry/dry, saturated/air-dry respectively, rather than means of already-rounded individual percentages. Input fixture `tests/fixtures/ref27_upv_table_i.json`. Three regressions in `tests/test_p0_ref27_group_audit.py`.

## Actual results
| Group | Sat-dry m/s | Air-dry m/s | Sat-airdry m/s | Sat-dry % | Air-dry % | Sat-airdry % |
|---|---:|---:|---:|---:|---:|---:|
| N | 724 | 545 | 179 | 18 | 13 | 4 |
| K | 706 | 464 | 242 | 18 | 12 | 5 |
| KV | 753 | 520 | 233 | 19 | 13 | 5 |

**All 18 group cells agree** with the source-printed Table I, under the explicit rounding/percentage method. Prior check of individual specimen arithmetic remains **19/27 exact**, **8 residuals ±1 m/s**. These residuals remain unresolved; group-level consistency is NOT proof that unrounded source observations or methodology are scientifically validated.

Executed `audit_ref27_group_averages` on isolated krc-cobalt with nine genuine source-extracted rows. Full isolated `PYTHONPATH=src .venv/bin/python -m pytest -q tests/` **240/240 PASS, 0 failures, 1.60 sec**, after incorporating 3 tests (previous 237).

## Critic and limitations
- Group table printed vs recomputed: PASS_ARITHMETIC_WITH_DECLARED_ROUNDING.
- Individual differences: 8 unresolved one-unit deviations, no default tolerance.
- Figures 1/2 contain plots, but numerical series/figure coordinates were **not extracted or checked in this run**. No unwarranted claim of independent graph validation.
- No source raw instrument measurements, uncertainty model or external independent human reviewer.
- Scientific acceptance NO_GO, publication_ready false.

## Next
Inspect reproducible figure/table relation only where original figure data and labels are accessible; independently test percentage definition and rounding alternatives; check whether raw measurement precision/uncertainty is specified. Maintain internal FREE_ONLY; no production, MEDIA or public changes.
