# KRC MEDIA — R3 Action-to-Plugin/MCP Compatibility Map — 2026-09-16
Зафіксовано repository-side parity map для перенесення MEDIA інтеграції з Custom GPT Actions у майбутній Plugin/App/MCP шар без зміни accepted R2/R3 semantics.

Status: COMPATIBILITY_MAP_READY / IMPLEMENTATION_NOT_AUTHORIZED / PUBLICATION_HOLD

## Principle

Custom GPT Actions do not automatically transfer through the planned GPT-to-Plugin migration. The future integration must be rebuilt and regression-tested.

Baseline migration rule:
- preserve operation semantics first;
- preserve free-only/fail-closed policy;
- preserve durable job/retry behavior;
- preserve explicit Gemini Free consent;
- optimize or consolidate tools only after parity is demonstrated.

## Canonical source

OpenAPI source:
`gpt_store/actions/media_public_r3_openapi.yaml`

Backend remains:
`https://voicebridge-krc-media-beta-kolemasakar.onrender.com`

No backend or Render mutation is authorized by this document.

## Operation compatibility map

| Current Action operation | Current purpose | Future app/MCP baseline |
| --- | --- | --- |
| `getPublicMediaCapabilities` | Read routing/safety state | read-only capability tool |
| `preflightPublicGeminiYoutube` | Validate YouTube URL and return Gemini Free disclosure | read-only/preflight tool; must not call Gemini |
| `lookupPublicGeminiYoutubeJob` | Find reusable durable YouTube job | read-only lookup tool |
| `startPublicGeminiYoutubeTranscription` | Start/retry Gemini Free direct processing | execution tool gated by explicit Gemini Free consent |
| `getPublicGeminiYoutubeJob` | Read YouTube durable job status | read-only status tool |
| `getPublicGeminiYoutubeSegments` | Read paginated YouTube transcript | read-only transcript tool |
| `preflightPublicInstagramCobalt` | Validate Instagram Cobalt route | read-only/preflight tool |
| `lookupPublicInstagramCobaltJob` | Find reusable durable Instagram job | read-only lookup tool |
| `startPublicInstagramCobaltTranscription` | Start/retry Instagram Cobalt + AssemblyAI | execution tool preserving free-only retry semantics |
| `startPublicFacebookCobaltTranscription` | Start/retry Facebook video+audio -> ffmpeg -> AssemblyAI | execution tool preserving canonical normalization path |
| `startPublicTelegramTranscription` | Start/retry Telegram public web + AssemblyAI | execution tool preserving public/no-login route |
| `getPublicNonYoutubeMediaJob` | Read Instagram/Facebook/Telegram job status | read-only shared status tool |
| `getPublicNonYoutubeMediaSegments` | Read paginated non-YouTube transcript | read-only shared transcript tool |

## Required policy invariants

The future app/MCP integration must preserve:
```text
paid_retrieval_fallback=false
paid_stt_fallback=false
paid_proxy_fallback=false
supadata_public_active=false
scrapecreators_public_active=false
cookie_login_fallback=false
```

Platform routing remains:
```text
YouTube   -> Gemini Developer API Free Tier direct URL
Instagram -> self-hosted Cobalt -> AssemblyAI universal-2
Facebook  -> Cobalt video+audio -> server ffmpeg mono PCM WAV 16 kHz -> AssemblyAI
Telegram  -> public Telegram web -> AssemblyAI universal-2
```

## Consent invariant

YouTube provider work must not start until the user has explicitly acknowledged the Gemini Free data-use boundary.

Equivalent future request contract must retain:
```text
provider=google_gemini
tier=free
data_use_acknowledged=true
```

Preflight must remain safe to call before consent and must not invoke Gemini provider work.

## Durable retry invariant

```text
COMPLETED -> reuse
PROCESSING -> reuse / concurrency protection
FAILED free-only -> fresh deterministic retry only on a new explicit retry request
FAILED with paid charge or credit_charge_uncertain -> replay blocked
NO automatic retry loop
```

Future tools must return enough state to audit at least:
- status;
- provider/provider_mode;
- retrieval_provider;
- retrieval credits;
- STT seconds where applicable;
- segment count/transcript presence;
- reused;
- credit_charge_uncertain;
- structured error when failed.

## Platform-specific hard guards

YouTube:
- no Cobalt fallback;
- no AssemblyAI fallback;
- no paid Gemini/proxy/Supadata/ScrapeCreators/cookie-login fallback.

Facebook:
- canonical retrieval is Cobalt video+audio;
- server-side ffmpeg normalization is mono PCM WAV 16 kHz;
- unsupported Cobalt only-audio path must not become canonical.

Telegram:
- public web retrieval only;
- no Telegram login/session/bot-token fallback.

Instagram:
- Cobalt route remains Instagram-only in the generic managed path;
- YouTube must not leak into this route.

## Authentication boundary

The current Action uses server-side bearer authentication. A future app/MCP implementation must select an authentication mechanism supported by the target plugin/app surface without exposing bearer values in skills, repository evidence, model-visible output, or logs.

Authentication design is not finalized by this checkpoint.

## Regression parity gate

Before any switch from the existing GPT to a replacement plugin/app, verify:
1. ordinary non-media Core KRC behavior;
2. capability/free-only state;
3. YouTube consent + direct Gemini route;
4. Instagram Cobalt route;
5. Facebook video+audio + ffmpeg normalization route;
6. Telegram public-web route;
7. durable reuse/retry semantics;
8. no paid/unapproved fallback;
9. MEDIA failure isolation from Core;
10. no secret leakage.

## Current boundary

```text
PLUGIN_MIGRATION_PREP=READY
MEDIA_ACTION_TO_MCP_MAP=READY
PLUGIN_APP_IMPLEMENTATION=NOT_AUTHORIZED
PLUGIN_MIGRATION=NOT_AUTHORIZED
PLUGIN_PUBLICATION=NOT_AUTHORIZED
GPT_BUILDER_BYPASS=STOPPED
BROWSER_AUTOMATION_START=BLOCKED_BY_OPENAI_SAFETY_LAYER
PUBLICATION=HOLD
MAIN_MUTATION=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

## Next preparation step

Prepare a plugin migration inventory for Core instructions, reference files, representative prompts, MEDIA test fixtures, and expected outputs. Do not implement or publish a plugin until the owner authorizes that phase and account-specific migration availability is confirmed.
