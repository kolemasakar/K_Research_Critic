# MEDIA BETA Decision Log

Version: 4.4
Status: ACTIVE / HISTORY_PRESERVED / R3E1_PASS / R3E2_SENTINEL_PREFLIGHT_PASS_CONFIRMATION_PENDING
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
R3_E2_INSTAGRAM=ISOLATED_SENTINEL_PASS / AUTHENTICATED_PREFLIGHT_PASS / CONFIRMATION_UI_PENDING / EXECUTION_HOLD
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

### D050 — R3-E2 Instagram read-only/free-only preflight accepted

Checkpoint 131 confirms the current Instagram route remains:

```text
Instagram -> OCI self-hosted Cobalt -> AssemblyAI universal-2 -> Neon
retrieval_credits=0
automatic_paid_fallback=false
paid provider fallback=NO
```

The relevant Instagram retrieval, URL normalization, persistence, and AssemblyAI pipeline files are unchanged from the accepted R2 head. Current OCI Cobalt runtime identity matches the accepted baseline. No Instagram job or provider work was created during this preflight.

Execution remains blocked until a dedicated R3-E2 route-scoped bearer, isolated Instagram execution surface, authenticated app-level preflight/lookup, and Instagram-specific confirmation acceptance are implemented.

### D051 — R3-E2 isolated Instagram surface and route-scoped bearer accepted

VoiceBridge accepts a dedicated R3-E2 credential only on the public Cobalt Instagram scope. The isolated R3-E2 MCP service exposes four Instagram-relevant read tools plus exactly one execution tool, `media_instagram_start`.

```text
VoiceBridge head=e640900bfddd367680badcc8e7cf349e471e2d8a
Validate #820=SUCCESS
KRC R3-E2 implementation head=7a09b857033a791a7dd6d10d7c41ed182f227e09
Tests #1678=SUCCESS
active service=krc-mcp-r3e2-instagram-sentinel-v2
active service id=srv-dan7vsijnfac73fmrtl0
active deploy=dep-dan800dii2qc73bm47k0
```

Authenticated Instagram preflight + durable lookup passed with zero provider work, zero new Instagram jobs, zero automatic paid fallback, and no start call.

### D052 — R3-E2 live execution remains gated

```text
R3E2_CONFIRMATION_CONTRACT=PASS
R3E2_CHATGPT_CONFIRMATION_UI=PENDING
R3E2_SCOPED_CREDENTIAL_ROTATION_BEFORE_LIVE=REQUIRED
media_instagram_start=HOLD
```

The first Render provisioning artifact `srv-dan7s6egekts7381bbj0` is not accepted and must not be used.

## Canonical authority

- `CURRENT_HANDOFF.md` version 17.4
- `132_R3E2_ISOLATED_SENTINEL_AUTHENTICATED_PREFLIGHT_PASS_CONFIRMATION_PENDING_2026_09_19.md`
- `131_R3E2_INSTAGRAM_READONLY_FREE_ONLY_PREFLIGHT_2026_09_19.md`
- `130_POST_R3E1_CONTROL_POINT_BEFORE_R3E2_2026_09_19.md`
- `129_R3E1_YOUTUBE_LIVE_DURABLE_REPLAY_IDEMPOTENCY_PASS_2026_09_19.md`
- `128_R3E1_RESTART_CONNECTIVITY_PASS_RECORD_REPLAY_PENDING_2026_09_19.md`
- `127_R3E1_NEON_CUTOVER_COMPLETE_DURABLE_ACCEPTANCE_PENDING_2026_09_19.md`
- `02_ROADMAP.md` version 6.0

## Hard boundary

```text
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
PAID_UPGRADE=NO
R3_E2_EXECUTION=HOLD
R3_E3_E4=HOLD
R4=HOLD
```
