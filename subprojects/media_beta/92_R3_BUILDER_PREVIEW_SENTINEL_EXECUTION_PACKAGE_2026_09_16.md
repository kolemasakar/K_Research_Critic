# KRC MEDIA — R3 Builder Preview Sentinel Execution Package — 2026-09-16
Пакет фіксує делегований сценарій виконання Builder Preview через private Sentinel Remote без публікації або production-активації.

Status: READY_FOR_SENTINEL_EXECUTION / BUILDER_ENTRY_STALLED / PUBLICATION_HOLD

## Control boundary

```text
profile_alias=KRC_CHATGPT_BUILDER
profile_id_storage=PRIVATE_SENTINEL_REMOTE_ONLY
KRC_CHAT_TINYFISH_FALLBACK=DELEGATE_TO_SENTINEL_REMOTE
HOST_DEPENDENCY=NONE
AUTH_BLOCKER=CLOSED
BUILDER_UI_CONTROL=PARTIAL
BUILDER_ENTRY=STALLED
```

The real Browser Context Profile identifier, cookies, session material, bearer tokens, API keys and signed media URLs must never be committed to this repository or copied into public evidence.

## Canonical inputs

Repository: `kolemasakar/K_Research_Critic`
Branch: `agent/krc-public-media-r3-integration`
Action schema: `gpt_store/actions/media_public_r3_openapi.yaml`
Instruction addendum: `prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md`
Core instructions: `prompts/GPT_STORE_INSTRUCTIONS.md`
Regression plan: `subprojects/media_beta/91_R3_BUILDER_PREVIEW_REGRESSION_PLAN_2026_09_16.md`

Core remains authoritative and must not be replaced.

## Sentinel execution order

1. Open the existing owner-authenticated `K-Research & Critic` GPT using private profile alias `KRC_CHATGPT_BUILDER`.
2. Capture a read-only snapshot of visible Builder identity, Instructions, Actions and relevant configuration before any edit.
3. Confirm that the current public GPT is the expected KRC identity and that Core instructions can be preserved.
4. Import the R3 OpenAPI schema as the MEDIA Action using the existing authorized bearer configuration; never expose the bearer value.
5. Append the R3 MEDIA addendum to the existing Core instructions; do not rewrite or replace Core.
6. Confirm the Builder accepts the draft configuration without requiring Publish/Update.
7. Execute checkpoint 91 regressions in order: Core, YouTube, Instagram, Facebook, Telegram.
8. Record only non-secret evidence and return it to KRC for repository checkpointing.
9. STOP before any Save/Update/Publish action that would alter the published GPT.

## Required returned evidence

Return only:
- Builder entry result and whether the expected KRC GPT was opened;
- pre-edit snapshot summary without secrets;
- whether schema import was accepted;
- whether addendum was appended while Core stayed intact;
- preview result for Core and each of the four MEDIA routes;
- provider mode/retrieval provider/status/credit fields where returned;
- confirmation that no paid or unapproved fallback occurred;
- confirmation that no Publish/Update/Delete action was executed;
- any blocker encountered, with the exact stage where execution stopped.

Do not return the actual Browser Context Profile identifier or authentication/session material to the public repository.

## Immediate STOP conditions

Apply all STOP conditions from checkpoint 91. Additionally stop immediately if:
- Builder identity is ambiguous or not the expected `K-Research & Critic` GPT;
- the browser session requests re-authentication that would require exposing credentials outside the private Sentinel path;
- importing the Action requires replacing an unknown existing Action without a recoverable snapshot;
- any operation would change the published GPT before regression evidence is complete.

## Release boundary

```text
R3_REPOSITORY=READY
R3_PREVIEW_PAYLOAD=READY
R3_REGRESSION_PLAN=READY
AUTH_BLOCKER=CLOSED
BUILDER_UI_CONTROL=PARTIAL
BUILDER_ENTRY=STALLED
PUBLICATION=HOLD
MAIN_MUTATION=DENIED
RENDER_CHANGE=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
STOP_BEFORE_PUBLISH_UPDATE=TRUE
```
