# KRC №81 — Crossref recovery with total drift and quantitative author-reported values
Date: 2026-10-25

## Scope / authorization
Owner approved continuation of P3/P4, FREE_ONLY; internal deterministic Critic, no invented external peer review. No production, MEDIA, public/plugin deployment or charged services.

## Implemented — P3
Updated `src/krc_research/paged_recovery.py` with bounded retries (max 2), exponential-ish short backoff, retryable network/HTTP conditions (429, 5xx), audit log of retry attempts, and an explicit opt-in `allow_total_drift` mode. Strict count equality stays default. When a changing index count is accepted explicitly, `provider_total_drift_detected=True`, `coverage_status=PARTIAL_TOTAL_DRIFT` and `complete_catalog_coverage=False`, even if the second page succeeds. Existing checkpoint SHA, page URLs, and original source records are preserved.

Additional tests in `tests/test_p0_paged_recovery.py` cover changing provider counts, bounded HTTP 429 retry and excessive retry count.

### Real Crossref recovery
Read original saved failed page-2 checkpoint in isolated `/tmp/krc-ext-s04-acceptance/paged_discovery_20261025.json`; a fresh direct check showed second-page HTTP 200 but provider reported a different total hits count than at page 1. Strict gate rightly failed before. New explicit-drift option made a new live page-2 call:
- `stopping_reason=MAX_PAGES_REACHED`
- `returned_unique_records=10` (previously 5)
- `pages=2`, page 2 status PASS
- original page 1 entry unchanged
- `provider_total_drift_detected=True`
- `coverage_status=PARTIAL_TOTAL_DRIFT`; `complete_catalog_coverage=False`.
This is a **bounded page recovery**, NOT proof of complete, reproducible Crossref index coverage. Isolated output `/tmp/krc-ext-s04-acceptance/crossref_recovery_v2_20261025.json`.

## Implemented — P4
New `src/krc_research/quantitative_table.py` validates a user/researcher supplied structured numeric row against exact text of a SHA256-checked source file, unit token and 1-based source page. The module returns provenance fields, row status and manifest hash, **not** instrument calibration/uncertainty validation or original experimental reproduction. It does **not automatically parse diagrams/tables**.

Added `tests/test_p0_quantitative_table.py`, which checks correct value, wrong value/unit, duplicate row, unsupported unit, bad source digest. The first live test run revealed a regex literal-escaping bug, which was corrected in commit `9578b420b927c00674fa7b0494646d0f129c4a62`; raw GitHub branch URL initially provided stale code, so staging used immutable commit URL and re-executed tests.

### Real journal PDF corpus numeric check
Original EXT-S04 MDPI `Buildings` (2024) publisher PDF at isolated `/tmp/krc-ext-s04-acceptance/buildings-14-00720.pdf`, SHA256 `9a40186cdce051ce2b8f313ea87af3e7c1b30653658621f0e7130679580fc07a`.
Physical PDF page 4, author-reported prior compression strength values:
- Mix A `53.7 MPa`, at `28 days` — `SOURCE_VALUE_MATCH`.
- Mix B `36.7 MPa` — `SOURCE_VALUE_MATCH`.
Both matched exact source text and unit; matching result `2/2`, manifest SHA256 `3feb21e79d69acf5d2e9b85bba29bcab31fb4f856dc430145485cd1b85023283`.
These are **structured extracted value references from prose**, not a separately verified experimental table or raw instrument readings.
`independent_experimental_validation=False`. Isolated output `/tmp/krc-ext-s04-acceptance/quantitative_mixes_v2_20261025.json`.

## Acceptance / tested boundaries
Full isolated regression on krc-cobalt after code refreshed from immutable commit: **222/222 PASS, 0 FAIL, 1.51s**. Previous baseline: 213.
Only internal engineering acceptance was reached. Full scientific acceptance **NO_GO**; original REF26 binary remains outstanding; no independent external scholarly reviewer was involved.
No source PDFs or temporary research outputs committed to repositories.

## Next
- P3: persist immutable provider snapshots externally for durable recovery, while honoring bounded free access and retention policy; add snapshot-level monotonicity checks and explicit publication-date filters.
- P4: parse accessible table/figure material and extract data series with exact row+column and uncertainty metadata; test consistency of computations and axes against originals.
- P2 external human scientific sign-off remains deferred to final acceptance per owner option 3.
