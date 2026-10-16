# Recommended Filename
`BOOTSTRAP_PACKAGE_2026-10-16_KRC_GEMINI_FREE_QUOTA_GUARDS.md`

## Recovery Instructions

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

## Project
K-Research & Critic (KRC) MEDIA / VoiceBridge.

## Project Topology
MULTI_REPOSITORY

## Current Phase
Gemini Free quota enforcement — test-only preparation.

## Current Objective
Забезпечити обробку публічних відео без авторизації в соцмережах і платних fallback, з достовірною звітністю та контролем безкоштовних квот.

## Repositories

| Field | Project state | Implementation |
|---|---|---|
| Role | Стан, рішення, acceptance і борги | Код, тести, runtime contract |
| Provider | GitHub | GitHub |
| Owner | kolemasakar | kolemasakar |
| Repository | K_Research_Critic | VoiceBridge |
| Repository Full Name | kolemasakar/K_Research_Critic | kolemasakar/VoiceBridge |
| Default Branch | main | main |
| Active Recovery Branch | agent/krc-public-media-r3-integration | agent/krc-media-gemini-migration |
| Repository URL | https://github.com/kolemasakar/K_Research_Critic | https://github.com/kolemasakar/VoiceBridge |
| Recovery Criticality | REQUIRED | REQUIRED |
| Responsibilities | Політика власника, evidence, release gates | Admission, Gemini provider, durable store, regression |

Default branches підтверджені GitHub metadata 16.10.2026; вони не замінюють Active Recovery Branch.

## Repository Access

| Repository Full Name | Access Method | Source Session Verification Status | Read Capability | Write Capability | Notes |
|---|---|---|---|---|---|
| kolemasakar/K_Research_Critic | GitHub connector | VERIFIED | PASS | PASS: checkpoint02e3c399 | Повторно перевірити в новому чаті |
| kolemasakar/VoiceBridge | GitHub connector; local git fetch | VERIFIED | PASS | PASS: commitc9f5ee7 | Новий чат не успадковує гарантований доступ |

## Source of Truth Map

| Engineering Domain | Authoritative Source |
|---|---|
| Політика, стан, допуски, борги | K_Research_Critic: docs/media/KRC_HANDOFF_STATE_AND_IMPLEMENTATION_DEBT_2026-10-16.md |
| Реалізація, API, схема зберігання і тести | VoiceBridge Active Recovery Branch, baselinec9f5ee7 |
| Спостережені квоти й тарифні екрани | K_Research_Critic: docs/media/KRC_OWNER_BILLING_SCREENSHOT_EVIDENCE_2026-10-16.md |
| Змінні правила провайдера | Офіційні Gemini API rate-limits/billing/video-understanding docs; перевіряти перед використанням |
| Фактично розгорнута версія | Render deployment metadata |

## Source of Truth Precedence
Рішення власника в project-state джерелі визначають дозволені дії. Код визначає реалізовану поведінку; roadmap не доводить реалізацію. Render визначає production SHA, а GitHub HEAD — лише доступний код. Screenshot квот — dated observation, не поточний залишок. Конфлікти, що впливають на Next Task, позначати RECOVERY_CONSISTENCY_WARNING; не виправляти мовчки.

## Current Status
- R4 PRIVATE=PARTIAL; PUBLIC=HOLD; TELEGRAM LIVE=BLOCKED.
- Instagram development=PAUSED. Лише anonymous public video routes; login/cookies/credentials заборонені.
- Авторизований Instagram session-test CANCELLED_NOT_EXECUTED.
- VoiceBridge GitHub baseline: c9f5ee7b9ccccdf407265c7d085cbec42aa553be.
- Render остання перевірка16.10: LIVE65737cfb7e3a89bdaaed95bdf5519d65abae0acf. c9f5ee7 не розгорнутий.
- Нові медіазапуски призупинені до account/quota gates; дозволу на production deploy немає.
- Gemini VoiceBridge screenshot: Free tier;3.7/3.8Flash по5RPM,250000TPM,20RPD.
- AssemblyAI screenshot: Free,$48.27grant remaining,$1.73consumed;Auto-pay і зв'язок робочого ключа з цим акаунтом не підтверджені.

## Completed Work
- Production65737cf: bounded Cobalt HTTP400 diagnostics;284/284 regression PASS.
- Test-onlyc9f5ee7: Gemini start включений у спільний process-local admission;scoped E1–E4 tokens враховані;read-only exempt.
- Public jobs показують provider_billing_verified=false,provider_cost_usd=null,provider_free_balance_usd=null. Legacy retrieval-credit поля не є provider invoice.
- TypeScript PASS;30/30targeted;285/285full regression,без skips/fails;GitHub parity PASS.
- Facebook fresh anonymous route16.10 COMPLETED,167.28s,3segments2630chars,STT168s;окреме читання transcript PASS.
- Два YouTube jobs на6yXU8a5CK2Q завершились503 service_unavailable,без transcript. Не доведено quota або social-login failure.
- Стан та implementation debt збережено checkpoint02e3c399.

## Known Open Engineering Items

| Item | Status | Relevance |
|---|---|---|
| Gemini5RPM/20RPD durable admission,Pacific reset/DST | KNOWN_DEFECT | Загальна60RPM межа не відповідає Gemini; Next Task |
| 250KTPM та8h/day video accounting | OPEN | Unknown duration/tokens не можна вважати0 |
| Restart/multi-instance atomic quota reservations | OPEN | Поточний admission process-local |
| Gemini deployed key→Free VoiceBridge project | RELEASE_GATE | Screenshot не доводить прив'язку ключа |
| AssemblyAI workspace/free grant/Auto-pay verification | RELEASE_GATE | Без нових paid starts |
| Gemini503 root cause і safe telemetry | OPEN | Порожні Render logs;не пояснюється автоматично квотами |
| Model free-eligibility allowlist,retry/backoff policy | DEFERRED | Не розширювати поточний Next Task |
| Production rollout | RELEASE_GATE | Лише окремий допуск після тестів |
| Instagram anonymous retrieval | DEFERRED | Розвиток PAUSED |
| Telegram fresh live acceptance | BLOCKED | LIVE BLOCKED |

## Next Task
Реалізувати й перевірити **durable Gemini request admission для5RPM/20RPD** у тестовому середовищі: атомарне резервування перед фактичним provider call, спільний облік моделі/проєкту для KRC, відновлення після restart, добовий reset у America/Los_Angeles з DST, dedup без повторного списання та fail-closed при недоступному сховищі. Перевірити межі5/6 і20/21,minute boundary,Pacific midnight/DST та конкурентні reservations. Без live calls,deploy,сесій соцмереж. TPM/video-hour guards залишаються окремим незакритим боргом; цей task не дає повного FREE_ONLY acceptance.

## Required Repository Resources

### kolemasakar/K_Research_Critic
Branch: agent/krc-public-media-r3-integration. Recovery Criticality: REQUIRED.
- docs/media/KRC_HANDOFF_STATE_AND_IMPLEMENTATION_DEBT_2026-10-16.md
- docs/media/KRC_OWNER_BILLING_SCREENSHOT_EVIDENCE_2026-10-16.md

### kolemasakar/VoiceBridge
Branch: agent/krc-media-gemini-migration. Recovery Criticality: REQUIRED.
Baseline: c9f5ee7b9ccccdf407265c7d085cbec42aa553be; перевірити нові commits перед роботою.
- docs/media/KRC_YOUTUBE_ADMISSION_AND_BILLING_VISIBILITY_2026-10-16.md
- src/cloud/src/public_media_admission.ts
- src/cloud/src/public_gemini_youtube.ts
- src/cloud/src/managed_server.ts
- src/cloud/src/config.ts
- src/cloud/src/managed_media_persistence.ts
- src/cloud/src/managed_media_service.ts
- src/cloud/tests/r2a_public_free_tier.test.ts
- src/cloud/tests/public_gemini_youtube.test.ts
- src/cloud/package.json
Завантажити прямі імпорти durable store/schema/migrations/tests лише коли вони потрібні для quota reservation. Перевірити AGENTS.md у recovery checkout.

## Recovery Verification Requirements
- Незалежно перевірити identity,default і active branches обох REQUIRED репозиторіїв.
- Прочитати мінімальні ресурси;повідомити користувачу фактичний доступ і прочитані файли по репозиторіях.
- Застосувати domain authority;звірити state docs,c9f5ee7 поведінку й наявні schema/tests.
- Runtime не REQUIRED для offline Next Task. Якщо потрібен runtime — спочатку read-only revalidation;не використовувати історичні jobs як current.
- Недоступність або невідповідність REQUIRED source блокує Recovery Complete.
- Combined Project Verification=PASS лише коли всі REQUIRED sources та checks пройдено.
- Recovery read-only. Реалізацію починати лише після завершення recovery та в межах явного дозволу користувача на запис.
- Не робити нових припущень про permissions,provider credentials чи billing entitlement.

## Recovery Status
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

## Workspaces
Path: /workspace/scratch/60e98122881e/VoiceBridge.
Role: source-session test checkout;GitRepository=kolemasakar/VoiceBridge.
SourceSessionVerification: localHEAD65737cf,tracked edits і документ уже відповідають GitHubc9f5ee7;не дублювати commit. RequiredForNextTask=NO;створити чистий checkout від remote branch. Scratch path може зникнути.

## Runtime / Infrastructure
Provider=Render;Service=VoiceBridge;ServiceID=srv-da1kic5bedkc73d6fk60;Workspace=tea-d9dsqdjrjlhs73ba1ga0;Environment=production.
Endpoint: не потрібний для offline Next Task;дізнаватися з provider metadata лише за потреби.
DeploymentSource=VoiceBridge agent/krc-media-gemini-migration.
LastVerified=2026-10-16 during checkpoint;LIVEdep-db8v5g3rjlhs73dlhhm0,commit65737cf.
RecoveryCriticality=REFERENCE_ONLY;RequiresRevalidation=YES перед runtime висновками/діями.

## Deployment Boundary
ActiveTestTarget=isolated checkout/fixtures. ProductionTarget=Render VoiceBridge.
PublicReleaseTarget=HOLD. AllowedRecoveryTarget=read-only GitHub і необхідні resources.
ProhibitedTargets=production mutation,provider starts,paid fallback,Instagram login/cookies,Telegram LIVE.
Наявність старої Gemini Free згоди не скасовує поточну паузу запусків.

## Ephemeral / Expiring Resources
Media jobs мають TTL default1h;історичні404 не доводять database loss.
DeployID,job state,logs,local checkouts та sessions: Do Not Assume Current; verify before reuse.
Не потрібні для Next Task;не повторювати live jobs для recovery.

## Temporary Artifact Handling
PERSISTENT:GitHub commits,state checkpoint,quota screenshot interpretation,bootstrap.
TEMPORARY_BUT_ACTIVE:source-session scratch checkout/build outputs;не REQUIRED.
Raw screenshot originals залишаються у вкладеннях власника;email,billing IDs,keys не переносити.
