# MEDIA BETA Roadmap

Version: 6.9
Status: **PLUGIN_FIRST / R3-E1_COMPLETE / R3-E2_COMPLETE / R3-E3_RUNTIME_STAGING / R3-E4_RUNTIME_STAGING / R3-F_CI_PASS / R3-G_OAUTH_DEPLOYED / FREE_ONLY / PUBLICATION_HOLD**
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
R3-E3 Facebook execution                      CI+DEPLOY_HEALTH+OAUTH_DISCOVERY PASS / AUTH CONFIRMATION PENDING
R3-E4 Telegram execution                      CI+DEPLOY_HEALTH+OAUTH_DISCOVERY PASS / AUTH CONFIRMATION PENDING
R3-F Full 13-operation parity                 LOCAL+CI PASS / RUNTIME ACCEPTANCE PENDING
R3-G Private operational hardening            OAUTH DEPLOYED / DISCOVERY PASS / TOKEN RESTART ACCEPTANCE PENDING
R3-H Migration/publication readiness          HOLD
R4 Owner-approved cutover/publication         HOLD
```

**Current position:** E3/E4 zero-side-effect staging runtimes are live on Render Free. CI and unauthenticated OAuth discovery are complete. The next boundary is secret-safe authenticated OAuth/MCP discovery and ChatGPT confirmation acceptance.

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

- authenticated OAuth/DCR + MCP discovery for E3/E4;
- ChatGPT Cancel/Allow-once on E3/E4;
- restart-safe OAuth token continuity across restart;
- live E3/E4 canaries, which require separate owner authorization;
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

1. Complete secret-safe authenticated OAuth/DCR and authenticated MCP discovery for E3/E4.
2. Validate ChatGPT Cancel and Allow-once while confirmation-probe-only remains enabled.
3. Obtain separate owner approval before any real Facebook or Telegram execution.
4. After that approval only, run one bounded canary per platform and prove Neon durability, restart/replay, duplicate-start idempotency and zero paid fallback.
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

Recovery authority: `CURRENT_HANDOFF.md` v18.3 + checkpoint 142.
