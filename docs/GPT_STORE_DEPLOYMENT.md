# GPT_STORE_DEPLOYMENT
Документ визначає основну GPT Store-модель розгортання K_Supervisor без обов'язкового developer API key.

Version: 1.0
Status: ACTIVE

## 1. Decision

K_Supervisor is GPT Store-first.

The primary public edition is a Custom GPT distributed through ChatGPT and intended to remain usable by signed-in users whose plan allows access to public GPTs, including the Free plan where the platform makes GPT access available.

The primary edition must not require a developer-owned OpenAI API key, a mandatory external backend, or a pinned API model.

## 2. Primary Runtime: GPT Store Edition

The primary runtime policy is:

```text
channel: chatgpt_store
model_policy: user_plan
developer_api_key_required: false
external_backend_required: false
recommended_model: null
allow_user_model_switch: true
```

`recommended_model: null` is intentional. K_Supervisor does not pin a model identifier that may later be retired or unavailable to a user. ChatGPT selects an available model according to the user's account and current platform behavior. Users with additional model choices may switch to another available model.

The GPT Store edition should prefer ChatGPT built-in capabilities, such as web search and data analysis, when they are enabled and available to the user.

## 3. Free and Paid User Behavior

K_Supervisor does not implement plan detection or billing logic.

Expected platform behavior is:

```text
Free user
  -> model/capabilities available to that user in ChatGPT
  -> K_Supervisor workflow

Paid user
  -> the same K_Supervisor workflow
  -> optional switch to additional models exposed by the user's plan
```

The workflow and CriticProfile rules must not depend on a specific named ChatGPT model.

## 4. No Developer Secret in the Store Edition

The GPT Store edition does not require:

```text
OPENAI_API_KEY
SEARCH_API_KEY
DATABASE_URL
```

These environment variables remain supported only by optional standalone/server integrations.

A Store release must not embed developer secrets in GPT instructions, knowledge files, configuration text, or user-visible artifacts.

## 5. Persistence Boundary

Custom GPT conversations do not provide the same server-side SQLite runtime used by the Python reference implementation.

Therefore the Store edition uses conversation-local workflow state plus explicit checkpoint/recovery artifacts when continuity across chats is needed.

The existing SQLite persistence layer remains part of the optional standalone/API edition and local engineering/test environment.

## 6. Optional Standalone/API Edition

The existing Python runtime is retained as an optional deployment profile:

```text
K_Supervisor Core
  |
  +-- GPT Store Edition       PRIMARY
  |     - ChatGPT-managed model
  |     - no developer API key
  |     - no mandatory backend
  |
  +-- Standalone/API Edition  OPTIONAL
        - Python runtime
        - SQLite persistence
        - provider factory
        - provider API keys when required
```

The OpenAI provider adapter implemented in Phase 11.3 is not deleted. It is an optional adapter for standalone/server execution, development, integration testing, and future external products.

## 7. Architecture Invariants

Both editions preserve:

- Supervisor orchestration semantics;
- explicit CriticProfile user approval;
- approved profile immutability;
- Research-Critic revision loop;
- evidence and source discipline;
- PASS/REVISE separation from execution status;
- explicit failure/limitation states;
- no hidden chain-of-thought persistence.

Deployment-specific infrastructure must not change those workflow contracts.

## 8. Publication Requirements

Before GPT Store publication:

- create the Custom GPT instructions package from the approved architecture;
- enable only required built-in ChatGPT capabilities;
- do not require an Action or external backend for the free core experience;
- do not pin a model identifier as a hard runtime dependency;
- verify the workflow on a Free account and at least one paid account;
- verify that model switching does not break workflow semantics;
- verify fresh-chat behavior and checkpoint recovery;
- review current OpenAI GPT Store publication requirements immediately before release.

## 9. Platform Assumptions

Platform assumptions in this document were verified on 2026-08-13 against OpenAI Help Center documentation:

```text
https://help.openai.com/en/articles/8554407-gpts-in-chatgpt
https://help.openai.com/en/articles/8554397-creating-and-editing-gpts
https://help.openai.com/en/articles/8798878-sharing-and-publishing-gpts
```

OpenAI may change plan availability, model names, model picker behavior, or GPT Store rules. These platform facts must be re-verified before public release.
