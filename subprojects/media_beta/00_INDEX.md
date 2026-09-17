# MEDIA BETA Documentation Index

Canonical documentation index for K-Research & Critic MEDIA BETA / Plugin migration work.

Version: 8.0
Status: **ACTIVE / PLUGIN_FIRST / R3-A_PASS / R3-B_PASS / R3-C_PASS / R3-D_PASS / R3-E1_BLOCKED_INFRASTRUCTURE / FREE_ONLY / PUBLICATION_HOLD**
Updated: 2026-09-17

## Product boundary

```text
public KRC Custom GPT: published / unchanged / protected
MEDIA migration candidate: private Remote Custom MCP / Plugin surface
backend authority: VoiceBridge MEDIA API
canonical MEDIA parity target: 13 operations
project cost policy: FREE_ONLY
```

Critical invariants:

```text
MEDIA unavailable/fails -> MEDIA fails closed
Core KRC               -> remains usable
paid mandatory infra   -> denied
paid provider fallback -> denied
```

## Canonical current reading order

1. `CURRENT_HANDOFF.md` — v16.0; current recovery authority.
2. `126_NEW_CHAT_TRANSITION_R3E1_FREE_ONLY_NEON_MIGRATION_GATE_2026_09_17.md` — new-chat transition checkpoint.
3. `125_FREE_ONLY_INFRASTRUCTURE_POLICY_AND_POSTGRES_AUDIT_2026_09_17.md` — free-only policy and PostgreSQL incident audit.
4. `02_ROADMAP.md` — v5.6; active gate sequence.
5. `124_R3D_CONSEQUENTIAL_ACTION_CONFIRMATION_PASS_2026_09_17.md` — R3-D PASS.
6. `121_R3C_NINE_TOOL_READONLY_VOICEBRIDGE_BINDING_PASS_2026_09_16.md` — R3-C PASS.
7. `117_R3B_AUTHENTICATED_REMOTE_MCP_HARDENING_PASS_2026_09_16.md` — R3-B PASS.
8. `113_R3A_CONTRACT_FREEZE_SECURE_ADAPTER_BASELINE_PASS_2026_09_16.md` — R3-A PASS.
9. current PR #22 head/CI and current Render/Neon non-secret evidence.

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
R3_E1=AUTHORIZED / PREPARED / BLOCKED_INFRASTRUCTURE
R3_E2=HOLD
R3_E3=HOLD
R3_E4=HOLD
```

## R3-C accepted authenticated read-only surface

```text
service=krc-mcp-auth-sentinel
surface=r3c_readonly
DISCOVERED_TOOL_COUNT=9
EXECUTION_TOOL_COUNT=0
VOICEBRIDGE_BINDING=SERVER_SIDE_ONLY
```

## R3-D accepted confirmation surface

```text
service=krc-mcp-r3d-confirmation-sentinel
surface=r3d_confirmation_probe
CHATGPT_CONFIRMATION_UI=PASS
APPROVE_PATH=PASS
CANCEL_PATH=PASS
NO_PRECONFIRM_EXECUTION=PASS
NO_EXECUTION_AFTER_DENY=PASS
```

## R3-E1 prepared YouTube surface

```text
service=krc-mcp-r3e1-youtube-sentinel
surface=r3e1_youtube_execution
tool_count=10
non_execution_tool_count=9
execution_tool_count=1
execution_tool=media_youtube_start
other_execution_tools=not_enabled
```

No live YouTube execution acceptance has been performed because durable PostgreSQL is currently blocked.

## Durable-state incident

```text
Render DB=voicebridge-krc-media-beta-db
Render DB state=suspended / billing
Render Free PostgreSQL=REJECTED_FOR_DURABLE_STATE
PAID_UPGRADE=DENIED
REAL_YOUTUBE_START=HOLD
```

## Free replacement authority

```text
PRIMARY_CANDIDATE=NEON_FREE
project=krc-media-beta-neon
subscription=free_v3
postgres=18
database=krc_media_beta
SECONDARY_CANDIDATE=SUPABASE_FREE
INFRA_CONTROLLED_FALLBACK=OCI_ALWAYS_FREE_SELF_HOSTED_POSTGRES
```

Neon already contains the expected VoiceBridge persistence tables. Audit-time row counts were `managed_jobs=0`, `client_jobs=0`, `stt_charges=10`; therefore it is not a full backup of the suspended Render database.

## Active next gate

The next bounded work is **Neon Free durable-state migration preflight**, not a real MEDIA start:

```text
schema/constraints/index audit
-> durable/idempotency field audit
-> server-side DATABASE_URL cutover plan
-> fail-closed/scale-to-zero validation
-> bounded cutover when explicitly approved if consequential
-> restart-resilient durable-state acceptance
-> resume R3-E1 only after PASS
```

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

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 126. R3-A/B/C/D PASS; R3-E1 authorized but infrastructure-blocked; project FREE-ONLY; continue from Neon Free durable-state migration preflight.`
