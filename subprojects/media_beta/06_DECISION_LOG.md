# MEDIA BETA Decision Log

Version: 4.2
Status: ACTIVE / HISTORY_PRESERVED / R3E1_PASS
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

### D038 — Staged execution remains route-bounded

```text
R3_E1_YOUTUBE=PASS
R3_E2_INSTAGRAM=HOLD
R3_E3_FACEBOOK=HOLD
R3_E4_TELEGRAM=HOLD
```

### D039 — Project infrastructure and provider policy is FREE-ONLY

```text
PROJECT_COST_POLICY=FREE_ONLY
PAID_DATABASE_UPGRADE=DENIED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
UNEXPECTED_BILLING_RISK=DENIED
```

### D040 — Render Free PostgreSQL rejected for durable KRC MEDIA state

The expired billing-suspended Render database is not an accepted durable dependency. Paid upgrade remains prohibited.

### D041 — Neon Free is the primary durable backend

```text
PRIMARY_DURABLE_BACKEND=NEON_FREE
project=krc-media-beta-neon
project_id=plain-snow-71973546
database=krc_media_beta
```

### D042 — Neon schema and runtime preflight required before execution

Schema, constraints, indexes, idempotency fields, scale-to-zero identity and free-plan state were verified before live execution.

### D043 — Neon DATABASE_URL cutover completed

```text
VOICEBRIDGE_DATABASE_CUTOVER=PASS
secret_exposed=false
paid_upgrade=false
```

### D044 — App-level durable lookup and restart connectivity required

A health endpoint alone was insufficient. R3-E1 had to exercise the VoiceBridge durable store before provider execution.

### D045 — R3-E1 uses a dedicated YouTube-scoped server-side bearer

A separate `KRC_MEDIA_R3E1_ACTION_TOKEN` is accepted only by the VoiceBridge YouTube Gemini handler. The general MEDIA action token and R3-C surface are not widened by R3-E1.

### D046 — Owner-approved Gemini Free Tier execution completed

After explicit owner acknowledgement of Gemini Developer API Free Tier data-use terms, one bounded YouTube execution completed:

```text
job_id=KRCM_3f4e62c1-2518-4815-839b-ece80935d794
status=COMPLETED
provider=gemini
provider_mode=youtube_gemini_direct
retrieval_credits_charged=0
stt_seconds_charged=0
credits_charged=0
```

### D047 — R3-E1 durable replay and idempotency accepted

The completed job and segments were read after VoiceBridge + R3-E1 restarts without provider replay. A duplicate start returned the same job with `reused=true` and `provider_work_started=false`.

Therefore:

```text
R3_E1=PASS / COMPLETE
NEON_DURABLE_REPLAY=PASS
DUPLICATE_START_IDEMPOTENCY=PASS
PAID_FALLBACK=NO
```

### D048 — STT charge table is a bounded quota ledger

The current persistence contract deletes `krc_media_stt_charges` rows older than two days. It must not be described as a long-term immutable audit trail. Long-term acceptance evidence is maintained in checkpoints/Git history.

### D049 — Acceptance-only startup probes disabled after test

All temporary execution/replay startup environment switches were disabled after evidence capture. Final R3-E1 runtime is healthy with no automatic acceptance execution.

## Canonical authority

- `CURRENT_HANDOFF.md` version 17.2
- `129_R3E1_YOUTUBE_LIVE_DURABLE_REPLAY_IDEMPOTENCY_PASS_2026_09_19.md`
- `128_R3E1_RESTART_CONNECTIVITY_PASS_RECORD_REPLAY_PENDING_2026_09_19.md`
- `127_R3E1_NEON_CUTOVER_COMPLETE_DURABLE_ACCEPTANCE_PENDING_2026_09_19.md`
- `02_ROADMAP.md` version 5.8

## Hard boundary

```text
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
PAID_UPGRADE=NO
R3_E2_E3_E4=HOLD
R4=HOLD
```
