# MEDIA BETA Roadmap

Version: 7.1
Status: **PLUGIN_FIRST / R3-E1_COMPLETE / R3-E2_COMPLETE / R3-E3_FACEBOOK_COMPLETE / R3-E4_TELEGRAM_LIVE_CANARY_ARMED / R3-F_CI_PASS / R3-G_OAUTH_RUNTIME_ACTIVE / FREE_ONLY / PUBLICATION_HOLD**
Updated: 2026-09-20

## End state

Build a production-grade private MEDIA surface for K-Research & Critic while preserving the published public KRC core.

The finished system must provide:

- the canonical 13 MEDIA operations;
- strict separation of 9 read operations and 4 consequential start operations;
- isolated execution surfaces for YouTube, Instagram, Facebook and Telegram;
- ChatGPT confirmation before each consequential start;
- server-side route-scoped credentials;
- restart-safe OAuth/DCR;
- Neon durable state;
- restart replay and duplicate-start idempotency;
- fail-closed behavior and no automatic paid fallback;
- PROJECT_COST_POLICY=FREE_ONLY;
- migration/publication readiness only after full parity and operational acceptance.

## Current roadmap position

```text
R3-A Contract freeze/security baseline        PASS
R3-B Authentication/secret hardening          PASS
R3-C 9-tool read-only binding                 PASS
R3-D Consequential-action confirmation        PASS
R3-E1 YouTube execution                       PASS / COMPLETE
R3-E2 Instagram execution                     PASS / COMPLETE
R3-E3 Facebook execution                      PASS / COMPLETE
R3-E4 Telegram execution                      LIVE CANARY ARMED / LIVE ACCEPTANCE PENDING
R3-F Full 13-operation parity                 LOCAL+CI PASS / RUNTIME ACCEPTANCE PENDING
R3-G Private operational hardening            OAUTH ACTIVE / TOKEN RESTART ACCEPTANCE PENDING
R3-H Migration/publication readiness          HOLD
R4 Owner-approved cutover/publication         HOLD
```

**Current position:** R3-E3 Facebook is fully accepted, including live FREE_ONLY execution, Neon durability, VoiceBridge restart durability, duplicate-start idempotency, and zero paid fallback. R3-E4 Telegram has completed OAuth and confirmation acceptance and is now armed for exactly one owner-approved bounded live canary.

## Canonical contract

```text
TOTAL_OPERATIONS=13
READ_OPERATIONS=9
EXECUTION_OPERATIONS=4
```

Execution operations:

- `media_youtube_start`
- `media_instagram_start`
- `media_facebook_start`
- `media_telegram_start`

## Current runtime

Accepted and healthy:

- R3-E1 YouTube;
- R3-E2 Instagram;
- R3-E3 Facebook — COMPLETE;
- VoiceBridge v0.6.0 on validated staging head;
- E3/E4 route-scoped bearer isolation;
- OCI Cobalt v11.7.1;
- Neon Free durable backend.

R3-E3 Facebook accepted evidence:

```text
job_id=KRCM_2dbbe3ba-c2da-49c4-9941-f64b22630880
status=COMPLETED
retrieval_provider=cobalt
retrieval_credits_charged=0
credits_charged=0
restart_durability=PASS
duplicate_start_idempotency=PASS
duplicate_reused=true
facebook_jobs=1
current_E3_probe_only=true
```

R3-E4 Telegram current readiness:

```text
CHATGPT_OAUTH=PASS
CANCEL=PASS
ALLOW_ONCE_PROBE=PASS
deploy=dep-danj16740ujc73c47c0g
deploy_status=live
current_E4_probe_only=false
provider_work_started=false
telegram_jobs=0
voicebridge_pre_warm_200=3/3
```

Still pending:

- one bounded Telegram live canary;
- Telegram Neon durability;
- Telegram VoiceBridge restart durability;
- Telegram duplicate-start idempotency;
- R3-F runtime parity closure;
- R3-G restart-safe OAuth token continuity.

## CI state

```text
KRC_RUN=35466720921
KRC_PYTHON_3_13=PASS
KRC_PYTHON_3_14=PASS
KRC_QUALITY=PASS

VOICEBRIDGE_RUN=35466722002
VOICEBRIDGE_CLOUD=PASS
VOICEBRIDGE_IMAGE_PARITY=PASS
VOICEBRIDGE_BROWSER_EXTENSION=PASS
VOICEBRIDGE_REPOSITORY_DOCS=PASS
```

The repositories are public and standard GitHub-hosted Ubuntu jobs ran successfully. Paid Actions usage remains denied and was not needed.

## Current safety invariant

```text
E3_CONFIRMATION_PROBE_ONLY=true
E3_PROVIDER_WORK_STARTED=false

E4_CONFIRMATION_PROBE_ONLY=false
E4_PROVIDER_WORK_STARTED=false
E4_OWNER_APPROVED_BOUNDED_LIVE_CANARY=true

NEON_TOTAL_JOBS=2
NEON_INSTAGRAM_JOBS=1
NEON_FACEBOOK_JOBS=1
NEON_TELEGRAM_JOBS=0

PROJECT_COST_POLICY=FREE_ONLY
AUTOMATIC_PAID_FALLBACK=DENIED
```

## Nearest tasks

1. Execute exactly one `media_telegram_start` for `https://t.me/techcrimes/12101`.
2. Verify durable Telegram job, public Telegram retrieval and zero retrieval credits.
3. Controlled-redeploy VoiceBridge on the validated head.
4. Verify Telegram job/segments survive restart.
5. Repeat the exact Telegram start once and require same job id, `reused=true`, no new provider work, and zero charge.
6. Return E4 to `CONFIRMATION_PROBE_ONLY=true`.
7. Close R3-E4.
8. Complete R3-F runtime parity and R3-G OAuth restart acceptance.
9. Enter R3-H migration/publication readiness.

## Infrastructure policy

```text
PROJECT_COST_POLICY=FREE_ONLY
RENDER_FREE_WEB_SERVICES=ACCEPTED
RENDER_POSTGRES=REJECTED_FOR_DURABLE_STATE
NEON_FREE_POSTGRES=PRIMARY_DURABLE_DATABASE
OCI_ALWAYS_FREE=ACCEPTED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
PAID_ACTIONS_USAGE=DENIED
```

## Storage policy

```text
AUTHORITATIVE_PROJECT_STATE=GITHUB_REPOSITORIES
HP_OMEN_LOCAL_DISK_AS_PROJECT_STORAGE=DENIED
LOCAL_WORKTREES=TRANSIENT_ONLY
```

Recovery authority: `CURRENT_HANDOFF.md` v19.0 + checkpoint 154.
