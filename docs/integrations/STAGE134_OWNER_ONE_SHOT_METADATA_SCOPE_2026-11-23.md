# Stage134 owner-directed bounded public metadata lookup

Date: 2026-11-23
Status: OWNER_DIRECTED_ONE_SHOT_METADATA_READ_ONLY / NOT_KRC_SIGNED_EXECUTION / PRODUCTION_NO_GO.

## Decision

The owner requested to perform the next step of the KRC Stage134 bibliography
review after an explicit prior statement that Crossref/Europe PMC reads need
separate owner consent. This authorizes this one bounded source-only verification
of the exact four existing real K_Science research DOIs. It does not approve
future/recurring provider access, installed KRC server dispatch, new external
permissions, a change to the K_Sentinel ingress or production deployment.

## Approved scope and budget

- Provider A: https://api.crossref.org/works/{percent-encoded-DOI}
- Provider B: https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={percent-encoded-DOI-query}&format=json&pageSize=1
- DOI 1: 10.1016/j.acme.2013.10.006
- DOI 2: 10.1016/j.proeng.2013.03.022
- DOI 3: 10.1016/j.ndteint.2015.01.003
- DOI 4: 10.1016/j.conbuildmat.2011.12.103
- Maximum 8 single-attempt GET requests: 4 DOIs x 2 providers.
- HTTPS only; exact hosts/paths/parameters; no redirects, cookies or credentials.
- Request timeout at most 10 seconds, response JSON limit 262144 bytes each.
- No retries, no scraping or extra DOI queries, no fulltext or PDF endpoints,
  no Crossref Metadata Plus subscription or paid content.
- No owner local-computer disk access; no installed KRC service modifications.
  Only isolated source-only process on the authorized KRC VM may run.
- Do not make additional network attempts for failed requests within this grant.

## Evidence and data minimization

Capture UTC observation, exact URL, HTTP status, response Content-Type,
response byte size and SHA256, and selected publicly depositable DOI/title/year
fields. Exclude abstracts, full-text links, personal contact data, secrets
and copyrighted full article text from public GitHub receipts.

A read-only provider response over TLS supports a direct provider observation,
not a provider-signed attestation. A SHA256 hash of received bytes establishes
identity of a captured response, not independently verified origin unless
separate trusted receipt/custody evidence is available. A missing Europe PMC
record is COVERAGE_GAP_METADATA_ONLY, not proof that the article is absent.
Two metadata matches never prove independent scientific experiments.

The installed Stage133 KRC owner-consent route's operation allowlist does not
include research.bibliography.audit; this scoped pilot MUST NOT be represented
as a KRC signed Stage134 POST/GET execution, and MUST NOT bypass/change the
installed KRC approval ledger. Cross-project E2E and production remain NO_GO.

Once the eight-request budget is exhausted or a provider call fails, record
results and outstanding errors. Every new network permission needs a separate
owner decision and approved server route.
