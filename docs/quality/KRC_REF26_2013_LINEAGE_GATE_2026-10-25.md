# KRC №72 — REF-26 university archive retry and physical specimen lineage gate
Date: 2026-10-25

## Research result
Selected K_Science source is EXT-S04 (2024, DOI 10.3390/buildings14030720). Origin REF-26 is Lencis, Udris & Korjakins, *Effect of Elevated Temperature Environment on Ultrasonic Pulse Velocity in Curing Concrete*, Civil Engineering '13, Part II pp. 11–18. REF-27 is their *Moisture Effect on the Ultrasonic Pulse Velocity in Concrete Cured under Normal Conditions and at Elevated Temperature* (2013), RTU original PDF checksum `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`.

REF-26 full university publisher proceedings text is indexed on the publisher PDF page: https://llufb.llu.lv/conference/Civil_engineering/2013/partII/Latvia_CivilEngineering2013Vol4Part2.pdf . Publisher extracted Table 1 at **physical PDF page 16 (index 15, printed p.14)** lists:
- N 1.28, 2.28, 7.28
- K 9.28, 11.28, 12.28
- KV 19.28, 21.28, 24.28

RTU-original REF-27 physical p.3 confirms precisely those nine specimen identifiers. Its Methods on p.2 explicitly says 9 specimens were previously used for elevated-temperature influence research. This is **same physical specimen cohort**, not a second independent specimen cohort. REF-27 has subsequently performed additional moisture measurements, which may constitute distinct observations; treat experiment/method/observation independence separately from specimen independence.

## Source-custody restrictions
Tried university RTU record /15928/fulltext; it returned HTML, not PDF. Tried `ortus0m.rtu.lv` PDF route, and university archives via `lbtufb.lbtu.lv` with HTTPS and `llufb.llu.lv` alternate; remote curl timed out. Public web text extraction of full publisher proceedings works and confirms printed table, but direct web PDF screenshot also timed out. **Therefore REF-26 physical PDF bytes and SHA256 are NOT verified.** No substitute archive file was disguised as the original.
REF-27 university PDF hash remains verified and has a previous 3/3 Methods/Results extraction PASS. No independent human reviewer assigned or signature issued.

## KRC engineering update
New module `src/krc_research/specimen_lineage.py`: canonical IDs, all pairwise physical specimen overlap counts and fail-closed review verdict. It expressly states no shared specimen IDs is not alone scientific independence proof. Tests `tests/test_p0_specimen_lineage.py` have positive case with 9/9 overlap plus negatives (duplicates, malformed IDs, disjoint samples).

`src/krc_research/scientific_cycle_v3.py` now accepts optional `package['specimen_lineage']` and records `specimen_lineage_audit`; any documented shared specimen cohort **blocks even conditional disciplinary gate** until independently reviewed. Added a regression in `tests/test_p0_scientific_cycle_v3.py`. This is a conservative gate, not an automatic causal determination.

Real isolated test run on `krc-cobalt`, `pytest -q tests/`: **139 PASS, 0 failures, 0.94s** (baseline 132). No production service restart, no new public network, MEDIA or plugin changes.

## Scientific Critic
- REF-26 publisher text identifies nine physical specimens: PASS TEXTUAL ONLY.
- REF-27 same specimen IDs and original PDF: PASS SHA-VERIFIED.
- REF-26 original PDF custody: SHORTFALL.
- Sample cohort independence REF26 versus REF27: **NOT INDEPENDENT (same nine specimens)**.
- Measurements may be different dates/different tests: **DO NOT TREAT AS DUPLICATE NUMERICAL OBSERVATIONS WITHOUT DATAPOINT MATCHING**.
- EXT-S04 adds no independent source dataset according to its own Data Availability statement.
- New authenticated independent human scientific review: NOT_RUN.
- Full scholarly acceptance: NO_GO.

## Next
Recover canonical original REF-26 PDF through an authorized university route if/when accessible; verify hash and original tables/plots; inspect original measurements, uncertainty, and sample chronology; arrange genuine independent research reviewer and a signed evidence review. Maintain FREE_ONLY.
