# Stage131 K5–K7 contract and provider checkpoint — 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO; DRAFT scientific integration contract.**

## K5 live provider diagnostic
Two public DOI lookups against Europe PMC through the existing KRC read-only HTTP adapter returned **HTTP 503** on krc-cobalt:
- 10.1038/nature12373
- 10.1038/s41586-020-2649-2
Crossref had returned METADATA_ONLY for the first DOI earlier. Do **not** interpret 503 as NOT_FOUND, retracted, missing publication, or a scientific determination. Do not bypass by using paid proxies or scraping. Fail closed as PARTIAL / PROVIDER_UNAVAILABLE. Do not mark TWO_PROVIDER_MATCH unless both metadata responses return valid, matched DOI.

## K6 four scientific operations — proposed wire freeze gates
The approved operation names are strictly:
- research.profile.validate
- research.evidence.preflight
- research.bibliography.audit
- research.inspection.review

Only Sentinel Stage127 is canonical external transport candidate. Its verified identity projection, NOT user-submitted claims, must map exact client, principal, repository and workflow ref into KRC-authenticated UDS. New external ports are forbidden. Each science request must have exact request_id, task_id, scoped operation, profile_ref, evidence_refs, consent_ref, science_payload with strict max byte size and canonical SHA-256 binding. Idempotency: identical replay rejected, changed payload with reused identifiers denied; never auto-approve because transport passed. Error codes, final JSON schemas and response-envelope hashing require joint KRC/Sentinel/K_Science review before T5; no finished schema freeze is claimed.

## K7 artifact acceptance contract
Verified code is private HardenedExchange/StreamExchange: per-principal/per-request scope, immutable artifact ID format, content SHA-256 verification and bound read chunk <=1 MiB, TTL expiration checks, bounded free-space reservation, no symlink following, storage reconciliation and advisory lock. Do not expose arbitrary filesystem paths or anonymous artifact GET. Exact authenticated Artifact GET route (if required) and network quota response need formal bilateral contract. All artifacts are KRC-owned in private Stage131 root; TTL, retention and maximum sizes must be versioned and tested with real service UID before activation.

## Tests
On unprivileged krc-cobalt Git checkout at previous tested head 4fbd014b1711ab2df833c6f1aa7720b62ddcc516:
`PYTHONPATH=src /home/krcops/stage131-test-venv/bin/python -m pytest -q tests/test_artifact_stage117.py tests/test_artifact_stream116.py tests/test_stage125_four_ops_uds.py tests/test_bibliography_bounded129.py tests/test_metadata_store130.py`
Result **24/24 PASS**. No service start or modifications.

## Blocks
K2: no Stage131 server activation. K3: no real owner consent. K5: Europe PMC 503 prevents two-provider positive check. K6: final schemas not ratified. K7: authenticated artifact fetch contract pending. K8: existing 10 known full-suite failures. K9: scientific E2E NOT_RUN.
