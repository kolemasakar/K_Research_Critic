# KRC MEDIA — R4 package correction: E1 restart-safe OAuth before private reconnect

Date: 2026-09-22  
Status: **AUTHORITATIVE CHECKPOINT / R4_PACKAGE_CORRECTED / E1_OAUTH_HARDENING_REQUIRED_BEFORE_RECONNECT / R4_A_NOT_AUTHORIZED / FREE_ONLY**

## Purpose

Correct checkpoint 167 execution ordering before any R4-A mutation.

Checkpoint 167 remains valid for the staged architecture:

```text
R4_PATH=PRIVATE_ASSEMBLY -> PRIVATE_ACCEPTANCE -> OPTIONAL_USER_SWITCH
SOURCE_PUBLIC_GPT=UNCHANGED
ROLLBACK_ANCHOR=EXISTING_PUBLIC_GPT
```

This checkpoint supersedes checkpoint 167 **only for the detailed R4-A execution sequence**.

No R4-A mutation is authorized by this checkpoint.

## New read-only finding

Current accepted E1 runtime:

```text
service=krc-mcp-r3e1-youtube-sentinel
service_id=srv-dall4qv40ujc73ednpqg
url=https://krc-mcp-r3e1-youtube-sentinel.onrender.com
mcp=https://krc-mcp-r3e1-youtube-sentinel.onrender.com/mcp

accepted_live_commit=88cdc465dd6b74c4941d1d2a15654e4adb29d608
accepted_live_deploy=dep-dan6nc3tqb8s73aqdbug
deploy_status=LIVE
```

Read-only wake/health validation on 2026-09-22:

```text
/healthz=200
surface=r3e1_youtube_execution
tool_count=10
non_execution_tool_count=9
execution_tool_count=1
other_execution_tools=not_enabled
provider_work_started=false
voicebridge_binding_configured=true
youtube_execution_enabled=true
```

OAuth discovery metadata is present:

```text
authorization_endpoint=/oauth/authorize
registration_endpoint=/oauth/register
token_endpoint=/oauth/token
grant_types=authorization_code,refresh_token
PKCE=S256
scope=krc.mcp.read
offline_access=supported
```

## E1 OAuth durability gap

The currently deployed E1 commit `88cdc465dd6b74c4941d1d2a15654e4adb29d608` imports:

```text
GLOBAL_OAUTH_STATE = OAuthState()
```

Therefore the deployed E1 OAuth/DCR client and token state is process-memory based.

A Render sleep/restart/redeploy can invalidate the ChatGPT-side E1 connection state.

The current KRC recovery code at validated runtime head:

```text
27585c0ce924c78529b90aaadbfbeee841d0d249
```

contains the accepted restart-safe OAuth implementation:

```text
RestartSafeOAuthState
KRC_MCP_OAUTH_SIGNING_KEY
signed dynamic client registrations
signed access tokens
signed refresh tokens
```

This implementation was live-accepted on R3C during checkpoint 166.

## Corrected R4-A ordering

### A0 — Freeze / exact-state preflight

Read-only only.

Required checks:

```text
CURRENT_HANDOFF=current
CHECKPOINT_168=current
PR22=OPEN / DRAFT / UNMERGED
PR45=OPEN / DRAFT / UNMERGED
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO

KRC_RUNTIME_VALIDATED_HEAD=27585c0ce924c78529b90aaadbfbeee841d0d249
POST_RUNTIME_CODE_DELTA=DOCUMENTATION_ONLY

E1_ACCEPTED_DEPLOY=dep-dan6nc3tqb8s73aqdbug
E1_ACCEPTED_COMMIT=88cdc465dd6b74c4941d1d2a15654e4adb29d608
VOICEBRIDGE_ACCEPTED_HEAD=db9fb62c57fc731732f88ff5b417a0f15be178b6
```

STOP if any runtime source changed after the validated head without a separately accepted validation package.

### A1 — E1 restart-safe OAuth hardening

This is the **first future R4-A state-changing operation**.

Scope is limited to:

```text
service=krc-mcp-r3e1-youtube-sentinel
purpose=restart-safe OAuth/DCR durability
```

Required mutation:

1. provision a dedicated server-side `KRC_MCP_OAUTH_SIGNING_KEY` on E1;
2. deploy E1 from the exact recovery code that contains `RestartSafeOAuthState`;
3. preserve existing E1 surface/tool contract;
4. do not change provider credentials;
5. do not change VoiceBridge bearer unless a separately diagnosed auth incompatibility requires a new owner-approved remediation;
6. do not expose any secret in chat, repository, logs, tool arguments, or documentation.

Not authorized by A1:

```text
MEDIA_PROVIDER_WORK=NO
media_youtube_start=NO
PUBLICATION=NO
SHARING=NO
SOURCE_GPT_MUTATION=NO
PR_MERGE=NO
```

### A1 acceptance

Required read-only/runtime acceptance:

```text
E1_DEPLOY=LIVE
/healthz=200
surface=r3e1_youtube_execution
tool_count=10
non_execution_tool_count=9
execution_tool_count=1
other_execution_tools=not_enabled
provider_work_started=false
voicebridge_binding_configured=true
youtube_execution_enabled=true

OAUTH_DCR=PASS
PKCE_S256=PASS
ACCESS_TOKEN=PASS
REFRESH_TOKEN=PASS
RESTART_CONTINUITY=PASS
```

The restart-continuity check must prove that a private E1 OAuth connection remains usable across the accepted restart boundary without requiring provider work.

If OAuth compatibility requires an additional code change beyond already accepted restart-safe behavior, STOP and prepare a separate minimal remediation delta before proceeding.

### A2 — Restore private E1 ChatGPT Plugin connection

Only after A1 PASS.

Target:

```text
name=KRC MCP R3E1 YouTube Sentinel
server=https://krc-mcp-r3e1-youtube-sentinel.onrender.com/mcp
visibility=PRIVATE
```

Use a fresh OAuth/DCR connection.

Acceptance:

```text
CHATGPT_CONNECTION=PASS
DISCOVERED_TOOL_COUNT=10
READ_TOOLS=9
EXECUTION_TOOLS=1
ONLY_EXECUTION_TOOL=media_youtube_start
OTHER_EXECUTION_TOOLS=0
```

No `media_youtube_start` invocation is authorized by this connection acceptance.

### A3 — Create/install private KRC Core Skill

Repository source:

```text
plugins/krc_migration_candidate/skills/krc_core/SKILL.md
```

Canonical source:

```text
prompts/GPT_STORE_INSTRUCTIONS.md
```

Required:

```text
CORE_SKILL_EXACT_SNAPSHOT=PASS
name=K-Research & Critic Core
visibility=PRIVATE / owner-only
sharing=NO
publication=NO
```

STOP if the exact skill candidate cannot be installed privately without semantic modification.

### A4 — Assemble private R4 Candidate Plugin

Target:

```text
name=K-Research & Critic R4 Candidate
visibility=PRIVATE
publication=NO
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

No legacy Custom GPT Action is created.

### A5 — Private assembly verification

No provider work.

Required:

```text
CORE_SKILL_BOUND=PASS
READ_OPERATIONS=9
EXECUTION_OPERATIONS=4
TOTAL_OPERATIONS=13
READ_ONLY_EXECUTION_LEAKAGE=0
FREE_ONLY_POLICY=PASS
SOURCE_PUBLIC_GPT_UNCHANGED=YES
REPLACEMENT_VISIBILITY=PRIVATE
```

Visibility verification of execution tools does not authorize calling them.

### A6 — STOP / checkpoint

After A5:

```text
R4_A=COMPLETE or FAILED
R4_B_PRIVATE_ACCEPTANCE_AUTHORIZED=NO
R4_C_USER_SWITCH_AUTHORIZED=NO
```

Create an exact state checkpoint and stop.

## R4-A rollback

### If A1 E1 OAuth deploy fails

Preferred rollback:

```text
restore E1 known-good commit=88cdc465dd6b74c4941d1d2a15654e4adb29d608
known-good deploy reference=dep-dan6nc3tqb8s73aqdbug
```

Then verify:

```text
/healthz=200
tool_count=10
provider_work_started=false
```

No public GPT change is involved.

### If A2 E1 Plugin connection fails

- remove/disconnect only the newly created E1 ChatGPT connection if necessary;
- retain accepted E1 Render runtime;
- do not touch R3C/E2/E3/E4 private connections;
- source GPT remains unchanged.

### If A3 Core Skill fails

- remove only the newly created private Core Skill if necessary;
- retain all existing private Plugin connections;
- source GPT remains unchanged.

### If A4/A5 Candidate assembly fails

- keep or remove only the private R4 Candidate;
- do not publish/share;
- do not alter the source GPT;
- do not merge PR #22 or #45.

## Hard boundary

```text
PROJECT_COST_POLICY=FREE_ONLY
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO

R4_A_AUTHORIZED=NO
R4_B_AUTHORIZED=NO
R4_C_AUTHORIZED=NO

PUBLIC_GPT_MUTATION=NO
PLUGIN_INSTALLATION_OR_CHANGE=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
ADDITIONAL_LIVE_MEDIA_STARTS=NO
```

## Validation model while GitHub Actions are unavailable

```text
GITHUB_ACTIONS_GATE=DISABLED_BY_AVAILABILITY
HISTORICAL_CI=REFERENCE_ONLY
CURRENT_VALIDATION=
  exact repository commit identity
  + Render exact-commit build/deploy evidence
  + live read-only health/protocol verification
  + account Plugin/Skill UI verification
```

## Canonical documentation sync

```text
CURRENT_HANDOFF.md=v20.1
02_ROADMAP.md=v8.2
00_INDEX.md=v9.5
06_DECISION_LOG.md=v5.5
08_CHAT_HANDOFF.md=v6.5
migration_candidate_README=SYNCED
PROJECT_SYNC_COMPLETE=YES
```

## Current result

```text
R4_PACKAGE_167_ARCHITECTURE=RETAINED
R4_A_SEQUENCE_167=SUPERSEDED_BY_168

E1_RESTART_SAFE_OAUTH_REQUIRED_BEFORE_RECONNECT=YES
R4_CUTOVER_PACKAGE=READY / CORRECTED
R4_ROLLBACK_PACKAGE=READY / CORRECTED

R4_A_PRIVATE_ASSEMBLY_REQUIRED=YES
R4_A_PRIVATE_ASSEMBLY_AUTHORIZED=NO
R4_CUTOVER_READY=NO
R4_CUTOVER=HOLD
```

Next state-changing gate:

```text
OWNER_APPROVAL_FOR_R4_A_ONLY
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_168_R4_PACKAGE_CORRECTED_E1_RESTART_SAFE_OAUTH_BEFORE_RECONNECT_2026_09_22`
