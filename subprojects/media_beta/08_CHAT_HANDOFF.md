# MEDIA BETA Chat Handoff

Канонічна інструкція відновлення K-Research & Critic MEDIA у новому чаті.

Version: 7.3
Status: **R3_A_TO_H_COMPLETE / R4_A_COMPLETE / R4_B_COMPLETE / PRIVATE_REPLACEMENT_ACCEPTED / R4_C_READY_NOT_AUTHORIZED / CUTOVER_HOLD**
Checkpoint date: 2026-09-22

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 176. R4-A COMPLETE. R4-B COMPLETE / PRIVATE_REPLACEMENT_ACCEPTED=YES: B1 PASS, B2 authenticated read-only 9/9 PASS with 0 infrastructure 429 and no provider work, B3 PASS; B4 optional/not run. R4-C is READY TO PROPOSE but NOT AUTHORIZED. No publication/share/public GPT mutation/PR merge.`

## Mandatory recovery order

1. `subprojects/media_beta/CURRENT_HANDOFF.md` — v20.9
2. `subprojects/media_beta/176_R4B_PRIVATE_ACCEPTANCE_COMPLETE_B1_B2_B3_PASS_R4C_PENDING_AUTHORIZATION_2026_09_22.md`
3. `subprojects/media_beta/175_R4B_READONLY_429_LEAKAGE_FIXED_DEPLOY_LIVE_B2_FINAL_AUTH_RERUN_PENDING_2026_09_22.md`
4. `subprojects/media_beta/174_R4B_VOICEBRIDGE_COLD_START_429_DIAGNOSED_WAKE_PASS_B2_AUTH_RERUN_PENDING_2026_09_22.md`
5. `subprojects/media_beta/173_R4B_B1_PASS_B2_BLOCKED_429_B3_PASS_2026_09_22.md`
6. `subprojects/media_beta/172_R4B_STARTED_STATIC_REGRESSION_PASS_LIVE_CANDIDATE_RESELECT_REQUIRED_2026_09_22.md`
7. `subprojects/media_beta/171_R4A_COMPLETE_A5_PASS_A6_STOP_R4B_PENDING_AUTHORIZATION_2026_09_22.md`
8. `subprojects/media_beta/167_R4_EXACT_CUTOVER_ROLLBACK_PACKAGE_READY_PRIVATE_ASSEMBLY_FIRST_2026_09_22.md`
9. `subprojects/media_beta/00_INDEX.md` — v10.3
10. `subprojects/media_beta/02_ROADMAP.md` — v9.0
11. `subprojects/media_beta/06_DECISION_LOG.md` — v6.3
12. current PR #22 / PR #45 state
13. current Render R3C/E1/E2/E3/E4/VoiceBridge health

## Current phase state

```text
R3_A_TO_H=COMPLETE
R4_NON_UI_PREFLIGHT=COMPLETE
R4_MANUAL_UI_PREFLIGHT=COMPLETE
R4_READONLY_PREFLIGHT=PASS / COMPLETE
R4_TECHNICAL_PREFLIGHT_DEBT=0
R4_B=COMPLETE
PRIVATE_REPLACEMENT_ACCEPTED=YES
R4_CUTOVER_READY=YES
R4_CUTOVER=HOLD / OWNER DECISION REQUIRED
```

## Current runtime baseline

```text
R3C=healthy / OAuth recovery PASS / 9 read-only / execution disabled
E1=healthy / 1 execution / other execution disabled
E2=healthy / confirmation_probe_only=true
E3=healthy / confirmation_probe_only=true
E4=healthy / confirmation_probe_only=true
VoiceBridge=healthy / v0.6.0 / TTL=3600
```

## Repository parity

```text
CORE_SKILL_EXACT_SNAPSHOT=PASS
MEDIA_CONTRACT_OPENAPI_PARITY=PASS
MEDIA_TOTAL_OPERATIONS=13
MEDIA_READ_OPERATIONS=9
MEDIA_EXECUTION_OPERATIONS=4
```

## Current PR / validation authority

```text
PR22=OPEN / DRAFT / UNMERGED
KRC exact runtime validated head=27585c0ce924c78529b90aaadbfbeee841d0d249
KRC validation=Render exact-commit build + live OAuth/read-only runtime PASS
GitHub Actions=current unavailable / not used
KRC historical CI run 35485995871=PASS (reference only)

PR45=OPEN / DRAFT / UNMERGED
VoiceBridge validated/deployed code head=174174aae0635736f05d812094b555544623270c
GitHub Actions=current unavailable / not used
VoiceBridge historical CI run 35492121039=PASS (reference only)
```

## Manual account UI evidence

```text
GPT_NAME=K-Research & Critic
GPT_IDENTITY=PASS
GPT_EDITOR_ACCESS=PASS
PUBLICATION_STATE=Published
VISIBLE_AUDIENCE=Everyone

SHARE_GPT_STORE_SURFACE=PASS
PLUGIN_SURFACE=PASS
PRIVATE_KRC_PLUGIN_INVENTORY=PASS
INSTALL_ADD_CONTROL=PASS
SKILLS_SURFACE=PASS
MIGRATE_CONTROL=NOT_FOUND_IN_CURRENT_UI
```

## Current account/plugin evidence

```text
MCP E3 Facebook 1=found
MCP E4 Telegram 1=found
global permission=Allow read actions
changes=confirmation required
app permission=Use my default
```

## R4 package state

```text
R4_CUTOVER_PACKAGE=READY / CORRECTED
A1_A2_A3=PASS
A4_PACKAGE_STATIC_VALIDATION=PASS
A4_PRIVATE_INSTALL=PASS
A5_PRIVATE_ASSEMBLY_VERIFICATION=PASS
A6_STOP_CHECKPOINT=COMPLETE
R4_A=COMPLETE
E1_RESTART_SAFE_OAUTH_REQUIRED_BEFORE_RECONNECT=YES
R4_A_SEQUENCE_167=SUPERSEDED_BY_168
R4_ROLLBACK_PACKAGE=READY
R4_A_PRIVATE_ASSEMBLY=PASS / COMPLETE
R4_B_PRIVATE_ACCEPTANCE=PASS / COMPLETE
R4_B_B4=OPTIONAL / NOT_RUN
PRIVATE_REPLACEMENT_ACCEPTED=YES
R4_C_USER_SWITCH_PUBLICATION=READY TO PROPOSE / NOT AUTHORIZED
SOURCE_PUBLIC_GPT=UNCHANGED
R4_CUTOVER_READY=YES
```

## Next gate

R4-B is complete. R4-C optional user switch/publication is now ready to propose but remains separately authorized.

Before any R4-C mutation, present the exact target audience/share/publication plan and rollback sequence and obtain explicit owner approval. The existing public GPT remains unchanged.

No `*_start`, provider work, publication/share, public GPT mutation, main mutation, or PR merge is authorized by R4-B completion.

## Hard boundary

```text
PROJECT_COST_POLICY=FREE_ONLY
R4_CUTOVER_AUTHORIZED=NO
PUBLIC_GPT_MUTATION=NO
PLUGIN_INSTALLATION_OR_CHANGE=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
ADDITIONAL_LIVE_MEDIA_STARTS=NO
```

## Recovery delta

```text
R3C_OAUTH_RECOVERY=PASS
MEDIA_GET_CAPABILITIES=PASS
PLUGIN_REQUIRED_SURFACES=PASS
RECOVERY_CONSISTENCY_WARNING=CLOSED
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO
CURRENT_VALIDATION_MODE=EXACT_COMMIT_RENDER_BUILD + LIVE_READONLY_RUNTIME
```

Terminal marker:

`MEDIA_BETA_CHAT_HANDOFF_V7_3_R4B_COMPLETE_PRIVATE_REPLACEMENT_ACCEPTED_R4C_PENDING_AUTHORIZATION_2026_09_22`
