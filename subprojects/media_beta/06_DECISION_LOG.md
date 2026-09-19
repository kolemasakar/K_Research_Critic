# MEDIA BETA Decision Log

Version: 4.7
Status: ACTIVE / AUDITED / HISTORY_PRESERVED / R3E2_COMPLETE / E3_E4_OAUTH_R3F_STAGING_READY / ACTIONS_HOLD
Updated: 2026-09-19

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

### D038 — Execution remains route-bounded

```text
R3_E1_YOUTUBE=PASS / COMPLETE
R3_E2_INSTAGRAM=PASS / COMPLETE
R3_E3_FACEBOOK=STAGING_READY / RUNTIME_PENDING
R3_E4_TELEGRAM=STAGING_READY / RUNTIME_PENDING
```

### D039 — Project policy remains FREE_ONLY

```text
PROJECT_COST_POLICY=FREE_ONLY
RENDER_FREE_WEB_SERVICES=ACCEPTED
RENDER_POSTGRES=REJECTED_FOR_DURABLE_STATE
NEON_FREE_POSTGRES=PRIMARY_DURABLE_DATABASE
OCI_ALWAYS_FREE=ACCEPTED
SELF_HOSTED_COBALT_ON_OCI=ACCEPTED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
PAID_ACTIONS_USAGE=DENIED
```

### D053 — R3-E2 accepted as PASS / COMPLETE

Confirmation UI, live canary, Neon durability, restart/replay and duplicate-start idempotency are accepted. Duplicate provider work is NO and new provider charge is 0.

### D054 — GitHub is authoritative storage

```text
HP_OMEN_LOCAL_DISK_AS_PROJECT_STORAGE=DENIED
AUTHORITATIVE_PROJECT_STATE=GITHUB_REPOSITORIES
LOCAL_WORKTREE_USE=TRANSIENT_ONLY
```

### D055 — GitHub Actions paid overage denied

```text
GITHUB_ACTIONS_MINUTES=2000/2000
ACTIONS_RESET=2026-10-01
PAID_ACTIONS_USAGE=DENIED
```

### D056 — E3/E4/OAuth/R3-F staging accepted into repositories

The integration branches contain Facebook and Telegram isolated execution staging, restart-safe OAuth/DCR staging and R3-F parity tests. This does not mean runtime acceptance.

### D057 — 2026-09-19 project/runtime audit boundary

Audit confirms:

```text
R3E1_RUNTIME=HEALTHY
R3E2_RUNTIME=HEALTHY
VOICEBRIDGE_RUNTIME=HEALTHY
COBALT_ENDPOINT=HEALTHY
NEON_DURABLE_STATE=CONSISTENT

R3E3_CODE=IN_REPOSITORY
R3E3_RUNTIME=NOT_ACCEPTED
R3E4_CODE=IN_REPOSITORY
R3E4_RUNTIME=NOT_ACCEPTED
OAUTH_RESTART_SAFE_CODE=IN_REPOSITORY
OAUTH_RESTART_SAFE_RUNTIME=NOT_ACCEPTED
R3F_LOCAL_PARITY=READY
R3F_CI=NOT_RUN
```

This distinction is authoritative: `STAGING_READY != DEPLOYED != PASS`.

### D058 — Final project goal

The target is a production-grade private MEDIA surface with all 13 operations, four isolated confirmation-gated execution paths, route-scoped server-side credentials, restart-safe OAuth, Neon durability, restart/idempotency guarantees, FREE_ONLY fail-closed behavior, and eventual migration/publication readiness without weakening the public KRC core.

## Canonical authority

- `CURRENT_HANDOFF.md` v18.2
- checkpoint 140
- `02_ROADMAP.md` v6.8
- `00_INDEX.md` v8.7

## Hard boundary

```text
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
LIVE_FACEBOOK_START=NO
LIVE_TELEGRAM_START=NO
R4=HOLD
```
