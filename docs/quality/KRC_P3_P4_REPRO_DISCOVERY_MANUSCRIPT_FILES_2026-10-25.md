# KRC №78 — P3 reproducible discovery, P4 manuscript-file claim trace
Date: 2026-10-25

## Scope
Owner-approved: automatic internal Critic now; independent external reviewer only for final scientific acceptance. FREE_ONLY, no production/public/MEDIA deployment.

## P3 implemented and tested
New `src/krc_research/reproducible_discovery.py` merges **bounded actual Crossref/OpenAlex query records** by normalized DOI; preserves each provider name, exact request URL/query, execution time, response digest and independent screening decision with rationale. Missing decisions automatically become `UNRESOLVED`; provider failures are separately surfaced; citations from two catalogs are **not counted as two experiments**.

`tests/test_p0_reproducible_discovery.py`: eight cases incl. aliases, unknown decisions, malformed provider export counts, duplicate query runs and metadata-only evidence guard.

### Actual K_Science EXT-S04 provider corpus
Replayed live Crossref/OpenAlex outputs from previous turn's two network calls for exact-query EXT-S04 (`/tmp/krc-ext-s04-acceptance/live_discovery_20261025.json`). Ten returned hits (five per catalog), **nine distinct normalized DOI records**, with one DOI `10.3390/buildings14030720` returned by both services.
- INCLUDE: EXT-S04, narrow relevance to UPV correction methodology.
- UNRESOLVED: 8 other DOI records, because full text has not been assessed.
- EXCLUDE: 0.
- Provider failures: 0 in this replay; manifest status PARTIAL due eight unresolved screening decisions.
- Manifest SHA256 `1e256398acbbd4023a114648eb7fa925d9e0d7a1ad04afd136ccd689d0211070`.
- The 9 refer to ten *returned hits*, NOT entire searched catalogs, systematic review yield or nine independent scientific experiments.
- Source body or experimental truth: not established from public metadata.
- Isolated output `/tmp/krc-ext-s04-acceptance/reproducible_discovery_20261025.json`.

## P4 implemented and tested
New `src/krc_research/manuscript_file_trace.py` verifies actual Markdown source files within approved directory, disallows symlinks/path traversal/reused paths/oversized files, computes SHA256 of actual bytes and requires exactly one matching text anchor per declared research claim and revision. Each version is independently passed to existing real `audit_manuscript_revisions` and Critic re-execution.

`tests/test_p0_manuscript_file_trace.py`: six new tests incl. duplicated passages, missing claim, changed actual document, path escape and symlink.

### Actual K_Science EXT-S04 markdown-file trial
Two **short methodological note files**, NOT a full-length scientific publication, authored and read on isolated host:
- `/tmp/krc-ext-s04-acceptance/manuscript-revisions/v1.md` SHA256 `69f50724edda24d4607e753f70f82a9249257f6f61e916928c08047fc5c3da0b`; unrevised generalization.
- `/tmp/krc-ext-s04-acceptance/manuscript-revisions/v2.md` SHA256 `a520d315a6a37f4a187adf09e7c1c85c71b4d985eb00a0862dd6502da136935f`; narrowed claim scope and stated nine reused REF26/REF27 samples.
- All claims C01/C02/C03 anchored uniquely at physical Markdown lines **3/5/7** in each version, matching the actual text content.
- 1 actual document revision; 2 actual package critic executions; verdicts `REVISE / REVISE`, final NO_GO. No independent reviewer, no original raw experimental data validation.
- Output `/tmp/krc-ext-s04-acceptance/real_manuscript_files_20261025.json`.

## Tests / correction log
Initial 189 PASS / 2 FAIL: test-fixture erroneously encoded literal `\\n` instead of newline, causing both line-position and duplicate-locator failures. The fixture was corrected without modifying the production code. Rerun **191/191 PASS**, zero failures (1.21s) on isolated `krc-cobalt`.

## Limits
- Bibliographic search was bounded top-five from each provider and does not satisfy full systematic review recall.
- Markdown claim anchors verify literal presence and source-file hashes, not correspondence with underlying experimental truth or citation correctness.
- Experimental independence of REF26/REF27 remains sample-overlap dependent; signed human scholarly review NOT RUN by approved owner option 3.
- Production, public plugin, MEDIA untouched.
- SCIENTIFIC_ACCEPTANCE: NO_GO.

## Next engineering steps
Systematic free-index pagination and declared stopping criteria/PRISMA counts; snapshot storage for exact reproducibility and correction/retraction status, then substantive experimental results extraction from primary evidence and manuscript-level scientific integrity Critic.
