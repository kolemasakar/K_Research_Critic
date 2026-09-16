# BOOTSTRAP PACKAGE — KRC Plugin-First / P101 Handoff — 2026-09-16

Use this file to resume K-Research & Critic MEDIA work in a new chat without relying on prior chat memory.

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/BOOTSTRAP_PACKAGE_2026-09-16_KRC_PLUGIN_FIRST_P101_HANDOFF.md і продовжуй з P101.`

## Mandatory recovery order

1. `subprojects/media_beta/BOOTSTRAP_PACKAGE_2026-09-16_KRC_PLUGIN_FIRST_P101_HANDOFF.md`
2. `subprojects/media_beta/101_CHAT_TRANSITION_P100_COMPLETE_PLUGIN_FIRST_P101_READY_2026_09_16.md`
3. `subprojects/media_beta/100_KRC_PLUGIN_FIRST_STRATEGY_DECISION_2026_09_16.md`
4. `subprojects/media_beta/100_KRC_MIGRATION_SURFACE_READINESS_SENTINEL_INSPECTION_PACKAGE_2026_09_16.md`
5. `subprojects/media_beta/99_KRC_CORE_MEDIA_MIGRATION_HARDENING_CHECKPOINT_2026_09_16.md`
6. `subprojects/media_beta/98_KRC_PLUGIN_MIGRATION_CANDIDATE_SKELETON_CHECKPOINT_2026_09_16.md`
7. `plugins/krc_migration_candidate/contracts/surface_decision_matrix.yaml`
8. `plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml`
9. `plugins/krc_migration_candidate/contracts/media_adapter.yaml`
10. `plugins/krc_migration_candidate/contracts/media_tools.yaml`
11. `plugins/krc_migration_candidate/regression/core_cases.yaml`
12. `plugins/krc_migration_candidate/regression/media_negative_cases.yaml`
13. `prompts/GPT_STORE_INSTRUCTIONS.md`
14. `plugins/krc_migration_candidate/skills/krc_core/SKILL.md`
15. current PR #22 state and latest CI

## Project identity

Repository:
`kolemasakar/K_Research_Critic`

PR:
`#22 — Stage R3 public MEDIA integration candidate`

Branch:
`agent/krc-public-media-r3-integration`

The transition source head before handoff-doc commits was:
`426f30350b781be742412467b238ad414feec1e3`

Source-head CI:
`35120308214 / SUCCESS`

At recovery, always re-read the current PR head and latest CI because transition documentation commits may have advanced the branch.

## Current strategic decision

```text
PLUGIN_FIRST_STRATEGY=ACCEPTED
LEGACY_MEDIA_ACTION_CREATION=HOLD
R3_OPENAPI_ROLE=PARITY_REFERENCE
CURRENT_PUBLIC_GPT=UNCHANGED
```

Do not resume the old Builder Action creation path as the default next step.

A temporary legacy Action can be reconsidered only under the explicit exception defined in:
`100_KRC_PLUGIN_FIRST_STRATEGY_DECISION_2026_09_16.md`

## Accepted readiness state

```text
PROJECT=ACTIVE
P99_CORE_MEDIA_MIGRATION_HARDENING=PASS
P100_MIGRATION_SURFACE_READINESS=PASS
P100A_SURFACE_DECISION_MATRIX=READY
P100B_AUTH_TRANSPORT_BINDING_SPEC=READY
P100C_SENTINEL_INSPECTION_PACKAGE=READY
CORE_SKILL_CANDIDATE=READY
MEDIA_TOOL_CONTRACT_CANDIDATE=READY
MEDIA_ADAPTER_CONTRACT=READY
CORE_REGRESSION_PACK=READY
MEDIA_NEGATIVE_REGRESSION_PACK=READY
MEDIA_OPERATION_PARITY_COUNT=13
```

## Public GPT / Builder state

Accepted read-only evidence:

```text
WORK_CLOUD_BROWSER=PASS
CHATGPT_AUTH=PASS
KRC_BUILDER_ENTRY=PASS
READ_ONLY_SNAPSHOT=PASS
CURRENT_ACTIONS=NONE
PUBLIC_GPT=UNCHANGED
```

The existing public KRC GPT remains usable and must not be updated, migrated, deleted, or otherwise mutated without separate approval.

## Core migration candidate

Canonical Core instructions:
`prompts/GPT_STORE_INSTRUCTIONS.md`

Candidate skill:
`plugins/krc_migration_candidate/skills/krc_core/SKILL.md`

CI guards exact snapshot parity.

Core regression pack covers:
- CriticProfile direct-run gate;
- CriticProfile review/edit gate;
- risk/cross-check floors;
- SHORTFALL handling;
- traceability;
- checkpoint recovery;
- Ukrainian/English behavior;
- mandatory Ukrainian protocol table;
- MEDIA failure isolation;
- no hidden reasoning exposure;
- no silent request-log re-enable.

## MEDIA migration candidate

Canonical MEDIA API parity source:
`gpt_store/actions/media_public_r3_openapi.yaml`

Accepted operation count:
`13`

Contract:
`plugins/krc_migration_candidate/contracts/media_tools.yaml`

Transport-neutral adapter:
`plugins/krc_migration_candidate/contracts/media_adapter.yaml`

Canonical routes:

```text
YouTube   -> Gemini Developer API Free Tier direct URL
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2
Facebook  -> Cobalt video+audio -> server ffmpeg mono PCM WAV 16 kHz -> AssemblyAI universal-2
Telegram  -> public Telegram web -> AssemblyAI universal-2
```

Free-only/fail-closed invariants:

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
FAILED free-only -> fresh deterministic retry on a NEW explicit retry request only
FAILED with paid charge or credit_charge_uncertain -> replay blocked
```

YouTube:
- preflight must not call Gemini;
- provider execution requires explicit `provider=google_gemini`, `tier=free`, `data_use_acknowledged=true` consent boundary.

## P100 decision matrix

File:
`plugins/krc_migration_candidate/contracts/surface_decision_matrix.yaml`

Key rules:

```text
MIGRATE_BUTTON_IS_STATE_CHANGING=true
MIGRATE_REQUIRES_SEPARATE_OWNER_APPROVAL=true
READ_FETCH_ONLY_FULL_MEDIA_PARITY=REJECTED
FAIL_CLOSED_ON_UNKNOWN_PERMISSIONS=true
```

Full MEDIA parity requires execution capability for:
- `startPublicGeminiYoutubeTranscription`
- `startPublicInstagramCobaltTranscription`
- `startPublicFacebookCobaltTranscription`
- `startPublicTelegramTranscription`

A surface that only supports read/fetch must not be accepted as the full replacement.

## Auth / transport binding

File:
`plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml`

Current state:

```text
FINAL_TRANSPORT=TBD_AFTER_SURFACE_INSPECTION
FINAL_AUTH=TBD_AFTER_SURFACE_INSPECTION
SECRET_PLACEMENT=SERVER_SIDE_ONLY
MODEL_VISIBLE_SECRET=false
REPOSITORY_SECRET=false
SKILL_SECRET=false
EVIDENCE_SECRET=false
```

Do not invent transport/auth before inspecting the actual account surface.

## Sentinel P101 contract

PR #22 is the canonical non-secret coordination channel.

Read:
`100_KRC_MIGRATION_SURFACE_READINESS_SENTINEL_INSPECTION_PACKAGE_2026_09_16.md`

P101 is READ ONLY.

Forbidden:

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
PUBLIC_GPT_DELETE=DENIED
RENDER_CHANGE=DENIED
MAIN_MUTATION=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

P101 evidence to collect when available:

```text
MIGRATION_CONTROL_PRESENT=
PLUGIN_SURFACE_PRESENT=
CONNECTED_APP_OPTION=
CUSTOM_MCP_OPTION=
MCP_CAPABILITY=
REMOTE_MCP_SUPPORTED=
AUTH_OPTIONS=
ACTION_CONFIRMATION_MODEL=
WEB_AVAILABILITY=
DESKTOP_ONLY_LIMITATION=
INSTALL_PERMISSION=
SHARE_PERMISSION=
PUBLISH_PERMISSION=
```

Never record secrets, concrete private browser profile IDs, cookies, session material, or credentials in the public repository.

## P101 execution logic

```text
IF migration/plugin surface is not available:
    record P101_SURFACE_NOT_AVAILABLE
    keep project active but waiting on platform surface
    STOP

IF surface is available:
    inspect read-only
    write non-secret evidence to PR #22
    classify against surface_decision_matrix.yaml
    derive proposed binding plan from auth_transport_binding.yaml
    DO NOT migrate/install/connect/upload/publish
```

## Current hard boundary

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

## First action in the new chat

1. Fetch PR #22 metadata.
2. Verify current head and latest CI.
3. Read checkpoint 101 and checkpoint 100 inspection package.
4. Check PR #22 for newer Sentinel evidence before asking the owner to relay anything manually.
5. Proceed with P101 only inside the read-only boundary.

Terminal marker:

`BOOTSTRAP_KRC_PLUGIN_FIRST_P101_HANDOFF_2026_09_16`
