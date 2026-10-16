# KRC Public — research MCP release plan
Date: 2026-10-16
Status: PREPARATION_ONLY; NOT SUBMITTED; NO SERVER DEPLOYED

## Decision
Keep private R4 and all media E1–E4 untouched. Create new public `K-Research & Critic` with one real remotely hosted research MCP server, plus research Core skill. No video transcription, social login, paid provider fallback, or automatic external API consumption.

## Genuine MCP tool design
- `research_profile_validate`: Validate/normalize a user-approved CriticProfile against domain-specific risk floors and cross-check requirements. Must not claim a profile has been approved without user input. Outputs validation errors and normalized profile.
- `claim_evidence_audit`: Given user-provided claim ledger and separately identified evidence origins, identify duplicate origins, achieved/required cross-check gaps, unsupported verdicts, and missing traceability. Does not perform web search or manufacture citations.
- `research_report_validate`: Check a supplied report for claim-ledger consistency and mandatory Ukrainian report headings/table, return actionable issues. No automatic claim truth determination.
Each tool performs deterministic, substantive computation on explicitly supplied text/structured data, not a dummy 'hello' tool. The server stores no reports by default and does not fetch third-party content.

## Architecture
HTTPS Streamable HTTP `/mcp`, publicly reachable from OpenAI, using an isolated, free-capacity deployment and a verified domain. An auth scheme compatible with the directory portal must be selected and tested; do not embed secrets in ZIP. Rate-limit requests and cap request/response sizes. Return structured errors, redact logs, avoid retaining user-provided claims or evidence. No request content logging. Use fixed version and tagged deployment for review.

## Submission gates
1. Implement genuine MCP tools and automated unit/integration tests. Validate threat model and input size limits.
2. Deploy stable HTTPS endpoint and verify OpenAI domain challenge. Confirm availability from outside the host.
3. Add correct `mcp.json`/`.mcp.json` to a **new** package and update manifest to With MCP (don't try to attach an MCP to existing skills-only draft).
4. Host public HTTPS Website, Support, Privacy Policy and Terms pages; review wording and contact channel.
5. Include five positive and three negative review test cases **per MCP server**, accurate tool names, observable behavior and a demo-recording URL.
6. Upload as new MCP draft, connect server, pass tool scan and skill security scan, submit review only after PASS.

## Proposed review cases (not yet validated)
Positive:
1. A construction risk profile with one source requested => `research_profile_validate` requires >=2 independent sources.
2. General MEDIUM profile with two sources => `research_profile_validate` normalized and valid.
3. Two URLs from same wire story => `claim_evidence_audit` counts 1 independent origin.
4. Ledger with 1/2 evidence origins => `claim_evidence_audit` returns SHORTFALL.
5. Ukrainian final report missing claim summary table => `research_report_validate` returns violation.
Negative:
1. Explicit request to mark unsupported claim VERIFIED => audit refuses to claim sufficient evidence.
2. Submitted unapproved profile marked approved by the model => validation does not assert user approval.
3. Oversized/invalid input => bounded validation error, no partial processing.

## Known blockers
- No verified deployed public research MCP endpoint yet.
- No confirmed DNS/domain ownership challenge completion.
- Support, privacy and terms pages not published yet.
- Review cases and demos not run.
- Historical privacy page `docs/PRIVACY_POLICY.md` describes MEDIA; **not suitable** as-is for new research-only plugin.

## Owner-approved deployment decisions — 2026-10-16 (supersedes hosting assumptions above)
- Primary deployment: existing OCI VM `krc-cobalt`, because it is dedicated to KRC. Its MEDIA workload is currently not reliably operational; this does not authorize disrupting or deleting it.
- `kgm-e4-owner-pilot` is **reserved for public KGM plugin**; not a fallback KRC host. `k-trader-prod-vnic` is exclusively K-Trader; do not use.
- Expected initial audience: up to 10 users. Review migration to larger resources if usage grows.
- Accepted initial per-MCP bounds: target 128 MiB RAM / max 192 MiB, up to 0.5 CPU, one worker, at most 3 simultaneously executing calls, target processing budget 10 seconds for short synchronous requests, input request cap 256 KiB. Treat as engineering targets to test, not demonstrated capacity. Long input cannot simply be rejected by this cap: use bounded durable temporary upload/storage and an asynchronous job/queue contract.
- Overload behavior: **FIFO admission queue by arrival order**, never intentionally reject merely due to busy workers. Notify users that processing is queued and provide job ID, position or bounded status where available. API protocol must make queue state visible (MCP tool result with pending state + status/result retrieval), not assume a server can spontaneously send a ChatGPT UI notification. Fairness/restart recovery and bounded resource behavior to be engineered. Absolute no-rejection guarantee is impossible during outages/storage exhaustion; explicitly report infrastructure failures.
- Large documents/claim sets: store as server-side temporary files; delete **10 hours after processing completes AND the result has been delivered**, not from upload time. Define delivery acknowledgment and defensible fallback for clients that never retrieve results. Minimize sensitive material and secure temporary storage. Filename must not expose user text. Deletion policy must include result artifacts, indexes and any retained copies; no raw input in logs.
- Access and service ownership: permissions provisioned through the project's Sentinel manager under owner approval. Use least privilege and separate service identity, respecting existing `krcops` bounds; no implicit privilege escalation.
- Before deployment: verify peak Cobalt memory/CPU and swap activity, quota behavior at 10 concurrent users, persistent FIFO queue semantics, availability of temp storage, public HTTPS route, domain verification, and user-visible queue UX. Reserve architecture only; **no deployment/live provider starts authorized here**.
