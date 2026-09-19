# MEDIA BETA Roadmap

Version: 6.7
Status: **PLUGIN_FIRST / R3-E1_COMPLETE / R3-E2_COMPLETE / R3-E3_STAGING_READY / R3-E4_STAGING_READY / OAUTH_STAGING_READY / R3-F_LOCAL_READY / FREE_ONLY / ACTIONS_HOLD / PUBLICATION_HOLD**
Updated: 2026-09-19

## Product position

```text
public KRC Custom GPT: published / unchanged / protected
private MEDIA migration candidate: Remote Custom MCP / Plugin surface
backend authority: VoiceBridge MEDIA API
MEDIA semantic parity target: 13 operations
project infrastructure policy: FREE_ONLY
project authoritative storage: GitHub repositories
```

## Current phase state

```text
R3-A=PASS
R3-B=PASS
R3-C=PASS
R3-D=PASS
R3-E1=PASS / COMPLETE
R3-E2=PASS / COMPLETE
R3-E3=STAGING_READY / DEPLOY_PENDING
R3-E4=STAGING_READY / DEPLOY_PENDING
R3-F=LOCAL_PARITY_READY / CI_PENDING
R3-G OAuth persistence=STAGING_READY / DEPLOY_PENDING
R3-H=HOLD
R4=HOLD
```

## Cost and operational constraints

```text
PROJECT_COST_POLICY=FREE_ONLY
RENDER_FREE_WEB_SERVICES=ACCEPTED
RENDER_POSTGRES=REJECTED_FOR_DURABLE_STATE
NEON_FREE_POSTGRES=PRIMARY_DURABLE_DATABASE
OCI_ALWAYS_FREE=ACCEPTED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
PAID_ACTIONS_USAGE=DENIED

GITHUB_ACTIONS_MINUTES=2000/2000
ACTIONS_RESET=2026-10-01
```

## Storage policy

```text
HP_OMEN_LOCAL_DISK_AS_PROJECT_STORAGE=DENIED
AUTHORITATIVE_PROJECT_STATE=GITHUB_REPOSITORIES
LOCAL_WORKTREES=TRANSIENT_ONLY
```

## Canonical MEDIA contract

```text
13 total operations
9 read/non-execution operations
4 execution operations
```

Execution operations:
- `media_youtube_start`
- `media_instagram_start`
- `media_facebook_start`
- `media_telegram_start`

## R3-E1 — YouTube

Status: **PASS / COMPLETE**.

## R3-E2 — Instagram

Status: **PASS / COMPLETE**.

Accepted: confirmation UI, Cancel/Allow-once, live canary, Neon durable state, restart/replay, status/segments after restart, duplicate-start idempotency, zero duplicate provider work, zero new provider charge.

## R3-E3 — Facebook

Status: **STAGING_READY / RUNTIME_DEPLOY_PENDING**.

Prepared:
- route-scoped bearer;
- isolated MCP surface;
- one execution tool only;
- durable lookup;
- status/segments isolation;
- paid/AI route denial;
- confirmation probe;
- cold-start warmup;
- replay probe.

## R3-E4 — Telegram

Status: **STAGING_READY / RUNTIME_DEPLOY_PENDING**.

Prepared:
- route-scoped bearer;
- isolated MCP surface;
- one execution tool only;
- durable lookup;
- status/segments isolation;
- confirmation probe;
- cold-start warmup;
- replay probe.

## R3-F — Full parity regression

Status: **LOCAL PACKAGE READY / CI PENDING**.

Local contract verifies all 13 operations, no execution leakage into R3-C, and exactly one own start operation per E1/E2/E3/E4 isolated execution surface.

## R3-G — Private operational hardening

OAuth restart-safe implementation is staged via optional `KRC_MCP_OAUTH_SIGNING_KEY`.

Runtime deployment acceptance is pending.

## Next gate

After Actions reset or explicit owner override:

1. CI VoiceBridge staging head.
2. CI KRC staging head.
3. Deploy server-side OAuth signing key and scoped bearers.
4. Deploy R3-E3 and R3-E4 sentinels on Render Free.
5. Read-only authenticated preflight/lookup.
6. Zero-side-effect ChatGPT confirmation acceptance.
7. Separate approval for bounded Facebook and Telegram live canaries.
8. Durable/restart/idempotency acceptance.

Recovery authority: `CURRENT_HANDOFF.md` + checkpoint 139.
