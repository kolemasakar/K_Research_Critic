# MEDIA BETA Decision Log

Version: 5.6
Status: **ACTIVE / R3_A_TO_H_COMPLETE / R3C_OAUTH_RECOVERY_PASS / R4_PACKAGE_CORRECTED / E1_OAUTH_HARDENING_REQUIRED / PRIVATE_ASSEMBLY_REQUIRED / R4_CUTOVER_HOLD / PUBLICATION_HOLD**
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

## Canonical authority

- `CURRENT_HANDOFF.md` v20.2
- checkpoint 169
- `02_ROADMAP.md` v8.3
- `00_INDEX.md` v9.6
- `08_CHAT_HANDOFF.md` v6.6

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
