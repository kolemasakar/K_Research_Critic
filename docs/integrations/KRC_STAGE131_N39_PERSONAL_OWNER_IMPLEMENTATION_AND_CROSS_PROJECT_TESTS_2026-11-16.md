# KRC Stage131 N39 — approved single-owner personal chat model, source and cross-project isolated evidence (2026-11-16)

## Decision authority
The sole KRC owner APPROVED the following, as the CURRENT requirements:
- one owner, no other plugin users or shared permissions until explicitly requested;
- initial chat message -> show research profile -> wait for explicit answer APPROVE or CANCEL;
- approval of the displayed profile includes the one research run and the right to retrieve its scoped resulting artifact(s), with no separate human grant ticket;
- execution must end after completion/cancellation and cannot continue beyond 24h from confirmation; saved artifacts remain readable while not cancelled and within their own retention TTL; cancellation forbids new work and new reads;
- new approval after cancellation requires a new profile, fresh event and request ID;
- existing GitHub branch `audit/n39-anchor-ledger` is accepted and sufficient for personal-stage audit. A different GitHub administrator, second account, independent WORM repository or additional human issuer is DEFERRED BY OWNER and NOT a development/release blocker unless the owner later changes the scope;
- approved rules do NOT authorize installed Stage127/Stage131/GET/signer changes. These require separate review/authorization.

Authoritative decision: `docs/integrations/KRC_STAGE131_N39_OWNER_APPROVED_SINGLE_USER_CONSENT_2026-11-16.md`. Earlier multi-user SOP DRAFT explicitly marked SUPERSEDED.

## Source implementation
`src/krc_research/stage131_n39_single_owner_chat_consent.py`
- `SignedChatEventVerifier`: schema + HMAC-verifies a trusted gateway owner, issuer, session, request, displayed profile digest, decision, event reference and timestamp; cannot accept unsigned untrusted prompt text.
- `SingleOwnerConsentLedger`: durable SQLite PROPOSED / APPROVED / RUNNING / COMPLETED / CANCELLED, one-time claim, 24h expiry, `can_continue()` for every new worker step, post-completion scoped artifact registration/read until owner cancellation.
- `is_authorized` hooks to actual `SignedArtifactReadBoundary.retrieval_authorizer`; existing HMAC/durable nonce/RequestLedger.COMPLETE/ArtifactExchange SHA/TTL remain enforced. A cancellation after completion denies subsequent signed reads.
- This is a **source-only staging candidate**; a real ChatGPT owner identity gateway and a signed-event issuer are NOT installed or verified. Tests sign synthetic events with test-only keys.

## Evidence / exact pins
- KRC source+test pin `8dbd9cec62e1c4da45c9ddf5eafe4eda68a900e4`.
- KRC owner-model isolated source tests `tests/test_stage131_n39_single_owner_chat_consent.py`: **7 PASS / 0 FAIL**, including real signed artifact boundary, cancellation, 24h, restart.
- KRC entire isolated pytest suite on krc-cobalt: **1164 PASS / 18 SKIP / 0 FAIL** (source/test commit `8dbd9ce...`).
- K_Sentinel standalone source regression `staging/transport_v2/test_stage131_n39_single_owner_chat127.py`, commit `02cdc937291e02710ac1c1a90cbf220a3d58e889`, loaded from exact connector file and executed with pinned KRC source on isolated krc-cobalt: **2 PASS / 0 FAIL**. Tests actual AF_UNIX signed HTTP 200 after owner consent, 403 after cancellation, no repeat execution, wrong profile/owner, and 24h.
- K_Science standalone `tests/test_n39_single_owner_real_krc_consumer.py`, commit `afd3fb1b13436a9a60e55016a28461e2419a5fd3`, loaded from exact connector files with its *actual* candidate validator, tightened schema, artifact receiver and pinned KRC source on isolated krc-cobalt: **2 PASS / 0 FAIL**. Verifies post-consent real artifact bytes/descriptor/header SHA equality and 403/410 fail before reading denied body.
- All synthetic artifacts, chat confirmations and keys; no live owner consent event, no new actual science task, no root grant, no production service or activation.
- The source tests in partner repos were authored/coordinated by KRC and run in an isolated checkout. They are **not** a substitute for a separately performed independent reviewer ACK, independent installed parity, or external N01–N40 full-case acceptance.

## Remaining technically necessary gates (not deferred owner policy)
1. Implement trusted chat UI approval/cancel and authenticated event issuer; bind owner identity and displayed research profile to the signed decision. Caller text alone never constitutes verified provenance.
2. Wire the approved ledger and `can_continue()` into the actual staging execution path and install-level artifact read adapter, without bypassing signed peer/nonce/ledger/storage checks. Test cancellation while a real simulated workload is running.
3. K_Sentinel independently executes N39 on the approved single-owner policy and formally returns ACK/MISMATCH; K_Science independently verifies authenticated profile consent, trusted descriptor, receiver 200/403/410 SHA/no retry. A separate root-issued read consent is NOT a requirement in this scope.
4. Installed Stage127/131 external GET N01–N40 and wider science E2E are still NOT_ACCEPTED until explicitly approved reviewed deployment; Production NO-GO. The 200 MiB load test remains OWNER_WAIVED / NOT_TESTED.

**STATUS: OWNER POLICY APPROVED / KRC SOURCE 1164 PASS / PARTNER ISOLATED SCENARIOS PASS / FORMAL INDEPENDENT AND RUNTIME INTEGRATION PENDING / PRODUCTION NO-GO.**
