# KRC Plugin Migration Candidate

Status: **PRIVATE_MCP_IMPLEMENTATION_VALIDATED / R3-H_COMPLETE / R4_READONLY_PREFLIGHT_COMPLETE / OWNER_CUTOVER_DECISION_PENDING / PUBLICATION_HOLD**

This directory contains the repository-side migration candidate for moving K-Research & Critic from the retiring Custom GPT surface to the OpenAI Plugin model while preserving Core behavior and the accepted FREE_ONLY MEDIA contract.

## Current implementation state

The project has advanced beyond the original repository-only canary stage.

Accepted runtime state:

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3_E1=COMPLETE
R3_E2=COMPLETE
R3_E3=COMPLETE
R3_E4=COMPLETE
R3_F=COMPLETE
R3_G=COMPLETE
R3_H=COMPLETE
R4_NON_UI_PREFLIGHT=COMPLETE
R4_MANUAL_UI_PREFLIGHT=COMPLETE
R4_READONLY_PREFLIGHT=PASS / COMPLETE
R4_TECHNICAL_PREFLIGHT_DEBT=0
R4=HOLD
```

The private MCP implementation has validated:

- authenticated remote MCP transport;
- OAuth DCR and restart-safe token continuity;
- runtime refresh-token continuity after access-token TTL;
- 9 read-only operations;
- 4 isolated execution operations;
- ChatGPT confirmation behavior for consequential actions;
- FREE_ONLY YouTube, Instagram, Facebook, and Telegram live canaries;
- durable replay/idempotency inside the configured retention window;
- 13-operation runtime parity;
- server-side-only VoiceBridge credentials.

The current live/private sentinels are **not** authorization to publish or share a replacement Plugin.

## Canonical candidate assets

- `skills/krc_core/SKILL.md` — Core instruction snapshot.
- `contracts/media_tools.yaml` — 13-operation MEDIA parity contract.
- `contracts/media_adapter.yaml` — transport-neutral VoiceBridge adapter contract.
- `contracts/surface_decision_matrix.yaml` — fail-closed surface-selection rules.
- `contracts/auth_transport_binding.yaml` — authentication/transport requirements.
- `mcp_canary/` — implemented remote-MCP protocol/runtime surfaces used through R3.
- `regression/core_cases.yaml` — Core behavioral fixtures.
- `regression/media_negative_cases.yaml` — MEDIA safety/negative fixtures.
- repository tests — Core parity, exact operation parity, auth, confirmation, FREE_ONLY and regression guards.

## Accepted operation model

```text
READ_OPERATIONS=9
EXECUTION_OPERATIONS=4
TOTAL_OPERATIONS=13

media_youtube_start
media_instagram_start
media_facebook_start
media_telegram_start
```

Each execution surface exposes only its own start operation. Other execution tools remain disabled.

## Authentication and permission boundary

Target architecture:

```text
ChatGPT Plugin/App
  -> authenticated remote MCP adapter
  -> server-side VoiceBridge scoped bearer
  -> existing VoiceBridge MEDIA API
```

VoiceBridge secrets must never appear in skill text, repository files, model-visible parameters, user-visible output, or documentation.

Current private-plugin permission model verified during R3-H review:

```text
global permission = Allow read actions
changes = confirmation required
E3 app permission = Use my default
E4 app permission = Use my default
```

## FREE_ONLY invariant

```text
PROJECT_COST_POLICY=FREE_ONLY
AUTOMATIC_PAID_FALLBACK=DENIED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
COOKIE_LOGIN_FALLBACK=DENIED
```

Accepted retrieval/STT routing remains documented in the MEDIA checkpoints and VoiceBridge candidate branch.

## R3-G operational hardening

Accepted:

```text
DCR=PASS
ACCESS_TOKEN_RESTART_CONTINUITY=PASS
REFRESH_TOKEN_RESTART_CONTINUITY=PASS
RUNTIME_REFRESH_AFTER_3600S_TTL=PASS
CHATGPT_RECONNECT_REQUIRED=NO
E3_TO_VOICEBRIDGE_ROUTE_AUTH=PASS
R3_G=COMPLETE
```

Managed-media staging retention is currently 3600 seconds. Expired canary rows are purged by policy; post-expiry `MEDIA_TRANSCRIPT_NOT_FOUND` is expected.

## R3-H / R4 preflight boundary

R3-H is complete. R4 read-only preflight is also complete: non-UI validation plus manual current-account UI inspection.

Allowed work:

- contract/document consistency;
- current account/plugin-surface inspection;
- permission/security review;
- rollback/recovery plan;
- release checklist.

Not authorized:

```text
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
ADDITIONAL_LIVE_MEDIA_STARTS=NO
R4=HOLD
```

## Canonical recovery authority

- `subprojects/media_beta/CURRENT_HANDOFF.md`
- `subprojects/media_beta/161_R3G_OPERATIONAL_HARDENING_COMPLETE_2026_09_20.md`
- `subprojects/media_beta/02_ROADMAP.md`

Public migration/cutover must remain separately owner-approved. Manual UI inspection confirmed the GPT identity, GPT Store/share controls, Plugin surface, private KRC plugin inventory, install/add controls and Skills surface. No explicit Migrate control was found in the current UI. Before any cutover, recover from CURRENT_HANDOFF v19.9 + checkpoint 166; GitHub Actions are currently unavailable, so use the recorded exact-commit Render/live read-only validation and obtain explicit owner approval.


## R3C OAuth recovery after checkpoint 165

```text
R3C_OAUTH_RECOVERY=PASS
R3C_RUNTIME_VALIDATED_HEAD=27585c0ce924c78529b90aaadbfbeee841d0d249
MEDIA_GET_CAPABILITIES=PASS
PLUGIN_REQUIRED_SURFACES=PASS
RECOVERY_CONSISTENCY_WARNING=CLOSED
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO
CURRENT_VALIDATION_MODE=EXACT_COMMIT_RENDER_BUILD + LIVE_READONLY_RUNTIME
R4_CUTOVER=HOLD
```

Canonical recovery is now `CURRENT_HANDOFF.md` v19.9 + checkpoint 166.
