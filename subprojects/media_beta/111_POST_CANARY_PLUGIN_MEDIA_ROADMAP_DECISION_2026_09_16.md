# KRC MEDIA — Post-Canary Plugin MEDIA Roadmap Decision — 2026-09-16

Status: **ROADMAP_APPROVED / BOUNDED_CANARY_CLOSED_PASS / IMPLEMENTATION_NOT_STARTED / PUBLICATION_HOLD**

## Trigger

Checkpoint 110 closed the bounded Remote MCP canary gate with a real owner-account ChatGPT invocation PASS. The owner then approved roadmap planning for progression from the proven one-tool read-only canary toward the real KRC MEDIA Plugin surface.

Final canary documentation head before this roadmap block:

```text
75a4b30e9f478fad892fafc017fea069ce949aec
workflow=35131580138
conclusion=SUCCESS
Tests / Python 3.13=PASS
Tests / Python 3.14=PASS
Quality gates=PASS
```

## Architectural decision

The proven Remote Custom MCP path remains the selected migration candidate.

```text
ChatGPT Plugin/App
-> authenticated remote MCP adapter
-> server-side VoiceBridge credential injection
-> existing VoiceBridge MEDIA API
-> existing provider/durable-state routes
```

The one-tool no-auth Render canary remains evidence only. It must not become the production MEDIA endpoint and must not receive VoiceBridge credentials.

## Non-negotiable invariants

```text
PUBLIC_GPT=UNCHANGED_UNTIL_FINAL_OWNER_GATE
MEDIA_OPERATION_TARGET_COUNT=13
MODEL_VISIBLE_SECRET=false
REPOSITORY_SECRET=false
VOICEBRIDGE_BEARER=SERVER_SIDE_ONLY
PAID_RETRIEVAL_FALLBACK=false
PAID_STT_FALLBACK=false
PAID_PROXY_FALLBACK=false
AUTOMATIC_RETRY_LOOP=false
MEDIA_FAILURE_BLOCKS_CORE=false
YOUTUBE_START_REQUIRES_EXPLICIT_CONSENT=true
```

## Roadmap

### R3-A — Contract freeze and secure adapter baseline

Goal: convert the design-only migration contracts into an implementation-ready Remote MCP contract without live provider work.

Required:

- reconcile `media_tools.yaml`, `media_adapter.yaml`, `auth_transport_binding.yaml`, and migration acceptance contract with the proven MCP surface;
- freeze exact 13-tool names, input/output schemas, annotations, error taxonomy, retry/idempotency semantics, and audit fields;
- classify 9 non-execution tools and 4 execution tools;
- require `readOnlyHint=true` only where semantically read-only;
- require execution tools to be non-read-only and auditable;
- keep Core skill parity unchanged;
- no VoiceBridge secret, no provider call, no deployment mutation.

Exit gate: repository contract/CI PASS.

### R3-B — Inbound authentication and secret-boundary hardening

Goal: replace the canary-only `No authentication` model before any VoiceBridge binding.

Required:

- revalidate the owner-account Plugin authentication surface at execution time;
- determine exact supported semantics of OAuth/Mixed or another managed authenticated mode;
- require authenticated user/plugin access for any endpoint that can reach VoiceBridge;
- keep outbound VoiceBridge bearer server-side only;
- prove secrets are absent from model-visible args, tool descriptions, repo, logs, evidence, and responses;
- prove auth failures fail closed without secret detail;
- do not reuse the current public no-auth canary as a credential-bearing endpoint.

Exit gate: authenticated isolated MCP endpoint with no VoiceBridge/provider binding, connection PASS, secret-sanitization PASS.

### R3-C — Read-only/non-execution VoiceBridge binding

Goal: prove real backend binding without creating provider jobs.

Initial surface: 9 non-execution operations:

```text
media_get_capabilities
media_youtube_preflight
media_youtube_lookup
media_youtube_status
media_youtube_segments
media_instagram_preflight
media_instagram_lookup
media_non_youtube_status
media_non_youtube_segments
```

Required:

- server-side VoiceBridge bearer injection;
- exact request/response mapping;
- structured errors and sanitization;
- bounded timeouts;
- no automatic retry;
- no provider start operation;
- no user-controlled secret field;
- real ChatGPT discovery and bounded read-only invocation tests.

Exit gate: 9-tool non-execution parity PASS with zero start-operation exposure.

### R3-D — Consequential-action confirmation semantics

Goal: verify ChatGPT permission/review behavior before exposing real provider-start operations.

Required:

- use a no-provider/no-charge synthetic execution probe or equivalent isolated mechanism;
- verify `readOnlyHint=false` actions are treated as actions rather than reads;
- verify the account permission mode requires review/confirmation for consequential execution;
- verify cancellation produces no backend/provider work;
- verify repeated/replayed requests cannot duplicate execution;
- record the exact UI/account behavior as evidence.

Exit gate: confirmation semantics PASS without provider work.

### R3-E — Staged execution binding

Goal: add the four start operations one route at a time under separate bounded gates.

Order:

```text
E1 YouTube start
E2 Instagram start
E3 Facebook start
E4 Telegram start
```

Each sub-gate requires:

- explicit owner authorization before the real start call;
- authenticated MCP endpoint;
- server-side VoiceBridge credential only;
- ChatGPT confirmation/action review behavior verified;
- durable job/idempotency checks;
- exact free-only/fail-closed route preserved;
- no automatic paid fallback;
- provider/audit charge fields inspected;
- failure must not affect Core KRC.

Additional YouTube rule:

```text
explicit consent payload required before start
provider=google_gemini
tier=free
data_use_acknowledged=true
```

Exit gate: all four execution routes PASS independently.

### R3-F — Full 13-operation parity and negative regression

Goal: validate the complete private Plugin surface as one coherent MEDIA system.

Required regression groups:

- all 13 operations discoverable with exact schemas;
- positive MEDIA parity;
- invalid URL/platform mismatch;
- invalid job/pagination;
- consent missing;
- free quota/provider unavailable;
- durable-state unavailable;
- charge-uncertain replay blocked;
- retry/idempotency rules;
- secret/error sanitization;
- no paid/unapproved fallback;
- Core regression pack;
- forced MEDIA failure with Core remaining usable;
- model-agnostic Core behavior;
- representative entry points/starters.

Exit gate: private full-parity Plugin acceptance PASS.

### R3-G — Private operational hardening

Goal: prepare the private Plugin for sustained owner use before any migration/publication decision.

Required:

- authenticated production-like endpoint separate from canary;
- health/observability without secret leakage;
- rate/timeout/concurrency controls;
- rollback plan;
- credential rotation procedure;
- deployment pinning and provenance;
- install/uninstall/reconnect recovery;
- multi-session/web availability validation;
- account permission behavior re-check.

Exit gate: private operational readiness PASS.

### R3-H — Migration/publication readiness

Goal: prove replacement readiness while the current public GPT remains unchanged.

Required:

- exact Core skill semantic parity;
- required reference assets enumerated and validated;
- sharing/audience model validated;
- Plugin description/privacy/metadata prepared;
- current public GPT remains available;
- old-link behavior documented;
- migration consequences revalidated against current account notice/UI;
- final cutover rollback/reconstruction package prepared.

Exit gate: `READY_FOR_OWNER_CUTOVER_DECISION` only. No migration/publication occurs here.

### R4 — Owner-approved cutover / migration / publication

Separate irreversible/consequential gate.

Requires explicit owner approval after R3-H PASS. Only then may the project consider:

```text
Plugin publication/share
Custom GPT migration
public user switch
main merge
PR #22 merge
related VoiceBridge PR merge/promotion
```

No R4 action is authorized by this roadmap approval.

## Gate dependency

```text
CANARY CLOSED PASS
-> R3-A contract freeze
-> R3-B auth hardening
-> R3-C 9-tool non-execution binding
-> R3-D confirmation semantics
-> R3-E staged 4 execution routes
-> R3-F full 13-operation parity
-> R3-G private operational hardening
-> R3-H migration/publication readiness
-> R4 separate owner cutover decision
```

No phase implies automatic authorization of the next state-changing phase.

## Immediate next implementation gate

The approved next executable engineering block is **R3-A only**.

R3-A is repository-only and must not:

```text
deploy a new live endpoint
change the live canary
bind VoiceBridge credentials
call providers
expose execution tools
change the public GPT
publish/share/migrate the Plugin
merge PR #22 or VoiceBridge PR #45
```

Terminal marker:

`KRC_POST_CANARY_PLUGIN_MEDIA_ROADMAP_APPROVED_2026_09_16`
