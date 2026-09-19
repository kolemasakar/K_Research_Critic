# MEDIA BETA Roadmap

Version: 6.8
Status: **PLUGIN_FIRST / R3-E1_COMPLETE / R3-E2_COMPLETE / R3-E3_STAGING_READY / R3-E4_STAGING_READY / R3-F_LOCAL_READY / R3-G_OAUTH_STAGING_READY / FREE_ONLY / ACTIONS_HOLD / PUBLICATION_HOLD**
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
R3-E3 Facebook execution                      STAGING_READY / CI+DEPLOY+ACCEPTANCE_PENDING
R3-E4 Telegram execution                      STAGING_READY / CI+DEPLOY+ACCEPTANCE_PENDING
R3-F Full 13-operation parity                 LOCAL_READY / CI_PENDING
R3-G Private operational hardening            OAUTH_STAGING_READY / DEPLOY_ACCEPTANCE_PENDING
R3-H Migration/publication readiness          HOLD
R4 Owner-approved cutover/publication         HOLD
```

**Current position:** R3-E1/E2 are closed; development has reached E3/E4 staging and prebuilt R3-F/R3-G work, but runtime acceptance is waiting on CI/deployment gates.

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
- VoiceBridge v0.6.0 health endpoint;
- OCI Cobalt v11.7.1;
- Neon Free durable backend.

Not yet accepted as runtime:

- R3-E3 Facebook staging head;
- R3-E4 Telegram staging head;
- restart-safe OAuth staging;
- full R3-F parity staging.

## Current operational hold

```text
GITHUB_ACTIONS_MINUTES=2000/2000
ACTIONS_RESET=2026-10-01
PAID_ACTIONS_USAGE=DENIED
```

Current E3/E4/OAuth/R3-F staging commits intentionally have zero workflow runs.

## Nearest tasks

### Before Actions reset

- keep the staged heads stable;
- avoid paid CI;
- no live Facebook/Telegram execution;
- prepare deployment/acceptance checklists and server-side configuration plan;
- keep all authoritative state in GitHub;
- clean non-authoritative HP-OMEN residue when elevated Windows rights are available.

### After reset or explicit override

1. run VoiceBridge CI;
2. run KRC CI;
3. deploy restart-safe OAuth signing key and E3/E4 scoped bearers;
4. deploy E3/E4 isolated Render Free sentinels;
5. run authenticated read-only preflight/lookup;
6. validate zero-side-effect ChatGPT confirmation flows;
7. obtain separate owner approval for bounded live canaries;
8. prove Neon persistence, restart/replay and duplicate-start idempotency;
9. close E3/E4;
10. run R3-F full parity acceptance;
11. finish R3-G operational hardening;
12. enter R3-H migration/publication readiness.

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

Recovery authority: `CURRENT_HANDOFF.md` + checkpoint 140.
