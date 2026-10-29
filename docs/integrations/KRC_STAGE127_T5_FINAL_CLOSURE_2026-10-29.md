# KRC FINAL CLOSURE — Stage127 T5 transport handoff (2026-10-29)

**Decision: ACK_WITH_LIMITATIONS. KRC'S STAGE127 TRANSPORT-ACCEPTANCE WORKSTREAM CLOSED.**
**STAGING ONLY / FREE_ONLY / Production NO-GO.**

## Closed deliverables (KRC)
1. Independent source review of KRC UDS `uds_verified123b.py`, `transport_auth123b.py`, `research_boundary120.py`, `uds_stage123.py`, `staging_service123c.py` and permitted operations. Order: SO_PEERCRED peer UID -> HTTP request shape/size/JSON -> HMAC-SHA256 signed assertion, identity claim tuple and ±300 s freshness -> operation allowlist -> principal-to-UID consistency -> ResearchBoundary/ledger. Sentinel verifies upstream OIDC/JWKS, audience and durable jti replay; KRC does not separately parse OIDC.
2. `transport.probe` outside allowed OPS -> HTTP403 `OPERATION_DENIED` *before* `ResearchBoundary.execute` and main request ledger; do not fabricate its presence in ledger.
3. Distinct server-side sanitized T2/T3 event audit: **NOT_INSTRUMENTED** in reviewed KRC UDS; this is a transparency limitation, not an evidence PASS.
4. Read-only krc-cobalt Stage127 `active/running` observed PID45059, NRestarts1, Stage126 PID37979 active without restart. Sentinel Stage127 file observed SHA256 `5f82e2ba1ba65cb4d6c186b86a4e7591d92bc1820a67b18b490b95c2d52`. No executable in-process loaded-code measurement claimed.
5. Sentinel source HEAD `b1440a999c28234a1db6c40d93e944f27ccd9748`, KRC formal ACK commit `dfa4803e637be30ebd84ad63f9debdc547d67b32`, evidence `docs/integrations/KRC_STAGE127_T5_INDEPENDENT_ACK_2026-10-29.md`. Sentinel T0–T5 PASS evidence belongs to Sentinel workflow; KRC ACK is scoped, not a full independent recreation of OIDC client runs.
6. Owner decision: single external staging transport Stage127 on Tailnet 100.118.132.8:19017, internal future Stage131 UDS, shared KRC service UID988, separate dedicated Stage131 keys and paths, no new external transport.

## Exclusions and transfer to scientific E2E backlog (NOT CLOSED)
- Stage131 is **not installed**; no runtime service, actual UID988 secret access or installed UDS SHA attestation.
- Real owner-scoped consent, revocation/replay custody and authorized internal science signer are not enabled.
- K6 JSON request/response version parity with actual `krc-transport/2`, external artifact GET, and provider-backed bibliography (Crossref metadata-only; Europe PMC previously 503) are not accepted.
- Source/dependency security, real authorized E2E-01..05 with SHA pinning, negative/rollback and K_Science sign-off remain pending.
- No boot auto-enable of Sentinel inferred; no production or publication approval.

## Closure semantics
KRC's **answer to Sentinel Stage127 T5 handoff is complete**. No additional KRC operational work is required to issue this scoped acknowledgment. K_Sentinel remains owner of closing its own T5 evidence and source-runtime attestations. Open KRC Stage131/science E2E actions are a *separate workstream*, not retroactive blockers to this scoped Stage127 acknowledgment.

No live science request, new secret, deployment, service restart, filesystem permissions change, production change or public publishing performed as part of closure.
