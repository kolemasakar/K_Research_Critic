# KRC P0-A/B/C/D integration checkpoint — 2026-10-25

## Execution scope
Owner approved P0-A canonical consolidation, P0-B Search/DOI/Source Ledger, P0-C linking to Critic and P0-D full-cycle acceptance. This checkpoint records **first engineering implementation**, not full P0-D completion. Branch `agent/krc-public-media-r3-integration`. No production, public, MCP server or MEDIA changes. PRIVATE plugin v0.19.14 remains unchanged.

## Files added
- `src/krc_research/canonical_evidence_ledger.py` — deterministic accounting of explicitly inspected scoped independent origins; abstract, metadata, unknown provenance, duplicates and mismatched scope do not count. Legacy v1.4 importer preserves historical verdicts only as reported and resets newly verified counts to zero.
- `src/krc_research/source_search_ledger.py` — SearchRun with exact provider, query, timestamp, hits, export count, and source DOI status; incomplete observations are PARTIAL_LOG not invented.
- `src/krc_research/scholarly_preflight.py` — offline aggregation of evidence, search log and existing manuscript gate; even a completely passing fixture never equates to journal acceptance or automatic publication readiness.
- `tests/test_p0_canonical_evidence_ledger.py` (12 test definitions after added cases).
- `tests/test_p0_source_search_ledger.py` (6 test definitions).
- `tests/test_p0_scholarly_preflight.py` (5 test definitions).

## Dataset-specific migration smoke check (executed)
Input: owner-uploaded `KRC_P07_claim_ledger_20261023_v1_4.json`.
- 12 unique C IDs, required>=1, all historical verdict/count comparisons consistent.
- Historical reported statuses **7 PASS / 5 SHORTFALL**.
- C09 is missing the `evidence_urls` key; migration handles absent URL list as empty, never invents evidence.
- Produced `KRC_CANONICAL_LEDGER_IMPORT_20261025.json` (conversation-local output, not committed) with **IMPORTED_UNVERIFIED**, 0 newly inspected experimental origin records, all independent accepted counts 0 in newly imported context. This does **not downgrade the earlier historical audit**; it correctly separates an import from real independent rereading.

## Verification limitations
New GitHub Python test functions have been committed but **were not executed on the actual GitHub source in this checkpoint**. An isolated local legacy-data migration smoke check did execute successfully, and code was fetched/inspected; do not label GitHub modules 23/23 PASS. No live Crossref/Crossmark provider connector or DOI retraction feed is integrated by the new offline code. `provenance_verified` is still an input assertion, not an independently established experimental lineage. No private-plugin runtime linkage, no automatic DOCX/PDF chart preservation, no author/journal final signoff.

## P0-D next gate
1. Run test suite on checked-out GitHub branch in reproducible Python environment; capture Python/pytest version, commit and exact stdout.
2. Wire SearchRun and Evidence collection to real permitted source providers, with search snapshots and first-party provenance signatures.
3. Implement a single canonical Critic output schema from the source ledger, including per-claim counted and excluded sources, correction/retraction status, exact checked passages and approval timing.
4. Re-run Scholarly path in installed private plugin with sample manuscript; verify end-to-end output vs offline module counts, including actual DOCX/PDF.
5. Human author/journal integrity approval and only then consider manuscript publication readiness.

Final status: `P0-A IMPLEMENTED_OFFLINE`; `P0-B SPEC+OFFLINE_VALIDATOR`; `P0-C OFFLINE_PREFLIGHT`; `P0-D NOT_YET_END_TO_END_ACCEPTED`. PZ still last per canonical Roadmap.
