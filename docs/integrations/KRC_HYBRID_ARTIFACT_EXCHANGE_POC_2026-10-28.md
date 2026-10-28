# KRC Hybrid Artifact Exchange — isolated proof of concept (2026-10-28)

Owner requirement: inline JSON result up to 1 MiB encoded response, larger results as private artifacts. Implemented an independently testable Python stdlib module `artifact_exchange.py` and pytest suite `test_artifact_exchange.py` in isolated local runtime, distributed as a conversation attachment (not yet installed on krc-cobalt or committed as code to GitHub).

**12/12 local tests PASS**. Tests: small inline, UTF-8 actual byte size cutoff, large JSON artifact, principal/request cross-access denial, hash corruption detection, quota, per-artifact cap, TTL cleanup, invalid filename, invalid artifact ID, symlink rejection, invalid JSON NaN.

The POC includes SQLite WAL index, random opaque artifact ID, metadata + SHA256, 7-day TTL, 200-MiB per-file and 2-GiB aggregate example quotas, 0700 directories, 0600 files, and fail-closed scoped artifact reads by principal+request. No listener; no production modification or Sentinel v1 integration.

**Important limitations / not ready for deployment**: file APIs buffer entire data in RAM and are not yet streaming; authorizer uses a passed-in principal string and relies on a future trusted authenticated UDS gateway to supply it; concurrent crash-consistency and quota recovery require stronger atomic commit/reconciliation; no idempotent same-request re-delivery yet; no disk free-space guard, no tested multi-process cleanup/download race; artifact type policy and document export connectors pending; use nonpublic content only after security review. Network E2E NO-GO. Separate Stage114 unchanged, FREE_ONLY.

Next: port code from the attached artifact into isolated KRC Git checkout, harden streaming + crash recovery + auth binding, integrate UDS v2 and run full tests. Do not claim 341 KRC regressions were run after this change: previous temp checkout was removed in a server restart and only new local POC suite was run.