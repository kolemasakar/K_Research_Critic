# MEDIA BETA Decision Log

Version: 4.0
Status: ACTIVE / HISTORY_PRESERVED / CURRENT_R3E1_FREE_ONLY_GATE
Updated: 2026-09-17

The full historical decision log remains preserved in Git history and numbered checkpoints. Current active decisions are summarized here and detailed in the canonical handoff, roadmap, and checkpoints.

## Active decisions

### D036 — Plugin-first authenticated Remote MCP path accepted

```text
PLUGIN_FIRST_STRATEGY=ACCEPTED
PUBLIC_KRC_CUSTOM_GPT=UNCHANGED
```

R3-A through R3-D were completed on private authenticated Remote MCP surfaces before any real MEDIA start operation was exposed.

### D037 — R3-A/B/C/D accepted

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
```

Accepted evidence includes contract freeze, OAuth + PKCE authenticated MCP, nine-tool read-only VoiceBridge binding, and owner-account consequential-action confirmation with both approve-once and deny/cancel paths.

### D038 — R3-E1 YouTube authorization is route-bounded

```text
R3_E1=AUTHORIZED
R3_E2=HOLD
R3_E3=HOLD
R3_E4=HOLD
```

R3-E1 authorization applies only to YouTube. It does not authorize Instagram, Facebook, Telegram, publication, sharing, migration, `main` mutation, PR #22 merge, or VoiceBridge PR #45 merge.

### D039 — Project infrastructure and provider cost policy is FREE-ONLY

Owner decision:

```text
PROJECT_COST_POLICY=FREE_ONLY
PAID_DATABASE_UPGRADE=DENIED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
UNEXPECTED_BILLING_RISK=DENIED
```

Any required production dependency that can only preserve mandatory state through paid upgrade is rejected.

### D040 — Render Free PostgreSQL rejected for durable KRC MEDIA state

`voicebridge-krc-media-beta-db` expired and became billing-suspended on 2026-09-17. Paid upgrade is prohibited.

```text
RENDER_FREE_POSTGRES=REJECTED_FOR_DURABLE_STATE
R3_E1=BLOCKED_INFRASTRUCTURE
REAL_YOUTUBE_START=HOLD
```

No live YouTube execution acceptance may run while the durable-state backend is unresolved.

### D041 — Neon Free selected as primary replacement candidate

Existing Neon project `krc-media-beta-neon` is already provisioned on `free_v3`, PostgreSQL 18, with database `krc_media_beta` and the expected VoiceBridge persistence tables.

```text
PRIMARY_CANDIDATE=NEON_FREE
SECONDARY_CANDIDATE=SUPABASE_FREE
INFRA_CONTROLLED_FALLBACK=OCI_ALWAYS_FREE_SELF_HOSTED_POSTGRES
```

Audit-time Neon row counts:

```text
managed_jobs=0
client_jobs=0
stt_charges=10
```

Neon is therefore a schema-bearing primary candidate, not a proven full backup of the suspended Render database.

### D042 — Next continuation point is Neon durable-state migration preflight

```text
NEXT_GATE=NEON_FREE_DURABLE_STATE_MIGRATION_PREFLIGHT
VOICEBRIDGE_DATABASE_CUTOVER=NOT_STARTED
REAL_MEDIA_START=NO
```

Required sequence: schema/constraint/index parity audit, durable/idempotency field audit, server-side DATABASE_URL cutover plan, fail-closed/scale-to-zero validation, bounded cutover if explicitly approved where consequential, restart-resilient persistence acceptance, zero-paid-fallback verification, then resume R3-E1 YouTube execution acceptance.

## Canonical authority

- `CURRENT_HANDOFF.md` version 16.0
- `126_NEW_CHAT_TRANSITION_R3E1_FREE_ONLY_NEON_MIGRATION_GATE_2026_09_17.md`
- `125_FREE_ONLY_INFRASTRUCTURE_POLICY_AND_POSTGRES_AUDIT_2026_09_17.md`
- `02_ROADMAP.md` version 5.6

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
