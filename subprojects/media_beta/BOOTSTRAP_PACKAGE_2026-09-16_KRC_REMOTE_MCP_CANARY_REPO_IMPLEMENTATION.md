# Bootstrap Package — K-Research & Critic MEDIA / Remote MCP Canary

## Recommended Filename

`BOOTSTRAP_PACKAGE_2026-09-16_KRC_REMOTE_MCP_CANARY_REPO_IMPLEMENTATION.md`

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

`P103 — REMOTE MCP CANARY REPOSITORY IMPLEMENTATION`

## Current Objective

Prepare and repository-validate a minimal read-only remote MCP canary for KRC MEDIA that proves MCP packaging and tool-discovery readiness without provider work, VoiceBridge calls, credentials, deployment, ChatGPT connection, public-GPT mutation, or release activation.

## Repositories

### 1. K-Research & Critic

- **Role:** Project state, Core/Plugin candidate, MEDIA contracts, MCP canary implementation target, regression and CI authority for the current phase.
- **Provider:** GitHub
- **Owner:** `kolemasakar`
- **Repository:** `K_Research_Critic`
- **Repository Full Name:** `kolemasakar/K_Research_Critic`
- **Default Branch:** `main`
- **Active Recovery Branch:** `agent/krc-public-media-r3-integration`
- **Repository URL:** `https://github.com/kolemasakar/K_Research_Critic`
- **Recovery Criticality:** `REQUIRED`
- **Responsibilities:** Current project checkpoints; Plugin-first strategy; account-surface evidence; MCP canary package; Core skill source/candidate; 13-operation MEDIA parity contracts; migration acceptance rules; tests; PR #22 staging state.

### 2. VoiceBridge

- **Role:** Existing MEDIA backend implementation behind the future MCP adapter.
- **Provider:** GitHub
- **Owner:** `kolemasakar`
- **Repository:** `VoiceBridge`
- **Repository Full Name:** `kolemasakar/VoiceBridge`
- **Default Branch:** `main`
- **Active Recovery Branch:** `agent/krc-media-gemini-migration` — accepted project branch; reverify only if this source becomes REQUIRED.
- **Repository URL:** `https://github.com/kolemasakar/VoiceBridge`
- **Recovery Criticality:** `REFERENCE_ONLY`
- **Responsibilities:** Actual VoiceBridge MEDIA backend/API implementation. It is explicitly not called or modified by the P103 canary.

### 3. AI_general

- **Role:** External OpenAI retirement/migration research reference already incorporated into KRC migration acceptance policy.
- **Provider:** GitHub
- **Owner:** `kolemasakar`
- **Repository:** `AI_general`
- **Repository Full Name:** `kolemasakar/AI_general`
- **Default Branch:** `main`
- **Active Recovery Branch:** `main`
- **Repository URL:** `https://github.com/kolemasakar/AI_general`
- **Recovery Criticality:** `REFERENCE_ONLY`
- **Responsibilities:** Reference research source `docs/openai-custom-gpts-retirement-to-plugins-2026-09-16.md`; it does not override KRC project-state or acceptance contracts.

## Repository Access

| Repository Full Name | Access Method | Source Session Verification Status | Read Capability | Write Capability | Notes |
|---|---|---|---|---|---|
| `kolemasakar/K_Research_Critic` | Connected GitHub integration | `VERIFIED` on 2026-09-16 | Yes | Yes | Repository identity/default branch/permissions and PR #22 staging branch verified. Recovery itself remains read-only. |
| `kolemasakar/VoiceBridge` | Connected GitHub integration | `VERIFIED_REPOSITORY_ACCESS_ONLY` on 2026-09-16 | Yes | Yes | Default branch and repository permissions verified. Active project branch was not reloaded because this source is REFERENCE_ONLY for P103. |
| `kolemasakar/AI_general` | Connected GitHub integration | `VERIFIED` on 2026-09-16 | Yes | Yes | Repository identity verified and retirement/migration research document read from `main`. |

Source-session access does not guarantee identical access in the recovery session. No credentials are transferred by this package.

## Project Composition

| Component | Responsibility | Repository or Workspace | Runtime | Dependency Direction |
|---|---|---|---|---|
| KRC Core / Plugin candidate | Research workflow, migration candidate, acceptance policy, MCP staging | `kolemasakar/K_Research_Critic` | Repository/CI | Core -> Plugin skill |
| Remote MCP candidate | Future ChatGPT integration edge; current phase is repository-only canary | `kolemasakar/K_Research_Critic` | No live runtime yet | Plugin/App -> Remote MCP |
| VoiceBridge MEDIA | Existing MEDIA API and provider orchestration | `kolemasakar/VoiceBridge` | Existing backend runtime | Remote MCP -> VoiceBridge -> providers |
| ChatGPT account surface | Custom MCP creation/connection UI and future capability validation | External OpenAI account surface | ChatGPT web | ChatGPT -> Remote MCP |
| OpenAI retirement research | External strategy/reference evidence | `kolemasakar/AI_general` | None | Research -> KRC acceptance rules |

The P103 canary intentionally stops before VoiceBridge and provider dependencies.

## Source of Truth Map

| Engineering Domain | Authoritative Source |
|---|---|
| Current project phase / Next Task | `subprojects/media_beta/103_KRC_REMOTE_MCP_CANARY_IMPLEMENTATION_PACKAGE_2026_09_16.md` on the Active Recovery Branch |
| Account-specific MCP surface evidence and classification | `subprojects/media_beta/102_KRC_P100_ACCOUNT_SURFACE_INSPECTION_RESULT_2026_09_16.md` |
| MCP canary semantics and hard boundaries | `subprojects/media_beta/103_KRC_REMOTE_MCP_CANARY_IMPLEMENTATION_PACKAGE_2026_09_16.md` |
| Migration acceptance / cutover rules | `plugins/krc_migration_candidate/contracts/migration_acceptance.yaml` |
| Surface selection rules | `plugins/krc_migration_candidate/contracts/surface_decision_matrix.yaml` |
| Auth / transport boundary | `plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml` |
| MEDIA operation parity | `plugins/krc_migration_candidate/contracts/media_tools.yaml` |
| MEDIA transport-neutral semantics | `plugins/krc_migration_candidate/contracts/media_adapter.yaml` |
| Core instructions | `prompts/GPT_STORE_INSTRUCTIONS.md` |
| Core migration snapshot | `plugins/krc_migration_candidate/skills/krc_core/SKILL.md`, validated against canonical Core by CI |
| PR state, current branch head and CI | Live GitHub PR #22 metadata and workflow results |
| VoiceBridge backend behavior, if later required | `kolemasakar/VoiceBridge` implementation on the then-verified active branch |
| OpenAI retirement research provenance | `kolemasakar/AI_general/docs/openai-custom-gpts-retirement-to-plugins-2026-09-16.md` |

## Source of Truth Precedence

1. **Live GitHub PR #22 metadata** overrides stored handoff documents for current head, PR state and CI state.
2. **P103 canary package** overrides older P100/P101 transition documents for the current phase and Next Task.
3. **P102 account-surface result** overrides earlier `SURFACE_AMBIGUOUS` / P101-inspection-pending state.
4. Domain contracts (`migration_acceptance.yaml`, `surface_decision_matrix.yaml`, `auth_transport_binding.yaml`, `media_tools.yaml`, `media_adapter.yaml`) override prose summaries for their respective domains.
5. `prompts/GPT_STORE_INSTRUCTIONS.md` is authoritative for Core semantics; `SKILL.md` is a migration snapshot and must remain parity-checked.
6. If VoiceBridge backend behavior becomes relevant, VoiceBridge implementation code overrides KRC prose describing backend internals; KRC project-state checkpoints still control approval/release state.
7. AI_general research informs strategy but does not override KRC project decisions or migration acceptance contracts.
8. Future direct account/runtime observations override old runtime evidence for volatile state, but only after explicit revalidation.

## Current Status

- P99 Core+MEDIA migration hardening: `PASS`.
- P100 migration-surface readiness: `PASS`; P102 migration-acceptance hardening: `PASS`.
- Account inspection completed read-only: `SURFACE_CLASSIFICATION=REMOTE_CUSTOM_MCP_CANDIDATE`; remote MCP UI/transport/auth surface visible; `EXECUTION_WRITE_ACTUAL=UNVERIFIED`.
- Visible MCP auth choices recorded as `OAuth | No_authentication | Mixed`; direct exposure of the VoiceBridge bearer is forbidden; OAuth is the preferred secure candidate if supported at connection stage.
- P103 repository-only MCP canary package is `READY_FOR_KRC_REPO_IMPLEMENTATION / NO_DEPLOY / NO_CONNECT`.
- Current public KRC remains unchanged; legacy MEDIA Custom GPT Action creation remains on HOLD.
- PR #22 is `OPEN / DRAFT / UNMERGED / mergeable`; engineering head verified as `e551bd327f9f4c05350fe1955a5dfdcc4e3f4a45` before this bootstrap-only artifact.
- Workflow `35121953154` on that engineering head completed `SUCCESS`: Python 3.13 PASS, Python 3.14 PASS, Quality gates PASS.
- No live KRC MCP endpoint, ChatGPT MCP connection, plugin installation, migration execution, Render mutation, public-GPT mutation, PR #22 merge or PR #45 merge is authorized or present.
- `RECOVERY_CONSISTENCY_WARNING`: `subprojects/media_beta/CURRENT_HANDOFF.md` still states `P101_READY`; it is stale and must not override P102/P103 or this Bootstrap Package.

## Completed Work

- Core migration candidate created with byte-for-byte parity guard against canonical Core instructions.
- 13-operation R3 MEDIA Action/API semantics mapped into transport-neutral Plugin/App/MCP contracts.
- Core regression pack and MEDIA negative/boundary regression pack created and passing.
- Migration surface decision matrix and auth/transport binding specification created and passing CI.
- OpenAI Custom GPT retirement research incorporated into migration acceptance guards: model independence, chat-history independence, sharing revalidation, reference-asset validation and non-assumption of Store metric portability.
- Read-only owner-account inspection completed; custom remote MCP surface detected and classified as preferred candidate while actual execution/write capability remains unverified.
- Repository-only P103 canary implementation specification created.
- PR #22 engineering head `e551bd327f9f4c05350fe1955a5dfdcc4e3f4a45` passed the full repository workflow `35121953154`.

## Known Open Engineering Items

| Item | Status | Relevance |
|---|---|---|
| Implement `krc_media_capabilities_canary` in the KRC staging branch and add repository tests/checkpoint | `OPEN` | This is the Next Task. |
| Actual ChatGPT remote MCP read/tool-scan capability against a real KRC endpoint | `BLOCKED` | Requires a later separately authorized deployment/connection after repo-only canary acceptance. |
| Actual execution/write capability for the four MEDIA start operations | `BLOCKED` | Must fail closed until a real later canary proves account capability. |
| Production ChatGPT-to-MCP authentication selection | `DEFERRED` | OAuth is preferred candidate; `No authentication` is not acceptable for a public production endpoint; exact live behavior must be verified later. |
| Replacement Plugin sharing/publish permissions | `DEFERRED` | Account inspection recorded them as unknown; not required for repo-only canary. |
| Full 13-operation live MCP mapping | `DEFERRED` | Must not start until repo-only canary and later live connection capability are accepted. |
| Live MCP deployment / ChatGPT connection | `RELEASE_GATE` | Requires separate owner authorization after repository canary PASS. |
| `CURRENT_HANDOFF.md` still points to P101 | `KNOWN_DEFECT` | Recovery must use this Bootstrap Package plus P102/P103; stale handoff is secondary only. |

## Next Task

**Implement and repository-test one minimal read-only Remote MCP canary in `kolemasakar/K_Research_Critic` on `agent/krc-public-media-r3-integration`, following P103.**

The single canary tool is:

```text
name=krc_media_capabilities_canary
mutation=false
provider_work=false
write=false
voicebridge_secret_required=false
```

The implementation must:

- live under the existing project/plugin subtree, never repository root;
- return deterministic sanitized capability data;
- perform no VoiceBridge call and no Gemini/AssemblyAI/Cobalt/Telegram/Facebook/Instagram/YouTube provider work;
- create no durable MEDIA job and perform no external state mutation;
- contain no real credential, bearer token, OAuth secret, cookie, browser state or model-visible secret;
- keep authentication pluggable and keep live deployment/connection absent;
- leave Core parity, 13-operation MEDIA contracts and VoiceBridge API unchanged;
- add tests proving read-only behavior, no network/provider work, no secret-bearing config, deterministic response, unchanged Core/MEDIA parity, and absence of deployment/live-endpoint claims;
- produce one repository checkpoint recording canary implementation/test acceptance;
- STOP after repository CI/acceptance. Do not deploy or connect the canary.

Recovery is read-only. This Bootstrap Package does not itself authorize repository mutation. After Recovery Complete, proceed with this Next Task only when the owner explicitly instructs the recovered chat to continue/execute repository implementation.

## Required Repository Resources

### `kolemasakar/K_Research_Critic`

- **Branch:** `agent/krc-public-media-r3-integration`
- **Recovery Criticality:** `REQUIRED`
- **Resources:**
  - `subprojects/media_beta/103_KRC_REMOTE_MCP_CANARY_IMPLEMENTATION_PACKAGE_2026_09_16.md`
  - `subprojects/media_beta/102_KRC_P100_ACCOUNT_SURFACE_INSPECTION_RESULT_2026_09_16.md`
  - `subprojects/media_beta/102_OPENAI_RETIREMENT_RESEARCH_INTEGRATION_ACCEPTANCE_HARDENING_2026_09_16.md`
  - `plugins/krc_migration_candidate/README.md`
  - `plugins/krc_migration_candidate/contracts/migration_acceptance.yaml`
  - `plugins/krc_migration_candidate/contracts/surface_decision_matrix.yaml`
  - `plugins/krc_migration_candidate/contracts/auth_transport_binding.yaml`
  - `plugins/krc_migration_candidate/contracts/media_tools.yaml`
  - `plugins/krc_migration_candidate/contracts/media_adapter.yaml`
  - `plugins/krc_migration_candidate/skills/krc_core/SKILL.md`
  - `prompts/GPT_STORE_INSTRUCTIONS.md`
  - `gpt_store/actions/media_public_r3_openapi.yaml`
  - `tests/test_krc_plugin_migration_candidate.py`
  - `tests/test_krc_p100_surface_readiness.py`
  - `tests/test_krc_migration_acceptance.py`
  - `pyproject.toml`
  - `.github/workflows/tests.yml`
  - live PR #22 metadata and workflow state for the current head

### `kolemasakar/VoiceBridge`

- **Branch:** `agent/krc-media-gemini-migration` — reverify only if promoted to REQUIRED.
- **Recovery Criticality:** `REFERENCE_ONLY`
- **Resources:** None required for the P103 repo-only canary. Do not load backend code merely to implement a canary that is forbidden from calling VoiceBridge.

### `kolemasakar/AI_general`

- **Branch:** `main`
- **Recovery Criticality:** `REFERENCE_ONLY`
- **Resources:** None required for the P103 implementation because its relevant conclusions are already canonicalized in `migration_acceptance.yaml`. Load `docs/openai-custom-gpts-retirement-to-plugins-2026-09-16.md` only if provenance or migration-policy re-audit becomes necessary.

## Runtime / Infrastructure

### ChatGPT custom MCP account surface

- **Provider:** OpenAI ChatGPT
- **Service:** Owner-account custom MCP / Plugin surface
- **Service ID:** Not applicable / not recorded
- **Environment:** ChatGPT web account surface
- **Endpoint:** No KRC MCP endpoint exists yet
- **Branch / Deployment Source:** None
- **Responsibility:** Future remote MCP connection/tool scan and permission validation
- **Recovery Criticality:** `REFERENCE_ONLY` for the current repo-only Next Task
- **Source Session Verified At:** 2026-09-16 via accepted read-only account-surface evidence in P102
- **Requires Revalidation:** `NO` for repository-only P103 implementation; `YES` before any live deployment, connection, Scan Tools, auth handshake, execution/write conclusion, sharing or publication action

No Render, OCI Cobalt, VoiceBridge runtime, Gemini, AssemblyAI, Telegram, Facebook, Instagram or YouTube runtime revalidation is required for the P103 repository-only canary because the canary is forbidden from invoking them.

## Deployment Boundary

| Boundary | Target |
|---|---|
| Active Test Target | Repository-only MCP canary code/tests on PR #22 staging branch |
| Production Target | Existing public KRC GPT and existing VoiceBridge runtime — unchanged |
| Public Release Target | Future replacement Plugin/App after separate migration and acceptance gates |
| Allowed Recovery Target | Read-only KRC staging-branch recovery; after owner authorization, repository-only canary implementation/tests |
| Prohibited Targets | `main`, Render mutation, live MCP deployment, live MCP connection, ChatGPT app connection, Plugin install/publish, GPT migration execution, public GPT update/delete, VoiceBridge secret exposure, PR #22 merge, PR #45 merge |

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
| Source-session engineering head before bootstrap-only artifact | `e551bd327f9f4c05350fe1955a5dfdcc4e3f4a45` |
| Engineering-head workflow | `35121953154` — `SUCCESS` |

Revalidate PR #22 head and CI at recovery. If the head moved, inspect newer checkpoints/commits before using P103.

## Temporary Artifact Handling

| Artifact | Classification | Recovery Rule |
|---|---|---|
| P102 account-surface inspection result | `PERSISTENT` | Canonical evidence for current surface classification until a newer direct inspection supersedes it. |
| P103 remote MCP canary implementation package | `PERSISTENT` | Canonical current phase/Next Task specification. |
| `CURRENT_HANDOFF.md` v6.0 / P101-ready | `PERSISTENT` historical but superseded | Do not use as current phase authority. |
| Live KRC MCP endpoint | Not created | Do not infer one exists. |
| ChatGPT MCP connection | Not created | Do not infer one exists. |
| Runtime session/tunnel/signed URL | None accepted for P103 | Do not create or assume during recovery. |

## Recovery Verification Requirements

- Verify `kolemasakar/K_Research_Critic` repository identity and `main` default branch.
- Verify Active Recovery Branch `agent/krc-public-media-r3-integration` exists and is the PR #22 head branch.
- Fetch live PR #22 metadata and current workflow state before trusting stored head/CI values.
- If PR #22 head is newer than the source-session engineering head, inspect newer checkpoint/implementation commits first and recompute the Next Task if necessary.
- Load all REQUIRED KRC resources listed above and no broader repository history unless needed to resolve a contradiction.
- Apply the Source of Truth Map and Source of Truth Precedence.
- Confirm that P102 account-surface classification and P103 canary package remain consistent with the current contracts.
- Confirm `CURRENT_HANDOFF.md` is stale relative to P102/P103; report `RECOVERY_CONSISTENCY_WARNING` rather than silently treating P101 as current.
- Confirm no live deployment/configuration resource is required for the P103 repository-only Next Task.
- Do not revalidate VoiceBridge/Render/OCI/provider runtimes merely for recovery of this Next Task.
- Inform the user which repositories were accessible and which REQUIRED resources were read.
- Do not expose or request credentials; no secret transfer is part of recovery.
- No unresolved REQUIRED-source failure may remain.
- `Combined Project Verification=PASS` only when the REQUIRED KRC repository/branch/resources, PR state and cross-source consistency checks pass.
- Recovery must finish before any repository write.

## Combined Project Verification

Source-session generator validation:

```text
K_Research_Critic repository: VERIFIED
K_Research_Critic Active Recovery Branch: VERIFIED
PR #22 engineering head: VERIFIED
PR #22 engineering-head CI: PASS
VoiceBridge repository access: VERIFIED / REFERENCE_ONLY
AI_general repository access: VERIFIED / REFERENCE_ONLY
Required runtime for P103 repo-only task: NONE
Cross-Source Consistency: RECOVERY_CONSISTENCY_WARNING_NON_BLOCKING
  reason=CURRENT_HANDOFF.md remains P101-ready while P102/P103 are newer
Combined Project Verification for bootstrap generation: PASS
```

The recovery session must perform its own verification; it must not inherit this PASS automatically.

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
