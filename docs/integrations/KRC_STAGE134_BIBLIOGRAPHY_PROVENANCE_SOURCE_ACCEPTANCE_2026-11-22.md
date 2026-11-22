# Stage134 bibliography provenance contract and offline implementation
Date: 2026-11-22
Status: SOURCE-ONLY; NO_SEND; NOT_INSTALLED; PRODUCTION_NO_GO
Owner: KRC; Science and Sentinel transport rollout require separate acceptance.

## Scope and outputs

The new pure KRC source API is `krc_research.stage134_bibliography_provenance.audit_stage134_provenance(bundle)`.
A backward-compatible entrypoint exists in `stage131_bibliography_adapter.audit_doi_provenance_offline(bundle)`.
Both receive an already supplied immutable object, perform deterministic validation, and never invoke
any provider, open a network connection, access a local credential, or authorize scientific work.

Machine contracts (JSON Schema draft 2020-12, additionalProperties=false):
- `schemas/stage134/bibliography_provenance_input_v1.schema.json`
- `schemas/stage134/bibliography_provenance_result_v1.schema.json`
These are separate from the exact SHA-pinned Stage133 external schema, which is unchanged.

## DOI validation

The input DOI is checked against a bounded, explicit ASCII DOI subset:
`10.<4..9 digits>/<1..180 ASCII suffix chars>`.
Dangerous or ambiguous fragments, query/fragment characters, percent escapes, path dot/dotdot
components, Unicode control/space and URL-form DOI input are denied, not silently decoded.
Normalized comparison uses ASCII lower-case. Restriction is intentional: rare legitimate DOI
forms outside this subset require explicit manual handling, not unsafe normalization.

The caller-supplied provider snapshot URL must match the generated canonical URL for the
same DOI and provider and pass the existing Stage134 exact URL allowlist.
Crossref `message.DOI` must match the requested DOI. Europe PMC match requires a matching
record DOI; a missing Europe PMC record is `COVERAGE_GAP_METADATA_ONLY`, not evidence
that an article does not exist. Conflicts in title/year require human review.

## Provenance and integrity

Each capture includes provider identifier, exact URL, timezone-aware captured_at,
a JSON payload and SHA-256 over its **canonical JSON bytes**. The runtime recomputes
and compares this digest and enforces 256 KiB per capture, 512 KiB per bundle, and
two distinct providers maximum.

CRITICAL: A hash computed over supplied payload bytes is integrity consistency only.
It does not cryptographically attest the named provider, actual HTTP fetch, timestamp,
copyright status or document authenticity. Even two matching providers are metadata
corroboration, not independent validation of the original experiment.
Every result explicitly reports:
- `provenance_status=PROVIDER_ORIGIN_NOT_AUTHENTICATED`
- `provider_snapshots[].integrity_status=CANONICAL_PAYLOAD_HASH_MATCH_ONLY`
- `scientific_independence.verified_origin_count=0`
- `scientific_independence.scientific_truth_verified=false`
- `scientific_independence.full_text_verified=false`
- `decision=HUMAN_EVIDENCE_REVIEW_REQUIRED`.

## Scientific-source independence and shared derivation

The input can include declared source IDs, origin IDs, document SHA-256 labels,
access levels, and derived_from source IDs. The engine requires unique IDs,
known parent references and acyclic lineage, and groups all records that share
a declared origin (case-insensitive) or a declared derivation path.
Lineage groups and counts are **unverified candidate labels**. Caller-declared
FULL_TEXT/METHODS_RESULTS_EXCERPT access or distinct origin IDs can never upgrade
to scientifically verified independence through this input interface.

True scientific independence needs separately authenticated KRC file/receipt
custody, inspected methods/results, validated source SHA-256 against actual
bytes, corroborated original experimental data and an explicit dependence
review. That future trusted decision must not be implemented by accepting
arbitrary client-supplied booleans or metadata-provider counts.

## Non-goals / separate release gates

- No Stage134 `research.bibliography.audit` external execution enabled.
- No provider calls to Crossref/Europe PMC; existing strict Stage134 HTTP
  fetcher remains disabled by default and is unchanged.
- No new Tailscale credentials, Sentinel workflow policy, KRC consent changes,
  broker/gateway/reader service changes, SQLite writes or production promotion.
- The Stage133 preflight/inspection positive E2E 2/2 and Science matrix 4/48
  are independent and unaffected.
- A real network metadata operation needs an independently reviewed
  `FREE_ONLY_METADATA` execution policy, allowed DOI/source set, bounded
  number of requests and retries, provider audit trace and separate owner approval.
- A real scientific acceptance also needs source/claim inspection and an
  independent reviewer. Metadata-only labels must never imply publication readiness.

## Test evidence

New isolated module tests exercise valid 2-provider DOI match, missing coverage,
wrong DOI, title/year conflict, duplicate providers, tampered canonical hash,
noncanonical/unsafe URL, malformed timestamp, oversize snapshot, schema denial,
source-ID collision, shared ancestry, cycles, unknown parent, and explicit
non-promotion of invented source independence. Existing Stage134 hardening tests
and broader project source regression must be run on the exact branch snapshot
before promotion. Source-only acceptance is not operational acceptance.
