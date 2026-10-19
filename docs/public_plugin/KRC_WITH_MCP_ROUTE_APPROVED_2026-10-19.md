# KRC PUBLIC — WITH_MCP route owner decision and readiness gate
Date: 2026-10-19
Status: WITH_MCP_ROUTE_APPROVED; DEPLOYMENT_NOT_APPROVED; PUBLICATION_NOT_STARTED

## Trigger
OpenAI support advised that personal Plus distribution of a migrated skills-only plugin is not currently supported/confirmed, and skills-only new public submissions are blocked. Owner selected option 1 on 2026-10-19: revisit a minimal research With MCP publication path.

## Scope
- Primary goal remains a discoverable KRC plugin installable by third-party ChatGPT Plus users, no extra KRC login or paid infrastructure.
- Preserve existing personal NO_MCP 0.19.8 PRIVATE release; no silent conversion or mutation.
- Preserve existing R4 MEDIA integrations and Cobalt/VoiceBridge production, server k-trader excluded.
- Use existing KRC Research MCP sources/deployment where authorized; read-only review first, no restart/route exposure until security gates pass.
- A separate With MCP public submission is expected: official docs state an MCP server cannot be added to an existing skills-only plugin submission.
- All changes FREE_ONLY, no payment method or billable provider enrollment.

## Verified source requirements
Official source: https://developers.openai.com/plugins/deploy/submission
- Verified publishing identity, organization/project publication permissions.
- Stable public HTTPS endpoint for remote MCP submission.
- 5 positive and 3 negative test cases; video walkthrough and release notes.
- websiteURL, supportURL, privacyPolicyURL, termsOfServiceURL for MCP review.
- Further MCP scanning and review; acceptance is not assured.

## Existing environment (historical evidence, not a live verified status)
- OCI host krc-cobalt, prior local Research MCP 127.0.0.1:9013 under systemd with constrained permissions; Cobalt production separately on 127.0.0.1:9000.
- Prior 120/120 requests PASS, 10 concurrent in twelve rounds, no service restarts; not a substitute for public endpoint and review.
- SentinelX 2026-10-19 tool reported only k-trader-prod-vnic currently online, so no krc-cobalt live inspection via this connection. Do not use K-Trader.
- Developer Portal skills-only candidate 0.1.0 and migrated private 0.19.8 have different identities. Do not assume transfer of users/discoverability.
- External service status, auth-free access, ownership of domain, privacy and legal URLs all require fresh verification.

## Execution roadmap
G0: Verify exact identity and immutable backup of public With MCP candidate and private KRC 0.19.8; preserve old private release.
G1: Obtain read-only access to KRC host and inspect public MCP source, service identity, tools/schema, protection, limits, data handling.
G2: Define genuinely useful minimal research MCP tool(s), read-only and unauthenticated user access where allowed; independent evidence trail; do not expose MEDIA.
G3: Review security: SSRF/abuse, rate limits, queue, 10-hour temporary retention if processing jobs require it, 10% disk free, logging minimization, no financial charges.
G4: Host a narrowly routed public HTTPS endpoint (separate path/domain), with security tests, authorization and owner approval before modification.
G5: Validate MCP operations, 5 positive and 3 negative cases, evidence and video; verify metadata/support/privacy/terms/legal materials.
G6: New With MCP developer portal package and review; confirm Plus user can install in real separate account after approval. Do not claim publication until verified.

## Current blockers
No live krc-cobalt connection through SentinelX free single active host slot; K-Trader is not an alternative. No public research MCP HTTPS endpoint confirmed in this session. Submission and guest Plus install are untested. Owner has not approved any production change.
