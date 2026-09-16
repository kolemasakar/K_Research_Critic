# R3 Builder Preview Prepared / UI Access Hold — 2026-09-16
Репозиторний payload для preview інтеграції MEDIA в існуючий public KRC підготовлено; browser authentication підтверджено, але стабільний вхід у Builder/editor ще не досягнуто.

Status: R3_BUILDER_PREVIEW_PREPARED / AUTH_BLOCKER_CLOSED / BUILDER_UI_CONTROL_PARTIAL / BUILDER_ENTRY_STALLED / PUBLIC_ACTIVATION_HOLD

## Authorized scope

Owner approved R3 Builder Preview only.
Allowed: read-only Builder snapshot; add R3 Action schema and compact MEDIA addendum to the existing public KRC draft; preview/regression-test without Publish/Update.
Forbidden: public activation, PR #22 merge, VoiceBridge PR #45 merge, Render mutation, route changes beyond accepted checkpoint 89 contract.

## Preview payload

Action schema:
`gpt_store/actions/media_public_r3_openapi.yaml`

Instruction addendum:
`prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md`

Current Core instructions remain authoritative and unchanged:
`prompts/GPT_STORE_INSTRUCTIONS.md`

## Accepted routing

YouTube -> Gemini Developer API Free Tier direct URL with explicit data-use consent.
Instagram -> OCI Cobalt -> AssemblyAI universal-2.
Facebook -> OCI Cobalt video+audio -> server ffmpeg mono PCM WAV 16 kHz -> AssemblyAI.
Telegram -> public Telegram web -> AssemblyAI universal-2.
No paid/Supadata/ScrapeCreators/cookies/login fallback.

## Retry semantics

COMPLETED -> reuse.
PROCESSING -> reuse / concurrency protection.
FAILED free-only -> fresh deterministic retry job on a new explicit retry request; never auto-loop.
FAILED with paid charge or `credit_charge_uncertain` -> replay blocked.

## Validation

Candidate branch: `agent/krc-public-media-r3-integration`.
The repository candidate has green Python 3.13, Python 3.14 and Quality gates at the latest validated pre-change head; repository policy, GPT Store package validation and coverage are included in those gates.
Builder-size guard for Core instructions plus the R3 addendum is included in candidate tests.

## Builder control channel

KRC Builder access is an account/browser-level control path and has no dependency on KRC backend hosts or on other projects' machines.

Canonical boundary:
```text
KRC_BUILDER_HOST_DEPENDENCY=NONE
HP_OMEN_DEPENDENCY=NONE
KGM_HOST_DEPENDENCY=NONE
KRC_BACKEND_ACCESS=krc-cobalt
KRC_BACKEND_ACCESS=PASS
```

Sentinel Remote established a dedicated TinyFish Browser Context Profile for KRC Builder access. The profile identifier is operational access metadata and is intentionally not persisted in this repository.

Confirmed by Sentinel Remote:
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

The GPT `K-Research & Critic` was identified in My GPTs. No GPT configuration mutation was performed; Save / Update / Publish / Delete were not used.

A later TinyFish invocation from the KRC work chat was blocked by the OpenAI safety layer before a browser run started. This is recorded as a client/tool execution boundary only and does not invalidate the Sentinel-authenticated profile evidence above.

## Project boundary

- `HP-OMEN` belongs only to K_AI Trading System and is irrelevant to KRC Builder availability.
- `kgm-e4-owner-pilot` belongs only to KGM and is irrelevant to KRC Builder availability.
- `krc-cobalt` is the relevant KRC backend/runtime host, not a Builder UI host.

## Next bounded action

When stable Builder/editor entry becomes available:
1. capture a read-only snapshot of current public KRC Instructions / Actions / configuration;
2. import `gpt_store/actions/media_public_r3_openapi.yaml`;
3. append `prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md` without replacing Core instructions;
4. run Builder Preview regression for Core + YouTube + Instagram + Facebook + Telegram;
5. record evidence in the repository;
6. STOP before Publish/Update.

Publication remains HOLD pending separate owner approval.
