# MEDIA BETA Documentation Index

Canonical documentation index for K-Research & Critic MEDIA BETA / Plugin migration work.

Version: 8.1
Status: **ACTIVE / PLUGIN_FIRST / R3-A_PASS / R3-B_PASS / R3-C_PASS / R3-D_PASS / R3-E1_NEON_CUTOVER_COMPLETE_DURABLE_ACCEPTANCE_PENDING / FREE_ONLY / PUBLICATION_HOLD**
Updated: 2026-09-19

## Product boundary

```text
public KRC Custom GPT: published / unchanged / protected
MEDIA migration candidate: private Remote Custom MCP / Plugin surface
backend authority: VoiceBridge MEDIA API
canonical MEDIA parity target: 13 operations
project cost policy: FREE_ONLY
```

## Canonical current reading order

1. `CURRENT_HANDOFF.md` — v17.0; current recovery authority.
2. `127_R3E1_NEON_CUTOVER_COMPLETE_DURABLE_ACCEPTANCE_PENDING_2026_09_19.md` — current cutover checkpoint.
3. `126_CHAT_TRANSITION_R3E1_FREE_ONLY_NEON_MIGRATION_GATE_2026_09_17.md` — historical transition checkpoint.
4. `125_FREE_ONLY_INFRASTRUCTURE_POLICY_AND_POSTGRES_AUDIT_2026_09_17.md` — free-only policy and Render PostgreSQL incident.
5. `02_ROADMAP.md` — v5.7.
6. `124_R3D_CONSEQUENTIAL_ACTION_CONFIRMATION_PASS_2026_09_17.md`.
7. `121_R3C_NINE_TOOL_READONLY_VOICEBRIDGE_BINDING_PASS_2026_09_16.md`.
8. `117_R3B_AUTHENTICATED_REMOTE_MCP_HARDENING_PASS_2026_09_16.md`.
9. `113_R3A_CONTRACT_FREEZE_SECURE_ADAPTER_BASELINE_PASS_2026_09_16.md`.
10. current PR #22 head/CI and current Render/Neon non-secret evidence.

Older checkpoints remain historical evidence and do not override the current handoff.

## Current repository / PR

```text
repository=kolemasakar/K_Research_Critic
branch=agent/krc-public-media-r3-integration
PR=#22
base=main
state=OPEN / DRAFT / UNMERGED
```

## Accepted R3 state

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3_E1=AUTHORIZED / PREPARED / NEON_CUTOVER_COMPLETE / DURABLE_RUNTIME_ACCEPTANCE_PENDING
R3_E2=HOLD
R3_E3=HOLD
R3_E4=HOLD
```

## Current durable-state authority

```text
RENDER_FREE_POSTGRES=REJECTED_FOR_DURABLE_STATE
PAID_UPGRADE=DENIED
PRIMARY_DURABLE_TARGET=NEON_FREE
project=krc-media-beta-neon
project_id=plain-snow-71973546
database=krc_media_beta
VOICEBRIDGE_DATABASE_CUTOVER=COMPLETE
cutover_deploy=dep-dan5uf0ae00c73dke480
cutover_status=LIVE
health=PASS
```

Neon schema parity is PASS. Current counts are `managed_jobs=0`, `client_jobs=0`, `stt_charges=10`, total recorded STT seconds `285`.

## Active next gate

The next bounded work is **post-cutover application-level durable runtime acceptance**, not real MEDIA provider execution:

```text
authenticated no-provider durable lookup/status
-> app-level Neon read proof
-> bounded durable create/read/status/segments acceptance
-> restart/cold-wake replay/idempotency
-> zero-paid-fallback and charge/audit validation
-> close database gate
-> resume R3-E1 YouTube live acceptance only after PASS
```

R3-C is historical accepted evidence and is not part of this recovery path unless separately requested.

## Preserved release boundary

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

## Recovery command

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 127. Neon DATABASE_URL cutover COMPLETE; continue with authenticated no-provider durable runtime acceptance; real media_youtube_start remains HOLD.`
