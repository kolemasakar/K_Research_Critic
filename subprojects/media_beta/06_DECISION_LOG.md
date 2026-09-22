# MEDIA BETA Decision Log

Version: 6.6
Status: **ACTIVE / R3_A_TO_H_COMPLETE / R4_A_COMPLETE / R4_B_COMPLETE / PRIVATE_REPLACEMENT_ACCEPTED / R4_C_IN_PROGRESS / WEB_LINK_ONLY_PATH_UNAVAILABLE / DISTRIBUTION_DECISION_PENDING / ZERO_MUTATION**
Updated: 2026-09-22

Historical decisions remain preserved in Git history and numbered checkpoints.

## Active decisions

### D036 — Plugin-first authenticated Remote MCP path accepted
```text
PLUGIN_FIRST_STRATEGY=ACCEPTED
PUBLIC_KRC_CUSTOM_GPT=UNCHANGED
```

### D037 — R3-A/B/C/D accepted
```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
```

### D038 — Four isolated execution surfaces accepted
```text
R3_E1_YOUTUBE=COMPLETE
R3_E2_INSTAGRAM=COMPLETE
R3_E3_FACEBOOK=COMPLETE
R3_E4_TELEGRAM=COMPLETE
OTHER_EXECUTION_TOOLS_PER_SURFACE=0
```

### D039 — Project policy remains FREE_ONLY
```text
PROJECT_COST_POLICY=FREE_ONLY
RENDER_FREE_WEB_SERVICES=ACCEPTED
NEON_FREE_POSTGRES=PRIMARY_DURABLE_DATABASE
OCI_ALWAYS_FREE=ACCEPTED
SELF_HOSTED_COBALT_ON_OCI=ACCEPTED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
PAID_ACTIONS_USAGE=DENIED
```

### D059 — Facebook R3-E3 accepted
```text
LIVE_CANARY=PASS
FREE_RETRIEVAL=cobalt
DURABLE_PERSISTENCE=PASS
RESTART_DURABILITY=PASS
DUPLICATE_START_IDEMPOTENCY=PASS
ZERO_PAID_FALLBACK=PASS
```

### D060 — Telegram R3-E4 accepted
The first no-spoken-audio fixture produced a valid bounded content failure. The approved replacement completed successfully.
```text
COMPLETED_CANARY=PASS
RETRIEVAL_PROVIDER=telegram_public_web
DURABLE_PERSISTENCE=PASS
RESTART_DURABILITY=PASS
DUPLICATE_START_IDEMPOTENCY=PASS
ZERO_CHARGE=PASS
```

### D061 — Full 13-operation runtime parity accepted
```text
R3_F=COMPLETE
READ_OPERATIONS=9
EXECUTION_OPERATIONS=4
TOTAL_OPERATIONS=13
READ_ONLY_EXECUTION_LEAKAGE=0
```

### D062 — OAuth / operational hardening accepted
```text
R3_G=COMPLETE
DCR=PASS
ACCESS_TOKEN_RESTART_CONTINUITY=PASS
REFRESH_TOKEN_RESTART_CONTINUITY=PASS
RUNTIME_REFRESH_AFTER_3600S_TTL=PASS
CHATGPT_RECONNECT_REQUIRED=NO
E3_TO_VOICEBRIDGE_SCOPED_AUTH=PASS
MANAGED_MEDIA_JOB_TTL_SECONDS=3600
```

### D063 — R3-H readiness review accepted
```text
R3_H=COMPLETE
ROLLBACK_PACKAGE=READY
R4_RELEASE_CHECKLIST=READY
R4=HOLD
```

### D064 — R4 non-UI read-only preflight accepted
```text
CORE_SKILL_PARITY=PASS
MEDIA_13_TOOL_PARITY=PASS
LIVE_RUNTIME_HEALTH=PASS
PRIVATE_PLUGIN_EXISTENCE=PASS
PLUGIN_PERMISSION_MODEL=PASS
CI=PASS
R4_NON_UI_PREFLIGHT=COMPLETE
```

### D065 — Automated account UI inspection may fail closed
Cloud Browser was blocked by Cloudflare human verification. No bypass was attempted and no mutation occurred.

### D066 — Manual R4 account UI preflight accepted
Manual screenshots on 2026-09-21 confirmed:
```text
GPT_NAME=K-Research & Critic
GPT_IDENTITY=PASS
GPT_EDITOR_ACCESS=PASS
PUBLICATION_STATE=Published
VISIBLE_AUDIENCE=Everyone

SHARE_CONTROL=PASS
GPT_STORE_SURFACE=PASS
CATEGORY_CONTROL=PASS

PLUGIN_SURFACE=PASS
PRIVATE_KRC_PLUGIN_INVENTORY=PASS
INSTALL_ADD_CONTROL=PASS

SKILLS_SURFACE=PASS
SKILLS_ADD_CONTROL=PASS

MIGRATE_CONTROL=NOT_FOUND_IN_CURRENT_UI
```

No state-changing UI action was performed.

### D067 — R4 read-only preflight is complete
Combined non-UI and manual UI evidence closes the technical preflight.
```text
R4_NON_UI_PREFLIGHT=COMPLETE
R4_MANUAL_UI_PREFLIGHT=COMPLETE
R4_READONLY_PREFLIGHT=PASS / COMPLETE
R4_TECHNICAL_PREFLIGHT_DEBT=0
R4_CUTOVER_AUTHORIZED=NO
NEXT_GATE=OWNER_CUTOVER_DECISION_IN_FRESH_CHAT
```

### D068 — No explicit migration control is assumed
No `Migrate` / `Перенести` control was found across the inspected GPT, editor, overflow, share, plugin, and skill surfaces.

Future R4 work, if owner-authorized, must use the validated Plugin/Skill path actually present in the account and must not depend on an unobserved migration button.

### D069 — Final project/docs sync accepted
Checkpoint 165 freezes the transition state before a new-chat generator is applied.
```text
PROJECT_SYNC_COMPLETE=YES
R4_READONLY_PREFLIGHT=COMPLETE
R4_CUTOVER_AUTHORIZED=NO
NEW_CHAT_READY=YES
CANONICAL_RECOVERY=CURRENT_HANDOFF_v19.8 + checkpoint_165
```
### D070 — R3C OAuth recovery accepted without GitHub Actions

GitHub Actions were unavailable and were not used as a current validation gate.

```text
R3C_RUNTIME_VALIDATED_HEAD=27585c0ce924c78529b90aaadbfbeee841d0d249
R3C_RENDER_DEPLOY=dep-dap55aegekts73fr0960 / LIVE
OAUTH_AUTHORIZE_GET=200
OAUTH_AUTHORIZE_POST=302
OAUTH_TOKEN_POST=200
MEDIA_GET_CAPABILITIES=PASS
R3C_TO_VOICEBRIDGE_BINDING=PASS
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO
CURRENT_VALIDATION_MODE=EXACT_COMMIT_RENDER_BUILD + LIVE_READONLY_RUNTIME
```

The legacy OAuth bridge is limited to an exact configured client-id/callback pair and upgrades successful authorization into restart-safe signed tokens.

### D071 — Plugin inventory drift warning closed

```text
PLUGIN_REQUIRED_SURFACES=PASS
LEGACY_PLUGIN_ENTRIES=NOT_REQUIRED
FUNCTIONAL_INVENTORY_DRIFT=NO
RECOVERY_CONSISTENCY_WARNING=CLOSED
REINSTALL_REQUIRED=NO
```

Checkpoint 164 remains a historical UI snapshot. Current accepted R3-B and R3-E2 surfaces are the newer R3B and Instagram-v5 connections. No Plugin install/remove/permission mutation was performed during reconciliation.

### D054 — GitHub remains authoritative storage
```text
AUTHORITATIVE_PROJECT_STATE=GITHUB_REPOSITORIES
LOCAL_WORKTREE_USE=TRANSIENT_ONLY
```

### D072 — Checkpoint 166 canonical sync accepted

```text
PROJECT_SYNC_COMPLETE=YES
CANONICAL_RECOVERY=CURRENT_HANDOFF_v19.9 + checkpoint_166
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO
CURRENT_VALIDATION_MODE=EXACT_COMMIT_RENDER_BUILD + LIVE_READONLY_RUNTIME
R4_CUTOVER_AUTHORIZED=NO
```

This supersedes checkpoint 165 as the current recovery entry point while preserving checkpoint 165 as historical evidence.

### D073 — R4 staged cutover/rollback package accepted

Checkpoint 167 defines the exact mutation and rollback order without authorizing execution.

```text
R4_PATH=PRIVATE_ASSEMBLY -> PRIVATE_ACCEPTANCE -> OPTIONAL_USER_SWITCH
R4_A_PRIVATE_ASSEMBLY_AUTHORIZED=NO
R4_B_PRIVATE_ACCEPTANCE_AUTHORIZED=NO
R4_C_USER_SWITCH_AUTHORIZED=NO

SOURCE_PUBLIC_GPT=KEEP_UNCHANGED
BUILTIN_MIGRATION_CONTROL=NOT_FOUND / NOT_USED
ROLLBACK_ANCHOR=EXISTING_PUBLIC_GPT

R4_CUTOVER_PACKAGE=READY
R4_ROLLBACK_PACKAGE=READY
R4_CUTOVER_READY=NO
```

R4-A requires a private KRC Core Skill, restoration of the E1 YouTube private MCP connection, and assembly of the private replacement Plugin. No new MEDIA execution is implicitly authorized.

### D074 — Public cutover is non-destructive by default

Because no built-in migration control is available in the inspected account UI, the default future R4-C plan does not delete, edit, or unpublish the existing K-Research & Critic GPT. Replacement sharing/publication and any later source-GPT retirement are separate owner decisions.

### D075 — E1 restart-safe OAuth is mandatory before reconnect

Read-only inspection established that the accepted live E1 commit `88cdc465...` still uses process-memory `OAuthState`, while the accepted recovery code at `27585c0...` contains `RestartSafeOAuthState`.

Therefore:

```text
E1_RESTART_SAFE_OAUTH_REQUIRED_BEFORE_RECONNECT=YES
R4_A_SEQUENCE_167=SUPERSEDED_BY_168
R4_A_FIRST_MUTATION=E1_OAUTH_HARDENING
R4_A_AUTHORIZED=NO
```

No E1 redeploy, reconnect, Plugin installation, Skill installation, provider work, publication or source-GPT mutation was performed during this review.

### D076 — R4-A private package assembly accepted through static gate

```text
A1_E1_RESTART_SAFE_OAUTH=PASS
A1_RESTART_CONTINUITY=PASS
A2_E1_PRIVATE_CONNECTION=PASS
A3_CORE_SKILL_PRIVATE_INSTALL=PASS
A4_PACKAGE_STATIC_VALIDATION=PASS
A4_PRIVATE_INSTALL=PENDING
```

The R4 Candidate references five already registered ChatGPT apps through `.app.json`; no raw `mcp.json` is included. A repo-local marketplace entry was added for private testing. This does not authorize publication/share or R4-B.

### D077 — A4 private install accepted

Work completed the Personal / Local installation of `K-Research & Critic R4 Candidate` with one Skill and five registered app mappings.

Real Work schema validation found and corrected only:
- unsupported `required` fields in `.app.json`;
- missing `interface.defaultPrompt`.

Repository manifests were reconciled to that validated shape.

```text
A4_PRIVATE_INSTALL=PASS
FINAL_VALIDATION_ERRORS=0
PUBLICATION=NO
SHARING=NO
MEDIA_PROVIDER_WORK=NO
A5=PENDING_NEW_CHAT
```

### D078 — R4-A private assembly accepted and stopped at A6

A5 in the fresh chat verified the assembled private R4 Candidate without executing any MEDIA start operation or provider work.

```text
PLUGIN_VISIBLE=PASS
CORE_SKILL_BOUND=PASS
SKILL_COUNT=1
REGISTERED_APP_COUNT=5
READ_OPERATIONS=9
EXECUTION_OPERATIONS=4
TOTAL_OPERATIONS=13
READ_ONLY_EXECUTION_LEAKAGE=0
FREE_ONLY=PASS
SOURCE_PUBLIC_GPT_UNCHANGED=YES
PUBLICATION=NO
SHARING=NO
A5=PASS
A6=COMPLETE
R4_A=COMPLETE
R4_B_AUTHORIZED=NO
R4_C_AUTHORIZED=NO
```

A permitted read-only `media_get_capabilities` probe returned HTTP 429/retryable; no provider work was started. This is recorded as a runtime probe warning, not as execution leakage or a package parity failure.

### D079 — R4-B authorized; static regression PASS; live Candidate reselect required

Owner authorized R4-B Private Acceptance after R4-A completion.

Repository/contract checks passed for Core snapshot/fixtures, risk and cross-check floors, claim ledger, traceability, language, checkpoint recovery, media/core isolation, model-agnostic behavior, 13-operation parity, consequential annotations, and FREE_ONLY fail-closed policy.

The active turn then stopped exposing the Personal/Local Candidate KRC tool namespaces. Direct orchestration therefore failed before MCP/provider/backend invocation. This is treated fail-closed and must not be replaced by unrelated public/global plugin results.

```text
R4_B_AUTHORIZED=YES
R4_B=IN_PROGRESS
B1_REPOSITORY_FIXTURE_REGRESSION=PASS
B1_LIVE_CANDIDATE_BEHAVIOR=PENDING
B2_LIVE_READONLY_REGRESSION=BLOCKED_PENDING_CANDIDATE_RESELECT
B3_CONTRACT_SCAN=PASS
B3_LIVE_CANDIDATE_VISIBILITY_SCAN=PENDING
B4_LIVE_EXECUTION=NOT_PERFORMED
PROVIDER_WORK_STARTED=false
ADDITIONAL_LIVE_MEDIA_STARTS=0
PRIVATE_REPLACEMENT_ACCEPTED=NO
R4_C_AUTHORIZED=NO
```

### D080 — R4-B live Candidate: B1 PASS / B2 blocked by VoiceBridge 429 / B3 PASS

Owner-provided live Candidate evidence confirms all 13 canonical operations are visible, B1 live Core behavior passes, and B3 visibility/confirmation scan passes. All nine B2 read-only operations reached the live path but returned the same retryable VoiceBridge HTTP 429.

```text
B1=PASS
B2=BLOCKED_BY_VOICEBRIDGE_429
B3=PASS
ALL_9_READONLY_ATTEMPTED=true
COMMON_ERROR=voicebridge_http_error / HTTP 429 / retryable=true
READ_ONLY_EXECUTION_LEAKAGE=0
EXECUTION_TOOLS_CALLED=0
PROVIDER_WORK_STARTED=false
R4_B_OVERALL=NOT_COMPLETE
R4_C_AUTHORIZED=NO
```

Decision: diagnose and minimally remediate only the shared read-only 429 path, then repeat B2 only. B1/B3 remain accepted unless remediation changes their governed components.

### D081 — VoiceBridge 429 root cause accepted as Render free-service cold start

Checkpoint 166 already documented the same sequence: retryable 429 while VoiceBridge was cold/asleep, initial health wake 503, then health 200 and successful read-only invocation.

Checkpoint 174 reproduced that sequence. During the B2 failure window R3C received the Candidate MCP calls with HTTP 200, while VoiceBridge had no corresponding request logs or HTTP metrics. Direct health wake returned 503 twice; Render then emitted `service_started` at 2026-09-22T16:46:28Z and health returned 200.

After wake, all nine canonical MEDIA route paths returned the expected authentication boundary 401 when probed without credentials, with zero 429 responses.

```text
ROOT_CAUSE=RENDER_FREE_SERVICE_COLD_START
CODE_CHANGE_REQUIRED=NO
CONFIG_CHANGE_REQUIRED=NO
REMEDIATION=READ_ONLY_HEALTH_WAKE
POST_WAKE_HEALTH=200
POST_WAKE_429_COUNT=0
AUTH_BOUNDARY_PRESERVED=PASS
B2_AUTHENTICATED_CANDIDATE_RERUN=PENDING
```

Direct unauthenticated probes do not count as B2 functional PASS. The remaining acceptance step is to repeat only B2 through the authenticated private Candidate while VoiceBridge is awake.

### D082 — Managed read-only 429 leakage fixed without weakening FREE_ONLY

Authenticated B2 showed that the cold-start blocker was cleared, but rapid non-YouTube read-only calls still returned retryable 429 after a successful preflight.

Root cause was `PublicMediaAdmissionController`: it applied provider admission rate/concurrency controls to every authenticated `/api/v1/media/managed/*` request, including preflight, lookup, status, and segments.

The minimal remediation restricts provider admission to the only route that can start provider work:

```text
POST /api/v1/media/managed/transcriptions
```

Read-only managed routes bypass provider admission and continue through their normal authentication/read handlers. FREE_ONLY, start-route rate limits, and concurrency limits remain intact.

```text
VoiceBridge code commit=eda6fce7236eaa3d119864236078fbe45e5379f3
VoiceBridge deployed head=174174aae0635736f05d812094b555544623270c
Render deploy=dep-dapb6f3m8hqs7395ntj0
deploy_status=LIVE
typescript_build=PASS
post_deploy_health=200
PR45=OPEN / DRAFT / UNMERGED
```

YouTube `lookup/status/segments` 404 responses are not infrastructure failures when they represent `MEDIA_TRANSCRIPT_NOT_FOUND / retryable=false` for missing or expired jobs. Runtime retention is 3600 seconds. B2 acceptance therefore evaluates expected authenticated read semantics, not an all-2xx requirement.

The remaining gate is one final authenticated Candidate B2 rerun with zero infrastructure 429 and zero execution/provider starts.

### D083 — R4-B private acceptance complete

The final authenticated Candidate B2 rerun after checkpoint 175 attempted all nine read-only MEDIA operations and satisfied the accepted read semantics for every operation.

```text
operations_attempted=9/9
accepted_pass=9
accepted_fail=0
infrastructure_HTTP_429=0
execution_start_calls=0
provider_work=0
```

Successful preflight/capability reads returned HTTP 200. Missing or expired lookup/status/segments returned the accepted negative read result `MEDIA_TRANSCRIPT_NOT_FOUND / HTTP 404 / retryable=false`. No provider execution was used to create fresh jobs.

Checkpoint 167 defines B4 as optional. Therefore R4-B acceptance is satisfied by B1/B2/B3 plus the confirmation and FREE_ONLY boundaries:

```text
CORE_REGRESSION=PASS
MEDIA_READONLY_REGRESSION=PASS
13_OPERATION_SCAN=PASS
EXECUTION_CONFIRMATION_BOUNDARY=PASS
FREE_ONLY_FAIL_CLOSED=PASS
B4=OPTIONAL / NOT_RUN
PRIVATE_REPLACEMENT_ACCEPTED=YES
R4_B=COMPLETE
```

R4-C may now be proposed but remains separately gated:

```text
R4_CUTOVER_READY=YES
R4_C_AUTHORIZED=NO
R4_CUTOVER=HOLD
SOURCE_PUBLIC_GPT_UNCHANGED=YES
PUBLICATION=NO
SHARING_CHANGE=NO
PR22_MERGE=NO
PR45_MERGE=NO
```

### D084 — R4-C non-destructive cutover proposal prepared

After R4-B completion, the exact R4-C contract from checkpoint 167 was recovered.

R4-C remains a separate final owner decision. The preferred cutover is non-destructive:

```text
SOURCE_PUBLIC_GPT=KEEP PUBLISHED / UNCHANGED
ROLLBACK_ANCHOR=EXISTING_PUBLIC_GPT
PR22_MERGE=NO
PR45_MERGE=NO
NEW_MEDIA_STARTS=NO
PROVIDER_WORK=NO
```

Before any replacement sharing/publication/user-switch mutation, the owner must select one exact audience:

```text
1=PRIVATE_OWNER_ONLY
2=LINK_ONLY_PILOT
3=PUBLIC_DISCOVERY
```

No audience is inferred from the generic instruction to continue.

Until an exact audience is selected:

```text
R4_C_AUTHORIZED=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
USER_SWITCH=NO
```

Checkpoint 177 is the canonical proposal/approval gate.

### D085 — R4-C LINK_ONLY_PILOT authorized; browser UI blocked before mutation

Owner explicitly selected audience option 2:

```text
R4_C_AUDIENCE=LINK_ONLY_PILOT
R4_C_AUTHORIZED=YES
```

Two ChatGPT browser attempts were made. The first used the browser profile session; the second also enabled credential-vault recovery.

Both stopped before Personal/Local Plugin management because:

```text
authenticated_ChatGPT_session=false
configured_ChatGPT_vault_credentials=false
Cloudflare_human_verification=blocking
personal_plugin_management_reached=false
```

No state-changing control was reached and no mutation occurred:

```text
PLUGIN_AUDIENCE_CHANGE=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
PUBLIC_DISCOVERY=NO
SOURCE_PUBLIC_GPT_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
MEDIA_STARTS=0
PROVIDER_WORK=0
```

R4-C remains authorized only for LINK_ONLY_PILOT and resumes at C2 once an authenticated ChatGPT UI session is available.

Browser run references:

```text
e3e6cd2a-5a55-4011-9079-7cda4d17c6e7
ea2a4b56-dd91-4415-aab3-bceb9ba6134e
```

### D086 — Personal Plus web surface cannot perform link-only sharing for the local marketplace Candidate

Manual UI evidence confirmed that the top-right `+` control opens the standalone MCP plugin creation form, not management for the existing local marketplace package. Searching Personal plugins for `K-Research & Critic R4 Candidate` returns no result.

Current OpenAI documentation distinguishes local marketplace plugins from workspace-shared plugins. Link-based plugin sharing is a managed-workspace capability; the current personal Plus web surface does not expose that control for the local Candidate.

```text
R4_C_LINK_ONLY_PILOT_INTENT=YES
WEB_LINK_ONLY_CONTROL=UNAVAILABLE
STATE_CHANGES=0
SOURCE_PUBLIC_GPT_UNCHANGED=YES
```

Supported next mechanisms require a fresh owner decision:
A local marketplace pilot; B managed workspace link pilot; C public directory.

## Canonical authority

- `CURRENT_HANDOFF.md` v21.2
- checkpoint 179
- `02_ROADMAP.md` v9.3
- `00_INDEX.md` v10.6
- `08_CHAT_HANDOFF.md` v7.6

## Hard boundary

```text
PROJECT_COST_POLICY=FREE_ONLY
PUBLIC_GPT_MUTATION=NO
PLUGIN_INSTALLATION_OR_CHANGE=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
ADDITIONAL_LIVE_MEDIA_STARTS=NO
R4_CUTOVER=HOLD
```
