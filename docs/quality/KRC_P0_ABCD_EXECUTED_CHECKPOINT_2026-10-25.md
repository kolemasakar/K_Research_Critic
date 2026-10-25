# KRC — P0-A/B/C/D executed checkpoint (2026-10-25)

## Scope and safety
Branch `agent/krc-public-media-r3-integration`. Private plugin 0.19.14 remains unchanged and NO_MCP/FREE_ONLY. No service/system package installation, public/MEDIA/production deploy, daemon restart, or third-party manuscript upload. Executed isolated read-only metadata calls and Python tests under `/tmp/krc-p0-offline-20261025` on the authorized `krc-cobalt` host. The sample CLI output contains only an *abbreviated reconstruction* of the owner's v1.4 ledger statuses; it is not a byte-level copy of the original JSON.

## 1: Tests of fetched GitHub code
Python 3.12.3 on KRC server; `pytest` not installed. Tests run by a stdlib Python test harness that executes each `test_*` function and implements just the `pytest.raises` context manager. This is **not pytest execution**, and no full runtime coverage or CI claim is made.
- 28/28 PASS across previous 4 modules
- 33/33 PASS after metadata adapter
- 35/35 PASS after editorial correction cases
- **37/37 PASS** after executable offline acceptance boundary.
All staged code/test files were fetched from GitHub by the GitHub connector and written to an isolated temp directory before running.

## 2: Real FREE_ONLY providers
- Added `src/krc_research/public_metadata_adapters.py`: Crossref DOI lookup, Europe PMC DOI search, Crossref editorial update lookup. Fixed allowlist bug caught by first live update test; reran tests and live lookup.
- Live Crossref+Europe PMC HTTP metadata available for exact DOI: `10.1038/s41467-021-22662-7`, `10.1021/nn204476h`, `10.1038/nmat2725`. All are **METADATA_ONLY**, not method or results inspections, not new independent experiment origins.
- Live Crossref `filter=updates:10.1038/nmat2725` returned erratum DOI `10.1038/nmat2749` with publisher relation type `erratum`, update date 2010-03-19. `retraction_clearance=NOT_ESTABLISHED`, not 'no retractions'.
- Provider design pinned to fixed allowlisted HTTPS hosts, bounded response size, timeout, exact DOI equality checks, no paid fallback. Crossref use and European PMC public APIs are documented; usage rates and terms must be respected.
- No bulk 18-record full retraction or novelty/screening audit has been completed.

## 3: Connection to Critic
- Added `src/krc_research/offline_acceptance.py`, executable as `python -m krc_research.offline_acceptance input.json output.json`.
- Canonical evidence status, reproducible SearchRun records, and manuscript gates feed `scholarly_preflight`.
- A private skill-only NO_MCP plugin **cannot call these GitHub Python modules by virtue of mentioning them in instructions**. Runtime plugin linkage remains **NOT_CONNECTED**. No simulated or falsely claimed integration.

## 4: P0-D partial real end-to-end check
- Created minimal fixture that faithfully preserves only the 12 IDs and *historical pass/shortfall statuses* from owner v1.4 (`7 PASS / 5 SHORTFALL`); not identical to full original attached JSON.
- Executed CLI to JSON on server. Result: historical 7/5 retained in `IMPORTED_UNVERIFIED`; 0 freshly verified method/results origins; new ledger 0 PASS /12 SHORTFALL; no dated search runs; manuscript gates open; `REVISE`, `NO_GO`, `submission_ready=false`. This is the correct fail-closed behavior, not a claim that earlier verified scientific findings were false.
- Created an engineering acceptance QA report in DOCX and PDF in the current conversation. DOCX rendered to two pages and inspected. It is **not** the full scientific manuscript export.
- A real plugin runtime from CriticProfile -> research -> canonical executed Python -> Critic -> author-approved journal manuscript and DOCX/PDF **has not been performed**. Therefore P0-D PARTIAL/NO_GO.

## Next explicit prerequisites
1. Determine and implement a supported execution boundary for private plugin, or retain NO_MCP and treat the offline preflight as manually invoked external QA. Do not violate paused publication/MCP rules silently.
2. Establish true dated search exports and automated passage-level inspected source references with reviewer-visible evidence provenance; no metadata-to-fulltext laundering.
3. Finish DOI/retraction checks for all bibliography items and genuine novelty check.
4. Execute live installed-plugin acceptance, export parity (DOCX/PDF images, formulas) and human author/journal approval. AI detector actual results only if accessible and expressly permitted; scores never invented.
5. Formal destructive negative/fault campaign remains PZ, last per roadmap.

Current private release 0.19.14; status: P0-A offline implementation PASS; P0-B metadata provider implementation PASS on three tested DOIs; P0-C offline integration PASS; P0-D runtime integration NOT_CONNECTED, full publication readiness NO_GO.
