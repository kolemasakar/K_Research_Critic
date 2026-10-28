# Stage131 K6/K7 contract checkpoint — 2026-10-28

**STAGING ONLY / FREE_ONLY / Production NO-GO.**

New versioned strict draft science request envelope: `schemas/stage131/science_request_envelope_v1.schema.json`, commit `6ac2ad2a3055cba78b6924f49116e0460fb4852d`. Restricts the four scientific operations, canonical K_Science principal, mandatory scoped consent reference, bounded evidence references, exact hex request ID, and rejects unknown properties. This is an **inner scientific request schema**, not an external Sentinel transport replacement. Existing Stage127 transport claims must be verified independently and mapped into this identity by trusted boundary code. JSON schema alone does not enforce byte-size limits or actual human consent.

New negative schema tests and existing Stage131 secret-path/consent/artifact tests on pinned Git checkout HEAD `a4f3f78105f364d46a7b76c056c5fce884afe92a`: **25/25 PASS**. No new service installed, no owner-issued real consent.

Artifact GET remains guarded by `HardenedExchange.read_stream` scope, TTL, SHA256 and bounded chunks in private UDS stack. External authenticated GET wire contract is still **DRAFT/NOT IMPLEMENTED**; no arbitrary file access or new public endpoint permitted. Final wire schemas of operation payloads, results, errors and artifact retrieval require joint K_Sentinel/K_Science review.

K5 Europe PMC repeat returned HTTP503; no two-provider positive metadata match, no scientific approval. Full unrelated GPT Store/Core/PDF regressions still red per prior checkpoint, not hidden.

Before K2 administrative installation: review pinned dependency lock, code ownership and root-controlled state/config/approvals paths, dedicated UID permissions, then manual owner/operator install with no automatic activation.
