# KRC Stage131 source digest handoff — 2026-11-01

Source tested pin: `aa413a565fc9b95fe12250511b9a18b0ea50c68d`.
Sentinel independent review pin: `0ed8c11f973eb231206eb65dc56a1c10ad525c64`.

## Resolved source-field mismatch
- `src/krc_research/stage131_signed_artifact_boundary.py` now computes a SHA-256 while copying the fully consumed, scoped, upstream-verified `HardenedExchange.read_stream` into a private disk spool. On success, both `body_bytes` (<=1 MiB) and `body_file` (>1 MiB) return the immutable hex `sha256` alongside `size_bytes` and `request_id`. Digest reflects exactly the returned spool payload, is never sourced from a user-controlled header, and can be mapped to `X-Content-SHA256` by a later authenticated UDS HTTP adapter.
- Before returning success, source stream completes; corruption and size errors close spool with no bytes/digest exposed. Caller is required to close `body_file` even on abort.
- `tests/test_stage131_signed_artifact_digest_contract.py` checks digest matches INLINE bytes and 1.4 MiB spooled bytes, and no digest/bytes on corruption. Profiled digest+spool+boundary tests **10/10 PASS** on krc-cobalt, after fixing the initial missing field in the spool success branch.
- Does not change previously agreed storage limits (artifact <=200 MiB, total 2 GiB, TTL 7d) or source-only staging safety.

## Precise verdicts
| Item | KRC verdict |
|---|---|
| Success payload includes server-calculated SHA256 for INLINE and ARTIFACT | ACK_SOURCE / 10 PASS |
| MIME + length + SHA HTTP response header semantics | ACK_DESIGN_ONLY, no actual signed UDS server handler |
| Actual 200MiB signed endpoint streaming, abort cleanup, disk quotas | BLOCKED / NOT_RUN |
| Source-to-installed parity and Sentinel 40 negative GET scenarios | BLOCKED / NOT_RUN |

Proposed eventual successful signed UDS response: `HTTP 200`, `Content-Type: application/octet-stream`, `Content-Length: size_bytes`, `X-Content-SHA256: sha256`, `Cache-Control: no-store`. Do NOT assert these actual headers have been emitted by a running server.

External Stage127 remains sole staging ingress; GET and signer OFF. Installed Stage131 unchanged; no secrets/production changes; 48 science E2E NOT_RUN. Production NO-GO.
