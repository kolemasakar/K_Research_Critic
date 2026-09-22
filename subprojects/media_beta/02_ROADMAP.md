# MEDIA BETA Roadmap

Version: 8.6
Status: **PLUGIN_FIRST / R3_A_TO_H_COMPLETE / R4_A_COMPLETE / R4_B_IN_PROGRESS / STATIC_REGRESSION_PASS / LIVE_CANDIDATE_RESELECT_REQUIRED / R4_CUTOVER_HOLD / FREE_ONLY / PUBLICATION_HOLD**
Updated: 2026-09-22

## Current roadmap position

```text
R3-A Contract freeze/security baseline        PASS
R3-B Authentication/secret hardening          PASS
R3-C 9-tool read-only binding                 PASS
R3-D Consequential-action confirmation        PASS
R3-E1 YouTube execution                       PASS / COMPLETE
R3-E2 Instagram execution                     PASS / COMPLETE
R3-E3 Facebook execution                      PASS / COMPLETE
R3-E4 Telegram execution                      PASS / COMPLETE
R3-F Full 13-operation parity                 PASS / COMPLETE
R3-G Private operational hardening            PASS / COMPLETE
R3-H Migration/publication readiness          PASS / COMPLETE

R4 Non-UI read-only preflight                 COMPLETE
R4 Manual account UI preflight                COMPLETE
R4 Read-only preflight overall                PASS / COMPLETE
R4 Package                                  READY
R4-A Private assembly                       PASS / COMPLETE
R4-B Private acceptance                     IN PROGRESS / STATIC PASS / LIVE RESELECT REQUIRED
R4-C User switch/publication                NOT AUTHORIZED
R4 Cutover                                  HOLD
```

## Recovery delta — 2026-09-22

```text
R3C_OAUTH_RECOVERY=PASS
R3C_RUNTIME_HEAD=27585c0ce924c78529b90aaadbfbeee841d0d249
R3C_RENDER_DEPLOY=dep-dap55aegekts73fr0960 / LIVE
MEDIA_GET_CAPABILITIES=PASS
R3C_TO_VOICEBRIDGE_BINDING=PASS
PLUGIN_REQUIRED_SURFACES=PASS
FUNCTIONAL_INVENTORY_DRIFT=NO
RECOVERY_CONSISTENCY_WARNING=CLOSED
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO
CURRENT_VALIDATION_MODE=EXACT_COMMIT_RENDER_BUILD + LIVE_READONLY_RUNTIME
```

No MEDIA execution tool was invoked during this recovery.

## R4-B progress — checkpoint 172

```text
R4_B_AUTHORIZED=YES
B1 repository fixture regression=PASS
B1 live Candidate behavior=PENDING
B2 nine read-only live regression=BLOCKED / Candidate reselect required
B3 contract scan=PASS
B3 live Candidate visibility=PENDING
B4 live execution=NOT PERFORMED
R4_C=NOT AUTHORIZED
```

## R4-A completion — checkpoint 171

```text
A0=PASS
A1=PASS
A2=PASS
A3=PASS
A4 package=PASS
A4 private install=PASS
A5 private assembly verification=PASS
A6 STOP checkpoint=COMPLETE
R4_A=COMPLETE
R4_B=NOT_AUTHORIZED
```

## R4-A progress — checkpoint 169

```text
A0=PASS
A1 E1 restart-safe OAuth=PASS
A1 restart continuity=PASS
A2 E1 private connection=PASS
A3 krc-core private Skill=PASS
A4 package static validation=PASS
A4 private Candidate install=PENDING
A5=PENDING
A6=PENDING
```

## R4-A corrected ordering — checkpoint 168

```text
A0 read-only freeze/preflight
A1 E1 restart-safe OAuth hardening
A1 acceptance incl. restart continuity
A2 restore private E1 ChatGPT Plugin connection
A3 create/install private KRC Core Skill
A4 assemble private R4 Candidate Plugin
A5 private assembly verification
A6 STOP / checkpoint

R4_A_SEQUENCE_167=SUPERSEDED_BY_168
E1_RESTART_SAFE_OAUTH_REQUIRED_BEFORE_RECONNECT=YES
R4_A_AUTHORIZED=NO
```

## R4 staged execution plan — checkpoint 167

```text
R4_A=PRIVATE_ASSEMBLY / NOT_AUTHORIZED
  A1=create/install private KRC Core Skill
  A2=restore private E1 YouTube MCP connection
  A3=assemble private K-Research & Critic R4 Candidate Plugin

R4_B=PRIVATE_ACCEPTANCE / NOT_AUTHORIZED
  Core regression
  nine read-only MEDIA operations
  13-operation visibility/permission scan
  no new *_start without separate explicit consent

R4_C=OPTIONAL_USER_SWITCH_PUBLICATION / NOT_AUTHORIZED
  source GPT stays unchanged by default
  replacement audience/share is a separate approval
```

```text
R4_CUTOVER_PACKAGE=READY
R4_ROLLBACK_PACKAGE=READY
R4_A=COMPLETE
R4_A5=PASS
R4_A6=COMPLETE
R4_B_AUTHORIZED=YES
R4_B=IN_PROGRESS
R4_B_LIVE_CANDIDATE_RESELECT_REQUIRED=YES
R4_CUTOVER_READY=NO
```

## R4 preflight accepted

### Non-UI

```text
CORE_SKILL_PARITY=PASS
MEDIA_13_TOOL_PARITY=PASS
LIVE_RUNTIME_HEALTH=PASS
EXECUTION_ISOLATION=PASS
CONFIRMATION_SAFE_STATE=PASS
PLUGIN_EXISTENCE=PASS
PLUGIN_PERMISSION_MODEL=PASS
OAUTH_HARDENING=PASS
VOICEBRIDGE_SCOPED_AUTH=PASS
FREE_ONLY_POLICY=PASS
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO
CURRENT_VALIDATION=PASS / exact-commit Render + live read-only runtime
ROLLBACK_PACKAGE=READY
```

### Manual account UI

```text
GPT_IDENTITY=PASS
GPT_EDITOR_ACCESS=PASS
PUBLICATION_STATE=Published
VISIBLE_AUDIENCE=Everyone

SHARE_CONTROL=PASS
GPT_STORE_SURFACE=PASS
CATEGORY_CONTROL=PASS

PLUGIN_SURFACE=PASS
PRIVATE_PLUGIN_INVENTORY=PASS
INSTALL_ADD_CONTROL=PASS

SKILLS_SURFACE=PASS
SKILLS_ADD_CONTROL=PASS

MIGRATE_CONTROL=NOT_FOUND_IN_CURRENT_UI
```

No UI mutation was made during inspection.

## Current path decision

The current account exposes the required Plugin and Skill surfaces directly. No explicit migration control was found.

Therefore, if R4 is later authorized, the cutover plan must use the validated Plugin/Skill path actually present in the account, not depend on an unobserved `Migrate` button.

## R4 cutover remains unauthorized

R4-B has started. Resume pending live Candidate checks only after explicitly reselecting the Personal/Local `K-Research & Critic R4 Candidate` surface. Preserve FREE_ONLY; no MEDIA execution, publication/share, public GPT mutation, or PR merge.

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

## Next state

**R4-B is IN PROGRESS.** Static repository/contract regression passed; live Candidate B1/B2/B3 remains pending due tool-surface re-selection requirement. R4-C remains HOLD.

Recovery authority: `CURRENT_HANDOFF.md` v20.5 + checkpoint 172.
