# KRC MEDIA — New-chat transition: R3-E1 free-only durable-state migration gate

Date: 2026-09-17
Status: AUTHORITATIVE TRANSITION / R3-E1 AUTHORIZED BUT INFRASTRUCTURE-BLOCKED

## Accepted phase state

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3_E1=AUTHORIZED / PREPARED / BLOCKED_INFRASTRUCTURE
R3_E2=HOLD
R3_E3=HOLD
R3_E4=HOLD
R3_F_AND_LATER=HOLD
```

R3-E1 authorization is limited to the YouTube route. It does not authorize Instagram/Facebook/Telegram start operations, publication, sharing, migration, `main` mutation, PR #22 merge, or VoiceBridge PR #45 merge.

## Owner infrastructure policy

```text
PROJECT_COST_POLICY=FREE_ONLY
PAID_DATABASE_UPGRADE=DENIED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
UNEXPECTED_BILLING_RISK=DENIED
```

KRC MEDIA must remain operable without paid infrastructure or automatic paid fallbacks. Any dependency that requires paid upgrade to preserve required durable state is rejected for the production design.

## Render PostgreSQL incident

```text
name=voicebridge-krc-media-beta-db
id=dpg-da1sdn3l550s73amicvg-a
plan=free
region=frankfurt
status=suspended
suspender=billing
expired=2026-09-17T02:43:40Z
```

Render Free PostgreSQL is rejected as the durable KRC MEDIA backend. No paid upgrade is authorized. Render-only rows remain at deletion risk during the provider grace period and must not be assumed recoverable.

## Neon Free primary replacement candidate

Existing project:

```text
project=krc-media-beta-neon
project_id=plain-snow-71973546
subscription=free_v3
region=aws-eu-central-1
postgres=18
branch=production
branch_id=br-summer-union-b2qlszfv
database=krc_media_beta
storage_limit=512MiB
current_synthetic_storage≈32MB
scale_to_zero=enabled
```

Existing tables:

```text
public.krc_managed_media_jobs
public.krc_media_client_jobs
public.krc_media_stt_charges
```

Observed row counts at audit time:

```text
managed_jobs=0
client_jobs=0
stt_charges=10
```

Neon therefore contains the expected persistence schema and some charge/audit history, but is not a full backup of the suspended Render database.

## Candidate order

```text
PRIMARY_CANDIDATE=NEON_FREE
SECONDARY_CANDIDATE=SUPABASE_FREE
INFRA_CONTROLLED_FALLBACK=OCI_ALWAYS_FREE_SELF_HOSTED_POSTGRES
RENDER_FREE_POSTGRES=REJECTED_FOR_DURABLE_STATE
```

No candidate may introduce mandatory payment or automatic paid fallback.

## R3-E1 implementation state

Prepared isolated contour:

```text
service=krc-mcp-r3e1-youtube-sentinel
service_id=srv-dall4qv40ujc73ednpqg
surface=r3e1_youtube_execution
code_commit=508cd2754787c3e8b9280a7b67c1605d143781d4
tool_count=10
non_execution_tool_count=9
execution_tool_count=1
youtube_execution_enabled=true
other_execution_tools=not_enabled
provider_work_started=false
```

The contour exposes the nine accepted R3-C tools plus only `media_youtube_start`. It requires explicit Gemini Free consent and is intended to rely on ChatGPT consequential-action confirmation already proven in R3-D.

The first R3-E1 CI run exposed one regression-test defect in the read-only delegation test (`320 passed / 1 failed`). The test monkeypatched the old R3-C backend symbol while R3-E1 delegates using its current local backend binding. The regression test was corrected in commit:

```text
3529cef70c54265ae49ee6ef21e1619c3ee34924
```

This fix does not call VoiceBridge, start provider work, or change execution authorization.

## Current hard blocker

```text
BLOCKER=FREE_DURABLE_POSTGRES_NOT_YET_ACCEPTED
REAL_YOUTUBE_START=HOLD
VOICEBRIDGE_DATABASE_CUTOVER=NOT_STARTED
PROVIDER_WORK=NO
```

Do not run live `media_youtube_start` until the free durable-state gate passes.

## Next bounded work in the new chat

```text
1. audit Neon schema, constraints and indexes against VoiceBridge persistence contract/migrations
2. audit existing Neon content and required durable/idempotency fields
3. prepare server-side-only VoiceBridge DATABASE_URL cutover plan to Neon Free
4. validate fail-closed connectivity and Neon scale-to-zero behavior
5. cut over only after explicit bounded approval if a consequential secret/config mutation is required
6. validate durable create/read/status/segments/replay/idempotency across restart
7. confirm zero paid fallback and audit/charge evidence
8. only after database gate PASS resume bounded R3-E1 YouTube execution acceptance
```

## Preserved security and release boundaries

```text
VOICEBRIDGE_SECRET_SERVER_SIDE_ONLY=true
DATABASE_CREDENTIAL_SERVER_SIDE_ONLY=true
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
R4=HOLD
```

## Canonical recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 126. R3-A/B/C/D PASS; R3-E1 YouTube authorized and prepared but blocked by expired Render Free PostgreSQL. Project is FREE-ONLY. Continue from Neon Free durable-state migration preflight; do not run real media_youtube_start until the database gate passes.`

Terminal marker:

`KRC_MEDIA_CHECKPOINT_126_CHAT_TRANSITION_R3E1_FREE_ONLY_NEON_GATE_2026_09_17`
