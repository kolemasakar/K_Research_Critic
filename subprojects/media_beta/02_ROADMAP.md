# MEDIA BETA Roadmap

Version: 7.0
Status: **PLUGIN_FIRST / R3-E1_COMPLETE / R3-E2_COMPLETE / R3-E3_CONFIRMATION_COMPLETE / R3-E4_CONFIRMATION_COMPLETE / R3-F_CI_PASS / R3-G_OAUTH_RUNTIME_ACTIVE / FREE_ONLY / LIVE_CANARY_APPROVAL_HOLD / PUBLICATION_HOLD**
Updated: 2026-09-19

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
R3-E3 Facebook execution                      ZERO-SIDE-EFFECT CONFIRMATION COMPLETE / LIVE CANARY HOLD
R3-E4 Telegram execution                      ZERO-SIDE-EFFECT CONFIRMATION COMPLETE / LIVE CANARY HOLD
R3-F Full 13-operation parity                 LOCAL+CI PASS / RUNTIME ACCEPTANCE PENDING
R3-G Private operational hardening            OAUTH DEPLOYED / DISCOVERY PASS / TOKEN RESTART ACCEPTANCE PENDING
R3-H Migration/publication readiness          HOLD
R4 Owner-approved cutover/publication         HOLD
```

**Current position:** E3/E4 zero-side-effect ChatGPT confirmation acceptance is complete, including OAuth connection, Cancel, and Allow-once paths. No real Facebook or Telegram provider work has occurred. The next boundary is separate owner approval for one bounded live canary per platform.

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

- R3-E1 YouTube sentinel;
- R3-E2 Instagram sentinel;
- VoiceBridge v0.6.0 staging head with E3/E4 route-scoped bearer support;
- R3-E3 Facebook sentinel in confirmation-probe-only mode;
- R3-E4 Telegram sentinel in confirmation-probe-only mode;
- OCI Cobalt v11.7.1;
- Neon Free durable backend.

Still pending acceptance:

- one separately authorized live Facebook canary;
- one separately authorized live Telegram canary;
- Neon persistence/restart/replay/idempotency for E3/E4;
- restart-safe OAuth token continuity across restart;
- R3-F runtime parity closure.

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

The repositories are public and these standard GitHub-hosted Ubuntu jobs were not blocked by the previously recorded 2000/2000 private-repository included-minutes state. Paid Actions usage remains denied and was not needed.

## Safety invariant

```text
E3_CONFIRMATION_PROBE_ONLY=true
E4_CONFIRMATION_PROBE_ONLY=true
E3_CONFIRMATION_PROBE_INVOCATIONS=1
E4_CONFIRMATION_PROBE_INVOCATIONS=1
E3_PROVIDER_WORK_STARTED=false
E4_PROVIDER_WORK_STARTED=false
NEON_MANAGED_JOBS=1
NEON_INSTAGRAM_JOBS=1
NEON_FACEBOOK_JOBS=0
NEON_TELEGRAM_JOBS=0
POST_DEPLOY_ERROR_LEVEL_LOGS=0
POST_DEPLOY_HTTP_5XX=0
```

## Nearest tasks

1. Obtain separate owner approval for one bounded Facebook live canary and one bounded Telegram live canary.
2. After approval only, disable probe-only mode in a controlled manner for the selected platform and run exactly one canary.
3. Prove Neon durability, restart/replay, duplicate-start idempotency and zero paid fallback.
4. Repeat for the second platform only after its separate owner approval.
5. Close R3-E3 and R3-E4.
6. Complete R3-F runtime parity acceptance.
7. Complete R3-G restart-safe token continuity and operational hardening.
8. Enter R3-H migration/publication readiness.

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

Recovery authority: `CURRENT_HANDOFF.md` v18.9 + checkpoint 149.
