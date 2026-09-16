# KRC — Chat Transition Checkpoint — P100 Complete / Plugin-First / P101 Ready — 2026-09-16

Status: CHAT_TRANSITION_READY / P100_PASS / PLUGIN_FIRST_ACCEPTED / P101_NEXT / PUBLICATION_HOLD

## Purpose

Canonical transition checkpoint for moving K-Research & Critic MEDIA work into a new chat after completion of P99/P100 migration preparation.

This checkpoint does not authorize migration, installation, app connection, custom MCP upload, public GPT mutation, Render mutation, merge to `main`, PR #22 merge, or VoiceBridge PR #45 merge.

## Repository / PR state at transition source

Repository: `kolemasakar/K_Research_Critic`

PR #22:
- title: `Stage R3 public MEDIA integration candidate`
- branch: `agent/krc-public-media-r3-integration`
- base: `main`
- source head before transition-doc commits: `426f30350b781be742412467b238ad414feec1e3`
- state: OPEN
- draft: true
- merged: false
- mergeable: true

Validation on source head:
- workflow run: `35120308214`
- conclusion: SUCCESS

## Accepted project state

```text
PROJECT=ACTIVE
P99_CORE_MEDIA_MIGRATION_HARDENING=PASS
P100_MIGRATION_SURFACE_READINESS=PASS
PLUGIN_FIRST_STRATEGY=ACCEPTED
LEGACY_MEDIA_ACTION_CREATION=HOLD
R3_OPENAPI_ROLE=PARITY_REFERENCE
CORE_SKILL_CANDIDATE=READY
MEDIA_TOOL_CONTRACT_CANDIDATE=READY
MEDIA_ADAPTER_CONTRACT=READY
CORE_REGRESSION_PACK=READY
MEDIA_NEGATIVE_REGRESSION_PACK=READY
MEDIA_OPERATION_PARITY_COUNT=13
P100A_SURFACE_DECISION_MATRIX=READY
P100B_AUTH_TRANSPORT_BINDING_SPEC=READY
P100C_SENTINEL_INSPECTION_PACKAGE=READY
P101_NEXT=READ_ONLY_ACCOUNT_SURFACE_INSPECTION
```

## Public KRC state

```text
CURRENT_PUBLIC_GPT=UNCHANGED
CURRENT_ACTIONS=NONE
WORK_CLOUD_BROWSER=PASS
CHATGPT_AUTH=PASS
KRC_BUILDER_ENTRY=PASS
READ_ONLY_SNAPSHOT=PASS
```

The current public GPT remains operational and must remain unchanged until a replacement path is accepted.

Do not create a temporary legacy MEDIA Custom GPT Action unless the explicit fallback exception in `100_KRC_PLUGIN_FIRST_STRATEGY_DECISION_2026_09_16.md` is separately authorized.

## Plugin-first decision

Canonical strategy decision:
`subprojects/media_beta/100_KRC_PLUGIN_FIRST_STRATEGY_DECISION_2026_09_16.md`

Accepted architecture:

```text
Current published KRC GPT
    -> keep unchanged until replacement acceptance

KRC Core
    -> Plugin skill candidate

KRC MEDIA semantics
    -> transport-neutral MEDIA adapter
    -> future supported Plugin App / Connector / remote MCP binding
    -> existing VoiceBridge MEDIA API

Cobalt / AssemblyAI / Gemini
    -> backend/provider details behind VoiceBridge
```

The R3 OpenAPI remains canonical parity evidence, not a currently authorized Builder Action deployment payload.

## Canonical MEDIA routing

```text
YouTube   -> Gemini Developer API Free Tier direct URL
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2
Facebook  -> Cobalt video+audio -> server ffmpeg mono PCM WAV 16 kHz -> AssemblyAI universal-2
Telegram  -> public Telegram web -> AssemblyAI universal-2
```

Hard policies:

```text
paid_retrieval_fallback=false
paid_stt_fallback=false
paid_proxy_fallback=false
supadata_public_active=false
scrapecreators_public_active=false
cookie_login_fallback=false
automatic_retry_loop=false
```

Retry semantics:

```text
COMPLETED -> reuse
PROCESSING -> reuse / concurrency protection
FAILED free-only -> fresh deterministic retry only on a new explicit retry request
FAILED paid or credit_charge_uncertain -> replay blocked
```

YouTube provider execution requires explicit Gemini Free data-use acknowledgement; preflight must not invoke provider work.

## Migration surface decision rules

Canonical matrix:
`plugins/krc_migration_candidate/contracts/surface_decision_matrix.yaml`

Important rules:
- migration itself is state-changing and requires separate owner approval;
- read/fetch-only integration is insufficient for full MEDIA parity;
- full parity requires execution capability for four start/retry operations;
- unknown permission/auth state -> fail closed;
- final Plugin/App/MCP packaging must be chosen only from the actual account-specific surface.

## Auth / transport boundary

Canonical spec:
`plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml`

Required invariants:
- secret placement: server-side / managed only;
- no model-visible secret;
- no repository/skill/evidence secret;
- current VoiceBridge semantics preserved;
- structured/sanitized errors;
- MEDIA failure never blocks Core;
- no automatic retry loop;
- charge-uncertain replay blocked.

Final auth and transport are intentionally TBD until P101 inspection.

## Sentinel coordination

PR #22 is the accepted non-secret coordination channel between KRC and private Sentinel Remote.

P101 must use:
`subprojects/media_beta/100_KRC_MIGRATION_SURFACE_READINESS_SENTINEL_INSPECTION_PACKAGE_2026_09_16.md`

Sentinel inspection is strictly READ ONLY.

Forbidden during P101 inspection:

```text
CLICK_MIGRATE=DENIED
CONFIRM_MIGRATION=DENIED
PLUGIN_INSTALL=DENIED
APP_CONNECT=DENIED
CUSTOM_MCP_UPLOAD=DENIED
CREDENTIAL_CREATE=DENIED
PLUGIN_SHARE_CHANGE=DENIED
PLUGIN_PUBLICATION=DENIED
PUBLIC_GPT_UPDATE=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

Required non-secret evidence includes:
- migration control presence;
- Plugin surface presence;
- connected app option;
- custom MCP option;
- read/fetch vs execution/write capability;
- remote MCP support;
- non-secret auth options;
- action confirmation/review model;
- web/desktop availability;
- install/share/publish permissions.

## Canonical candidate assets

Core:
- `prompts/GPT_STORE_INSTRUCTIONS.md`
- `plugins/krc_migration_candidate/skills/krc_core/SKILL.md`

MEDIA:
- `gpt_store/actions/media_public_r3_openapi.yaml`
- `prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md`
- `plugins/krc_migration_candidate/contracts/media_tools.yaml`
- `plugins/krc_migration_candidate/contracts/media_adapter.yaml`
- `plugins/krc_migration_candidate/contracts/surface_decision_matrix.yaml`
- `plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml`

Regression:
- `plugins/krc_migration_candidate/regression/core_cases.yaml`
- `plugins/krc_migration_candidate/regression/media_negative_cases.yaml`
- `tests/test_krc_plugin_migration_candidate.py`
- `tests/test_krc_p100_surface_readiness.py`

Recent checkpoints:
- `98_KRC_PLUGIN_MIGRATION_CANDIDATE_SKELETON_CHECKPOINT_2026_09_16.md`
- `99_KRC_CORE_MEDIA_MIGRATION_HARDENING_CHECKPOINT_2026_09_16.md`
- `100_KRC_MIGRATION_SURFACE_READINESS_SENTINEL_INSPECTION_PACKAGE_2026_09_16.md`
- `100_KRC_PLUGIN_FIRST_STRATEGY_DECISION_2026_09_16.md`

## Next phase — P101

P101 objective:

```text
READ_ONLY ACCOUNT-SPECIFIC MIGRATION / PLUGIN SURFACE INSPECTION
```

Execution order:
1. read this transition checkpoint and bootstrap package;
2. verify current PR #22 head and latest CI before any work;
3. read checkpoint 100 inspection package;
4. check whether account-specific migration/plugin surface is available;
5. if unavailable -> record `P101_SURFACE_NOT_AVAILABLE` and STOP; do not invent an implementation;
6. if available -> inspect read-only and return non-secret evidence through PR #22;
7. classify surface using `surface_decision_matrix.yaml`;
8. produce a proposed binding plan from `auth_transport_binding.yaml`;
9. do not migrate/install/connect/upload/publish without separate owner approval.

## Hard boundary at transition

```text
MIGRATION_EXECUTION=DENIED
PLUGIN_APP_BINDING=NOT_STARTED
CUSTOM_MCP_IMPLEMENTATION=NOT_STARTED
PLUGIN_INSTALLATION=DENIED
APP_CONNECTION=DENIED
CUSTOM_MCP_UPLOAD=DENIED
PLUGIN_PUBLICATION=DENIED
PUBLIC_GPT=UNCHANGED
PUBLICATION=HOLD
MAIN_MUTATION=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

Terminal marker:

`KRC_MEDIA_CHAT_TRANSITION_P100_COMPLETE_PLUGIN_FIRST_P101_READY_2026_09_16`
