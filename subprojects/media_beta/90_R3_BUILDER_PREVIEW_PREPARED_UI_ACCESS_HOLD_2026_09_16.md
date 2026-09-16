# R3 Builder Preview Prepared / UI Access Hold — 2026-09-16
Репозиторний payload для preview інтеграції MEDIA в існуючий public KRC підготовлено та перевірено; публічна активація не виконувалась.

Status: R3_BUILDER_PREVIEW_PREPARED / UI_ACCESS_HOLD / PUBLIC_ACTIVATION_HOLD

## Authorized scope

Owner approved R3 Builder Preview only.
Allowed: add R3 Action schema and compact MEDIA addendum to the existing public KRC draft, then preview/regression-test without Publish/Update.
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
PROCESSING -> reuse.
FAILED free-only -> one fresh deterministic retry only after a new explicit retry request.
Paid or charge-uncertain replay -> blocked.

## Validation

Candidate branch: `agent/krc-public-media-r3-integration`.
Repository candidate CI at accepted pre-preview head was green for Python 3.13, Python 3.14, repository policy, GPT Store package validation, and coverage gate.
Builder-size guard for Core instructions plus the R3 addendum is included in the candidate tests.

## Current blocker

The blocker is **not a KRC host outage**. The current KRC remote-control channel provides server filesystem/terminal access but does not expose interactive control of the authenticated ChatGPT Builder UI. Therefore no Builder fields were edited and no draft was saved.

`HP-OMEN` is the Windows development host for **K_AI Trading System** and is not part of KRC infrastructure or KRC Builder access. Its online/offline state is irrelevant to KRC R3 Builder Preview.

`kgm-e4-owner-pilot` belongs to **KGM** and likewise is not a KRC Builder dependency.

Relevant KRC infrastructure access remains through `krc-cobalt`; that access is sufficient for backend/runtime verification but not for ChatGPT Builder UI interaction.

## Next bounded action

When an authorized browser-capable ChatGPT Builder control path is available, open the existing public `K-Research & Critic` GPT, snapshot current Builder state, append the R3 MEDIA addendum, import the R3 OpenAPI schema as the MEDIA Action, validate authentication/configuration without provider work where possible, run Core + YouTube + Instagram + Facebook + Telegram preview regressions, and stop before Publish/Update.
