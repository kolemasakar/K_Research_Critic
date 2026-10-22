# KRC P0.3 — Source and DOI provenance

Status: DESIGN only. FREE_ONLY, no deployment.

Pipeline: register research question and exact searches; collect metadata; normalize DOI; deduplicate records; inspect actual primary texts; distinguish originals from derivatives; link each material claim to inspected evidence and author-approved bibliography.

Gates: reproducible search protocol; metadata reconciliation; version and retraction check; duplicate detection; independent evidence count; missing full text flagged METADATA_ONLY; no fabricated citations; human review.

Interfaces: SearchRun, Work, EvidenceOrigin, ClaimEvidence, Citation, ExclusionDecision. Use public metadata sources only within published limits and mark unavailable sources without paid fallback.

Acceptance pending: provider integration, live DOI checks, negative fixtures and claim-to-citation audit. No behavioral acceptance asserted.
