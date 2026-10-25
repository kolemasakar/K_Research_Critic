# KRC №79 — paged scholarly discovery and exact claim/source passages
Date: 2026-10-25

## Scope
Owner-approved P3/P4 internal development. FREE_ONLY. External scientific reviewer required only at final scientific admission; no claimed reviewer approval, no production, MEDIA or public plugin changes.

## Code implemented
- `src/krc_research/paged_discovery.py`: real bounded Crossref/OpenAlex paging (max 5 pages, max 10 results/page), per-page URL, timestamp, raw normalized JSON SHA-256, raw/unique hit counts, explicit stopping reason and fail-closed partial provider failure. Its `scoped_prisma_flow` reports identified records, DOI duplicate count, unresolved work and missing DOI counts **for retrieved pages only**, not a complete systematic PRISMA study.
- `src/krc_research/claim_passage_links.py`: page-bound claim-source locators via the existing hash-checked PDF/Markdown file inspector; checks exact phrases, source file SHA and approved root; does not automatically establish scientific support or reviewer acceptance.
- Added 8 page/discovery tests and 5 passage tests. Full isolated `pytest -q tests/` on krc-cobalt: **204/204 PASS, zero failures** (baseline 191).

## Live EXT-S04 pagination
Query: `Methodology for Determining the Correct Ultrasonic Pulse Velocity in Concrete`, page_size=5, max_pages=2 for both public indexes.
- Crossref page 1: 5 results; page 2: **HTTPError**; status `PROVIDER_FAILURE`, 5 retained records.
- OpenAlex page 1+2: 10 results; stop `MAX_PAGES_REACHED` (catalog not fully searched).
- Only 15 actually returned provider rows; **14 distinct DOI**, **1 cross-provider DOI duplication**, **1 selected follow-up DOI** `10.3390/buildings14030720`, **13 unresolved**, zero studies accepted into full-text systematic synthesis.
- The result is a **partial scoped search**, not an exhaustive worldwide systematic review and not 14 independent experiments.
- Actual remote output `/tmp/krc-ext-s04-acceptance/paged_discovery_20261025.json`. Both queries are bounded, free only; failures not disguised as empty results.

## Actual hashed scientific corpus passages
Three requested locators verified on real PDFs saved in isolated environment:
- C01 / EXT-S04 publisher PDF: physical page 3 Methods, "Three devices were used to measure the UPV"; PDF SHA256 `9a40186cdce051ce2b8f313ea87af3e7c1b30653658621f0e7130679580fc07a`.
- C02 / REF-27 original RTU 2013 PDF: physical page 2 Methods, "9 concrete specimens"; PDF SHA256 `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c`.
- C03 / EXT-S04 publisher PDF: physical page 14 Limitations, "No new data were created or analyzed in this study."
- All three returned `EXACT_PASSAGE_FOUND`. **This verifies literal quote presence only, not that a corresponding scientific claim is supported**. No independent reviewer attestation issued and `all_scientific_claims_validated=False`.
- Result `/tmp/krc-ext-s04-acceptance/claim_passages_20261025.json`.

## QA and limitations
- Technical regression PASS: 204/204.
- Crossref continuation failed; correct partial stop.
- PRISMA flow remains scoped to received results only, not full systematic study including eligibility, exclusion rationale and independent review.
- REF-26 original publisher PDF SHA still unavailable.
- Scientific peer review NOT RUN, scholarly publication status NO_GO.
- No live production deployment.

## Next tasks
Implement retry/backoff and recovery checkpoints for paginated public metadata while respecting free API rate limits and deterministic constraints; apply transparent source eligibility criteria, snapshot content hashes, and separate figure/table quantitative checks with independent verification.
