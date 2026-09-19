# MEDIA BETA Documentation Index

Canonical documentation index for K-Research & Critic MEDIA BETA / Plugin migration work.

Version: 8.4
Status: **ACTIVE / PLUGIN_FIRST / R3-A_PASS / R3-B_PASS / R3-C_PASS / R3-D_PASS / R3-E1_PASS / R3-E2_ISOLATED_SENTINEL_PREFLIGHT_PASS_CONFIRMATION_PENDING / FREE_ONLY / PUBLICATION_HOLD**
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

1. `CURRENT_HANDOFF.md` — v17.4.
2. `132_R3E2_ISOLATED_SENTINEL_AUTHENTICATED_PREFLIGHT_PASS_CONFIRMATION_PENDING_2026_09_19.md` — current R3-E2 checkpoint.
3. `131_R3E2_INSTAGRAM_READONLY_FREE_ONLY_PREFLIGHT_2026_09_19.md` — read-only R3-E2 preflight.
4. `130_POST_R3E1_CONTROL_POINT_BEFORE_R3E2_2026_09_19.md` — pre-R3-E2 control point.
5. `129_R3E1_YOUTUBE_LIVE_DURABLE_REPLAY_IDEMPOTENCY_PASS_2026_09_19.md` — R3-E1 closure.
6. `128_R3E1_RESTART_CONNECTIVITY_PASS_RECORD_REPLAY_PENDING_2026_09_19.md`.
7. `127_R3E1_NEON_CUTOVER_COMPLETE_DURABLE_ACCEPTANCE_PENDING_2026_09_19.md`.
8. `125_FREE_ONLY_INFRASTRUCTURE_POLICY_AND_POSTGRES_AUDIT_2026_09_17.md`.
9. `02_ROADMAP.md` — v5.8.
10. `124_R3D_CONSEQUENTIAL_ACTION_CONFIRMATION_PASS_2026_09_17.md`.
11. `121_R3C_NINE_TOOL_READONLY_VOICEBRIDGE_BINDING_PASS_2026_09_16.md`.
12. `117_R3B_AUTHENTICATED_REMOTE_MCP_HARDENING_PASS_2026_09_16.md`.
13. `113_R3A_CONTRACT_FREEZE_SECURE_ADAPTER_BASELINE_PASS_2026_09_16.md`.
14. current PR #22 / PR #45 head and current Render/Neon evidence.

Older checkpoints remain historical evidence and do not override the current handoff.

## Current accepted R3 state

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3_E1=PASS / COMPLETE
R3_E2=ISOLATED_SENTINEL_PASS / AUTHENTICATED_PREFLIGHT_PASS / CONFIRMATION_UI_PENDING / EXECUTION_HOLD
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
VOICEBRIDGE_DATABASE_CUTOVER=PASS
R3E1_LIVE_PERSISTENCE=PASS
R3E1_RESTART_REPLAY=PASS
R3E1_DUPLICATE_START_IDEMPOTENCY=PASS
```

The accepted R3-E1 live job was stored exactly once in Neon and recovered after VoiceBridge + R3-E1 restarts. Runtime jobs remain subject to configured TTL.

`krc_media_stt_charges` is a short-retention quota ledger, not a long-term audit log.

## Active next gate

The R3-E2 scoped bearer, isolated Instagram surface, authenticated preflight and durable lookup are PASS. Execution remains HOLD pending credential rotation and owner-account ChatGPT confirmation UI acceptance.

R3-C is historical accepted evidence and is not part of the current execution path unless separately requested.

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

`Віднови K-Research & Critic MEDIA з subprojects/media_beta/CURRENT_HANDOFF.md та checkpoint 132. R3-E1 PASS; R3-E2 isolated sentinel + authenticated preflight PASS; confirmation UI and credential rotation pending; execution HOLD.`
