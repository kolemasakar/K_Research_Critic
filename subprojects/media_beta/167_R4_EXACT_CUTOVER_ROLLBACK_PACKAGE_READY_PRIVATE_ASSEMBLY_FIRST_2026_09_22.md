# KRC MEDIA — R4 exact cutover + rollback package

Date: 2026-09-22  
Status: **AUTHORITATIVE CHECKPOINT / R4_PACKAGE_READY / PRIVATE_ASSEMBLY_REQUIRED / CUTOVER_NOT_AUTHORIZED / FREE_ONLY**

## Purpose

Prepare the exact R4 state-changing sequence and rollback path without executing any R4 mutation.

This package is based on:

- checkpoint 166 current recovery state;
- accepted R3-A..H runtime evidence;
- current account manual UI evidence from checkpoint 164;
- current Plugin permission inventory;
- current runtime skill catalogue;
- current Render service/deploy state;
- current OpenAI product documentation cross-check on 2026-09-22.

No R4 mutation is authorized by this checkpoint.

## Current product/account facts

Current account evidence:

```text
MIGRATION_CONTROL=NOT_FOUND_IN_CURRENT_UI
PLUGIN_SURFACE=PRESENT
PLUGIN_ADD_CONTROL=PRESENT
SKILLS_SURFACE=PRESENT
SKILLS_ADD_CONTROL=PRESENT
PUBLIC_GPT=Published / Everyone
```

Current OpenAI documentation states that Plugins can package reusable skills plus connected apps, Custom GPT Actions do not automatically transfer, migration availability may be account/workspace dependent, and the replacement should be tested before users switch.

Account-specific observed UI/runtime state is authoritative for execution.

## Current accepted baseline

```text
CURRENT_HANDOFF=v19.9
RECOVERY_CHECKPOINT=166

R3_A_TO_H=COMPLETE
R3C_OAUTH_RECOVERY=PASS
R3C_READONLY_RUNTIME=PASS
MEDIA_GET_CAPABILITIES=PASS
PLUGIN_REQUIRED_SURFACES=PASS
RECOVERY_CONSISTENCY_WARNING=CLOSED

PROJECT_COST_POLICY=FREE_ONLY
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO
CURRENT_VALIDATION_MODE=EXACT_COMMIT_RENDER_BUILD + LIVE_READONLY_RUNTIME

PUBLIC_GPT_MUTATION=NO
R4_CUTOVER_AUTHORIZED=NO
```

## Current replacement gaps

### Core Skill

The repository candidate exists and has exact Core snapshot parity:

```text
canonical=prompts/GPT_STORE_INSTRUCTIONS.md
candidate=plugins/krc_migration_candidate/skills/krc_core/SKILL.md
CORE_SKILL_EXACT_SNAPSHOT=PASS
```

However, no KRC Core skill is currently exposed in the runtime skill catalogue.

Therefore:

```text
KRC_CORE_SKILL_REPO_CANDIDATE=READY
KRC_CORE_SKILL_CURRENT_RUNTIME_INSTALL=NOT_VERIFIED / NOT_EXPOSED
PRIVATE_SKILL_ASSEMBLY_REQUIRED=YES
```

### MEDIA surfaces

Current installed/available private KRC surfaces:

```text
KRC MCP Canary Sentinel=FOUND
KRC MCP Auth Sentinel R3B=FOUND
KRC MCP R3C Readonly=FOUND
KRC MCP R3D Confirmation Sentinel=FOUND
KRC MCP R3E2 Instagram Sentinel-v5=FOUND
MCP E3 Facebook 1=FOUND
MCP E4 Telegram 1=FOUND
```

The accepted R3-E1 Render runtime exists:

```text
service=krc-mcp-r3e1-youtube-sentinel
service_id=srv-dall4qv40ujc73ednpqg
mcp_base=https://krc-mcp-r3e1-youtube-sentinel.onrender.com
accepted_live_deploy=dep-dan6nc3tqb8s73aqdbug
accepted_live_commit=88cdc465dd6b74c4941d1d2a15654e4adb29d608
R3_E1_YOUTUBE=COMPLETE
```

But the expected E1 ChatGPT Plugin connection is currently not installed under the checked R3-E1 names.

Therefore:

```text
E1_RENDER_RUNTIME=EXISTS / ACCEPTED
E1_CURRENT_PLUGIN_CONNECTION=NOT_INSTALLED
E1_PRIVATE_RECONNECT_REQUIRED=YES
FULL_13_OPERATION_REPLACEMENT_READY=NO
```

## Selected R4 strategy

Because no built-in Migrate control is visible, R4 uses a **plugin-first staged replacement**.

It does NOT make the source GPT read-only and does NOT delete or unpublish it.

```text
R4_PATH=PRIVATE_ASSEMBLY -> PRIVATE_ACCEPTANCE -> OPTIONAL_USER_SWITCH
BUILTIN_MIGRATION_BUTTON=NOT_USED
SOURCE_PUBLIC_GPT=UNCHANGED_UNTIL_SEPARATE_FUTURE_DECISION
ROLLBACK_ANCHOR=EXISTING_PUBLIC_GPT
```

## R4-A — Private assembly

### Authorization scope required

A future owner approval for R4-A authorizes only the following private/reversible changes.

It does **not** authorize publication, public sharing, source-GPT mutation, PR merges, or new provider work.

### Exact mutation sequence

#### A1 — Create/install KRC Core Skill candidate privately

Source must be exactly:

```text
plugins/krc_migration_candidate/skills/krc_core/SKILL.md
```

Target identity:

```text
name=K-Research & Critic Core
visibility=PRIVATE / owner only
sharing=NO
publication=NO
```

Acceptance immediately after creation:

```text
skill_visible_to_owner=true
core_snapshot_source=checkpoint_167 canonical candidate
core_semantic_drift=0
```

STOP if the product surface cannot create/install the exact candidate privately.

#### A2 — Restore the private E1 YouTube MCP connection

Target:

```text
name=KRC MCP R3E1 YouTube Sentinel
server=https://krc-mcp-r3e1-youtube-sentinel.onrender.com/mcp
access=PRIVATE
```

Before reconnect:

- verify E1 Render service identity;
- verify current E1 health/read-only discovery path;
- verify OAuth mode and current restart-safety compatibility;
- do not expose any bearer/provider secret.

If current E1 OAuth cannot sustain the required private connection, STOP and require a separately reviewed minimal OAuth remediation package before continuing.

No `media_youtube_start` is authorized by R4-A.

#### A3 — Assemble the private replacement Plugin

Target identity:

```text
name=K-Research & Critic R4 Candidate
visibility=PRIVATE
public_listing=NO
sharing=NO
```

Required composition:

```text
Core:
  K-Research & Critic Core skill

MEDIA:
  R3C read-only surface
  E1 YouTube execution surface
  E2 Instagram execution surface
  E3 Facebook execution surface
  E4 Telegram execution surface
```

No legacy Custom GPT Action is added.

If the Plugin product surface cannot compose the required Skill + existing app/MCP surfaces without weakening the permission model, STOP.

### R4-A acceptance

```text
PRIVATE_REPLACEMENT_EXISTS=YES
PRIVATE_REPLACEMENT_PUBLIC=false
CORE_SKILL_BOUND=PASS
MEDIA_SURFACES_BOUND=PASS
READ_OPERATIONS=9
EXECUTION_OPERATIONS=4
TOTAL_OPERATIONS=13
FREE_ONLY_POLICY=PASS
SOURCE_PUBLIC_GPT_UNCHANGED=YES
```

Only after these pass may R4-B be considered.

## R4-A rollback

If any A-stage mutation fails:

1. keep the existing public GPT unchanged;
2. remove/uninstall only the newly created R4 Candidate Plugin if necessary;
3. remove/uninstall only the newly created KRC Core skill if necessary;
4. disconnect only the newly recreated E1 Plugin connection if necessary;
5. do not modify R3C/E2/E3/E4 accepted existing private surfaces;
6. do not modify VoiceBridge/provider credentials unless a separately approved security remediation requires it;
7. preserve PR #22/#45 open/draft/unmerged.

Rollback success:

```text
PUBLIC_GPT=UNCHANGED
R3_ACCEPTED_RUNTIME=UNCHANGED
PUBLICATION_CHANGE=NONE
USER_SWITCH=NONE
```

## R4-B — Private acceptance

R4-B requires a **separate owner approval after R4-A passes**.

### B1 — Core regression

Validate against repository fixtures:

- CriticProfile gate;
- risk floors;
- cross-check floors;
- claim ledger;
- traceability;
- language behavior;
- model-agnostic behavior;
- checkpoint recovery.

No external provider work is required for Core regression.

### B2 — MEDIA read-only regression

Required read-only coverage:

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

No automatic retries that could cause provider work.

### B3 — Consequential tool scan

Verify exactly four execution tools are visible and correctly marked consequential:

```text
media_youtube_start
media_instagram_start
media_facebook_start
media_telegram_start
```

No execution call is performed merely for visibility verification.

### B4 — Optional bounded execution acceptance

Any new live `*_start` requires its own explicit owner approval/consent.

Default:

```text
ADDITIONAL_LIVE_MEDIA_STARTS=NO
```

### R4-B acceptance

```text
CORE_REGRESSION=PASS
MEDIA_READONLY_REGRESSION=PASS
13_OPERATION_SCAN=PASS
EXECUTION_CONFIRMATION_BOUNDARY=PASS
FREE_ONLY_FAIL_CLOSED=PASS
PRIVATE_REPLACEMENT_ACCEPTED=YES
```

Only after R4-B passes may R4-C be proposed.

## R4-B rollback

Failure in B does not affect the source GPT.

- stop acceptance;
- keep replacement private;
- fix only the failing private replacement component;
- if necessary remove the replacement Plugin and return to the accepted R3 private surfaces;
- do not publish/share/switch users.

## R4-C — Optional user switch / publication

R4-C is a **separate, final owner decision**.

It is not authorized by this package.

### Preferred non-destructive cutover

Because the account currently has no built-in migration control, the preferred cutover is:

1. keep existing K-Research & Critic GPT published and unchanged;
2. configure the accepted replacement Plugin's intended audience;
3. publish/share the replacement only to the explicitly approved audience;
4. verify access from the intended user context;
5. direct users to the replacement Plugin only after access verification;
6. retain the source GPT as rollback anchor until a later explicit retirement decision or platform migration flow.

### Not included in R4-C by default

```text
DELETE_SOURCE_GPT=NO
UNPUBLISH_SOURCE_GPT=NO
EDIT_SOURCE_GPT=NO
BUILTIN_MIGRATE=NO / unavailable
PR22_MERGE=NO
PR45_MERGE=NO
```

Repository merges remain separate release decisions.

## R4-C rollback

If replacement publication/access fails:

1. stop directing users to the replacement;
2. reduce replacement visibility to private where the product allows;
3. keep/restore the existing public GPT as the active user entry point;
4. retain accepted private runtime components for diagnosis;
5. do not merge PR #22/#45 as a rollback mechanism.

## Approval boundaries

### Approval 1 — R4-A only

Authorizes private assembly mutations only.

```text
CORE_SKILL_PRIVATE_CREATE_INSTALL=YES
E1_PRIVATE_RECONNECT=YES
R4_CANDIDATE_PRIVATE_CREATE=YES
PUBLICATION=NO
PUBLIC_GPT_MUTATION=NO
LIVE_MEDIA_STARTS=NO
```

### Approval 2 — R4-B only

Authorizes private regression/acceptance after R4-A PASS.

Consequential MEDIA starts remain separately consented.

### Approval 3 — R4-C only

Authorizes the exact audience/share/publication/user-switch actions presented at that time.

## Stop conditions

Immediate STOP if any is true:

- exact Core skill source cannot be preserved;
- E1 cannot be restored privately without weakening authentication;
- 13-operation parity cannot be shown;
- any execution tool appears on the read-only surface;
- confirmation semantics are ambiguous;
- FREE_ONLY policy cannot be proven;
- required Plugin/Skill composition is unavailable on the current account;
- audience/sharing controls differ materially from the reviewed plan;
- rollback anchor would be lost;
- a state-changing control appears that was not included in the approved mutation list.

## GitHub Actions constraint

```text
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO
ACTIONS_REQUIRED_FOR_R4_A=NO
ACTIONS_REQUIRED_FOR_R4_B=NO
ACTIONS_REQUIRED_FOR_R4_C=NO
```

Until Actions return, use:

- exact repository commit identity;
- Render exact-commit build/deploy evidence where runtime code changes are separately approved;
- live read-only health/protocol verification;
- current Plugin/Skill/account UI inspection;
- explicit manual owner confirmation for consequential UI actions.

Historical CI remains reference evidence only.

## Current gate result

```text
R4_CUTOVER_PACKAGE=READY
R4_ROLLBACK_PACKAGE=READY
R4_PRIVATE_ASSEMBLY_REQUIRED=YES
R4_PRIVATE_ASSEMBLY_AUTHORIZED=NO
R4_PRIVATE_ACCEPTANCE_AUTHORIZED=NO
R4_USER_SWITCH_AUTHORIZED=NO
R4_CUTOVER_READY=NO
R4_CUTOVER=HOLD
```

The next state-changing step, if the owner later approves it, is **R4-A private assembly only**.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_167_R4_EXACT_CUTOVER_ROLLBACK_PACKAGE_READY_PRIVATE_ASSEMBLY_FIRST_2026_09_22`
