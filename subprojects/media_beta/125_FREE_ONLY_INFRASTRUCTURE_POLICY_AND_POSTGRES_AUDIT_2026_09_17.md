# KRC MEDIA — Free-only infrastructure policy and PostgreSQL audit

Date: 2026-09-17
Status: AUTHORITATIVE POLICY / R3-E1 INFRASTRUCTURE HOLD

## Owner policy

```text
PROJECT_COST_POLICY=FREE_ONLY
PAID_DATABASE_UPGRADE=DENIED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
UNEXPECTED_BILLING_RISK=DENIED
```

KRC MEDIA must remain operable on infrastructure and provider tiers that do not require paid subscription or paid fallback. A provider/service that can only preserve required project state by upgrading to a paid plan is not acceptable as the durable production dependency.

## Render PostgreSQL incident

Render database:

```text
name=voicebridge-krc-media-beta-db
id=dpg-da1sdn3l550s73amicvg-a
region=frankfurt
plan=free
created=2026-08-18T02:43:40Z
expired=2026-09-17T02:43:40Z
status=suspended
suspender=billing
```

Render Free PostgreSQL is time-limited and expires after 30 days. After expiry there is a 14-day grace period to upgrade; otherwise the database and data are deleted. Since paid upgrade is denied by owner policy, Render Free PostgreSQL is rejected as a durable KRC MEDIA database backend.

## Effect on R3-E1

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3_E1=BLOCKED_INFRASTRUCTURE
BLOCKER=RENDER_POSTGRES_SUSPENDED
REAL_YOUTUBE_START=HOLD
```

No real `media_youtube_start` acceptance call may be executed until a free durable PostgreSQL replacement is bound and validated for durable job state, replay/idempotency, status, segments and charge/audit records.

## Existing Neon candidate audit

An existing Neon project is already provisioned:

```text
project=krc-media-beta-neon
project_id=plain-snow-71973546
region=aws-eu-central-1
subscription=free_v3
postgres=18
branch=production
branch_id=br-summer-union-b2qlszfv
database=krc_media_beta
storage_limit=512MiB
current_synthetic_storage≈32MB
history_retention=6h
scale_to_zero=enabled
```

Existing tables:

```text
public.krc_managed_media_jobs
public.krc_media_client_jobs
public.krc_media_stt_charges
```

Observed row counts on 2026-09-17:

```text
krc_managed_media_jobs=0
krc_media_client_jobs=0
krc_media_stt_charges=10
```

This confirms that Neon already contains the expected VoiceBridge schema and some audit/charge history, but it is not a complete copy of the suspended Render durable job state.

## Free replacement candidates

### Candidate A — Neon Free

Current public Neon Free plan is $0 with no time limit/no credit card requirement, 0.5 GB storage per project, free compute allowance and automatic scale-to-zero. The existing KRC Neon project is already within these limits and is the primary migration candidate.

Required validation before acceptance:

- obtain/use server-side Neon connection string only;
- bind VoiceBridge to Neon without exposing credentials;
- run schema parity check;
- verify durable create/read/status/segments behavior;
- verify replay/idempotency across service restart;
- verify free-plan compute/storage budget under expected MEDIA usage;
- add free-tier exhaustion fail-closed handling;
- document export/backup procedure independent of provider retention.

### Candidate B — Supabase Free

Supabase Free currently includes a Postgres database with 500 MB database size and pauses projects after one week of inactivity. It is technically compatible but introduces inactivity-pause behavior and a separate platform stack. Keep as secondary managed fallback candidate.

### Candidate C — self-hosted PostgreSQL on OCI Always Free Compute

OCI Always Free compute/block volume resources can host standard PostgreSQL indefinitely within Always Free limits. This provides maximum control and avoids managed free-database expiration, but adds operational responsibility for PostgreSQL patching, backup, monitoring and recovery. Keep as infrastructure-controlled fallback candidate.

Oracle Autonomous Always Free is not PostgreSQL and therefore is not a drop-in replacement for the current VoiceBridge PostgreSQL persistence contract.

## Decision

```text
PRIMARY_CANDIDATE=NEON_FREE
SECONDARY_CANDIDATE=SUPABASE_FREE
INFRA_CONTROLLED_FALLBACK=OCI_ALWAYS_FREE_SELF_HOSTED_POSTGRES
RENDER_FREE_POSTGRES=REJECTED_FOR_DURABLE_STATE
PAID_UPGRADE=DENIED
```

## Data preservation risk

The suspended Render database remains subject to deletion after the provider grace period. Because owner policy prohibits paid upgrade, recovery of any Render-only rows may not be possible through the normal managed access path. Do not assume those rows are preserved elsewhere. The current Neon database has the expected schema but `managed_jobs=0` and therefore must not be treated as a full Render backup.

## Next bounded work

```text
1. audit Neon schema against VoiceBridge repository migrations
2. audit Neon table content and constraints without exposing secrets
3. prepare VoiceBridge DATABASE_URL cutover plan to Neon Free
4. perform read-only/preflight connectivity validation
5. perform restart-resilient durable-state acceptance
6. resume R3-E1 only after database gate PASS
```

No paid resource creation, no Render database upgrade, no public GPT mutation, no Plugin publication/share, no PR merge, and no real provider-start call is authorized by this checkpoint.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_125_FREE_ONLY_POSTGRES_AUDIT_R3E1_INFRA_HOLD_2026_09_17`
