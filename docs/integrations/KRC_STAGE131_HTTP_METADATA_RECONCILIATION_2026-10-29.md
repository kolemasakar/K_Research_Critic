# Stage131 HTTP provider + metadata reconciliation checkpoint (2026-10-29)

**Source-only, STAGING ONLY / FREE_ONLY / Production NO-GO.** Running pinned Stage131 installation from `49f8b857b46ebdf45636deffe90f8a4ee578bddf` NOT modified. Current source branch `a88bd6a588c311ffa789bff7a795ff7a899adc3a`.

New:
- `stage131_bibliography_http.py`: allowlisted Crossref/Europe PMC metadata HTTPS; 256 KiB cap; 0-10 sec timeout; 1-3 bounded attempts (default 2); retry only 429/503, URL network transient errors and timeout; no full-text retrieval or credentials; network only when explicit call.
- `stage131_bibliography_reconcile.py`: strict DOI, normalized title and publication year comparison; unmatched/missing fields get REVIEW_REQUIRED, full_text_verified=False and experimental_independence_verified=False.
- Fake HTTP and reconciliation tests, plus earlier adapter/classifier. **21/21 PASS** via RD isolated hash-locked test environment. First run 20 pass /1 failure due malformed JSON expected classification; fixed test to assert INVALID_PROVIDER_RESPONSE. Second 21/21 PASS.
Caveats: opener injectable for deterministic tests; live egress/real response size and license tests not yet performed; source-only, no in-service dispatch and no provider rate-limit/SLA acceptance. Formal schema ACK, scoped owner consent and reviewed signer pending; scientific E2E-01..05 NOT RUN.
