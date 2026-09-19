# KRC — GPT-to-Plugin Migration Inventory — 2026-09-16
Зафіксовано повний repository-side inventory поточного public KRC та R3 MEDIA candidate для майбутньої міграції у Plugin без передчасної зміни чинного GPT.

Status: MIGRATION_INVENTORY_READY / MIGRATION_NOT_AUTHORIZED / PUBLICATION_HOLD

## Current public KRC identity

Source: `gpt_store/manifest.yaml`

```text
name=K-Research & Critic
default_language=uk-UA
primary_channel=chatgpt_store
publication_state=published
store_category=Research & Analysis
```

Current native capabilities:
```text
web_search=true
code_interpreter_data_analysis=true
image_generation=false
apps=false
actions=false
```

Current Knowledge configuration:
```text
knowledge.required=false
knowledge.files=[]
```

Therefore there are no current public GPT Knowledge files requiring migration parity.

## Authoritative Core asset

Canonical instructions:
`prompts/GPT_STORE_INSTRUCTIONS.md`

Current manifest instruction version:
`2.2-request-log-disabled-runtime-accepted`

Core behaviors that must survive migration:
- Ukrainian default reporting;
- CriticProfile two-stage/direct gate semantics;
- risk-based cross-check floors;
- independent-source accounting;
- claim-level cross-check ledger/output;
- traceability and shortfall disclosure;
- localized report labels;
- checkpoint/recovery contract;
- Core workflow must remain independent of optional MEDIA failures.

Planned migration mapping:
`GPT_STORE_INSTRUCTIONS.md -> Plugin skill baseline`

## Current public request-log state

Request-log prototype remains retained but public runtime is disabled because external Action consent disrupted public UX.

Migration requirement:
- do not silently re-enable request logging;
- preserve `public_enabled_target=false` unless separately authorized;
- logging failure must never block Core.

## Conversation starters / representative Core prompts

Preserve representative tests for:
- research topic + CriticProfile approval;
- comparison of two technologies with independent sources;
- claim verification with supporting/contradicting evidence;
- task resume from KRC checkpoint;
- equivalent English-language cases.

OpenAI migration guidance warns that conversation starters and previous chats may not copy, so these are regression fixtures rather than assumed migration output.

## R3 MEDIA candidate assets

MEDIA is not active in the current public manifest and therefore should be treated as a new integration for the replacement architecture, not as an automatically transferable production Action.

Canonical candidate assets:
- `gpt_store/actions/media_public_r3_openapi.yaml`
- `prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md`
- `subprojects/media_beta/91_R3_BUILDER_PREVIEW_REGRESSION_PLAN_2026_09_16.md`
- `subprojects/media_beta/96_R3_MEDIA_ACTION_TO_PLUGIN_MCP_COMPATIBILITY_MAP_2026_09_16.md`

## MEDIA representative fixtures

YouTube:
- select a supported public URL at execution time;
- mandatory Gemini Free preflight and explicit data-use consent.

Instagram accepted control:
`https://www.instagram.com/reel/DF1CIrPSVmf/`

Facebook accepted control:
`https://www.facebook.com/reel/636216875539019`

Telegram success control:
`https://t.me/techcrimes/12107`

Telegram failure/retry fixture:
`https://t.me/techcrimes/12101`

Fixtures must be revalidated for public availability at execution time.

## Expected MEDIA provider matrix

```text
YouTube   -> Gemini Developer API Free Tier direct URL
Instagram -> OCI self-hosted Cobalt -> AssemblyAI universal-2
Facebook  -> OCI Cobalt video+audio -> server ffmpeg mono PCM WAV 16 kHz -> AssemblyAI universal-2
Telegram  -> public Telegram web -> AssemblyAI universal-2
```

No automatic paid retrieval/STT/proxy, Supadata public fallback, ScrapeCreators public fallback, cookies, or login fallback.

## Replacement-plugin regression inventory

Core regression:
1. CriticProfile direct-run path.
2. CriticProfile review path.
3. independent-source cross-check floor by risk.
4. claim-level ledger and traceability.
5. checkpoint/recovery behavior.
6. web-search research case.
7. data-analysis case where appropriate.
8. Ukrainian and English response behavior.

MEDIA regression:
1. capabilities/free-only state;
2. YouTube preflight without provider call;
3. YouTube explicit consent gate;
4. YouTube direct Gemini route;
5. Instagram Cobalt route;
6. Facebook video+audio + ffmpeg normalization;
7. Telegram success path;
8. Telegram FAILED free-only explicit retry path;
9. COMPLETED/PROCESSING reuse;
10. paid/credit-uncertain replay blocked;
11. MEDIA failure isolation from Core;
12. no secret leakage.

## Migration-specific checks

OpenAI guidance requires explicit validation because migrated plugins may behave differently.

Verify after migration:
- correct skill selection;
- Core instructions preserved semantically;
- reference assets/tools available as intended;
- native web/data-analysis workflow still works on supported surface;
- selected model differences do not alter required KRC protocol;
- sharing/access of replacement matches intended audience;
- custom MEDIA integration is rebuilt and tested rather than assumed transferred.

## Current platform boundary

```text
CUSTOM_GPT_RETIREMENT_PREP=ACTIVE
MIGRATION_INVENTORY=READY
CORE_TO_PLUGIN_SKILL_MAP=READY
MEDIA_ACTION_TO_MCP_MAP=READY
GPT_MIGRATION=NOT_AUTHORIZED
PLUGIN_APP_IMPLEMENTATION=NOT_AUTHORIZED
PLUGIN_PUBLICATION=NOT_AUTHORIZED
PUBLICATION=HOLD
MAIN_MUTATION=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```

## Next preparation step

Wait for the account-specific GPT migration option or explicit owner authorization to begin plugin/app implementation. When either condition is met, inspect the actual migration surface first and derive the implementation plan from the available plugin/app permissions rather than assuming Enterprise-only controls apply.
