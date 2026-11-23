# Stage134: correction - public internet research is NOT prohibited

Date: 2026-11-23
Owner instruction: enable normal public searching, browsing, fact-checking
and metadata retrieval as a permanent KRC core capability.
Disposition: RESEARCH_POLICY_CORRECTED / SOURCE_IMPLEMENTED /
LIVE_SERVICE_NOT_UPDATED / PRIVATE_SIGNED_ROUTE_SEPARATE.

## Root cause

The Stage131 public metadata adapter wrongly defaulted to
allow_network=False, and the Stage131 composition gate also required
provider_approved=True before any ordinary public DOI lookup. This
promoted the private scientific execution approval model to general
web research and caused PROVIDER_DISABLED on routine lookups.

The prior eight-request Crossref/Europe PMC pilot budget was only a
one-off technical acceptance scope. It must NOT be treated as a
standing ban or global cap on the KRC research engine's internet access.

## Implemented source changes

- src/krc_research/stage131_bibliography_adapter.py:
  lookup_doi_metadata() now defaults to allow_network=True and
  automatically selects the bounded FREE_ONLY HTTPS metadata fetcher
  when the caller supplies no test callback. Callers do not need
  individual provider-approved flags for routine read-only DOI
  verification. The return continues to state full_text_verified=False
  and experimental_independence_verified=False.
- src/krc_research/stage131_safe_composition.py:
  bibliography_metadata_gate() defaults to public lookups, not
  PROVIDER_DISABLED. Its old provider_approved argument is accepted
  only for backward compatibility and does not gate public research.
  allow_network=False is an explicit offline/test opt-out.
- src/krc_research/stage131_bibliography_http.py:
  clarifies the actual trust boundary; strict HTTPS/URL validation,
  no redirects, per-request timeout, response-size controls and
  measured rate-limits remain mandatory.
- Existing public_discovery and paged_discovery Crossref/OpenAlex
  network research routes continue to be available and are not
  dependent on signed science owner profiles.

## Crucial separation

Routine public read-only KRC research:
  FREE_ONLY, NETWORK_AVAILABLE_BY_DEFAULT, no per-DOI owner grant.

Signed K_Science/KRC research.bibliography.audit through Stage127:
  separate owner-scoped immutable work profile, signed envelope,
  replay and artifact custody; unchanged Stage127 operation allowlist.
  Source-only offline snapshots remain a supported deterministic mode,
  NOT a mandate to disable web search.
  Existing installed signed Stage133 bridge is NOT being promoted.

Provenance and scientific truth:
  a Crossref DOI match is bibliographic verification, NOT evidence
  of document custody or independent experiments. Avoid paying for
  external APIs or exposing unpublished articles to providers.

## Acceptance and deployment boundary

- The corrected policy is canonical in KRC main:
  docs/RESEARCH_NETWORK_ACCESS_POLICY_2026-11-23.md
- The corrected adapter/composition behavior and regression tests
  are in KRC PR36 source branch. Full repository regression
  and unchanged installed runtime inspection must be recorded
  against the final code commit before any deployment.
- This correction does not authorize server service installation,
  provider credential changes, external signed route enablement,
  production promotion or HP-OMEN local disk access.
- Normal public internet research is authorized as a CORE FUNCTION,
  including searches beyond the four DOI examples when requested.
  Additional providers can be integrated using safe source adapters,
  without a new owner consent solely because the source is online.
