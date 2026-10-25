# KRC × K_Science — EXT-S04 real-source pilot (2026-10-25)

## Selection / canonical registry
K_Science source: `literature/source_register/INTERNATIONAL_SEARCH_2026-10-23.md`, record **EXT-S04**.
Lencis, U.; Udris, A.; Kara De Maeijer, P.; Korjakins, A. (2024). *Methodology for Determining the Correct Ultrasonic Pulse Velocity in Concrete*. **Buildings 14(3), 720**. DOI: **10.3390/buildings14030720**.
Publisher full HTML: https://www.mdpi.com/2075-5309/14/3/720
Version notes: https://www.mdpi.com/2075-5309/14/3/720/notes
University research catalog: https://ortus0m.rtu.lv/science/en/publications/40038

## Source inspection / actual access
Publisher HTML sections **2. Measuring Devices and Concrete Specimens**, **3. Results** and **3.4 Methodology** inspected through public web text. It reports an UPV correction `kV=f(c;t;W;T)` for curing environment, age, moisture and temperature. Methods section describes 27 cube specimens in moisture/elevated-temperature testing and 28 cube specimens in a separate negative-temperature series. These are distinguished within the same publication, not treated as two independent article origins.

**Critical origin limitation:** The publication summarizes the results from previous publications and the Data Availability Statement says no new data created or analyzed in this study. Consequently, it is a methodological synthesis containing details of studies, **not two new independent experiments**, and source origin must be traced to the earlier works for evidence counting.

The publisher Version Notes record HTML updates on **2025-06-25** and **2026-08-28**. Their scientific effect was not assessed; an HTML update is not proof of correction or misconduct.

The original PDF binary URL `https://www.mdpi.com/2075-5309/14/3/720/pdf` returned HTTP 403 from the KRC server. Therefore **no authoritative PDF bytes, PDF SHA-256, figure extraction or reviewer-signed full-text attestation** were produced. Publisher HTML is not falsely classified as a hash-anchored PDF.

## Executed KRC offline research
Fixture: `tests/fixtures/kscience_ext_s04_real_article_pilot.json`, commit `58e560efeaf12710963dffd3849c5aaafdcc902f`.
Server command: `PYTHONPATH=src .venv/bin/python` importing `run_scientific_cycle()`, running the real KRC v3 code with the selected source, three paper-specific claims, **no invented inspection receipt or reviewer approval**.
Input SHA256: `346d961fbb379b99c394099317be7b4571d530af60934f69b6daa0d8ae0f7ad2`.
Source/claim mappings:
- **C01:** paper specifies four-factor coefficient `kV=f(c;t;W;T)` — **publisher HTML supports descriptive statement**, KRC independent evidence SHORTFALL (missing cryptographically attested source).
- **C02:** paper describes **27** cubes for an elevated-temperature study and **28** cubes for the negative-temperature study — publisher METHODS supports the report, independent origin validation SHORTFALL.
- **C03:** study proves a **universally valid standalone strength prediction** solely from corrected UPV — **UNSUPPORTED OVERGENERALIZATION** in the paper; KRC SHORTFALL requiring at least two independent scoped origins.

Observed KRC verdicts: `C01 SHORTFALL`, `C02 SHORTFALL`, `C03 SHORTFALL`; **deterministic Critic REVISE**, final `NO_GO`, publication-ready false.
Generated remote output `/tmp/krc-ext-s04-result-20261025.json` (not committed, no implied sandbox attachment).

## Live bibliography query
Actual `audit_bibliography(['10.3390/buildings14030720'])`:
- Crossref `METADATA_ONLY`
- Europe PMC `NOT_FOUND` (coverage limitation, not DOI invalidity)
- Crossref editorial updates `NO_UPDATES_RETURNED`
- overall `PARTIAL`
- retraction clearance `NOT_ESTABLISHED`
Remote output `/tmp/krc-ext-s04-bibliography-20261025.json`.

## Scientific assessment / independence
The article addresses UPV correction and confounding factors relevant to K_Science; **it does not establish a validated relation from geodetic adjustment to concrete compressive strength**. No independent reanalysis of measurements, uncertainties, table values or figures was executed. The word *Review* on the publisher issue and its Data Availability statement further motivate first tracing included experiments to original articles.

## Acceptance verdict
**SOURCE_CHOSEN=PASS / PUBLISHER_HTML_READ=PASS / LIVE_BIBLIOGRAPHIC_QUERY=PARTIAL / KRC_E2E_EXECUTED=PASS / INDEPENDENT_EVIDENCE_ATTESTATION=SHORTFALL / SCIENTIFIC_PUBLICATION=NO_GO.**

Next: obtain licensed original publisher PDF or authorized exact content snapshot; persist its SHA-256 and page locators; resolve historical experiment origins; obtain genuinely independent reviewer approval; rerun evidence and Critic; never auto-promote because a web page or DOI exists. No change to production, MEDIA or plugin.
