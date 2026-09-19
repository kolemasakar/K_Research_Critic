# KRC MEDIA — R3-E2 complete / R3-E3 / R3-E4 / OAuth / R3-F staging checkpoint

Date: 2026-09-19
Status: **R3_E2_PASS_COMPLETE / R3_E3_STAGING_READY / R3_E4_STAGING_READY / OAUTH_STAGING_READY / R3_F_LOCAL_READY / FREE_ONLY / ACTIONS_HOLD**

## Owner storage rule

Local HP-OMEN disks are not an accepted project storage location.

```text
HP_OMEN_LOCAL_DISK_AS_PROJECT_STORAGE=DENIED
AUTHORITATIVE_PROJECT_STATE=GITHUB_REPOSITORIES
LOCAL_WORKTREE_USE=TRANSIENT_ONLY
```

After verified repository transfer, temporary local staging worktrees and patch artifacts must be removed.

## R3-E2 final closure

Owner acceptance establishes:

```text
R3_E2_CHATGPT_CONFIRMATION_UI=PASS
R3_E2_CANCEL_PATH=PASS
R3_E2_APPROVE_PATH=PASS
R3_E2_LIVE_CANARY=PASS
R3_E2_DURABLE_NEON=PASS
R3_E2_RESTART_REPLAY=PASS
R3_E2_STATUS_SEGMENTS_AFTER_RESTART=PASS
R3_E2_DUPLICATE_START_IDEMPOTENCY=PASS
R3_E2_DUPLICATE_PROVIDER_WORK=NO
R3_E2_NEW_PROVIDER_CHARGE=0
R3_E2_ERROR_SCAN=PASS
R3_E2=PASS / COMPLETE
```

Accepted job:

```text
job_id=KRCM_04e6d847-449c-4d0f-82c7-b494871d9322
status=COMPLETED
provider=assemblyai
provider_mode=cobalt_retrieval_stt
retrieval_provider=cobalt
segment_count=1
media_duration_seconds=42.24
stt_seconds_charged=43
credits_charged=0
retrieval_credits_charged=0
metadata_credits_charged=0
credit_charge_uncertain=false
provider_data_deleted=true
```

Duplicate start returned the same durable completed job with no new provider processing and no new charge.

## Governing cost / CI constraint

```text
PROJECT_COST_POLICY=FREE_ONLY
GITHUB_ACTIONS_MINUTES=2000/2000
ACTIONS_RESET=2026-10-01
PAID_ACTIONS_USAGE=DENIED
```

The staging transfer uses CI-skip semantics. Full CI validation is deferred until reset or separate owner decision.

## R3-E3 Facebook staging

Prepared implementation:
- dedicated R3-E3 route-scoped bearer;
- isolated Facebook MCP surface;
- exactly one execution tool: `media_facebook_start`;
- Facebook durable lookup;
- Facebook-only status/segments isolation;
- paid/AI continuation routes blocked for R3-E3 bearer;
- zero-side-effect confirmation probe;
- bounded health warmup;
- no automatic retry of consequential POST;
- restart/replay probe.

No R3-E3 runtime deployment or live Facebook provider work is authorized by this checkpoint.

## R3-E4 Telegram staging

Prepared implementation:
- Telegram route-scoped bearer;
- isolated Telegram MCP surface;
- exactly one execution tool: `media_telegram_start`;
- Telegram durable lookup;
- Telegram-only status/segments isolation;
- zero-side-effect confirmation probe;
- bounded health warmup;
- restart/replay probe.

No R3-E4 runtime deployment or live Telegram provider work is authorized by this checkpoint.

## OAuth restart-safe staging

Prepared optional `KRC_MCP_OAUTH_SIGNING_KEY` implementation.

When configured:
- DCR client registration survives restart;
- access tokens survive restart;
- refresh tokens survive restart;
- tampered/expired tokens fail closed;
- signing-key rotation invalidates old credentials;
- authorization codes remain short-lived, single-use and in-memory.

## R3-F parity staging

Prepared contract:

```text
READ_OPERATIONS=9
EXECUTION_OPERATIONS=4
TOTAL_OPERATIONS=13
R3C_EXECUTION_TOOLS=0
R3E1_OWN_START_ONLY=true
R3E2_OWN_START_ONLY=true
R3E3_OWN_START_ONLY=true
R3E4_OWN_START_ONLY=true
```

## Validation before repository transfer

```text
KRC combined R3C/R3D/R3E1/R3E2/R3E3/R3E4/OAuth/R3-F=65/65 PASS
VoiceBridge relevant free-only/cross-route/durability regression=23/23 PASS
Facebook+Telegram scoped route targeted suite=11/11 PASS
```

Neon safety check:

```text
managed_jobs=1
facebook_jobs=0
telegram_jobs=0
```

Therefore this staging work caused no Facebook or Telegram provider processing or charge.

## Next gate

After Actions reset or separate owner override:

1. run CI for VoiceBridge staging head;
2. run CI for KRC staging head;
3. deploy server-side OAuth signing key and scoped bearers;
4. deploy R3-E3 / R3-E4 isolated sentinels on Render Free;
5. run authenticated read-only preflight/lookup;
6. validate ChatGPT confirmation Cancel/Allow-once in zero-side-effect mode;
7. request separate owner authorization for one bounded Facebook live canary and one bounded Telegram live canary;
8. run Neon persistence, restart/replay and duplicate-start idempotency acceptance.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_139_R3E2_COMPLETE_E3_E4_OAUTH_R3F_STAGING_READY_ACTIONS_HOLD_2026_09_19`
