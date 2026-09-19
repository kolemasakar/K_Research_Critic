# MEDIA BETA Decision Log

Version: 4.1
Status: ACTIVE / HISTORY_PRESERVED / CURRENT_R3E1_NEON_CUTOVER_GATE
Updated: 2026-09-19

The full historical decision log remains preserved in Git history and numbered checkpoints. Current active decisions are summarized here and detailed in the canonical handoff, roadmap, and checkpoints.

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

### D038 — R3-E1 YouTube authorization is route-bounded

```text
R3_E1=AUTHORIZED
R3_E2=HOLD
R3_E3=HOLD
R3_E4=HOLD
```

### D039 — Project infrastructure and provider cost policy is FREE-ONLY

```text
PROJECT_COST_POLICY=FREE_ONLY
PAID_DATABASE_UPGRADE=DENIED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
UNEXPECTED_BILLING_RISK=DENIED
```

### D040 — Render Free PostgreSQL rejected for durable KRC MEDIA state

`voicebridge-krc-media-beta-db` expired and became billing-suspended on 2026-09-17. Paid upgrade remains prohibited.

### D041 — Neon Free selected as primary replacement

```text
PRIMARY_CANDIDATE=NEON_FREE
project=krc-media-beta-neon
project_id=plain-snow-71973546
database=krc_media_beta
SECONDARY_CANDIDATE=SUPABASE_FREE
INFRA_CONTROLLED_FALLBACK=OCI_ALWAYS_FREE_SELF_HOSTED_POSTGRES
```

### D042 — Neon migration preflight required before cutover

The preflight audited schema, constraints, indexes, durable/idempotency fields, scale-to-zero identity and free-plan status before any configuration mutation.

### D043 — Owner-approved Neon DATABASE_URL cutover completed

On 2026-09-19 the owner explicitly approved the bounded cutover.

```text
VOICEBRIDGE_DATABASE_CUTOVER=COMPLETE
target=Neon Free / krc_media_beta
Render service=voicebridge-krc-media-beta-kolemasakar
deploy=dep-dan5uf0ae00c73dke480
commit=3e8cb29b3815e1bf98f143682644899b801826e0
deploy_status=LIVE
health=HTTP 200 / status=ok
secret_exposed=false
paid_upgrade=false
provider_work=false
```

Only `KRC_MEDIA_DATABASE_URL` was changed. The database credential remained server-side.

### D044 — Database gate remains open until app-level durable runtime acceptance

Health and deploy success do not exercise the lazy PostgreSQL store. Therefore:

```text
NEON_SCHEMA_PARITY=PASS
VOICEBRIDGE_DATABASE_CUTOVER=COMPLETE
APP_LEVEL_DURABLE_LOOKUP_AFTER_CUTOVER=PENDING
APP_LEVEL_DURABLE_CREATE_READ_RESTART_ACCEPTANCE=PENDING
REAL_YOUTUBE_START=HOLD
```

Required sequence: authenticated no-provider durable lookup/status, app-level Neon read proof, bounded durable create/read/status/segments acceptance, restart/cold-wake replay/idempotency, zero-paid-fallback and audit/charge validation, then database-gate closure.

R3-C is not required for this recovery path and remains untouched unless separately requested.

## Canonical authority

- `CURRENT_HANDOFF.md` version 17.0
- `127_R3E1_NEON_CUTOVER_COMPLETE_DURABLE_ACCEPTANCE_PENDING_2026_09_19.md`
- `126_CHAT_TRANSITION_R3E1_FREE_ONLY_NEON_MIGRATION_GATE_2026_09_17.md` — historical
- `125_FREE_ONLY_INFRASTRUCTURE_POLICY_AND_POSTGRES_AUDIT_2026_09_17.md`
- `02_ROADMAP.md` version 5.7

## Hard boundary

```text
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
PAID_UPGRADE=NO
R4=HOLD
```
