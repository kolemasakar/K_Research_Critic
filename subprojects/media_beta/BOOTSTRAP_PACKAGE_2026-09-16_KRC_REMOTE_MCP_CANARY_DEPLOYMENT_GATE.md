# Bootstrap Package — K-Research & Critic MEDIA / Remote MCP Canary Deployment Gate

## Recommended Filename

`BOOTSTRAP_PACKAGE_2026-09-16_KRC_REMOTE_MCP_CANARY_DEPLOYMENT_GATE.md`

## Recovery Instructions

```text
Recovery Instructions

1. Read the entire Bootstrap Package.
2. Treat it as the authoritative entry point for project recovery.
3. Do not reconstruct previous chat history.
4. Do not make architectural assumptions.
5. Inspect Project Topology, Repositories, Repository Access, Source of Truth Map, Source of Truth Precedence, and any Workspaces or Runtime / Infrastructure sections.
6. Identify the Next Task and derive the minimum required components, sources and resources.
7. Check repository access independently for every REQUIRED repository.
8. For every accessible REQUIRED repository, verify provider, owner, repository name, full name, Default Branch and Active Recovery Branch when specified.
9. Use Active Recovery Branch for recovery when specified.
10. Stop recovery for a source if its identity does not match the Bootstrap Package.
11. Inform the user that repository access was found and identify each verified repository and branch.
12. Read only the Required Repository Resources needed for the Next Task.
13. Inform the user exactly which resources were read, grouped by repository.
14. If a REQUIRED source is unavailable, denied, incomplete or incorrectly identified, report the limitation, request only the minimum action required to restore access, use file upload only as fallback, and do not declare Recovery Complete.
15. OPTIONAL and REFERENCE_ONLY sources do not block recovery unless the Next Task makes them required.
16. Use the Source of Truth Map for domain authority and Source of Truth Precedence for conflicts.
17. If an authoritative implementation repository is accessible, do not infer current implementation behavior from documentation; read the implementation.
18. Do not infer project approval, roadmap or acceptance state solely from implementation code when an authoritative project-state source is available.
19. Revalidate REQUIRED volatile runtime/infrastructure state.
20. Do not assume source-session jobs, sessions, deploy IDs, signed URLs, locks, leases, queues or other ephemeral state remain current.
21. Perform a cross-source consistency check for domains required by the Next Task.
22. If authoritative sources disagree, report RECOVERY_CONSISTENCY_WARNING. Do not silently reconcile conflicting state.
23. Recovery is read-only. Do not modify repositories, workspaces, deployments or runtime state unless the user explicitly authorizes a write operation.
24. Report Project Topology, access status for each REQUIRED source, verified identities and branches, resources read, runtime verification, consistency result, unavailable REQUIRED resources, Combined Project Verification and Recovery status.
25. Combined Project Verification is PASS only when every REQUIRED source and verification condition for the Next Task has passed.
26. Continue from the Next Task only after Combined Project Verification is PASS and Recovery is complete.
```

## Project

K-Research & Critic — MEDIA / Plugin-first migration and Remote MCP integration.

## Project Topology

`COMBINED_PROJECT`

## Current Phase

`P105 — REMOTE MCP CANARY REPOSITORY ACCEPTED / BOUNDED DEPLOYMENT GATE`

## Current Objective

Validate real ChatGPT remote-MCP connectivity and tool discovery using the already repository-accepted, read-only `krc_media_capabilities_canary`, while preserving zero provider work, zero VoiceBridge binding, zero production MEDIA execution tools, zero public-GPT mutation and zero secret exposure.

## Repositories

### 1. K-Research & Critic

- **Role:** Project-state authority, Plugin/MCP candidate implementation, canary source/tests, migration acceptance contracts, CI and PR-state authority for the next phase.
- **Provider:** GitHub
- **Owner:** `kolemasakar`
- **Repository:** `K_Research_Critic`
- **Repository Full Name:** `kolemasakar/K_Research_Critic`
- **Default Branch:** `main`
- **Active Recovery Branch:** `agent/krc-public-media-r3-integration`
- **Repository URL:** `https://github.com/kolemasakar/K_Research_Critic`
- **Recovery Criticality:** `REQUIRED`
- **Responsibilities:** Current checkpoints 102–105; Remote MCP canary implementation; Core/Plugin candidate; MEDIA contracts; migration acceptance; tests; PR #22 staging state.

### 2. VoiceBridge

- **Role:** Existing MEDIA backend behind the future production MCP adapter.
- **Provider:** GitHub
- **Owner:** `kolemasakar`
- **Repository:** `VoiceBridge`
- **Repository Full Name:** `kolemasakar/VoiceBridge`
- **Default Branch:** `main`
- **Active Recovery Branch:** `agent/krc-media-gemini-migration` — reverify only if this source becomes REQUIRED.
- **Repository URL:** `https://github.com/kolemasakar/VoiceBridge`
- **Recovery Criticality:** `REFERENCE_ONLY`
- **Responsibilities:** Actual MEDIA backend/API implementation. The bounded canary must not call or modify it.

### 3. AI_general

- **Role:** OpenAI retirement/migration research provenance already incorporated into KRC acceptance policy.
- **Provider:** GitHub
- **Owner:** `kolemasakar`
- **Repository:** `AI_general`
- **Repository Full Name:** `kolemasakar/AI_general`
- **Default Branch:** `main`
- **Active Recovery Branch:** `main`
- **Repository URL:** `https://github.com/kolemasakar/AI_general`
- **Recovery Criticality:** `REFERENCE_ONLY`
- **Responsibilities:** Research provenance only; does not override current KRC checkpoints or contracts.

## Repository Access

| Repository Full Name | Access Method | Source Session Verification Status | Read Capability | Write Capability | Notes |
|---|---|---|---|---|---|
| `kolemasakar/K_Research_Critic` | Connected GitHub integration | `VERIFIED` on 2026-09-16 | Yes | Yes | PR #22, branch head and latest CI were revalidated in this source session. Recovery itself remains read-only. |
| `kolemasakar/VoiceBridge` | Connected GitHub integration | `NOT_REVALIDATED_FOR_THIS_GENERATION / historical project access known` | Not assumed | Not assumed | REFERENCE_ONLY for the Next Task; do not block recovery on it. |
| `kolemasakar/AI_general` | Connected GitHub integration | `READ_VERIFIED` on 2026-09-16 | Yes | Not required | Research document was read from `main`; no write is required for the Next Task. |

Source-session access does not guarantee identical access in a new session. Never transfer credentials.

## Source of Truth Map

| Engineering Domain | Authoritative Source |
|---|---|
| Current project phase / deployment stop boundary | `subprojects/media_beta/105_KRC_REMOTE_MCP_CANARY_SENTINEL_SYNC_2026_09_16.md` |
| Repository canary acceptance | `subprojects/media_beta/104_KRC_REMOTE_MCP_CANARY_REPO_ACCEPTANCE_2026_09_16.md` |
| Canary implementation behavior | `plugins/krc_migration_candidate/mcp_canary/server.py` plus `tests/test_krc_mcp_canary.py` |
| Account-specific custom-MCP surface evidence | `subprojects/media_beta/102_KRC_P100_ACCOUNT_SURFACE_INSPECTION_RESULT_2026_09_16.md` |
| Migration acceptance / cutover policy | `plugins/krc_migration_candidate/contracts/migration_acceptance.yaml` |
| Surface-selection rules | `plugins/krc_migration_candidate/contracts/surface_decision_matrix.yaml` |
| Auth / transport boundary | `plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml` |
| MEDIA operation parity | `plugins/krc_migration_candidate/contracts/media_tools.yaml` |
| MEDIA transport-neutral semantics | `plugins/krc_migration_candidate/contracts/media_adapter.yaml` |
| Core semantics | `prompts/GPT_STORE_INSTRUCTIONS.md` |
| Core migration snapshot | `plugins/krc_migration_candidate/skills/krc_core/SKILL.md`, parity-checked by CI |
| Current PR/head/CI | Live GitHub PR #22 metadata and latest workflow results |
| VoiceBridge backend behavior if later needed | `kolemasakar/VoiceBridge` implementation on a then-revalidated branch |
| OpenAI migration research provenance | `kolemasakar/AI_general/docs/openai-custom-gpts-retirement-to-plugins-2026-09-16.md` |

## Source of Truth Precedence

1. Live GitHub PR #22 metadata overrides stored handoff files for current head, PR state and CI state.
2. Checkpoint 105 overrides older P101/P103 handoffs for current phase and stop boundary.
3. Checkpoint 104 is authoritative for repository-canary acceptance; implementation code/tests are authoritative for actual canary behavior.
4. Checkpoint 102 is authoritative for the latest accepted account-surface classification until a newer direct inspection supersedes it.
5. Domain contracts override prose summaries for migration acceptance, surface selection, auth/transport, MEDIA parity and adapter semantics.
6. `prompts/GPT_STORE_INSTRUCTIONS.md` overrides migration snapshot prose for Core semantics.
7. If VoiceBridge becomes relevant, VoiceBridge implementation overrides KRC prose about backend internals; KRC project checkpoints still control approvals and release gates.
8. AI_general research informs policy provenance but never overrides KRC project decisions.
9. Any future direct runtime/account observation supersedes old volatile evidence only after explicit revalidation.

## Current Status

- Plugin-first strategy remains accepted; legacy MEDIA Custom GPT Action creation remains on HOLD.
- Account surface was inspected read-only and classified `REMOTE_CUSTOM_MCP_CANDIDATE`; custom MCP, remote MCP and auth surface were visible, while actual execution/write capability remains unverified.
- Repository-only `krc_media_capabilities_canary` is implemented and accepted; it is deterministic, read-only, has no network I/O, no provider work, no secret requirement and no VoiceBridge binding.
- MCP protocol core supports tool discovery/call with fail-closed unknown-tool/argument handling; it is not a deployed HTTPS MCP service.
- Current PR #22 head before this bootstrap-only commit: `4b4906d4e1b7f34b02e47dcdbc1a1bbdd0d0ad21`.
- Workflow `35123303282` on that head completed `SUCCESS`.
- PR #22 is `OPEN / DRAFT / UNMERGED / mergeable` against `main`.
- No live MCP endpoint, ChatGPT MCP connection, VoiceBridge bearer binding, production MEDIA MCP tool, Render mutation, public-GPT mutation, migration execution, PR #22 merge or PR #45 merge is accepted as current state.
- `RECOVERY_CONSISTENCY_WARNING`: `subprojects/media_beta/CURRENT_HANDOFF.md` remains P101-oriented and is superseded by checkpoints 102–105 and this package.

## Completed Work

- P99 Core+MEDIA migration hardening completed and CI-accepted.
- P100 migration-surface readiness completed and CI-accepted.
- OpenAI retirement research incorporated into model-independent, chat-history-independent, sharing/reference-asset migration acceptance guards.
- Owner-account surface inspected read-only; remote custom MCP selected as preferred candidate, with execution/write capability explicitly left unverified.
- Repository-only Remote MCP canary implementation completed under the Plugin candidate subtree.
- Canary tests prove read-only behavior, deterministic response, no external network/provider work, no secrets, no deployment endpoint and unchanged Core/MEDIA parity.
- Repository acceptance checkpoint 104 completed.
- Sentinel sync checkpoint 105 recorded accepted state and explicit STOP before deployment/connection.
- Latest verified PR #22 head `4b4906d4e1b7f34b02e47dcdbc1a1bbdd0d0ad21` passed workflow `35123303282`.

## Known Open Engineering Items

| Item | Status | Relevance |
|---|---|---|
| Bounded deployment of only the read-only MCP canary | `RELEASE_GATE` | This is the next state-changing phase and requires separate owner authorization. |
| Select isolated deployment provider/endpoint for the canary | `OPEN` | Must not reuse or mutate production targets by assumption; choose only inside the owner-authorized deployment phase. |
| ChatGPT `Scan Tools` / connection test against the deployed canary | `RELEASE_GATE` | Required to prove real remote MCP discovery/connection; no production MEDIA tools may be exposed. |
| ChatGPT-to-canary authentication handshake | `OPEN` | Must follow actual supported account surface; production VoiceBridge bearer remains forbidden. |
| Actual execution/write capability for four MEDIA start operations | `BLOCKED` | Not part of the read-only canary; must fail closed until a later separately authorized execution-capability phase. |
| VoiceBridge bearer injection at MCP edge | `DEFERRED` | Forbidden for the canary; only future production binding may introduce server-side injection. |
| Full 13-operation live MCP mapping | `DEFERRED` | Must not start until canary deployment/connection acceptance. |
| Replacement Plugin sharing/publish permissions | `DEFERRED` | Not needed for bounded canary validation. |
| `CURRENT_HANDOFF.md` stale at P101 | `KNOWN_DEFECT` | Non-blocking when this package and checkpoints 102–105 are used. |

## Next Task

**After explicit owner authorization in the recovered chat, execute one bounded Remote MCP canary deployment-and-connection validation using only `krc_media_capabilities_canary`.**

The coordinated substeps serve one objective:

1. Revalidate PR #22 head/CI and the accepted canary implementation.
2. Select an isolated, non-production remote HTTPS deployment target for the canary; do not assume Render or any existing runtime is authorized.
3. Deploy only the repository-accepted read-only MCP canary implementation.
4. Confirm the deployed surface exposes only `krc_media_capabilities_canary` and no VoiceBridge/production MEDIA tools.
5. Use the owner-account ChatGPT custom-MCP surface to perform bounded `Scan Tools` / connection validation.
6. Record only non-secret evidence: tool discovery result, transport/auth mode, web availability, confirmation behavior and connection result.
7. Verify `mutation=false`, `provider_work=false`, `secret_required=false`, no VoiceBridge call, no durable MEDIA job and no public-GPT mutation.
8. STOP after canary connection acceptance or a clearly recorded blocker.

Hard exclusions for this Next Task:

```text
FULL_MEDIA_13_TOOL_DEPLOYMENT=DENIED
VOICEBRIDGE_SECRET_BINDING=DENIED
MEDIA_PROVIDER_WORK=DENIED
WRITE_EXECUTION_TOOL_TEST=DENIED
PUBLIC_GPT_CHANGE=DENIED
GPT_MIGRATION_EXECUTION=DENIED
PLUGIN_PUBLICATION=DENIED
MAIN_MUTATION=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

Recovery remains read-only. This package defines the Next Task but does not itself authorize its state-changing deployment/connection steps.

## Required Repository Resources

### `kolemasakar/K_Research_Critic`

- **Branch:** `agent/krc-public-media-r3-integration`
- **Recovery Criticality:** `REQUIRED`
- **Resources:**
  - `subprojects/media_beta/105_KRC_REMOTE_MCP_CANARY_SENTINEL_SYNC_2026_09_16.md`
  - `subprojects/media_beta/104_KRC_REMOTE_MCP_CANARY_REPO_ACCEPTANCE_2026_09_16.md`
  - `subprojects/media_beta/103_KRC_REMOTE_MCP_CANARY_IMPLEMENTATION_PACKAGE_2026_09_16.md`
  - `subprojects/media_beta/102_KRC_P100_ACCOUNT_SURFACE_INSPECTION_RESULT_2026_09_16.md`
  - `subprojects/media_beta/102_OPENAI_RETIREMENT_RESEARCH_INTEGRATION_ACCEPTANCE_HARDENING_2026_09_16.md`
  - `plugins/krc_migration_candidate/mcp_canary/server.py`
  - `plugins/krc_migration_candidate/mcp_canary/__init__.py`
  - `tests/test_krc_mcp_canary.py`
  - `plugins/krc_migration_candidate/contracts/migration_acceptance.yaml`
  - `plugins/krc_migration_candidate/contracts/surface_decision_matrix.yaml`
  - `plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml`
  - `plugins/krc_migration_candidate/contracts/media_tools.yaml`
  - `plugins/krc_migration_candidate/contracts/media_adapter.yaml`
  - `prompts/GPT_STORE_INSTRUCTIONS.md`
  - `plugins/krc_migration_candidate/skills/krc_core/SKILL.md`
  - `pyproject.toml`
  - `.github/workflows/tests.yml`
  - live PR #22 metadata and current workflow state

### `kolemasakar/VoiceBridge`

- **Branch:** `agent/krc-media-gemini-migration` — reverify only if promoted to REQUIRED.
- **Recovery Criticality:** `REFERENCE_ONLY`
- **Resources:** None required for bounded canary deployment/connection because VoiceBridge calls and secrets are forbidden.

### `kolemasakar/AI_general`

- **Branch:** `main`
- **Recovery Criticality:** `REFERENCE_ONLY`
- **Resources:** None required unless migration-policy provenance must be re-audited.

## Recovery Verification Requirements

- Verify `kolemasakar/K_Research_Critic` identity and `main` default branch.
- Verify Active Recovery Branch `agent/krc-public-media-r3-integration` exists and is PR #22 head.
- Re-fetch PR #22 metadata and latest CI; if head moved, inspect newer checkpoints/commits before accepting this Next Task.
- Load the REQUIRED KRC resources listed above and read actual canary implementation/tests, not documentation alone.
- Apply the Source of Truth Map and precedence rules.
- Confirm checkpoint 105 still represents the latest accepted stop boundary.
- Confirm the canary still has no network/provider/secret/VoiceBridge dependency and no live deployment config.
- Confirm `CURRENT_HANDOFF.md` is stale relative to checkpoints 102–105; report `RECOVERY_CONSISTENCY_WARNING` rather than following P101.
- Revalidate the ChatGPT custom-MCP account surface before any connection attempt because account/UI capabilities are volatile.
- If a deployment target is later owner-authorized, verify it is isolated from production and revalidate that runtime before use.
- Do not infer or reuse source-session URLs, sessions, deployment IDs, tunnels or credentials.
- Inform the user of verified repository access and exact resources read.
- No unresolved REQUIRED-source failure may remain.
- Combined Project Verification may be `PASS` for recovery before a deployment target exists; deployment itself remains a separate owner gate.

## Recovery Status

```text
[ ] Bootstrap Loaded
[ ] Project Topology Identified
[ ] Required Sources Identified
[ ] Required Repository Access Checked
[ ] Required Repository Identities Verified
[ ] Required Resources Loaded
[ ] Runtime Revalidated If Required
[ ] Cross-Source Consistency Checked
[ ] Recovery Verification Reported
[ ] Recovery Complete
```

## Project Composition

| Component | Responsibility | Repository or Workspace | Runtime | Dependency Direction |
|---|---|---|---|---|
| KRC Core / Plugin candidate | Research workflow and migration candidate | `kolemasakar/K_Research_Critic` | Repository/CI | Core -> Plugin skill |
| Remote MCP canary | Read-only transport/tool-discovery proof | `kolemasakar/K_Research_Critic` | No live runtime yet | ChatGPT -> Remote MCP canary |
| ChatGPT account surface | Custom MCP connection, Scan Tools and capability validation | OpenAI account workspace | ChatGPT web | ChatGPT -> Remote MCP |
| VoiceBridge MEDIA | Existing production-like MEDIA API and provider orchestration | `kolemasakar/VoiceBridge` | Existing backend runtime | Future production MCP -> VoiceBridge -> providers |
| Migration research | Retirement/migration provenance | `kolemasakar/AI_general` | None | Research -> KRC policy |

## Workspaces

| Path | Role | Git Repository | Branch | Source Session Verification | Required for Next Task |
|---|---|---|---|---|---|
| ChatGPT Work Cloud Browser | Account-surface inspection/connection workspace | N/A | N/A | Historical read-only evidence accepted in checkpoint 102; not assumed current | Yes for the connection substep; revalidate before use |

## Runtime / Infrastructure

### Current Remote MCP canary runtime

- **Provider:** None
- **Service:** Not deployed
- **Service ID:** None
- **Environment:** None
- **Endpoint:** None
- **Branch / Deployment Source:** `agent/krc-public-media-r3-integration` candidate only
- **Responsibility:** Future bounded remote-MCP canary endpoint
- **Recovery Criticality:** `OPTIONAL` during read-only recovery; becomes `REQUIRED` only after owner authorizes the deployment phase and a target is selected
- **Source Session Verified At:** 2026-09-16 repository state only
- **Requires Revalidation:** `YES` after any deployment target is created

### Existing VoiceBridge / provider runtimes

They are not required for the bounded canary Next Task because the canary is forbidden from calling them. Do not revalidate or mutate them merely for recovery.

## Deployment Boundary

| Boundary | Target |
|---|---|
| Active Test Target | Future isolated remote HTTPS endpoint exposing only `krc_media_capabilities_canary` |
| Production Target | Existing public KRC GPT and existing VoiceBridge/provider runtime — unchanged |
| Public Release Target | Future replacement Plugin/App after later full acceptance gates |
| Allowed Recovery Target | Read-only recovery of PR #22 and account surface; no deployment during recovery |
| Allowed Execution Target after explicit owner gate | Newly selected isolated canary runtime only |
| Prohibited Targets | `main`, existing production/public GPT, existing VoiceBridge service, production provider paths, full 13-tool MEDIA surface, public Plugin publication, PR #22 merge, PR #45 merge |

## Ephemeral / Expiring Resources

| Resource Type | Identifier | Source Session State | Source Session Verified At | May Expire | Recovery Rule |
|---|---|---|---|---|---|
| GitHub Actions workflow | `35123303282` | `SUCCESS` for head `4b4906d4...` | 2026-09-16 | No for historical result; head may move | Do Not Assume Current; verify latest head/workflow before reuse |
| ChatGPT account session | Not recorded | Previously usable through Work Cloud Browser | 2026-09-16 | Yes | Do Not Assume Current; verify before reuse |
| Remote MCP endpoint | None | Not created | N/A | N/A | Do not invent; create only after owner authorization |
| Tunnel/signed URL/session token | None accepted | None | N/A | Yes | Do Not Assume Current; never transfer secrets |

## Pull Request State

| Field | Value |
|---|---|
| Repository | `kolemasakar/K_Research_Critic` |
| PR Number | `22` |
| PR State | `OPEN` |
| Draft | `true` |
| Base | `main` |
| Head | `agent/krc-public-media-r3-integration` |
| Merged | `false` |
| Mergeable | `true` |
| Verified head before bootstrap-only commit | `4b4906d4e1b7f34b02e47dcdbc1a1bbdd0d0ad21` |
| Verified workflow | `35123303282` — `SUCCESS` |

Revalidate PR #22 head/CI on recovery because this Bootstrap Package commit advances the branch.

## Repository Dependency Graph

```text
ChatGPT account surface
        |
        v
isolated Remote MCP canary runtime   [future / owner-gated]
        |
        v
krc_media_capabilities_canary        [repository-accepted]

NO edge to VoiceBridge or providers during this phase.

Future only:
ChatGPT -> production MCP adapter -> VoiceBridge -> Gemini / Cobalt / AssemblyAI / Telegram public web
```

## Temporary Artifact Handling

| Artifact | Classification | Recovery Rule |
|---|---|---|
| Checkpoint 105 Sentinel sync | `PERSISTENT` | Current accepted stop-boundary evidence. |
| Checkpoint 104 repository acceptance | `PERSISTENT` | Canonical canary acceptance state. |
| Repository canary implementation/tests | `PERSISTENT` | Required implementation source for next phase. |
| `CURRENT_HANDOFF.md` v6.0 / P101-ready | `PERSISTENT` historical but superseded | Do not use as current phase authority. |
| Earlier P103 implementation bootstrap | `PERSISTENT` historical but superseded | Useful provenance only; its Next Task is complete. |
| Live canary endpoint | Not created | Never assume one exists. |
| ChatGPT MCP connection | Not created | Never assume one exists. |

## Combined Project Verification

Source-session generator validation:

```text
K_Research_Critic repository: VERIFIED
K_Research_Critic Active Recovery Branch: VERIFIED
PR #22 source head: VERIFIED
PR #22 source-head CI: PASS
Remote MCP canary repository acceptance: PASS
VoiceBridge: REFERENCE_ONLY / not revalidated for this generation
AI_general: REFERENCE_ONLY / research source read verified
Required live canary runtime: NONE EXISTS YET
Cross-Source Consistency: RECOVERY_CONSISTENCY_WARNING_NON_BLOCKING
  reason=CURRENT_HANDOFF.md remains P101-oriented while checkpoints 102-105 are newer
Combined Project Verification for bootstrap generation: PASS
```

The recovery session must perform its own verification and must not inherit this PASS automatically.
