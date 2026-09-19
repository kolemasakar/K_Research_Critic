# KRC — P100 Migration Surface Readiness / Sentinel Inspection Package — 2026-09-16

Status: PREPARED / READ_ONLY_INSPECTION_ONLY / MIGRATION_NOT_AUTHORIZED / PUBLICATION_HOLD

## Purpose

Prepare the exact read-only inspection contract for the account-specific GPT -> Plugin migration/app surface when it becomes available. This package must not trigger migration, installation, app connection, MCP upload, sharing, publication, or any public GPT mutation.

## Canonical inputs

- PR #22 branch: `agent/krc-public-media-r3-integration`
- P99 checkpoint: `subprojects/media_beta/99_KRC_CORE_MEDIA_MIGRATION_HARDENING_CHECKPOINT_2026_09_16.md`
- surface matrix: `plugins/krc_migration_candidate/contracts/surface_decision_matrix.yaml`
- auth/transport spec: `plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml`
- MEDIA contract: `plugins/krc_migration_candidate/contracts/media_tools.yaml`
- MEDIA adapter: `plugins/krc_migration_candidate/contracts/media_adapter.yaml`
- Core regression: `plugins/krc_migration_candidate/regression/core_cases.yaml`
- MEDIA negative regression: `plugins/krc_migration_candidate/regression/media_negative_cases.yaml`

## Known OpenAI migration facts to validate against the actual account surface

Current OpenAI guidance indicates:
- migration availability is rollout/account/workspace dependent;
- GPT instructions are expected to become a Plugin skill;
- custom GPT Actions do not transfer automatically;
- connected apps may transfer as apps where applicable;
- conversation starters, previous chats, and selected model are not guaranteed to transfer;
- replacement Plugin begins private until sharing is configured;
- after migration the original GPT remains usable until retirement but becomes read-only;
- MCP/app write/modify availability varies by plan/workspace/surface.

These are planning assumptions only. The actual account UI/permissions observed by Sentinel are authoritative for P101.

## Sentinel trigger

Sentinel Remote may run this package when either condition is true:
1. an in-product migration notice/control appears for `K-Research & Critic`; or
2. KRC explicitly asks Sentinel to re-check migration/app availability.

Do not infer availability from documentation alone.

## Read-only inspection sequence

1. Open the owner-authenticated ChatGPT account through the existing private KRC browser profile path.
2. Confirm the identified GPT is exactly `K-Research & Critic`.
3. Inspect only; do not activate controls that can mutate state.
4. Record whether a GPT migration control/banner is present.
5. Record the exact visible migration wording and eligibility prerequisites without secrets.
6. Record whether Plugins are available in the account/workspace.
7. Record available Plugin/App setup types relevant to KRC:
   - built-in GPT migration;
   - connected app/plugin app flow;
   - custom MCP/app flow if shown.
8. Record whether the available custom app/MCP surface supports:
   - read/fetch only;
   - execution/write/modify tools;
   - remote MCP transport;
   - supported credential mechanisms;
   - per-action confirmation/review behavior;
   - web availability;
   - desktop-only limitations, if any.
9. Record installation, sharing and publication controls/permissions shown for the replacement surface.
10. Do not connect an app, upload MCP, install Plugin, create credentials, start migration, alter sharing, or publish.
11. Return only non-secret evidence to PR #22.

## Explicit forbidden actions

```text
CLICK_MIGRATE=DENIED
CONFIRM_MIGRATION=DENIED
PLUGIN_INSTALL=DENIED
APP_CONNECT=DENIED
CUSTOM_MCP_UPLOAD=DENIED
CUSTOM_MCP_ENABLE=DENIED
CREDENTIAL_CREATE=DENIED
CREDENTIAL_ROTATE=DENIED
PLUGIN_SHARE_CHANGE=DENIED
PLUGIN_PUBLICATION=DENIED
PUBLIC_GPT_UPDATE=DENIED
PUBLIC_GPT_DELETE=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

The migration control itself is treated as consequential because current OpenAI guidance says the original GPT becomes read-only after migration. Therefore Sentinel must not click it during P100/P101 read-only inspection.

## Required returned evidence

Return a machine-readable summary containing at least:

```text
SENTINEL_P100_INSPECTION=<NOT_RUN|RUN>
KRC_GPT_IDENTITY=<PASS|FAIL|AMBIGUOUS>
MIGRATION_CONTROL_PRESENT=<YES|NO|UNKNOWN>
MIGRATION_CONTROL_VISIBLE_TEXT=<non-secret summary>
PLUGIN_SURFACE_PRESENT=<YES|NO|UNKNOWN>
CONNECTED_APP_OPTION=<YES|NO|UNKNOWN>
CUSTOM_MCP_OPTION=<YES|NO|UNKNOWN>
MCP_CAPABILITY=<READ_FETCH_ONLY|EXECUTION_WRITE|NOT_PRESENT|UNKNOWN>
REMOTE_MCP_SUPPORTED=<YES|NO|UNKNOWN>
AUTH_OPTIONS=<non-secret list or UNKNOWN>
ACTION_CONFIRMATION_MODEL=<non-secret summary or UNKNOWN>
WEB_AVAILABILITY=<YES|NO|UNKNOWN>
DESKTOP_ONLY_LIMITATION=<YES|NO|UNKNOWN>
INSTALL_PERMISSION=<YES|NO|UNKNOWN>
SHARE_PERMISSION=<YES|NO|UNKNOWN>
PUBLISH_PERMISSION=<YES|NO|UNKNOWN>
MIGRATION_EXECUTED=NO
PLUGIN_INSTALLED=NO
APP_CONNECTED=NO
MCP_UPLOADED=NO
CREDENTIAL_MUTATION=NO
PUBLIC_GPT_MUTATION=NO
```

Do not return cookies, access tokens, bearer values, browser profile identifiers, internal authentication state, or sensitive account metadata.

## Decision rules for KRC after evidence returns

KRC may classify the surface as:

- `SURFACE_READY_FOR_BINDING_DESIGN` — execution/write capable, server-side auth feasible, intended surface/audience feasible, and no hard invariant conflicts;
- `SURFACE_READ_ONLY_INSUFFICIENT` — only read/fetch capability available for a MEDIA integration that requires four execution operations;
- `SURFACE_AVAILABLE_WITH_PERMISSION_BLOCKER` — suitable surface exists but required owner/admin permissions are absent;
- `SURFACE_NOT_AVAILABLE` — migration/app/MCP option not yet present;
- `SURFACE_AMBIGUOUS` — evidence is incomplete or state-changing action would be needed to inspect further.

No classification authorizes migration or activation.

## Hard STOP conditions

Stop immediately if:
- the GPT identity is ambiguous;
- opening details would require exposing credentials/profile identifiers;
- the next UI action is `Migrate`, `Install`, `Connect`, `Upload`, `Enable`, `Share`, `Publish`, `Update`, or another state-changing control;
- permissions cannot be inspected without mutation;
- a safety layer blocks browser automation before the read-only run starts.

If browser automation is prestart-blocked again, return the blocker through PR #22 without retry loops or bypass attempts.

## Current boundary

```text
PROJECT=ACTIVE
P100_SURFACE_READINESS=PREPARED
P100A_SURFACE_DECISION_MATRIX=READY
P100B_AUTH_TRANSPORT_BINDING_SPEC=READY
P100C_SENTINEL_INSPECTION_PACKAGE=READY
MIGRATION_EXECUTION=DENIED
PLUGIN_INSTALLATION=DENIED
CUSTOM_MCP_UPLOAD=DENIED
PLUGIN_PUBLICATION=DENIED
PUBLIC_GPT=UNCHANGED
PUBLICATION=HOLD
MAIN_MUTATION=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```
