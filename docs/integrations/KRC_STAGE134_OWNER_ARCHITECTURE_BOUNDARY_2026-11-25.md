# KRC / K_Sentinel / K_Science - owner architecture decision (2026-11-25)

Status: OWNER_DIRECTION_RECORDED; EXISTING_TRANSPORT_REUSE; STAGE134_EXTERNAL_E2E_NOT_RUN.

## Responsibility boundary

- K_Science specifies the scientific task, supplies source data, receives results and may independently verify their scientific suitability. It must not implement KRC operation-specific wire construction, provider orchestration, or research algorithms.
- K_Sentinel owns the existing universal authenticated transport: caller identity, routing, bounded opaque payload, secure delivery, artifact transport, replay and transport error handling. Reuse Stage127. Do not create another transport or operation-specific Sentinel route.
- KRC owns task interpretation, operation selection, preparation of the exact research profile and protocol-level request, schemas, consent, dispatch, research, provenance, result construction and scientific limitations.

## Evidence and actual gap

Sentinel PR39 already verifies opaque bibliography forwarding (six synthetic tests) and signed identity policy separately. Its Stage127 transport is not specific to bibliography. KRC PR36 already implements the operation/schema/consent and result path. Stage134 immutable release 62007ba9de3700a8fbd24a527c49b6392e3a41e2 is installed in staging in DEFAULT_DENY mode per owner terminal output on 2026-11-25. Independent process-status observation confirms services running, but authenticated external functional acceptance is still pending.

Existing Stage127 POST /staging/v2/execute accepts request_id, operation and payload; the KRC boundary matches the supplied payload against its server-owned immutable approved profile. Therefore existing transport compatibility alone does not prove that the current caller can submit only a high-level task without assembling a KRC-specific envelope. Current K_Science Stage133 workflow selects pinned operation-specific inputs; Stage134 independent result validator is not a generic task entrypoint. Do not solve this by adding one sender/workflow per KRC operation.

## Revised work

1. Identify and reuse the existing Sentinel caller entrypoint and generic delivery primitive. Ask Sentinel to demonstrate the supported invocation of an opaque KRC-produced request from the already trusted caller, not design a replacement transport. If no such caller entrypoint is available under the installed identity policy, report that exact gap to Sentinel.
2. In KRC, provide or reuse a stable task-to-request preparation interface and a generic execution/result contract over that transport. The source of the exact wire request is KRC, not K_Science. Preserve existing Stage133 behavior. A narrowly scoped KRC-produced immutable dispatch artifact is an acceptable candidate for review; not a new transport or a live approved design.
3. K_Science supplies domain task and inputs and invokes the established generic interface. Retain its independent result checking as a consumer function; do not create stage134-specific sender or workflow. Avoid putting private raw captures or proposals in public GitHub workflow inputs, logs, or files.
4. Verify installed Stage133 regression, then valid-identity Stage134 default deny, then the exact owner-approved one-shot real E2E. Existing approval scope unchanged: KS-50902e5cfe263a8c760fc2dfa4a26882 / SHA256 5f5866fd563758cfa305b9a28c5cbb8862903feb617581266bc2f57b3b84dad7. No server approval TTL starts until the ready staging window. No bypass, blind retry, paid provider or production activation.

## Nonclaims

This decision does not mean an end-to-end generic task invocation has been demonstrated. No code, service, approval ledger or identity policy was modified by this documentation update. Production NO_GO. Normal KRC FREE_ONLY public internet research remains available by default and is separate from the signed offline inter-project consent path.
