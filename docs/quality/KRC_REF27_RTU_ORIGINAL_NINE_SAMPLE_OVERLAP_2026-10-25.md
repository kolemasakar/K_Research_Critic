# KRC №71 — original RTU REF-27 and exact experimental specimen overlap (2026-10-25)

## Source selection
K_Science EXT-S04 (2024, DOI 10.3390/buildings14030720) cites two same-team precursor studies:
- REF-26: Lencis, Udris, Korjakins, 2013, *Effect of Elevated Temperature Environment on Ultrasonic Pulse Velocity in Curing Concrete*, Civil Engineering '13, pages 11–18. Official publisher PDF (web-indexed, not host-downloadable): https://lbtufb.lbtu.lv/conference/Civil_engineering/2013/partII/Latvia_CivilEngineering2013Vol4Part2-11-18.pdf
- REF-27: Lencis, Udris, Korjakins, 2013, *Moisture Effect on the Ultrasonic Pulse Velocity in Concrete Cured under Normal Conditions and at Elevated Temperature*, Construction Science 14, pages 71–78, DOI 10.2478/cons-2013-0011. Original RTU institutional PDF: https://ortus.rtu.lv/science/en/publications/16677/fulltext

## Original REF-27 binary captured
The exact RTU university Full text link returned a PDF on krc-cobalt; **8 pages**, **230,806 bytes**, SHA256:
`4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`.
Isolated file path `/tmp/krc-ext-s04-acceptance/ref27_rtu_original_2013.pdf` (not stored in repository). PDF title and DOI match institutional bibliographic entry.

KRC `source_file_inspection.inspect_source_file` execution: `TEXT_MATCH_WITH_METHODS_RESULTS`, 3 of 3 passages found, pages **2** METHODS ("9 concrete specimens", "initially were employed") and **3** RESULTS ("maximum water absorption"). PDF hash tied to actual inspected bytes; output `/tmp/krc-ext-s04-acceptance/ref27_inspection.json`. It is **not** a reviewer-signed attestation.

## Sample-level cross-check
- REF-26 Table 1, publisher indexed PDF page 4 (printed page 14): nine specimen identifiers, groups N (1.28, 2.28, 7.28), K (9.28, 11.28, 12.28), KV (19.28, 21.28, 24.28).
- REF-27 original RTU PDF physical page 3 (printed page 73), Table I: **identical nine identifiers**:
  - N-1.28, N-2.28, N-7.28
  - K-9.28, K-11.28, K-12.28
  - KV-19.28, KV-21.28, KV-24.28
- REF-27 original Methods, physical p.2: explicitly states that nine 15×15×15 cm concrete specimens were **initially used for elevated temperature impact research**, and then reused in a moisture-saturation study. Same ultrasonic tester UK-1401 and a +10°C/17 h, +30°C/7 h climatic cycle.
- REF-26 describes **27** specimens overall, whereas REF-27 uses a **nine-specimen subset** drawn from the earlier trial. This is a strong **same-specimen subset** conclusion supported by exact IDs and first-hand REF-27 PDF. These may represent different **measurements** performed at different times; they are **not independent specimens**. Independence must be evaluated by claim/dataset, not number of publications.
- EXT-S04 (2024) summarizes prior investigations, with Data Availability claiming no new data created or analyzed. Do not count 2024 as another independent experimental origin.

## Boundary / unresolved
REF-26 primary publisher PDF is indexed and its Table 1 accessible via web, but direct download attempts to KRC server repeatedly timed out. Its binary SHA is unknown. Web screenshot also timed out; tabular alignment was checked by indexed text but **not visually validated against the binary**. REF-27 original full PDF IS hash verified. No independent scientific reviewer or cryptographically signed human attestation for either. Full raw data, precision, uncertainty and duplicate-set validation not run; no scientific claim promoted to validated PASS.

Live bibliography for REF-27: Crossref METADATA_ONLY, Europe PMC NOT_FOUND, editorial updates NO_UPDATES_RETURNED; retraction clearance NOT_ESTABLISHED.

## Implemented and tested
Updated evidence fixture `tests/fixtures/kscience_ext_s04_2013_origin_review.json` with university PDF digest, 8 page custody, nine exact sample IDs and one-origin policy.
Updated `tests/test_p0_ext_s04_prior_origin.py` with exact-ID and actual-publisher-custody assertions.
Executed isolated `pytest -q tests/` on `krc-cobalt`: **132 PASS / 0 FAIL in 0.93s**.

## Acceptance
- Official REF-27 8-page binary, SHA and exact text passages: **PASS**
- REF-26 vs REF-27 same specimen IDs: **HIGH_CONFIDENCE_CROSS_SOURCE_MATCH**
- Claim-specific independent experiment counting: **SHARED_SPECIMEN_COHORT; DO_NOT_DOUBLE_COUNT**
- REF-26 original PDF on KRC: **SHORTFALL**
- Authenticated independent human scientific review: **SHORTFALL**
- Full scholarly research acceptance: **NO_GO**
- KRC deterministic engineering regressions: **132/132 PASS**

Next: obtain REF-26 publisher PDF with hash, verify tables visually and check any data-level conflicts, then ask an authorized independent reviewer to inspect originals and sign a scoped review; until then keep NO_GO.
