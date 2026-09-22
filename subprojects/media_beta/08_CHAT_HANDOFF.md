# MEDIA BETA Chat Handoff

Канонічна інструкція відновлення K-Research & Critic MEDIA у новому чаті.

Version: 6.9
Status: **R3_A_TO_H_COMPLETE / R4_A_COMPLETE / R4_B_IN_PROGRESS / STATIC_REGRESSION_PASS / LIVE_CANDIDATE_RESELECT_REQUIRED / CUTOVER_HOLD**
Checkpoint date: 2026-09-22

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 172. R4-A COMPLETE. R4-B AUTHORIZED / IN PROGRESS: static repository regression PASS; live Candidate B1/B2/B3 pending and requires explicit Personal/Local Candidate re-selection. No *_start/provider/publication/share/public GPT mutation/PR merge.`

## Mandatory recovery order

1. `subprojects/media_beta/CURRENT_HANDOFF.md` — v20.5
2. `subprojects/media_beta/172_R4B_STARTED_STATIC_REGRESSION_PASS_LIVE_CANDIDATE_RESELECT_REQUIRED_2026_09_22.md`
3. `subprojects/media_beta/171_R4A_COMPLETE_A5_PASS_A6_STOP_R4B_PENDING_AUTHORIZATION_2026_09_22.md`
3. `subprojects/media_beta/170_R4A_A4_PRIVATE_INSTALL_PASS_A5_NEW_CHAT_PENDING_2026_09_22.md`
4. `subprojects/media_beta/168_R4_PACKAGE_CORRECTED_E1_RESTART_SAFE_OAUTH_BEFORE_RECONNECT_2026_09_22.md`
3. `subprojects/media_beta/167_R4_EXACT_CUTOVER_ROLLBACK_PACKAGE_READY_PRIVATE_ASSEMBLY_FIRST_2026_09_22.md`
4. `subprojects/media_beta/166_R3C_OAUTH_RECOVERY_PLUGIN_INVENTORY_RECONCILED_NO_ACTIONS_VALIDATION_2026_09_22.md`
5. `subprojects/media_beta/165_FINAL_PROJECT_DOCS_SYNC_NEW_CHAT_READY_2026_09_21.md`
6. `subprojects/media_beta/164_R4_MANUAL_UI_READONLY_PREFLIGHT_COMPLETE_OWNER_CUTOVER_DECISION_PENDING_2026_09_21.md`
7. `subprojects/media_beta/163_R4_READONLY_PREFLIGHT_NON_UI_COMPLETE_UI_GATE_BLOCKED_2026_09_21.md`
8. `subprojects/media_beta/162_R3H_READINESS_REVIEW_COMPLETE_R4_HOLD_2026_09_20.md`
9. `subprojects/media_beta/161_R3G_OPERATIONAL_HARDENING_COMPLETE_2026_09_20.md`
10. `subprojects/media_beta/00_INDEX.md` — v9.5
11. `subprojects/media_beta/02_ROADMAP.md` — v8.2
12. `subprojects/media_beta/06_DECISION_LOG.md` — v5.5
13. current PR #22 / PR #45 state
14. current Render R3C/E1/E2/E3/E4/VoiceBridge health

## Current phase state

```text
R3_A_TO_H=COMPLETE
R4_NON_UI_PREFLIGHT=COMPLETE
R4_MANUAL_UI_PREFLIGHT=COMPLETE
R4_READONLY_PREFLIGHT=PASS / COMPLETE
R4_TECHNICAL_PREFLIGHT_DEBT=0
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
VoiceBridge validated/deployed code head=db9fb62c57fc731732f88ff5b417a0f15be178b6
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
R4_B_PRIVATE_ACCEPTANCE=PENDING / NOT_AUTHORIZED
R4_C_USER_SWITCH_PUBLICATION=NOT_AUTHORIZED
SOURCE_PUBLIC_GPT=UNCHANGED
R4_CUTOVER_READY=NO
```

## Next gate

R4-B is already authorized and in progress. Explicitly reselect `@K-Research & Critic R4 Candidate`, recover checkpoint 172, and run only pending live Candidate B1/B2/B3 checks. No new R4-B authorization is required. Do not run any MEDIA `*_start`, provider work, publication/share, public GPT mutation, or PR merge.

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

`MEDIA_BETA_CHAT_HANDOFF_V6_9_R4B_IN_PROGRESS_STATIC_PASS_LIVE_CANDIDATE_RESELECT_REQUIRED_2026_09_22`
