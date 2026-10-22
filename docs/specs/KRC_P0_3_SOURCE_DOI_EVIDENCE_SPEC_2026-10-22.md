# KRC P0.3 — Source and DOI provenance

Status: DESIGN only. FREE_ONLY, no deployment.

Pipeline: register research question and exact searches; collect metadata; normalize DOI; deduplicate records; inspect actual primary texts; distinguish originals from derivatives; link each material claim to inspected evidence and author-approved bibliography.

Gates: reproducible search protocol; metadata reconciliation; version and retraction check; duplicate detection; independent evidence count; missing full text flagged METADATA_ONLY; no fabricated citations; human review.

Interfaces: SearchRun, Work, EvidenceOrigin, ClaimEvidence, Citation, ExclusionDecision. Use public metadata sources only within published limits and mark unavailable sources without paid fallback.

Acceptance pending: provider integration, live DOI checks, negative fixtures and claim-to-citation audit. No behavioral acceptance asserted.

## P0.3 implementation checkpoint — 2026-10-22
- Offline parser implemented at `src/krc_research/doi_provenance.py`; tests at `tests/test_p03_doi_provenance.py`.
- 16 isolated local pytest tests PASS (DOI normalization, invalid input, Crossref/DataCite fixture parsing, duplicate/conflict handling, independent-source accounting).
- Crossref live metadata response inspected through public URL `https://api.crossref.org/works/10.1038/nature12373`; metadata: DOI `10.1038/nature12373`, `Nanometre-scale thermometry in a living cell`, Nature 500 (2013). Full-text claim verification was NOT performed.
- DataCite public access and metadata schema confirmed from official documentation, but direct test response was unavailable through the retrieval environment. Its parser passed only synthetic fixture tests.
- OpenAlex capability/documentation checked, no live ingestion; API usage must obey free quota and rate limits.
- Existing offline evidence audit counts caller-supplied origin IDs, without independent automatic verification that origins are truly independent; this is a known P0.3 acceptance limitation.
- Integration in private installed plugin, live provider transport, article full-text inspection, citation rendering and end-to-end manuscript audit remain NOT_RUN.
- PRIVATE plugin version 0.19.9 release `pluginrel_6ada324010bc8191a11a4d76a6090aa8` contains Protocol Router section and fields; plugin behavioral invocation not verified. No public/production/MEDIA changes.
