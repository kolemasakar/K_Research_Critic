# KRC P0 reviewer attestation / contradiction gate — 2026-10-25

## Implemented
- `src/krc_research/reviewer_attestation.py`: separate reviewer-key HMAC over receipt SHA-256, source-document SHA-256, reviewer ID and zoned inspection time; validates trusted reviewer identity, prohibits reviewer==researcher, bounds timestamp validity (30 days), refuses altered signatures and mismatched artifacts.
- `src/krc_research/research_pipeline_v2.py`: accepts reviewer attestations through an explicit trusted-server parameter (separate from research JSON), verifies signatures, computes allowable receipt hashes, passes verified receipts into research scoring and executes deterministic Critic. Unresolved contradiction records are now surfaced and block publication/approval regardless of positive evidence.
- `tests/test_p0_reviewer_attestation.py` and `tests/test_p0_signed_review_cycle.py` cover identity, forgeries, signature expiry, artifact changes, missing trust configuration and contradictory sources.

## Test execution
On isolated krc-cobalt test tree `/tmp/krc-p0-offline-20261025`: `pytest -q tests/` -> **94 PASS / 0 FAIL in 0.60s**, process exit 0. Prior baseline was 80 PASS. Synthetic signatures/keys appear **only in tests**, never production credentials.

## Limitations / no-go
- A reviewer's valid signature establishes trusted approval of a specific receipt/doc digest, NOT scientific validity, actually inspecting original publisher content, or methodological correctness. The signature issuance and key management service is **not deployed**; available verification is an integration hook only.
- `trace_verified` is still an untrusted boolean recorded inside receipts. Separate trusted reviewer-key verification is needed as well.
- `artifact_attestation.py` currently handles local plaintext bytes, not arbitrary PDF scientific papers; correct DOI metadata does not prove full text.
- Critic is executed deterministic rule audit, not independent expert scientific peer review. The source conflict guard is deliberately conservative and still requires semantic evaluation of relevance and refutation.
- 12-claim Si-C ledger prior status 7 reported PASS / 5 SHORTFALL; no new independently attested original paper has been supplied, hence **scientific reacceptance remains 0 newly substantiated PASS**.
- Publication and journal submission stay NO_GO; AI detectors not run; no guarantee of publishing or detector evasion.

## Next
Issue independent reviewer service identity and secure key outside GitHub; bind HMAC keys to approved operator identity, keep reviewer trace server-side; capture publisher full text with licensed rights and reproducible passage locators; extend Critic to handle scientific rebuttals, novelty and method comparison. Recheck live DOI update/retraction only with provider provenance.

No changes to KRC production MCP 9013, MEDIA, public routes or plugin 0.19.14.
