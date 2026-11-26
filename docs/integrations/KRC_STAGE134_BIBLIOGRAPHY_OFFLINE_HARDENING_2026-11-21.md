# Stage134 bibliography metadata adapter security checkpoint
Date: 2026-11-21
Disposition: SOURCE_ONLY / PROVIDER_NETWORK_DISABLED / NO_SEND / NOT_INSTALLED / PRODUCTION_NO_GO.

## Scope
This is a separate KRC track from Stage133 POST/GET integration. It hardens the existing Crossref and Europe PMC metadata-only fetcher in src/krc_research/stage131_bibliography_http.py, and clarifies missing-provider records in the Stage131 metadata classifiers. It does not enable research.bibliography.audit in the installed route, does not modify K_Sentinel, and never asserts scientific source independence or publication approval.

## Exact security guards
- Strict HTTPS scheme, exact allowed hosts and API paths. Reject credentials, nondefault ports, fragments, control/non-ASCII URL bytes, unexpected query arguments, duplicate query parameters, fulltext endpoints, DOI traversal, percent-encoding ambiguity and noncanonical Crossref encoded DOI paths.
- Custom opener rejects any HTTP redirect (no automatic Location following). For injected response mocks with geturl(), final URL must equal the originally validated URL.
- Accept only JSON content type and identity encoding, bounded Content-Length and maximum 262144 response bytes. JSON must decode to an object. No PDF or fulltext fetching.
- Bounded retry for HTTP 429/503 and explicit distinction between transient provider limit, provider 404, malformed provider response, and network connection errors.
- Default metadata lookup remains PROVIDER_DISABLED. Controlled network use is still not approved; injected fake fetcher in tests is never actual external traffic.
- Europe PMC absence when Crossref DOI matches is COVERAGE_GAP_METADATA_ONLY, not a claim the paper is nonexistent, fraudulent or scientifically invalid. Two DOI matches still establish metadata only, not independent experimental evidence.

## Test evidence
Added offline test matrix for host spoofing, injection, redirect, response type/encoding, rate-limit and coverage-gap handling. Existing legacy bibliography source unit tests retained with stricter response metadata fixtures.
Stage134 isolated suite: 49 PASS / 0 FAIL with fake providers, zero real network calls. Full unified KRC single-process regression with Stage134 overlay: 1211 PASS / 17 SKIPPED / 0 FAIL in 56.87 s on krc-cobalt (2026-11-21). This is a local source acceptance, not independent external reviewer signoff or installed runtime acceptance. No new science E2E added. Consent and account policies unchanged.

## Outstanding acceptance
- External public API usage requires reviewed FREE_ONLY_METADATA consent/scope, bounded request budget/cadence, credential-free privacy review and copyright/license policy.
- Integrate full bibliographic workflow with KRC owner authorization, source audit, evidence provenance, DOI metadata correlation and operation result schema.
- Real provider smoke tests and installation must be separately approved and carried out only after security review; no inference of Crossref/Europe PMC coverage from fixtures.
- Actual Stage133 installed cross-UID E2E and K_Science contract ACK are separate Stage133 blockers. Project overall remains NO-GO for production.
