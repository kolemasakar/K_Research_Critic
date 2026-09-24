# MEDIA BETA Roadmap

Version: 9.10
Status: **R3_9_PUBLIC_GPT_ACCEPTED / NATIVE_MIGRATION_PREFLIGHT_PASS / CUSTOM_ACTIONS_NOT_TRANSFERRED / MEDIA_REBIND_PREBUILD_NEXT / FREE_ONLY**
Updated: 2026-09-24

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
R4-B Private acceptance                     PASS / COMPLETE
R4-C Native Plugin migration                PREFLIGHT PASS / MEDIA REBIND PREBUILD
R4 Cutover                                  HOLD / REBIND PREBUILD BEFORE MIGRATION
```

## Native migration preflight PASS — checkpoint 194

Live migration dialog confirmed:

```text
INSTRUCTIONS_AND_FILES=NO_PROBLEMS_DETECTED
CUSTOM_ACTIONS=UNSUPPORTED
PLUGIN_INITIAL_VISIBILITY=PRIVATE
PUBLIC_PLUGIN_SHARING=UNAVAILABLE
SOURCE_GPT_AFTER_MIGRATION=READ_ONLY
FINAL_MIGRATION_EXECUTION=NO
```

Next phase is MEDIA rebind prebuild using the already validated five-app R4 mapping. Final migration remains separately gated.

## Native Plugin migration semantics — verified current OpenAI behavior

```text
instructions -> Skill
knowledge -> reference files
connected apps -> Plugin apps
custom Actions -> NOT transferred
selected model -> NOT transferred
migrated Plugin -> starts private
source GPT after completed migration -> read-only, still usable until retirement
```

Roadmap consequence: R4-C preflight must stop before final migration confirmation. After inspecting the generated Skill/app surface, create a separate integration-rebuild gate for the 13-operation MEDIA contract using the accepted R3C/E1-E4 app/MCP path.

## R3.9 public GPT accepted — checkpoint 193

```text
PUBLIC_ROLLBACK_BASELINE=CAPTURED_AND_VERIFIED
PUBLIC_R39_BUILDER_DELTA=APPLIED
PUBLIC_GPT=PUBLISHED_IN_GPT_STORE
PUBLIC_PRODUCTION_AUTH=PASS
ACTION_SCHEMA=9 read + 4 execution = 13
S1_CORE_GATE=PASS
S2_MEDIA_PREAPPROVAL_GATE=PASS
S3_READONLY_AND_GEMINI_CONSENT_BOUNDARY=PASS
S4_CONSEQUENTIAL_CONFIRMATION_BOUNDARY=PASS
S4_CONFIRMATION_CANCELLED=PASS
START_HTTP_REQUEST_DURING_S4=0
PROVIDER_WORK_DURING_PUBLIC_SMOKE=0
FREE_ONLY=PASS
PUBLIC_PRIVACY_POLICY_ACTIVE_BRANCH=READY
LIVE_BUILDER_PRIVACY_URL_RECONCILIATION=PASS
NATIVE_PLUGIN_MIGRATION_PREFLIGHT=NEXT
```

The source public GPT remains published as the rollback anchor. Native migration execution, Plugin publication/sharing, PR merges and new provider work remain outside the next read-only preflight gate.

## R3.9 private staging accepted — checkpoint 192

```text
PRIVATE_STAGING=ACCEPTED
S1_CORE_GATE=PASS
S2_MEDIA_PREAPPROVAL_GATE=PASS
S3_READONLY_AND_GEMINI_CONSENT_BOUNDARY=PASS
S4_CONSEQUENTIAL_CONFIRMATION_BOUNDARY=PASS
SELECTED_REGRESSION_TESTS=92/92 PASS
ACTION_TRANSPORT_AUTH=PASS
FREE_ONLY=PASS
PROVIDER_WORK_DURING_S4=0
NATIVE_PLUGIN_MIGRATION=AVAILABLE / DEFERRED
PUBLIC_GPT_MUTATION=NO
NEXT=PUBLIC_GPT_ROLLBACK_BASELINE_SNAPSHOT
```

Release note: the dedicated staging credential must not be promoted to public production. A fresh production credential is required at the public activation gate.

## R3.9 exact validation and private staging — checkpoint 183

```text
SELECTED_REGRESSION_TESTS=91
PASS=91
FAIL=0
R39_ACTION_SCHEMA=media_public_r39_openapi.yaml
ACTION_BOUNDARY=9 non-consequential + 4 consequential
BUILDER_INSTRUCTIONS=GPT_STORE_UNIFIED_R39_INSTRUCTIONS.md
BUILDER_CHARS=7404/8000
NATIVE_MIGRATION_PLUS=AVAILABLE
DISPLAYED_DEADLINE=2026-12-11
R4_C=DEFERRED_UNTIL_R39_UNIFIED_ACCEPTANCE
NEXT=PRIVATE MEDIA BETA STAGING
PUBLIC_GPT_MUTATION=NO
```

## R3.9 Unified KRC GPT — checkpoint 182

```text
R3_9=ACTIVE
ROUTING_CONTRACT=contracts/krc_unified_media_routing.yaml
STAGING_MANIFEST=gpt_store/unified_r39_manifest.yaml
NEW_STATIC_TESTS=tests/test_krc_unified_r39.py
CORE_UNCHANGED=PASS
CORE_PLUS_MEDIA_ADDENDUM_CHARS=7404/8000
MEDIA_OPS=9 read + 4 execution = 13
R4_APP_IDS=5 / unchanged
PUBLIC_GPT_MUTATION=NO
R4_C=PAUSED
```

Next: exact-branch regression/runtime validation, then prepare an exact Builder delta. No public GPT mutation before that gate.

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

## R4-C pause decision — checkpoint 181

```text
R4_C=PAUSED_PENDING_SUPPORTED_CHATGPT_DISTRIBUTION
CURRENT_PRODUCTION_ENTRY_POINT=EXISTING_PUBLIC_GPT
LOCAL_MARKETPLACE_PILOT=OPTIONAL / NOT_REQUIRED
TRIGGER_1=NATIVE_MIGRATION_AVAILABLE_IN_PLUS_ACCOUNT
TRIGGER_2=SUPPORTED_PLUGIN_DISTRIBUTION_TO_ORDINARY_CHATGPT_USERS
```

Do not spend further implementation effort on Node/Codex/local pilot solely to achieve the end-user cutover. Re-check product support when either trigger appears.

## R4-C local marketplace pilot — checkpoint 180

```text
R4_C_DISTRIBUTION=LOCAL_MARKETPLACE_PILOT
PILOT_BUNDLE_READY=YES
ZIP_SHA256=e6cf16718183b3403179798b3e0ef7d5e5dfa703c1b160d6bfc16a56afea9868
NEXT_GATE=marketplace + plugin + Core Skill + 5/5 app availability
MEDIA_STARTS=0
PROVIDER_WORK=0
```

## R4-C distribution correction — checkpoint 179

```text
current_account=PERSONAL_PLUS
candidate_type=LOCAL_MARKETPLACE_PACKAGE
web_link_only_control=NOT_AVAILABLE
plus_control=NEW_MCP_PLUGIN_FORM_ONLY
state_changes=0
next_decision=A local marketplace pilot | B managed workspace link pilot | C public directory
```

## R4-C link-only pilot — checkpoint 178

```text
R4_C_AUDIENCE=LINK_ONLY_PILOT
R4_C_AUTHORIZED=YES
C0_ROLLBACK_ANCHOR_FREEZE=PASS
C1_AUDIENCE_SELECTION=PASS
C2_LINK_ONLY_SHARE_MUTATION=BLOCKED_BEFORE_MUTATION
C3_ACCESS_VERIFICATION=PENDING
C4_USER_SWITCH=PENDING
UI_AUTH_BLOCKER=OPEN
ZERO_STATE_CHANGES=YES
```

## R4-C proposal — checkpoint 177

```text
R4_C_PROPOSAL_READY=YES
CUTOVER_STYLE=NON_DESTRUCTIVE
SOURCE_PUBLIC_GPT=KEEP PUBLISHED / UNCHANGED
AUDIENCE_SELECTION_REQUIRED=YES
OPTIONS=PRIVATE_OWNER_ONLY | LINK_ONLY_PILOT | PUBLIC_DISCOVERY
PUBLICATION_CHANGE=HOLD
USER_SWITCH=HOLD
ROLLBACK_ANCHOR=EXISTING_PUBLIC_GPT
```

## R4-B completion — checkpoint 176

```text
B1=PASS
B2=PASS
B3=PASS
B4=OPTIONAL / NOT_RUN
CORE_REGRESSION=PASS
MEDIA_READONLY_REGRESSION=PASS
13_OPERATION_SCAN=PASS
EXECUTION_CONFIRMATION_BOUNDARY=PASS
FREE_ONLY_FAIL_CLOSED=PASS
PRIVATE_REPLACEMENT_ACCEPTED=YES
R4_B=COMPLETE
R4_CUTOVER_READY=YES
R4_C_AUTHORIZED=PAUSED
```

R4-C may now be proposed, but no publication/share or source-GPT mutation is authorized.

## R4-B read-only admission fix — checkpoint 175

```text
B1=PASS
B3=PASS
remaining_non_youtube_429_root_cause=read-only routes consumed provider admission budget
fix=read-only managed routes bypass provider admission
provider-start rate/concurrency guards=PRESERVED
VoiceBridge exact deployed SHA=174174aae0635736f05d812094b555544623270c
Render deploy=dep-dapb6f3m8hqs7395ntj0
deploy_status=LIVE
post_deploy_health=200
B2_FINAL_AUTHENTICATED_RERUN=PENDING
```

For missing/expired jobs, authenticated `MEDIA_TRANSCRIPT_NOT_FOUND / 404 / retryable=false` is valid read semantics and does not require a new provider start.

## R4-B VoiceBridge remediation — checkpoint 174

```text
B1=PASS
B3=PASS
B2_429_ROOT_CAUSE=RENDER_FREE_SERVICE_COLD_START
B2_429_REMEDIATION=PASS
POST_WAKE_HEALTH=200
POST_WAKE_9_ROUTE_PATHS=401_AUTH_BOUNDARY / ZERO_429
B2_AUTHENTICATED_CANDIDATE_RERUN=PENDING
R4_B_OVERALL=NOT_COMPLETE
```

No code/config mutation was required. Repeat only authenticated B2 while VoiceBridge is awake.

## R4-B live Candidate — checkpoint 173

```text
B1=PASS
B2=BLOCKED_BY_VOICEBRIDGE_429
B3=PASS
all_9_readonly_attempted=true
common_http_status=429
retryable=true
execution_tools_called=0
provider_work_started=false
R4_B_OVERALL=NOT_COMPLETE
```

Next gate: read-only 429 diagnosis/remediation on shared VoiceBridge path, then repeat only B2.

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

R4_C=PAUSED_PENDING_SUPPORTED_CHATGPT_DISTRIBUTION
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
R4_B=COMPLETE
R4_B_B1=PASS
R4_B_B2=PASS
R4_B_B3=PASS
R4_B_B4=OPTIONAL / NOT_RUN
PRIVATE_REPLACEMENT_ACCEPTED=YES
R4_CUTOVER_READY=YES
R4_C_AUTHORIZED=PAUSED
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

MIGRATE_CONTROL=AVAILABLE / owner UI confirmed
```

No UI mutation was made during inspection.

## Current path decision

The current account exposes the required Plugin and Skill surfaces directly. No explicit migration control was found.

Therefore, if R4 is later authorized, the cutover plan must use the validated Plugin/Skill path actually present in the account, not depend on an unobserved `Migrate` button.

## R4 cutover remains unauthorized

R4-B is complete and the private replacement is accepted. R4-C is ready to propose but remains unauthorized. Preserve FREE_ONLY; no publication/share, public GPT mutation, additional MEDIA execution, or PR merge without separate explicit approval.

## Hard boundary

```text
PROJECT_COST_POLICY=FREE_ONLY
R4_CUTOVER_AUTHORIZED=NO / PAUSED
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

**R4-B is COMPLETE.** B1/B2/B3 passed; B4 was optional and not run. The private replacement is accepted. R4-C is ready to propose but remains HOLD pending separate owner authorization.

Recovery authority: `CURRENT_HANDOFF.md` v21.8 + checkpoint 193.
