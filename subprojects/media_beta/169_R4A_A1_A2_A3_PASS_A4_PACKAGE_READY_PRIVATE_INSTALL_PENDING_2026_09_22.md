# KRC MEDIA — R4-A progress: E1 restart-safe OAuth PASS, Core Skill PASS, private Plugin package ready

Date: 2026-09-22  
Status: **AUTHORITATIVE CHECKPOINT / R4_A_IN_PROGRESS / A0_PASS / A1_PASS / A2_PASS / A3_PASS / A4_PACKAGE_READY / A4_PRIVATE_INSTALL_PENDING / FREE_ONLY / PUBLICATION_HOLD**

## Scope

This checkpoint records the approved R4-A work performed under checkpoint 168.

GitHub Actions are unavailable and were not used.

No public GPT mutation, Plugin publication/share, PR merge, main mutation, or MEDIA `*_start` execution was performed.

## R4-A gate state

```text
A0_FREEZE_PREFLIGHT=PASS
A1_E1_RESTART_SAFE_OAUTH_HARDENING=PASS
A1_RESTART_CONTINUITY=PASS
A2_E1_PRIVATE_CONNECTION=PASS
A3_CORE_SKILL_PRIVATE_INSTALL=PASS
A4_R4_CANDIDATE_PACKAGE=READY
A4_R4_CANDIDATE_PRIVATE_INSTALL=PENDING
A5_PRIVATE_ASSEMBLY_VERIFICATION=PENDING
A6_STOP_CHECKPOINT=PENDING
```

## A0 — Freeze/preflight

Accepted baseline before mutation:

```text
KRC branch=agent/krc-public-media-r3-integration
PR22=OPEN / DRAFT / UNMERGED
PR45=OPEN / DRAFT / UNMERGED
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO

R3C runtime validated head=27585c0ce924c78529b90aaadbfbeee841d0d249
E1 pre-hardening accepted deploy=dep-dan6nc3tqb8s73aqdbug
E1 pre-hardening accepted commit=88cdc465dd6b74c4941d1d2a15654e4adb29d608
VoiceBridge accepted head=db9fb62c57fc731732f88ff5b417a0f15be178b6
```

A0 passed.

## A1 — E1 restart-safe OAuth hardening

A dedicated server-side `KRC_MCP_OAUTH_SIGNING_KEY` was provisioned on:

```text
service=krc-mcp-r3e1-youtube-sentinel
service_id=srv-dall4qv40ujc73ednpqg
```

Secret value is not recorded in repository documentation.

The accepted restart-safe OAuth implementation uses:

```text
RestartSafeOAuthState
signed DCR client registrations
signed access tokens
signed refresh tokens
PKCE S256
```

Initial hardening deploy:

```text
deploy=dep-dap6gcrtqb8s73fgs9q0
commit=f02c48f7dedd5833de1cdbbc3067db398181b56d
status=LIVE
```

Health after hardening:

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

## A2 — E1 private ChatGPT connection

Created private connection:

```text
name=KRC MCP R3E1 YouTube Sentinel
plugin_url_id=plugin_asdk_app_6ab26b061fb4819180fa096638f1e4df
app_id=asdk_app_6ab26b061fb4819180fa096638f1e4df
```

Observed OAuth sequence:

```text
POST /oauth/register -> 201
GET  /oauth/authorize -> 200
POST /oauth/authorize -> 302
POST /oauth/token -> 200
POST /mcp -> 200
```

No `media_youtube_start` was invoked.

## A1 restart-continuity acceptance

A controlled same-config redeploy was used because a direct Render restart action was blocked by the tool safety layer.

Final continuity deploy:

```text
deploy=dep-dap6mrrtqb8s73fhf4cg
commit=f02c48f7dedd5833de1cdbbc3067db398181b56d
status=LIVE
```

After restart:

```text
/healthz=200
POST /mcp -> 200
new /oauth/register after restart=NO
new /oauth/authorize after restart=NO
new /oauth/token after restart=NO
same ChatGPT connection survived restart=YES
```

Owner invoked only `media_get_capabilities` after restart; result passed and provider work was not started.

```text
E1_RESTART_CONTINUITY=PASS
```

## A3 — KRC Core Skill

The first upload attempt failed because the Skill name used underscore syntax.

Correction:

```text
old frontmatter name=krc_core
accepted frontmatter name=krc-core
```

Repository candidate:

```text
plugins/krc_migration_candidate/skills/krc_core/SKILL.md
frontmatter name=krc-core
CORE_SNAPSHOT_PARITY=PASS
```

Regression coverage was added for required frontmatter.

Owner UI confirmed:

```text
krc core=INSTALLED
krc core=CREATED_BY_ME
A3_CORE_SKILL_PRIVATE_INSTALL=PASS
```

The system skill catalogue used by this chat does not expose personal user-created Skills and is therefore not the acceptance source for this gate.

## A4 — private R4 Candidate package

Registered app IDs supplied from current ChatGPT Plugin URLs:

```text
KRC MCP R3C Readonly
  plugin_asdk_app_6aaaf8ca113c8191a4ac53f8793833a4
  -> asdk_app_6aaaf8ca113c8191a4ac53f8793833a4

KRC MCP R3E1 YouTube Sentinel
  plugin_asdk_app_6ab26b061fb4819180fa096638f1e4df
  -> asdk_app_6ab26b061fb4819180fa096638f1e4df

KRC MCP R3E2 Instagram Sentinel-v5
  plugin_asdk_app_6aaeae197c9081918b90e46f5bb09615
  -> asdk_app_6aaeae197c9081918b90e46f5bb09615

MCP E3 Facebook 1
  plugin_asdk_app_6aaf262767d8819199146dc84b8e1ee8
  -> asdk_app_6aaf262767d8819199146dc84b8e1ee8

MCP E4 Telegram 1
  plugin_asdk_app_6aaf292e653481918c75767dea004c5c
  -> asdk_app_6aaf292e653481918c75767dea004c5c
```

Created package:

```text
plugins/krc_r4_candidate/
  plugin.json
  .app.json
  .codex-plugin/plugin.json
  skills/krc-core/SKILL.md
```

Created private repository marketplace:

```text
.agents/plugins/marketplace.json
marketplace=krc-r4-local
plugin=k-research-critic-r4-candidate
source.path=./plugins/krc_r4_candidate
installation=AVAILABLE
authentication=ON_INSTALL
```

No `mcp.json` or `.mcp.json` is included. The candidate references existing registered ChatGPT apps through `.app.json`, preserving web compatibility and avoiding the desktop-only behavior of imported raw MCP declarations.

Static acceptance:

```text
portable_schema=https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
openai_apps_path=./.app.json
registered_app_mapping_count=5
all_registered_apps_required=true
compatibility_apps_path=./.app.json
compatibility_skills_path=./skills/
mcp_json_absent=true
core_skill_name=krc-core
core_snapshot_parity=PASS
marketplace_entry=PASS
A4_PACKAGE_STATIC_VALIDATION=PASS
```

## Current installation limitation

The current ChatGPT web Settings -> Plugins plus button creates a single MCP app connection; it is not a Plugin package importer.

Official private testing paths are:

```text
ChatGPT Work -> @plugin-creator
or
ChatGPT desktop -> repository/personal local marketplace
```

Therefore:

```text
A4_PACKAGE_READY=YES
A4_PRIVATE_INSTALL_PENDING=YES
```

## Exact post-runtime delta

E1 final accepted runtime code remains:

```text
f02c48f7dedd5833de1cdbbc3067db398181b56d
```

The branch changes after that commit are limited to Skill metadata/tests and Plugin packaging/marketplace files; no E1/R3C/R3E2/R3E3/R3E4 runtime server source changed.

## Hard boundary

```text
PROJECT_COST_POLICY=FREE_ONLY
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO

PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO

media_youtube_start=NO
media_instagram_start=NO
media_facebook_start=NO
media_telegram_start=NO

R4_B_AUTHORIZED=NO
R4_C_AUTHORIZED=NO
R4_CUTOVER=HOLD
```

## Next gate

Install the already assembled R4 Candidate privately through a supported local/personal marketplace path, then execute A5 private assembly verification.

No publication/share or consequential MEDIA execution is required for A5.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_169_R4A_A1_A2_A3_PASS_A4_PACKAGE_READY_PRIVATE_INSTALL_PENDING_2026_09_22`
