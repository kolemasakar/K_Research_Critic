# KRC №70 — EXT-S04 provenance trace to 2013 original reports (2026-10-25)

## Existing K_Science source
EXT-S04: Lencis, Udris, Kara De Maeijer, Korjakins (2024), `Methodology for Determining the Correct Ultrasonic Pulse Velocity in Concrete`, DOI `10.3390/buildings14030720`. Authenticated MDPI PDF SHA-256 already fixed in KRC №69: `9a40186cdce051ce2b8f313ea87af3e7c1b30653658621f0e7130679580fc07a`. This is a methodological consolidation with no new data reported.

## Direct precursor source REF26 (2013)
Lencis, Udris, Korjakins, `Effect of Elevated Temperature Environment on Ultrasonic Pulse Velocity in Curing Concrete`, Civil Engineering '13 conference proceedings, Part II pp. 11–18. Official institutional registry: https://ortus0m.rtu.lv/science/en/publications/15928 . University publisher full proceedings: https://lbtufb.lbtu.lv/conference/Civil_engineering/2013/partII/Latvia_CivilEngineering2013Vol4Part2.pdf .

Publisher-indexed FULL_TEXT was accessible via web textual indexing, including PDF viewer physical pp. 13–18 (report printed pp. 12–17). Key experimental facts:
- **27 concrete cubes, 15×15×15 cm**;
- ultrasonic device **UK-1401**, nominal 70 kHz and 15 cm measurement path;
- groups `N` standard moist-room, `K` released from formwork in elevated-temperature cycle, `KV` still in formwork for cycling;
- climatic chamber cycle **17 h at +10°C, 7 h at +30°C**;
- measurements of faces top, side and bottom; references to 9 diagonal tests per specimen face;
- Table 1 gives face-wise UPV percentage differences; Table 2 gives UPV changes after removal of surface concrete layers, e.g. group K average +4.6% after ~1.5 cm removal for seven-day specimens.
- 2024 EXT-S04 reports **27 cubes in the matching experimental setup**, specifically citing REF26 and REF27. This is strong provenance evidence for reutilization of the 2013 sample cohort in 2024. **Do not count 2013 REF26 and 2024 EXT-S04 as two independent experimental origins.**

This is a content-level qualitative cross-check of publisher-indexed text and tables, **not file-hash or independently signed review** for REF26. The LBTU university-hosted original full PDF repeatedly timed out over server HTTPS; no original binary SHA exists. Web PDF screenshot request also timed out, hence precise table layout/figures were NOT visually inspected and table extraction is tentative.

## REF27 (2013)
Lencis, Udris, Korjakins, `Moisture Effect on the Ultrasonic Pulse Velocity in Concrete Cured under Normal Conditions and at Elevated Temperature`, Construction Science 14:71–78, DOI `10.2478/cons-2013-0011`. Institutional registry: https://ortus0m.rtu.lv/science/en/publications/16677 . Institutional abstract supports moisture-dependent UPV under standard and elevated curing. Full-text access via institutional registry timed out. A third-party transcription exists but was not used for scientific primary evidence.
Live KRC `audit_bibliography(['10.2478/cons-2013-0011'])` on `krc-cobalt`: Crossref=METADATA_ONLY; Europe PMC=NOT_FOUND; Crossref updates=NO_UPDATES_RETURNED; overall PARTIAL and retraction clearance NOT_ESTABLISHED.
REF27 sample reuse relative to REF26: **POSSIBLE, NOT PROVEN**. Do not count REF27 as an independent experiment without actual specimen/dataset identification.

## Executed offline logic
Added frozen evidence-origin manifest `tests/fixtures/kscience_ext_s04_2013_origin_review.json`.
Added `tests/test_p0_ext_s04_prior_origin.py`: verifies two source citations sharing 2013 cohort count as only one independent origin, refuses a claimed PASS for a source with unavailable independent inspection and preserves REF27 unresolved status.
Real run `pytest -q tests/` in isolated `/tmp/krc-p0-offline-20261025` on `krc-cobalt`: **129 PASS / 0 FAIL in 1.01 s** (previous 126). Synthetic source citations in one regression test demonstrate accounting invariants; no authentic independent reviewer attestation was created.

## Verdict
- Original 2013 sources identified: **PASS**
- REF26 original manuscript indexed and Methods/Results qualitatively compared: **PARTIAL** (no cryptographic binary custody)
- REF26 / EXT-S04 sample cohort reuse: **HIGH-CONFIDENCE_SOURCE_REUSE**
- REF27 reuse: **UNRESOLVED**
- Independent original data replication: **SHORTFALL**
- KRC core accounting regression: **PASS 129/129**
- Full scientific admission: **NO_GO**

Immediate next: retrieve REF26/REF27 publisher PDFs via accessible authorized routes, compare original experiment identifiers and tables; obtain independent reviewer signature. Keep FREE_ONLY and production/MEDIA unchanged.
