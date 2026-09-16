# KRC MEDIA — R3 Repository Preview Ready / Builder Access Blocked — 2026-09-16
Зафіксовано завершення repository-side R3 integration candidate, виправлення карти доступів та вибір окремого browser-capable каналу для ChatGPT Builder.

Status: R3 REPOSITORY CANDIDATE / PREVIEW READY / BROWSER CHANNEL SELECTED / USER CONNECT PENDING / PUBLIC ACTIVATION HOLD

## Accepted repository candidate

Branch: `agent/krc-public-media-r3-integration`
Accepted pre-preview head: `445a6d59ac3365b31634ba957181a052ea88f2e4`
Draft PR: `#22` — OPEN / DRAFT / UNMERGED

CI run `35089649341`:
- Python 3.13: PASS
- Python 3.14: PASS
- Repository policy: PASS
- GPT Store package: PASS
- Coverage gate: PASS

## R3 candidate files

- `gpt_store/actions/media_public_r3_openapi.yaml`
- `prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md`
- `tests/test_krc_media_r3_public_integration_candidate.py`

## Canonical routing

- YouTube -> Gemini Developer API Free Tier direct URL; explicit data-use consent before new provider work.
- Instagram -> OCI self-hosted Cobalt -> AssemblyAI universal-2.
- Facebook -> OCI Cobalt video+audio -> server ffmpeg mono PCM WAV 16 kHz -> AssemblyAI universal-2.
- Telegram -> public Telegram web -> AssemblyAI universal-2.

No automatic paid retrieval/STT/proxy, Supadata public fallback, ScrapeCreators public fallback, cookies, or login fallback.

Retry semantics: COMPLETED and PROCESSING reuse; FAILED free-only may create a fresh deterministic retry on a new explicit retry request; paid or charge-uncertain replay remains blocked.

## Live runtime revalidation

From authorized `krc-cobalt` RDC host:
- `/api/v1/health` -> HTTP 200 / `status=ok` / `service=voicebridge-cloud`.
- `/api/v1/media/public-capabilities` without Action bearer -> HTTP 401 Unauthorized, confirming the expected authentication boundary.

No Render mutation was performed.

## Builder access state

Owner explicitly approved `R3 BUILDER PREVIEW` on 2026-09-16.

KRC-relevant remote infrastructure:
- `krc-cobalt` — KRC host / backend and runtime verification access.

Project-boundary correction:
- `HP-OMEN` belongs to **K_AI Trading System**; it is not KRC infrastructure and is not a KRC Builder dependency.
- `kgm-e4-owner-pilot` belongs to **KGM**; it is not a KRC Builder dependency.
- Cross-project host availability must not be used to infer KRC Builder availability.

The current KRC RDC capability provides server filesystem/terminal access, not interactive control of the authenticated ChatGPT Builder UI. The Builder blocker is therefore a **browser/UI-control capability gap**, not an offline-host condition.

Selected remediation channel: **TinyFish ChatGPT plugin**, because it exposes a live browser workflow with navigation, clicking, form interaction, and web-app state inspection.

Channel state:
- `KRC_BUILDER_HOST_DEPENDENCY=NONE`
- `KRC_BACKEND_ACCESS=krc-cobalt`
- `KRC_BACKEND_ACCESS=PASS`
- `KRC_BUILDER_BROWSER_CHANNEL=TinyFish`
- `KRC_BUILDER_BROWSER_CHANNEL_STATE=PENDING_USER_INSTALL_OR_CONNECT`
- `PUBLIC_ACTIVATION=HOLD`

Security boundary:
- OpenAI login remains inside the authorized browser session; credentials are not to be copied into repository files, shell history, or KRC infrastructure.
- TinyFish is a browser-control capability, not a KRC infrastructure host.
- No cross-project workstation is a prerequisite for Builder access.

## Safety boundary

No public GPT publication/activation occurred.
No merge of PR #22 or VoiceBridge PR #45 occurred.
No change to `K_Research_Critic/main` occurred.
No Render deploy/runtime change occurred.

## Resume point

After the owner installs/connects TinyFish, resume with:
1. read-only snapshot of the current public KRC Builder instructions/actions;
2. import `gpt_store/actions/media_public_r3_openapi.yaml` as preview Action;
3. append `prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md` without replacing Core instructions;
4. run preview regression: ordinary Core KRC + YouTube + Instagram + Facebook + Telegram;
5. stop before Publish/Update and keep publication/activation HOLD until separate owner approval.
