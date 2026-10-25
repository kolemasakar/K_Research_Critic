# KRC №80 — Crossref checkpoint recovery and literal numeric source audit
Date: 2026-10-25.

## Scope
P3 fail-closed recovery of interrupted free public bibliography queries. P4 report-only numeric/unit phrase checks in SHA-anchored original PDFs. Combined-review policy remains: deterministic Critic now; independent external scientist at final acceptance. FREE_ONLY. Production, MEDIA, public plugin untouched.

## Code and tests
- `src/krc_research/paged_recovery.py`: resume only a `PROVIDER_FAILURE` checkpoint with valid canonical manifest SHA, matching requested URLs, sequential prior pages and previous record counts. Preserve validated earlier page content, request the missing page onward, and **reject changed provider-reported total** or malformed page; record failed retry instead of pretending search completion.
- `tests/test_p0_paged_recovery.py`: five checks: resumed missing pages, checkpoint tampering, no pointless resume of finished run, count-change rejection, preserving prior results on retry failure.
- `src/krc_research/numeric_quote_audit.py`: compare exact decimal literal and adjacent unit inside hash-verified source passage with a declared numeric claim, reusing the existing source-file inspector; never assert numerical correctness or scientific truth.
- `tests/test_p0_numeric_quote_audit.py`: four tests including incorrect number, incorrect unit and changed document digest.
- Isolated complete test run on krc-cobalt: **213/213 PASSED**, zero failures, 1.23s. Prior baseline 204 tests.

## Actual original research corpus tests
Original EXT-S04 MDPI 2024 source PDF SHA256 `9a40186cdce051ce2b8f313ea87af3e7c1b30653658621f0e7130679580fc07a`, physical p4 Methods. Two numerical literals checked against exact excerpts:
- **53.7 MPa at 28 days** — LITERAL_NUMBER_IN_SOURCE.
- **36.7 MPa** — LITERAL_NUMBER_IN_SOURCE.

These are values the **authors report for two mixes** from previous experimental results; KRC did not independently verify compression machines, raw readings or uncertainty. `scientific_results_validated=False`. Remote output `/tmp/krc-ext-s04-acceptance/reported_numbers_20261025.json`.

Attempted a real restart from previously stored Crossref page-2 failure checkpoint `/tmp/krc-ext-s04-acceptance/paged_discovery_20261025.json`. Checkpoint signature/structure validated and previous five returned records remained intact. Re-request of page 2 did **not** yield an acceptable consistent result; recorded `PROVIDER_FAILURE`, `ValueError`, five records retained, no false promotion to full coverage. Remote output `/tmp/krc-ext-s04-acceptance/crossref_recovery_20261025.json`.

## Integrity / scientific Critic
- Engineering 213 PASS.
- Complete systematic literature discovery remains SHORTFALL; Crossref offset page remains incomplete.
- Quantitative source excerpt match is NOT measurement replication.
- Original REF26 PDF binary remains unverified.
- No independent academic reviewer, no source data reanalysis; SCIENTIFIC_ACCEPTANCE=NO_GO.
- Temporary test outputs and source PDF on remote server are not committed and subject to the agreed retention/cleanup policy.

## Next
Review sustainable live Crossref pagination with free-provider constraints; checkpoint adaptive retries and cautious total drift accounting. Build claim-to-table data extraction and unit-aware quantitative comparison with robust normalization; require human scientific examination before acceptance. Keep all public/production functions on hold.
