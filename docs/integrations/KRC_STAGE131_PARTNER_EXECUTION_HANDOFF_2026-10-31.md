# Stage131 KRC / K_Science / Sentinel execution handoff — 2026-10-31

Status: SOURCE_ONLY_REVIEW_READY. STAGING ONLY / FREE_ONLY / Production NO-GO.

## KRC source completed
- Added stage131_pre_dispatch_custody_gate.py: no caller Boolean as authorizer; require trusted authorizer callable and request/task/operation/principal context binding BEFORE dispatch. 46/46 focused tests PASS.
- Production caution: real runtime MUST construct the KRC-owned ConsentCustody128 internally; an untrusted caller-supplied callable is unsafe. This new gate is not wired to runtime.
- Stage117 now returns committed expires_at_epoch. Expiry, owner, digest checks passed in isolated storage; prior bibliography source remains disabled by default.
- Last confirmed deployed Stage131 source pinned 49f8b857b46ebdf45636deffe90f8a4ee578bddf, signer disabled. No deployment or real research.

## K_Science assigned independent tasks
1. Pin new KRC source blobs; rerun consumer fixture/semantic validation of science result task_id + operation correlation, malformed approvals, artifact expiry and wrong principal/request_id. Distinguish scientific acceptance from transport completed.
2. Publish per-case ACK/MISMATCH, exact schema/source SHA, failures and proposed inner science result/error schema. Verify Stage117 descriptor now includes expiry.
3. Keep 48 real scientific E2E NOT_RUN, no owner grants or Science HMAC.

## K_Sentinel assigned independent tasks
1. Review pre-dispatch trust boundary: no client consent Boolean/verifier, OIDC + durable replay and signed UDS identity claim binding before KRC custody.
2. Deliver versioned DISABLED external artifact GET proposal: route, authenticated principal/repository/workflow scope, request_id+artifact_id binding, server-clock TTL and SHA verification before streaming, error 403/404/410/429/5xx mapping, audit/replay/timeout cases. X-KRC-Request-ID is selector only.
3. ACK/MISMATCH source versus installed Stage131 parity and preservation of sole Stage127 ingress. No new service, port or key.

## KRC remaining gates
- Full inner science semantics and reviewed enabled signer/consent issue-verify-revoke/expiry tests; separately authorized staging deployment/rollback.
- Bibliography adapter integration and provider license/security/rate limits approval; full test regression.
- External GET must stay disabled pending partner signoff. 48 real scientific E2E NOT_RUN. Production NO-GO.