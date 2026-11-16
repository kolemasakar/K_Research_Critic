# KRC N39 — OWNER APPROVED SINGLE-USER CONSENT MODEL (2026-11-16)

Decision status: **APPROVED BY KRC OWNER IN CHAT**, limited to the personal-use phase. This decision replaces the contradictory multi-user, independently administered issuer and off-platform witness *requirements* in the earlier DRAFT SOP. It does **NOT** authorize deployment, grant the assistant permission to impersonate chat authentication, or waive N39 authorization, cancellation, crash, and provenance tests.

## Scope
- Sole user and sole human decision-maker: KRC owner. No sharing/installation for third parties until a separate explicit instruction or supported plugin distribution changes the account scope.
- Existing protected GitHub branch `audit/n39-anchor-ledger` and current GitHub repository ownership are **accepted and sufficient for development**. No independent GitHub admin account, independent WORM repository, or extra witness is required for the current phase. The previously noted single-owner governance risk is **OWNER_ACCEPTED / DEFERRED**, not a release blocker. Do not reintroduce it until the owner requests.
- An initial research message creates a **PROPOSAL**, not permission to dispatch. The system presents the exact research profile and waits for the owner's explicit confirmation (approve or cancel) in the chat. **The confirmation after the profile** is the authoritative consent, not the request text alone.
- An authenticated chat/session gateway must derive the actual owner identity and conversation/message reference from trusted platform metadata. A caller-provided `owner=true`, free text, synthetic identity, or an unauthenticated message is not sufficient.
- Consent binds exact proposed profile digest, unique research/request ID, owner, chat session, confirmation event/time, and one authorized research run. Profile modification invalidates the old proposal/approval; new confirmation required.
- The owner's confirmation includes permissions required to conduct that single approved research and to retrieve its resulting scoped artifacts, subject to storage TTL, cancellation and existing signed-read security checks. **No separate human approval or root-operator ticket for normal reads in the personal phase.** This supersedes the earlier strict independent retrieval-grant model; clients/tests must be migrated explicitly, and old source-only Sentinel N39 ACK cannot automatically be applied to this revised semantics.
- Authorized research may execute for up to **24 hours from confirmation**, and no later than explicit cancellation or completion. On completion, no further execution on that approval; result retrieval remains permitted for the recorded artifact's retention period while the owner's consent has not been explicitly cancelled. Cancel immediately blocks new dispatch and subsequent artifact reads for the request; previously transmitted bytes cannot be retracted. After cancellation, reauthorization requires a **fresh profile presentation and fresh explicit approval**, with a new consent/request reference; never reactivate or replay the revoked token.
- If the request does not finish within 24 h, the system halts further new processing; continuation needs renewed authorization. Do not turn a consumed execution grant into new work by changing the duration. Existing fail-closed RequestLedger and durable nonce replay controls remain in force.
- Research profile confirmation is not blanket permission for unrelated assets, other people's data, paid provider calls or public release. FREE_ONLY and existing disabled deployed GET/signer constraints remain.
- Auditing uses existing protected GitHub anchor ledger, concise local tamper-evident journal, and the trusted chat confirmation event. Do not create a second repository or require independent administration. No personal or private chat data in the public GitHub audit branch; publish hashes only.
- Keep existing signed peer/HMAC/nonce, ledger ownership, artifact hash and TTL checks. Chat permission must be verified server-side from trusted, durable chat-event provenance; a simple inline text field is not authority.

## Owner-simplified flow
1. OWNER: submits research request.
2. KRC: derives profile, presents details and Cancel/Approve. Stores proposed profile hash and request reference.
3. OWNER: explicitly approves or cancels in the same authenticated chat; gateway persists an immutable event reference and timestamp tied to that profile.
4. KRC: verifies owner/session and exact hash, marks consent one-time with expiration <=24 h; dispatches only the authorized task. Never dispatch on the initial proposal.
5. KRC: records state STARTED/COMPLETED/CANCELLED/EXPIRED and resulting artifacts. Completion closes execution.
6. Read: same approved scope may retrieve generated artifacts until artifact retention expires, unless cancellation/revocation. After explicit cancellation: 403 FORBIDDEN on future authorized read attempts; expired artifact after valid consent: 410 GONE. Missing completed ledger: 404 NOT_FOUND; invalid signature/replay: 403.
7. Audit: preserve profile digest, consent decision/event reference, timestamps and state transitions, GitHub SHA checkpoint (no public personal details). Crash reconciliation never repeats the research.

## Release/acceptance changes
- KRC must implement a staging-only chat confirmation adapter and tests for owner/session provenance, profile changes, one-time dispatch, 24 h time limit, completion and cancellation, post-completion read, digest/TTL, replay and recovery.
- K_Sentinel must independently retest N39 for the **revised owner-approved personal-mode policy** (including 403 post-cancel and 200 post-completion if artifact is still live), not simply retain the earlier independent-root-grant ACK as final.
- K_Science must validate client confirmation UX, trusted consent-event binding, read statuses and SHA.
- No production or installed changes without separate explicit deployment approval. `N39_PERSONAL_POLICY_APPROVED / NEW_POLICY_INTEGRATION_AND_EXTERNAL_ACCEPTANCE_PENDING / Production NO-GO`.

## Deferred by owner
- Any second GitHub admin account / independent WORM store / independent human approval operator.
- Multi-user permissions, sharing plugins to other accounts, additional users.
- Elevated workflow complexity not required to preserve one-owner confirmation, cancellation, provenance and replay guarantees.
