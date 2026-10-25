# KRC №77 — live FREE_ONLY scholarly discovery and manuscript Critic revision
Date: 2026-10-25

## Scope and preserved policy
P3 live public Crossref/OpenAlex metadata lookup and P4 manuscript text diff with actual KRC Critic re-execution. Owner approves automatic Critic now; independent external scientific reviewer is mandatory at final scientific acceptance. No production, MEDIA, public plugin, or billed-provider work.

## Implemented
- `src/krc_research/public_discovery.py`: FREE_ONLY Crossref and OpenAlex search, HTTPS/host/path allowlist, 1–10 records, response size cap, explicit execution timestamp, exact URL/query, bounded timeout and fail-closed provider errors. Returned records are always METADATA_ONLY.
- `reconcile_discovery`: normalizes provider DOI variants, counts the same DOI in two catalogs as **one bibliographic work**, and reports **zero scientifically verified independent experimental origins**.
- `src/krc_research/manuscript_revision.py`: 2–5 manuscript snapshots, mandatory actual text diff, per-manuscript SHA256, added/removed line counts, requires separately changed research packages, invokes `execute_revision_history` and deterministic Critic for every revision. This records reviewed *supplied* changes, not autonomous writing or factual scientific validation.
- New tests `test_p0_public_discovery.py` and `test_p0_manuscript_revision.py`. Current isolated krc-cobalt complete regression: **177/177 PASS, 0 failures, 1.02s**; previous baseline 161.

## Actual live provider queries (not simulated)
Query: `Methodology for Determining the Correct Ultrasonic Pulse Velocity in Concrete`, with 5 returned records per provider.
- Crossref: `METADATA_RETRIEVED`, total search matches **1,255,853**, returned 5. This is broad provider relevance matching, not count of eligible publications.
- OpenAlex: `METADATA_RETRIEVED`, total search matches **2,896**, returned 5.
- Both returned DOI `10.3390/buildings14030720`; crosscheck `CROSS_PROVIDER_METADATA_MATCH`; `unique_matched_works=1`; `independent_experimental_origins_verified=0`.
- These broad returned counts cannot be interpreted as a systematic complete literature collection.
- Live JSON outputs isolated at `/tmp/krc-ext-s04-acceptance/live_discovery_20261025.json` and `live_crosscheck_20261025.json`.

## Actual manuscript-controlled test (EXT-S04)
Two manually authored scoped text snapshots were supplied for the control corpus.
1. Before: overgeneralized universal strength law / erroneously independent 2013 replication. Manuscript SHA256 `449ce0a93014d5f59ddd89c5f899d6c1477ecfdca200e099b9cac70a3e757dc1`.
2. After: narrowed to UPV correction subject to moisture/temperature/age/curing and repeated nine-specimen 2013 cohort, without implied independent replication. Manuscript SHA256 `0e71614a47a6a75d22bcb9cbda60f1c7926314ecc7c7922ee81e75be9fffebf0`.
One real content revision; diff reports +1/-1 line for the supplied text. Two different research packages and two actually executed deterministic Critic rounds. Both returned `REVISE` and `NO_GO`; no independent researcher/reviewer attestation and no validated new experimental results. Isolated result at `/tmp/krc-ext-s04-acceptance/manuscript_revision_20261025.json`.

## Critic findings / boundaries
- Code/test acceptance PASS, live metadata transport PASS for both catalogs.
- Reproducible selected search and DOI agreement established, not full text proof or originality certification.
- This stage does not automatically search exhaustively, identify all publications, read original graphs, validate measured samples, or produce a full standalone scholarly manuscript.
- Automatic Critic remains a deterministic internal audit, not an independent academic peer review. FULL_SCIENTIFIC_ACCEPTANCE=NO_GO.

## Next technical sequence
P3 extend search reproducibility with provider-specific returned-hits snapshots, eligibility filters, duplicate origin/DOI reconciliation and false-positive controls. P4 integrate actual manuscript artifact files into revised research bundles with line/passage provenance and checksums; then independent external scientific review at final acceptance. Maintain FREE_ONLY.
