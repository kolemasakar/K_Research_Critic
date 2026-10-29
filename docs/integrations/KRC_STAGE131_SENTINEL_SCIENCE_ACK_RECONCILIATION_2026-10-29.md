# KRC Stage127/131: reconciliation of Sentinel and K_Science ACK — 2026-10-29

**Decision: ACK_SOURCE_MAPPING_WITH_BLOCKERS; scientific E2E remains NOT_READY.** This is KRC's acknowledgement of the independent reviews, **not** a final schema-bundle approval.

## Independent inputs
- Sentinel: `kolemasakar/Sentinel-Remote` commit `59b45147`, `docs/KRC_STAGE131_BIBLIOGRAPHY_AND_CONTRACT_SENTINEL_ACK_2026-10-29.md`; ACK_WITH_LIMITATIONS.
- K_Science: `kolemasakar/K_Science` commit `16896c040b96b065f7188fbeec792a74f654a8c7`, `docs/integrations/stage127-science-e2e/CONTRACT_ACK_TO_KRC.md`; ACK_SOURCE_MAPPING_WITH_BLOCKERS.
- KRC source inspected at `55f56805f65f64ff50cdc5a6d1332a01abfc56cc`; deployed Stage131 remains `49f8b857b46ebdf45636deffe90f8a4ee578bddf`. Never treat newer source code as deployed.

## Current schema pins (Git blob SHA, immutable at inspected commit)
| Artifact | Blob SHA | Status |
|---|---|---|
| `schemas/stage131/uds_response_transport_v2.schema.json` | `2ae1dd5a3176ca6432892f8034dfe3dc15df8969` | **DRAFT / incomplete early-error and artifact semantics** |
| `schemas/stage131/science_request_envelope_v1.schema.json` | `13617f0302c261f7477191b11764f99f7ea2c325` | **DRAFT / not external Sentinel wire** |
| `src/krc_research/uds_verified123b.py` | `6cacd6e9eec78b0a3de5f3a529506124974f1d12` | Source implementation evidence only |

## Confirmed source boundary
- External consumer request is only `request_id`, `operation`, `payload`, after Sentinel OIDC/replay. External Science HMAC prohibited.
- Internal signed UDS `krc-transport/2` includes trusted identity+MAC; KRC checks peer UID, signed identity and operation allowlist prior to ResearchBoundary.
- Early `send_json` errors contain `{"error":"CODE"}`, NOT necessarily `version` or `request_id`. Verified source status: 400 INVALID_REQUEST, 404 NOT_FOUND, 413 REQUEST_TOO_LARGE, 415 UNSUPPORTED_MEDIA_TYPE, 403 UNAUTHORIZED/OPERATION_DENIED/auth errors, 409 non-completed boundary output. 507 RESPONSE_TOO_LARGE in lower handler requires fixture reconciliation.
- Completed transport does NOT mean scientific approval; inline threshold applies to full serialized wrapper; artifact GET is internal only until separately authorized external GET.
- `science_response_v1` remains a proposal, not actual output wire.

## Accepted corrections
- K_Science scientific matrix **48 NOT_RUN** (not earlier 28). K_Science recorded original PDF SHA256 `d6b803c8bff86f1662cd4309eccc29518de2958798216596bee9f4309151f1e7`; figures 1–9 reviewed locally. This is not experiment independence proof.
- DOI `10.1088/1757-899X/365/3/032058` in Crossref; Europe PMC DOI search has 0 hits. This is COVERAGE_GAP, not paper absent. Metadata-only ≠ source independence or fulltext attestation.
- Stage131 installed/restarted, signer disabled, workflow `staging-disabled`. Source-only bibliography HTTP adapter with offline tests is not installed in active release.

## Acceptance gates
1. Produce **machine-readable complete outer + inner contract bundle** (external request, signed UDS request, completed inline, completed artifact, rejected, pending_reconciliation, early HTTP errors with optional/missing request_id, 507 and 409 mapping), exact fixtures & validator tests, hash-lock every schema.
2. Approve source→deployed signer-enabled entrypoint only after true owner-scoped consent issue, verify, revoke, replay and expiry tests. No user consent inferred here.
3. Review real DOI provider HTTP network safety (redirect, hostname restrictions, headers, response size, 429/503/timeout, Retry-After bounds), license/coverage and field-level reconciliation.
4. Pin external authenticated artifact GET or keep artifacts **NOT_RUN**.
5. Seek explicit K_Science/Sentinel final ACK after executable contract tests, then separately authorize E2E-01–05. Until then no science dispatch, no Stage131 restart/change, no production.

**Stage127 transport ACK remains CLOSED. STAGING ONLY / FREE_ONLY / Production NO-GO.**
