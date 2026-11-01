# KRC — CONTROLLED PROJECT SNAPSHOT AND CHAT TRANSITION — 2026-11-01

Scope: K-Research & Critic (KRC), K_Sentinel Stage127, K_Science Stage131. **STAGING ONLY / FREE_ONLY / Production NO-GO.**

## Authoritative baseline and status
- KRC working branch `agent/krc-public-media-r3-integration`. Latest HTTP hardening source change `e4586c880efa6d1b1030d502306749a1fbb5882a`; negative tests commit `4e8352e26eb836c10ce7bbcaf5c7b1b84da5dd55`; last published hardening report `fde9646c605044a7e3fccf59d46ba73fabe6686f`.
- Exact `src/krc_research/stage131_signed_artifact_uds.py` blob `8b0decd563c932bfedc703f1328f6bba9ce32429`; HTTP hardening report blob `71fd9ed4606ced285b764557c26f07f87eb1ae61`.
- Separate **source-only**, manually instantiated `SignedArtifactUDSServer`: internal `POST /v1/artifacts/read`, `krc-artifact-get/1`, `artifact.read`. Not part of deployed or approved Stage127 external ingress or installed Stage131.
- Signed HMAC-SHA256 canonical JSON verifier, trusted peer UID via `SO_PEERCRED`, identity matching, durable SQLite nonce registry, completed RequestLedger read-only match, Artifact Storage owner/request scope+trusted TTL+full size/SHA256 verification before success bytes.
- Existing storage contract unchanged: <=1 MiB INLINE, >1 MiB ARTIFACT, max artifact 200 MiB, total storage 2 GiB, retention TTL 7 days. Successful in-process artifact result has `size_bytes`, `sha256`, `body_bytes` or private/unlinked `body_file`. HTTP 200 emits Content-Length, X-Content-SHA256, no-store; spool closes in finally. No new storage built.
- HTTP hardening source: rejects CL+TE and duplicate/non-decimal CL with 400, 5 s socket inactivity timeout, ThreadingMixIn, exception sanitization to 503. **Remaining risk**: no absolute request deadline, unbounded active threads, unverified extra bytes after declared length, incomplete disconnect coverage. Do not claim these fully remediated.

## Evidence
- Focused signed UDS HTTP positive/replay: 1/1 PASS in temporary AF_UNIX server using synthetic data.
- Focused HTTP hardening + previous UDS tests: 3/3 PASS on isolated source checkout.
- Last full KRC source suite BEFORE HTTP hardening: **1108 passed, 17 skipped**. **The full repository regression AFTER HTTP hardening has NOT been executed/verified here.** Do not reuse 1108 as post-hardening evidence.
- Separate earlier large artifact focused source tests 19/19 PASS on 3 MiB synthetic source, not near-200 MiB installed server acceptance.
- K_Sentinel independent source audit `90beb13c2c3d2c8dd729e56ff565424f211e6901` documents additional HTTP hardening gates.
- K_Sentinel 40 external GET negatives: NOT_RUN. K_Science 48 true science E2E: NOT_RUN. Final partner ACK/MISMATCH OPEN.

## Open blocking work (priority)
1. Bound concurrent active UDS worker count, implement **absolute total request deadline** (not merely socket inactivity), reject ambiguous or undeclared request-body bytes, sanitize all error paths; add slowloris, chunked/duplicated CL, simultaneous slow and fast, malformed/deadline, disconnect and resource exhaustion negatives.
2. Validate Artifact Storage authoritative hash vs bytes, mutation and expiry boundary, completed ledger owner binding; test near 200 MiB, 2 GiB storage quota/low disk, retention TTL=7 days, cleanup on interruption and bounded memory.
3. Produce deterministic captured positive AND negative **actual isolated UDS HTTP** fixtures, versioned status/header/body schemas and immutable pins; independent canonical MAC vector/nonce replay across restart and 200 MiB evidence. No route deployment.
4. Request Sentinel source ACK/MISMATCH and separately execute 40 negative external adapter tests with external GET **OFF by default**, then K_Science independent receipt and science semantic ACK. No scientific approval inferred from transfer success.
5. Source-to-installed parity, ACL/key lifecycle, rollback, consent signer and separate explicit user authorization are activation gates. **Do not enable signer, external GET, providers or production, and do not change live Stage127.**

## Partner links
- KRC issue #28: https://github.com/kolemasakar/K_Research_Critic/issues/28
- K_Sentinel PR #38: https://github.com/kolemasakar/Sentinel-Remote/pull/38
- K_Science PR #7: https://github.com/kolemasakar/K_Science/pull/7
- KRC latest hardening: docs/integrations/KRC_STAGE131_SIGNED_GET_HTTP_HARDENING_2026-11-01.md
- KRC latest UDS proof: docs/integrations/KRC_STAGE131_SIGNED_GET_ISOLATED_UDS_2026-11-01.md

## Transition rule
Use this snapshot and current immutable Git SHA as the source of truth, cross-check against latest partner review on new chat, continue from priority item 1, do not start from historic Stage126/131 planning again. No automated background monitoring or scheduled backup.
