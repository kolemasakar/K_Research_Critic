# KRC N39 — OWNER-APPROVED SIMPLIFIED PROJECT-CHANNEL CONSENT (2026-11-16)

**Decision:** the current KRC user is the sole owner, working in the authenticated ChatGPT Project. No separately distributed plugin exists. The owner's logged-in ChatGPT session is treated as sufficient *user-facing* identity establishment. KRC must not demand another login, identity challenge, independent GitHub administrator, extra human approver, per-confirmation user signature or separate read consent.

This document **amends** earlier owner-approved single-user consent design. Any sentence in the previous document that mandates a second authenticated ChatGPT-user identity event/HMAC for a human response is superseded for this personal Project mode. Do not reactivate a second identity check in tests.

## Minimal intended workflow

1. The owner requests research inside their current ChatGPT Project.
2. KRC creates a research proposal and presents a fixed, concrete profile: task, scope, sources, constraints and intended outputs. No research dispatch yet.
3. The owner replies APPROVE or CANCEL to this presented profile in the same project context. No second login, OTP, password, operator or HMAC signature on the user response.
4. The trusted *internal* Project action handler passes only the action, original request reference and profile digest to the KRC consent ledger. The ledger records an opaque event reference, one-time allowance, 24h limit, state and cancellation. The rest of the existing technical controls still apply (replay, RequestLedger, artifact scope, SHA, TTL).
5. Any profile change requires presenting the modified profile and re-confirming. Approval of one profile does not authorize a different research, paid-provider action, plugin publication or access outside its generated artifacts.
6. On owner CANCEL, no more research steps or future reads. The same consent cannot be replayed or reopened; start a fresh request/profile if needed.

## Trust boundary: minimum technical requirement

The **only necessary identity boundary is the already-authenticated ChatGPT Project access**. A KRC server cannot independently infer the identity of an arbitrary incoming HTTP client merely from a text label claiming it came from the project. Therefore this exemption applies only to the **trusted internal project action handler**, with no public unauthenticated approve/cancel endpoint.

- The project handler is the already-approved internal route invoked after the ChatGPT Project interaction. There is **no separate owner login**.
- ProjectChannelVerifier's private in-process invocation marker prevents accidentally treating arbitrary user-supplied JSON as a direct consent event; it does not prove a ChatGPT account and must not be advertised as a cryptographic or external authentication mechanism.
- If a future installed transport receives arbitrary inbound HTTP without a trusted project boundary, do not expose the direct consent method at that transport. Preserve existing transport access protection; that is not a new human identity challenge.
- Never write personal ChatGPT session identifiers, login credentials or private chat text into the public GitHub audit branch.

## Source change and evidence

- New source-only adapter: `src/krc_research/stage131_n39_project_channel_consent.py`, classes `ProjectChannelVerifier` and `TrustedProjectConsentAdapter`. No external app/plugin deployment or credential provisioning.
- Existing `SingleOwnerConsentLedger` supports either the optional previously tested signed gateway or this simpler trusted internal project channel. The signed gateway is NOT mandatory for the owner's personal project path.
- Tests `tests/test_stage131_n39_project_channel_consent.py`: no second owner challenge, no dispatch before approval, exact profile/chat/request binding, denial of untrusted JSON and profile changes, single execution, 24h limit, cancel/reapprove, post-completion read.
- The existing root-grant/multi-user issuer workflows are historical/optional and are not current personal release blockers.

## Scope and gate

**OWNER SIMPLIFICATION APPROVED / SOURCE-ONLY ADAPTER IMPLEMENTED / ACTUAL TRUSTED CHATGPT PROJECT HANDLER NOT YET CONNECTED / STAGING EXTERNAL GET OFF / PRODUCTION NO-GO.** This permission decision does not approve installed runtime or production deployment, and the current source tests do not establish that a live ChatGPT message reached KRC through an authenticated connector.
