# MEDIA BETA Decision Log

Version: 4.6
Status: ACTIVE / HISTORY_PRESERVED / R3E2_COMPLETE / E3_E4_OAUTH_R3F_STAGING_READY / ACTIONS_HOLD
Updated: 2026-09-19

Historical decisions remain preserved in Git history and numbered checkpoints. Current active decisions are summarized below.

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

### D038 — Staged execution remains route-bounded

```text
R3_E1_YOUTUBE=PASS / COMPLETE
R3_E2_INSTAGRAM=PASS / COMPLETE
R3_E3_FACEBOOK=STAGING_READY / DEPLOY_PENDING
R3_E4_TELEGRAM=STAGING_READY / DEPLOY_PENDING
```

### D039 — Infrastructure/provider policy is FREE_ONLY

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

### D040 — Render PostgreSQL rejected; Render Free Web remains accepted

Render Free Web Services and `.onrender.com` endpoints remain valid. Render PostgreSQL is not accepted as durable project state.

### D041 — Neon Free is primary durable backend

```text
project=krc-media-beta-neon
project_id=plain-snow-71973546
database=krc_media_beta
```

### D047 — R3-E1 durable replay/idempotency accepted

R3-E1 is PASS / COMPLETE.

### D053 — R3-E2 accepted as PASS / COMPLETE

Owner acceptance establishes:

```text
confirmation_ui=PASS
cancel_path=PASS
approve_path=PASS
live_canary=PASS
durable_neon=PASS
restart_replay=PASS
status_segments_after_restart=PASS
duplicate_start_idempotency=PASS
duplicate_provider_work=NO
new_provider_charge=0
error_scan=PASS
```

### D054 — HP-OMEN local disk is not authoritative project storage

```text
HP_OMEN_LOCAL_DISK_AS_PROJECT_STORAGE=DENIED
AUTHORITATIVE_PROJECT_STATE=GITHUB_REPOSITORIES
LOCAL_WORKTREE_USE=TRANSIENT_ONLY
```

After verified repository transfer, temporary local staging trees and patch artifacts must be removed.

### D055 — GitHub Actions paid overage is denied until reset

```text
GITHUB_ACTIONS_MINUTES=2000/2000
ACTIONS_RESET=2026-10-01
PAID_ACTIONS_USAGE=DENIED
```

New staging commits may use CI-skip semantics. Full CI is deferred until reset or separate owner decision.

### D056 — R3-E3 / R3-E4 / OAuth / R3-F staging accepted for repository storage

Prepared implementation includes:

- R3-E3 Facebook scoped bearer + isolated execution surface;
- R3-E4 Telegram scoped bearer + isolated execution surface;
- zero-side-effect confirmation probes;
- cold-start warmup with no automatic consequential POST retry;
- durable lookup/replay isolation;
- restart-safe OAuth/DCR via optional signing key;
- R3-F 13-operation parity regression package.

Local validation prior to repository transfer:

```text
KRC combined=65/65 PASS
VoiceBridge relevant regression=23/23 PASS
Facebook/Telegram scoped targeted=11/11 PASS
```

This staging decision does not authorize live Facebook or Telegram provider work.

## Canonical authority

- `CURRENT_HANDOFF.md` version 18.1
- checkpoint 139
- `02_ROADMAP.md` version 6.7
- `00_INDEX.md` version 8.6

## Hard boundary

```text
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
PAID_UPGRADE=NO
LIVE_FACEBOOK_START=NO
LIVE_TELEGRAM_START=NO
R4=HOLD
```
