# KRC Stage131 N39 personal-owner consent migration and independent test handoff (2026-11-16)

**Owner policy: APPROVED in chat.** This replaces the multi-user issuance and independent WORM administrative prerequisites for the current personal-use phase. The protected GitHub ledger `audit/n39-anchor-ledger` is accepted. No additional account, repository or independent administrator is required for development or as a release gate.

## Precise owner-approved user flow

1. Sole owner submits a request -> KRC generates a proposed, displayable research profile; **no dispatch on the initial prompt**.
2. Owner must explicitly APPROVE or CANCEL the displayed profile in the same chat. The trusted gateway supplies an authenticated owner/session/event reference and exact profile SHA-256 to the server. Never trust a caller's string `owner=true`.
3. Approval is scoped to one research request, its profile and its resulting scoped artifacts. It includes required research/retrieval permissions; no separate human grant for the same scoped artifacts.
4. Research execution must be claimed only once, starts before 24h from confirmation, ends on completion/cancellation/24h cap. No automatic second run after crash.
5. Completion closes execution. Valid saved artifact reads may continue until artifact retention TTL while not cancelled; explicit CANCEL blocks all future reads and work for this request. Reapproval is a new request and confirmation, never replay of revoked consent.
6. Source-only authorization still requires signed UDS peer/HMAC/durable nonce, RequestLedger.COMPLETE, trusted ArtifactExchange SHA/TTL, and verified owner consent. Revoke -> 403, valid post-completion read -> 200, artifact TTL expired with valid scope -> 410, no matching completed Ledger -> 404.
7. Current GitHub Ruleset ID 27332825 is ACTIVE and accepted as sufficiently reliable for this owner-only phase. Administrative independence/WORM and alternate GitHub account are explicitly deferred by owner, **not release blockers** unless future scope changes.

## Implemented / still required

- SOURCE-only `src/krc_research/stage131_n39_single_owner_chat_consent.py`: `SignedChatEventVerifier` verifies a keyed gateway decision with owner, issuer, chat/session, request, exact profile digest, timestamp, unique event reference. `SingleOwnerConsentLedger` retains PROPOSED/APPROVED/RUNNING/COMPLETED/CANCELLED state, 24h execution limit, one-time claim and registered resulting artifact ownership, and can serve as `SignedArtifactReadBoundary.retrieval_authorizer`.
- Unit/integration tests `tests/test_stage131_n39_single_owner_chat_consent.py` use an isolated **synthetic** gateway key; no real ChatGPT authentication or production consent is issued.
- **NOT YET INTEGRATED:** actual trusted chat gateway event issuer and verifier secret provisioning, UX of displayed profile + approval/cancel, cancellation propagation into running workers, installed Stage127/131 acceptance, runtime parity. These are technical partner gates, not excuses to revive separate human issuer/administrator requirements.
- Historical independent Sentinel root-owned ACK pertains to earlier N39 model; this revised policy needs new independent Sentinel and Science tests.

## Required independent N39 scenarios

- NO_DISPATCH before explicit post-profile approval; reject signed envelope for wrong owner, chat/session, request, or profile hash; reject stale/unsigned event.
- APPROVE exactly once; 24h expiry at boundary; interruption/complete/cancel closes further execution.
- After COMPLETE, valid same-owner scoped artifact returns 200 + exact Content-Length, trusted descriptor SHA-256 == X-Content-SHA256 == body SHA-256. Wrong scope -> 403/404 per established gate ordering.
- CANCEL after COMPLETE immediately denies new artifact reads with 403, and cancellation during running prevents new work. Regrant requires a NEW displayed profile and confirmation.
- TTL = 410 only for still-authorized reads; signed nonce replay -> 403; wrong peer/HMAC -> 403; no new science execution on retrieval or crash recovery.
- Audit: preserve only minimal protected event references/profile SHA and GitHub anchor SHA. Single-owner accepted GitHub controls should be independently verified, but **lack of second GitHub account is not a mismatch**.

## Deployment state
Staging/source-only work approved; **installed runtime / GET / signer changes NOT authorized**. Full external N01-N40 requires partner approval and later owner-controlled reviewed deployment. 200 MiB load OWNER_WAIVED/NOT_TESTED. Production NO-GO.
