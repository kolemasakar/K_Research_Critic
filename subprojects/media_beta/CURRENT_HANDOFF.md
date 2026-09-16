# KRC MEDIA — CURRENT HANDOFF

Version: 6.0
Status: ACTIVE_HANDOFF / P100_PASS / PLUGIN_FIRST_ACCEPTED / P101_READY / PUBLICATION_HOLD
Date: 2026-09-16

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md і продовжуй з P101.`

## Canonical recovery files

1. `subprojects/media_beta/CURRENT_HANDOFF.md`
2. `subprojects/media_beta/BOOTSTRAP_PACKAGE_2026-09-16_KRC_PLUGIN_FIRST_P101_HANDOFF.md`
3. `subprojects/media_beta/101_CHAT_TRANSITION_P100_COMPLETE_PLUGIN_FIRST_P101_READY_2026_09_16.md`
4. `subprojects/media_beta/100_KRC_PLUGIN_FIRST_STRATEGY_DECISION_2026_09_16.md`
5. `subprojects/media_beta/100_KRC_MIGRATION_SURFACE_READINESS_SENTINEL_INSPECTION_PACKAGE_2026_09_16.md`
6. current PR #22 head/CI and newer non-secret Sentinel evidence

Historical `subprojects/media_beta/08_CHAT_HANDOFF.md` remains a checkpoint-88 recovery artifact and is no longer the current handoff.

## Repository / PR

```text
repository=kolemasakar/K_Research_Critic
PR=22
branch=agent/krc-public-media-r3-integration
base=main
state=OPEN / DRAFT / UNMERGED
```

Validated source state before transition documentation:

```text
head=426f30350b781be742412467b238ad414feec1e3
workflow=35120308214
conclusion=SUCCESS
```

At recovery always fetch current PR metadata again because the handoff commits advance the branch.

## Accepted state

```text
PROJECT=ACTIVE
P99_CORE_MEDIA_MIGRATION_HARDENING=PASS
P100_MIGRATION_SURFACE_READINESS=PASS
PLUGIN_FIRST_STRATEGY=ACCEPTED
LEGACY_MEDIA_ACTION_CREATION=HOLD
R3_OPENAPI_ROLE=PARITY_REFERENCE
P101_NEXT=READ_ONLY_ACCOUNT_SURFACE_INSPECTION
```

## Public KRC

```text
CURRENT_PUBLIC_GPT=UNCHANGED
CURRENT_ACTIONS=NONE
WORK_CLOUD_BROWSER=PASS
CHATGPT_AUTH=PASS
KRC_BUILDER_ENTRY=PASS
READ_ONLY_SNAPSHOT=PASS
```

Do not create a legacy MEDIA Custom GPT Action as the default continuation path.

## Plugin/MEDIA readiness

```text
CORE_SKILL_CANDIDATE=READY
MEDIA_TOOL_CONTRACT_CANDIDATE=READY
MEDIA_ADAPTER_CONTRACT=READY
CORE_REGRESSION_PACK=READY
MEDIA_NEGATIVE_REGRESSION_PACK=READY
MEDIA_OPERATION_PARITY_COUNT=13
P100A_SURFACE_DECISION_MATRIX=READY
P100B_AUTH_TRANSPORT_BINDING_SPEC=READY
P100C_SENTINEL_INSPECTION_PACKAGE=READY
```

Core skill:
`plugins/krc_migration_candidate/skills/krc_core/SKILL.md`

MEDIA contracts:
- `plugins/krc_migration_candidate/contracts/media_tools.yaml`
- `plugins/krc_migration_candidate/contracts/media_adapter.yaml`
- `plugins/krc_migration_candidate/contracts/surface_decision_matrix.yaml`
- `plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml`

Regression:
- `plugins/krc_migration_candidate/regression/core_cases.yaml`
- `plugins/krc_migration_candidate/regression/media_negative_cases.yaml`
- `tests/test_krc_plugin_migration_candidate.py`
- `tests/test_krc_p100_surface_readiness.py`

## MEDIA routing

```text
YouTube   -> Gemini Developer API Free Tier direct URL
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2
Facebook  -> Cobalt video+audio -> server ffmpeg mono PCM WAV 16 kHz -> AssemblyAI universal-2
Telegram  -> public Telegram web -> AssemblyAI universal-2
```

Policies:

```text
paid_retrieval_fallback=false
paid_stt_fallback=false
paid_proxy_fallback=false
supadata_public_active=false
scrapecreators_public_active=false
cookie_login_fallback=false
automatic_retry_loop=false
```

Retry:

```text
COMPLETED -> reuse
PROCESSING -> reuse / concurrency protection
FAILED free-only -> fresh deterministic retry only on a new explicit retry request
FAILED paid or credit_charge_uncertain -> replay blocked
```

## P101

P101 objective:
`READ_ONLY ACCOUNT-SPECIFIC MIGRATION / PLUGIN SURFACE INSPECTION`

Use:
`subprojects/media_beta/100_KRC_MIGRATION_SURFACE_READINESS_SENTINEL_INSPECTION_PACKAGE_2026_09_16.md`

Process:
1. fetch PR #22 current head and CI;
2. read newer PR #22 Sentinel evidence first;
3. check whether migration/plugin surface is available;
4. if unavailable -> record `P101_SURFACE_NOT_AVAILABLE` and STOP;
5. if available -> inspect read-only;
6. collect only non-secret capability evidence;
7. classify using `surface_decision_matrix.yaml`;
8. derive a proposed binding using `auth_transport_binding.yaml`;
9. do not execute migration/install/connect/upload/publish.

## Hard boundary

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
`KRC_MEDIA_CURRENT_HANDOFF_V6_0_P101_READY_2026_09_16`
