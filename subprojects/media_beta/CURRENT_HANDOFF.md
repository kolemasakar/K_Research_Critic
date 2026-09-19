# KRC MEDIA — CURRENT HANDOFF

Version: 18.2
Status: **ACTIVE_HANDOFF / R3-A_PASS / R3-B_PASS / R3-C_PASS / R3-D_PASS / R3-E1_PASS_COMPLETE / R3-E2_PASS_COMPLETE / R3-E3_STAGING_READY / R3-E4_STAGING_READY / R3-F_LOCAL_READY / R3-G_OAUTH_STAGING_READY / FREE_ONLY / ACTIONS_HOLD / PUBLICATION_HOLD**
Date: 2026-09-19

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 140. R3-E1 і R3-E2 PASS / COMPLETE. R3-E3 Facebook і R3-E4 Telegram code staging знаходяться в integration branches, але CI/deploy/runtime acceptance для них ще не виконані. Restart-safe OAuth та R3-F parity також staged, не runtime-accepted. PROJECT_COST_POLICY=FREE_ONLY. GitHub Actions 2000/2000, reset 2026-10-01, paid Actions denied. HP-OMEN не є authoritative storage.`

## Canonical current authority

1. `CURRENT_HANDOFF.md` — v18.2.
2. `140_PROJECT_AUDIT_DOCS_RUNTIME_SYNC_2026_09_19.md` — current project/runtime audit.
3. `139_R3E2_COMPLETE_R3E3_R3E4_OAUTH_R3F_STAGING_READY_ACTIONS_HOLD_2026_09_19.md` — staging checkpoint.
4. `138_R3E2_RESTART_REPLAY_STATUS_SEGMENTS_PASS_2026_09_19.md`.
5. `137_R3E2_INSTAGRAM_LIVE_CANARY_DURABLE_FREE_ONLY_PASS_2026_09_19.md`.
6. `134_R3E2_CHATGPT_CONFIRMATION_UI_PASS_ZERO_SIDE_EFFECT_2026_09_19.md`.
7. `133_FREE_ONLY_INFRASTRUCTURE_POLICY_RENDER_WEB_ALLOWED_POSTGRES_REJECTED_2026_09_19.md`.
8. `129_R3E1_YOUTUBE_LIVE_DURABLE_REPLAY_IDEMPOTENCY_PASS_2026_09_19.md`.
9. `02_ROADMAP.md`.
10. current PR #22 / PR #45 heads and current runtime evidence.

## Repository / PR authority

```text
KRC repository=kolemasakar/K_Research_Critic
branch=agent/krc-public-media-r3-integration
PR=22
state=OPEN / DRAFT / UNMERGED
audited_staging_head=be142a547506b4f724d1a7bfcd9d8c9244f97726

VoiceBridge repository=kolemasakar/VoiceBridge
branch=agent/krc-media-gemini-migration
PR=45
state=OPEN / DRAFT / UNMERGED
audited_staging_head=8b5d9fe8590e7b1be5cd94a20724b9826c40f5c1
```

The audit checkpoint and documentation-sync commits follow these staging heads and use `[skip ci]`.

## Phase state

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3_E1=PASS / COMPLETE
R3_E2=PASS / COMPLETE
R3_E3=STAGING_READY / CI+DEPLOY+ACCEPTANCE_PENDING
R3_E4=STAGING_READY / CI+DEPLOY+ACCEPTANCE_PENDING
R3_F=LOCAL_PARITY_READY / CI_PENDING
R3_G_OAUTH=STAGING_READY / DEPLOY_ACCEPTANCE_PENDING
R3_H=HOLD
R4=HOLD
MEDIA_OPERATION_COUNT=13
NON_EXECUTION_COUNT=9
EXECUTION_COUNT=4
```

## Current runtime audit

```text
R3E1_HEALTH=PASS
R3E1_SURFACE=r3e1_youtube_execution
R3E1_TOOL_COUNT=10
R3E1_PROVIDER_WORK_STARTED=false

R3E2_HEALTH=PASS
R3E2_SURFACE=r3e2_instagram_execution
R3E2_TOOL_COUNT=5
R3E2_CONFIRMATION_PROBE_ONLY=false
R3E2_PROVIDER_WORK_STARTED=false

VOICEBRIDGE_HEALTH=HTTP_200 / status=ok / version=0.6.0

COBALT_HTTP_ROOT=200
COBALT_VERSION=11.7.1
COBALT_FACEBOOK_SERVICE=present
COBALT_INSTAGRAM_SERVICE=present
```

The deployed runtime remains the accepted E1/E2 baseline. The new E3/E4/OAuth staging implementation is not yet runtime-accepted.

## Durable Neon state

```text
provider=Neon Free
project=krc-media-beta-neon
project_id=plain-snow-71973546
branch=production
branch_id=br-summer-union-b2qlszfv
database=krc_media_beta

managed_jobs=1
instagram_jobs=1
facebook_jobs=0
telegram_jobs=0
stt_charge_rows=1
stt_seconds=43
```

Current durable job remains the accepted Instagram canary:
`KRCM_04e6d847-449c-4d0f-82c7-b494871d9322`, status `COMPLETED`.

## R3-E2 accepted closure

```text
CHATGPT_CONFIRMATION_UI=PASS
CANCEL_PATH=PASS
APPROVE_PATH=PASS
LIVE_CANARY=PASS
DURABLE_NEON=PASS
RESTART_REPLAY=PASS
STATUS_SEGMENTS_AFTER_RESTART=PASS
DUPLICATE_START_IDEMPOTENCY=PASS
DUPLICATE_PROVIDER_WORK=NO
NEW_PROVIDER_CHARGE=0
ERROR_SCAN=PASS
R3_E2=PASS / COMPLETE
```

## R3-E3 / R3-E4 staging

Repository implementation now includes:

- isolated Facebook and Telegram execution surfaces;
- exactly one route-specific execution tool on each surface;
- dedicated VoiceBridge scoped bearer support;
- route-scoped durable lookup/status/segments;
- zero-side-effect confirmation probes;
- cold-start health warmup;
- no automatic retry of consequential POST;
- restart/replay probes.

No Facebook or Telegram live job exists in Neon. No live E3/E4 acceptance has occurred.

## OAuth / R3-F staging

Restart-safe OAuth/DCR is implemented behind optional `KRC_MCP_OAUTH_SIGNING_KEY`, but is not yet deployed/accepted.

R3-F local contract verifies 13 total operations: 9 read and 4 execution, with no execution leakage into R3-C and exactly one own start tool per E1/E2/E3/E4 surface.

Pre-transfer local validation:

```text
KRC_COMBINED=65/65 PASS
VOICEBRIDGE_RELEVANT_REGRESSION=23/23 PASS
FACEBOOK_TELEGRAM_SCOPED_TARGETED=11/11 PASS
```

## GitHub Actions constraint

```text
GITHUB_ACTIONS_MINUTES=2000/2000
ACTIONS_RESET=2026-10-01
PAID_ACTIONS_USAGE=DENIED
AUDITED_KRC_STAGING_HEAD_WORKFLOW_RUNS=0
AUDITED_VOICEBRIDGE_STAGING_HEAD_WORKFLOW_RUNS=0
```

Full CI for E3/E4/OAuth/R3-F remains pending.

## Cost / infrastructure policy

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

## Storage rule

```text
HP_OMEN_LOCAL_DISK_AS_PROJECT_STORAGE=DENIED
AUTHORITATIVE_PROJECT_STATE=GITHUB_REPOSITORIES
LOCAL_WORKTREE_USE=TRANSIENT_ONLY
```

The former HP-OMEN staging directory is not authoritative. Any access-denied residual copies are housekeeping residue only and must not be used as source.

## Final goal

Production-grade private MEDIA execution for KRC with all 13 operations, isolated confirmation-gated execution for YouTube/Instagram/Facebook/Telegram, server-side route-scoped credentials, restart-safe OAuth, Neon durable state, restart/idempotency guarantees, fail-closed FREE_ONLY provider policy, and migration/publication readiness without weakening the public KRC core.

## Next gate

After Actions reset or separate owner override:

1. VoiceBridge CI.
2. KRC CI.
3. Deploy restart-safe OAuth signing key and E3/E4 route-scoped bearers.
4. Deploy isolated E3/E4 Render Free sentinels.
5. Authenticated read-only preflight/lookup.
6. Zero-side-effect ChatGPT Cancel/Allow-once acceptance.
7. Separate owner approval for one Facebook and one Telegram live canary.
8. Neon durable/restart/idempotency acceptance.
9. Close E3/E4.
10. Run full R3-F and R3-G acceptance.
11. Proceed to R3-H only after all prior gates pass.

## Hard release boundary

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

Terminal marker:

`KRC_MEDIA_CURRENT_HANDOFF_V18_2_AUDITED_SYNC_E3_E4_STAGING_ACTIONS_HOLD_2026_09_19`
