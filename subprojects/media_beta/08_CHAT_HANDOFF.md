# MEDIA BETA Chat Handoff

Канонічна інструкція відновлення K-Research & Critic MEDIA у новому чаті.

Version: 6.1
Status: **R3_A_TO_H_COMPLETE / R4_READONLY_PREFLIGHT_COMPLETE / OWNER_CUTOVER_DECISION_PENDING / CUTOVER_HOLD**
Checkpoint date: 2026-09-21

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 164. R3-A..H COMPLETE. R4 read-only preflight COMPLETE: non-UI + manual current-account UI. GPT identity/share/GPT Store/Plugin inventory/Skills PASS. Explicit Migrate control was not found. No mutation performed. R4 cutover HOLD pending explicit owner decision.`

## Mandatory recovery order

1. `subprojects/media_beta/CURRENT_HANDOFF.md` — v19.7
2. `subprojects/media_beta/164_R4_MANUAL_UI_READONLY_PREFLIGHT_COMPLETE_OWNER_CUTOVER_DECISION_PENDING_2026_09_21.md`
3. `subprojects/media_beta/163_R4_READONLY_PREFLIGHT_NON_UI_COMPLETE_UI_GATE_BLOCKED_2026_09_21.md`
4. `subprojects/media_beta/162_R3H_READINESS_REVIEW_COMPLETE_R4_HOLD_2026_09_20.md`
5. `subprojects/media_beta/161_R3G_OPERATIONAL_HARDENING_COMPLETE_2026_09_20.md`
6. `subprojects/media_beta/00_INDEX.md` — v9.1
7. `subprojects/media_beta/02_ROADMAP.md` — v7.8
8. `subprojects/media_beta/06_DECISION_LOG.md` — v5.1
9. current PR #22 / PR #45 state
10. current Render E1/E2/E3/E4/VoiceBridge health

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
R3C=healthy / 9 read-only / execution disabled
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

## Current PR / CI authority

```text
PR22=OPEN / DRAFT / UNMERGED
KRC validated code head=dbcebdff0201fd9240a7aeafa5f5d5dd46ca08f7
KRC CI run 35485995871=PASS

PR45=OPEN / DRAFT / UNMERGED
VoiceBridge validated/deployed code head=db9fb62c57fc731732f88ff5b417a0f15be178b6
VoiceBridge CI run 35492121039=PASS
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

## Next gate

Start a fresh chat before the first R4 mutation.

The new chat must:

1. recover from CURRENT_HANDOFF v19.7 + checkpoint 164;
2. confirm the intended Plugin/Skill cutover path;
3. show exact state-changing actions before executing them;
4. show rollback steps;
5. obtain explicit owner cutover approval;
6. keep PR #22/#45 unmerged until separately approved.

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

Terminal marker:

`MEDIA_BETA_CHAT_HANDOFF_V6_1_R4_PREFLIGHT_COMPLETE_OWNER_CUTOVER_DECISION_PENDING_2026_09_21`
