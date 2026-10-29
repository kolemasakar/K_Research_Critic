# Stage131 live DOI integration findings — 2026-10-29

STAGING ONLY / FREE_ONLY / Production NO-GO.

Source HEAD tested: `2b33deb821345c78096de945d2c7da7a0292d6b4`. Actual installed and running Stage131 remains pinned `49f8b857b46ebdf45636deffe90f8a4ee578bddf`; no restart, deployment, config or key change.

Live HTTPS via explicit opt-in source-only fetcher, bounded timeout and response-size:
- K_Science selected DOI `10.1088/1757-899X/365/3/032058`: Crossref DOI field `10.1088/1757-899x/365/3/032058` (case-insensitive match), Europe PMC `DOI:` query hitCount=0; reconciliation `DOI_MISMATCH_OR_ABSENT`, not TWO_PROVIDER_MATCH. Zero hits do **not** prove publication absent; Europe PMC coverage narrower.
- Control DOI `10.1038/nature12373`: Europe PMC hitCount=1; field reconciliation title=MISMATCH, year=MATCH, overall REVIEW_REQUIRED. Require metadata normalization/source inspection before asserting error.
- Repeated offline bounded HTTP, adapter, reconciliation, classifier suite: **21/21 PASS** in 1.68s.

Release gate: new bibliography source is NOT reviewed/pinned/deployed. For selected K_Science article Crossref is metadata authority where Europe PMC record is absent; missing provider should be classified COVERAGE_GAP, not external 503, independent metadata verification or full-text quality proof. DOI uppercase X is canonical case-insensitive. Provider validation must not equate multi-provider coverage with scientific source independence. Consent/signer remain disabled; scientific E2E NOT RUN.

Pending: review hardening of URL allowlist including query structure, redirect/host constraints, title normalization, author/year/venue reconciliation, HTTP response content type and bounded decompression; vendor license and no fulltext download. Partner schema ACK and a reviewed new release before any Stage131 runtime update.
