# KRC MEDIA — R3 Repository Preview Ready / Builder Entry Stalled — 2026-09-16
Зафіксовано repository-side R3 integration candidate, коректну карту доступів і окремий authenticated browser-capable канал для ChatGPT Builder; стабільний Builder/editor entry ще не підтверджено.

Status: R3 REPOSITORY CANDIDATE / PREVIEW READY / AUTH BLOCKER CLOSED / BUILDER UI PARTIAL / BUILDER ENTRY STALLED / PUBLIC ACTIVATION HOLD

## Repository candidate

Branch: `agent/krc-public-media-r3-integration`.
Draft PR: `#22` — OPEN / DRAFT / UNMERGED.
Canonical files:
- `gpt_store/actions/media_public_r3_openapi.yaml`
- `prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md`
- `tests/test_krc_media_r3_public_integration_candidate.py`

## Accepted routing

- YouTube -> Gemini Developer API Free Tier direct URL; explicit data-use consent before new provider work.
- Instagram -> OCI self-hosted Cobalt -> AssemblyAI universal-2.
- Facebook -> OCI Cobalt video+audio -> server ffmpeg mono PCM WAV 16 kHz -> AssemblyAI universal-2.
- Telegram -> public Telegram web -> AssemblyAI universal-2.

No automatic paid retrieval/STT/proxy, Supadata public fallback, ScrapeCreators public fallback, cookies, or login fallback.

Retry semantics:
```text
COMPLETED -> reuse
PROCESSING in-flight -> reuse / concurrency protection
FAILED free-only -> fresh deterministic retry job on a new explicit retry request
FAILED with paid charge or credit_charge_uncertain -> replay blocked
```
No automatic retry loop is allowed.

## Backend/runtime verification

Relevant KRC infrastructure host: `krc-cobalt`.
Latest read-only runtime evidence from KRC access:
- `/api/v1/health` -> HTTP 200 / `status=ok` / `service=voicebridge-cloud`.
- `/api/v1/media/public-capabilities` without Action bearer -> HTTP 401 Unauthorized, confirming the expected authentication boundary.

No Render mutation was performed.

## Builder/browser access state

Owner approved `R3 BUILDER PREVIEW` only.

Canonical dependency map:
```text
KRC_BUILDER_HOST_DEPENDENCY=NONE
HP_OMEN_DEPENDENCY=NONE
KGM_HOST_DEPENDENCY=NONE
KRC_BACKEND_ACCESS=krc-cobalt
KRC_BACKEND_ACCESS=PASS
```

Sentinel Remote established a dedicated TinyFish Browser Context Profile for KRC Builder access. Its operational profile identifier is not persisted in this repository.

Sentinel Remote confirmed:
```text
KRC_BROWSER_PROFILE=PASS
CHATGPT_AUTH=PASS
MY_GPTS_ACCESS=PASS
KRC_GPT_IDENTIFIED=PASS
BUILDER_UI_CONTROL=PARTIAL
BUILDER_ENTRY=STALLED
AUTH_BLOCKER=CLOSED
HOST_DEPENDENCY=NONE
```

`K-Research & Critic` is identified in My GPTs. No GPT mutation occurred; Save / Update / Publish / Delete were not used.

A later TinyFish call from this KRC work chat was blocked by the OpenAI safety layer before browser execution began. Treat this as a client/tool execution restriction, not an authentication regression.

## Project boundary

- `HP-OMEN` belongs only to K_AI Trading System; never use its state to infer KRC Builder availability.
- `kgm-e4-owner-pilot` belongs only to KGM; never use its state to infer KRC Builder availability.
- `krc-cobalt` is KRC backend/runtime infrastructure; Builder access is a separate account/browser-level control path.

## Safety boundary

```text
PUBLICATION=HOLD
PUBLIC_GPT_CHANGE=DENIED
RENDER_CHANGE=DENIED
MAIN_MUTATION=UNCHANGED
PR45=UNCHANGED
```

PR #22 remains draft/unmerged. Public GPT publication/activation, `main` merge, Render mutation and VoiceBridge PR #45 merge require separate owner authorization.

## Resume point

When stable Builder/editor entry becomes available, execute only in this order:
1. read-only snapshot of current public KRC Builder Instructions / Actions / configuration;
2. confirm the current Core state;
3. import `gpt_store/actions/media_public_r3_openapi.yaml`;
4. append `prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md` without replacing `prompts/GPT_STORE_INSTRUCTIONS.md`;
5. run Builder Preview regression: Core, YouTube, Instagram, Facebook, Telegram;
6. record evidence in the repository;
7. STOP before Publish/Update.
