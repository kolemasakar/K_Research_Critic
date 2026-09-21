# MEDIA BETA Chat Handoff

Канонічна інструкція відновлення K-Research & Critic MEDIA у новому чаті.

Version: 6.0
Status: **R3_A_TO_H_COMPLETE / R4_NON_UI_PREFLIGHT_COMPLETE / ACCOUNT_UI_GATE_PENDING / CUTOVER_HOLD**
Checkpoint date: 2026-09-21

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 163. R3-A..H COMPLETE. R4 non-UI read-only preflight COMPLETE; Cloudflare blocked account UI migration/install/share/publish inspection; mutation=NO. R4 cutover HOLD.`

## Mandatory recovery order

1. `subprojects/media_beta/CURRENT_HANDOFF.md`
2. `subprojects/media_beta/163_R4_READONLY_PREFLIGHT_NON_UI_COMPLETE_UI_GATE_BLOCKED_2026_09_21.md`
3. `subprojects/media_beta/162_R3H_READINESS_REVIEW_COMPLETE_R4_HOLD_2026_09_20.md`
4. `subprojects/media_beta/161_R3G_OPERATIONAL_HARDENING_COMPLETE_2026_09_20.md`
5. `subprojects/media_beta/00_INDEX.md`
6. `subprojects/media_beta/02_ROADMAP.md`
7. `subprojects/media_beta/06_DECISION_LOG.md`
8. current PR #22 / PR #45 state
9. current Render E1/E2/E3/E4/VoiceBridge health
10. current account Plugin permissions
11. current account migration/install/share/publish UI — manual read-only check only

## Current phase state

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3_E1=COMPLETE
R3_E2=COMPLETE
R3_E3=COMPLETE
R3_E4=COMPLETE
R3_F=COMPLETE
R3_G=COMPLETE
R3_H=COMPLETE

R4_READONLY_PREFLIGHT=PARTIAL_PASS
R4_NON_UI_PREFLIGHT=COMPLETE
R4_ACCOUNT_UI_GATE=PENDING
R4_CUTOVER=HOLD
```

## Current runtime baseline

```text
R3C=healthy / 9 read-only / execution disabled
E1=healthy / 1 execution / other execution disabled
E2=healthy / confirmation_probe_only=true
E3=healthy / confirmation_probe_only=true
E4=healthy / confirmation_probe_only=true
VoiceBridge=healthy / v0.6.0 / TTL=3600
Render error-level logs since 2026-09-21T00:00Z=0
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

## Current account/plugin evidence

```text
MCP E3 Facebook 1=found
MCP E4 Telegram 1=found
global permission=Allow read actions
changes=confirmation required
app permission=Use my default
```

## Remaining gate

Manual/read-only account UI inspection immediately before any cutover:

```text
KRC_GPT_IDENTITY
MIGRATION_CONTROL
INSTALL_PERMISSION
SHARE_PERMISSION
PUBLISH_PERMISSION
```

Do not click Migrate/Install/Connect/Share/Publish during inspection.

## Hard boundary

```text
PROJECT_COST_POLICY=FREE_ONLY
PUBLIC_GPT_MUTATION=NO
PLUGIN_INSTALLATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
ADDITIONAL_LIVE_MEDIA_STARTS=NO
R4_CUTOVER=HOLD
```

Terminal marker:

`MEDIA_BETA_CHAT_HANDOFF_V6_0_R4_NON_UI_PREFLIGHT_COMPLETE_UI_GATE_PENDING_2026_09_21`
