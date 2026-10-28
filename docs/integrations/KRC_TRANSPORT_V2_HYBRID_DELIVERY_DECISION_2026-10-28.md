# KRC Transport Only v2 — hybrid result delivery decision

Date: 2026-10-28. Status: APPROVED DESIGN, NOT IMPLEMENTED.

Owner requirement: results up to 1 MiB are sent inline as before; larger research outputs are stored in private KRC Artifact Exchange and returned as an authenticated reference to K_Science.

1 MiB = 1,048,576 bytes including UTF-8 JSON envelope and metadata, not document text alone. Target inline encoded response <= 900 KiB to leave headroom; hard response limit <= 1 MiB. Calculate after complete JSON UTF-8 encoding; avoid Base64 file bodies. If larger than 1 MiB, store resulting output as artifact and send small JSON manifest with artifact_id, filename, mime type, byte length, SHA256 and expires_at. Only authorized download via K_Sentinel; no public object URLs or caller-specified paths.

Proposed staging quotas (not provisioned): 200 MiB per artifact, 2 GiB aggregate, 7 day TTL, disk free-space guard and safe cleanup. Files and inline payload must remain subject to operation and client authorization; download requires authentication on every request. Support explicit failure on exceeded storage quota or size, not silent truncation. Ensure idempotency and request_id binding on both routes. Distinguish a 1 MiB inline JSON payload from an actual document file; if original result is a binary artifact use artifact delivery regardless of size unless an explicit safe inline representation is supported.

Implementation responsibilities: KRC format and store results, choose route, authorize file access, maintain hash/TTL; K_Sentinel carries inline envelope or authorized artifact exchange requests without scientific interpretation; K_Science verifies SHA256 and stores the output. Current staging_backend114 is in-process only and has no artifact store, download endpoint, or automatic routing. Existing Stage114 v1 and production untouched, FREE_ONLY.
