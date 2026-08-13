# GPT_STORE_DEPLOYMENT
Документ визначає основну GPT Store-модель розгортання K_Supervisor без обов'язкового developer API key.

Version: 1.1
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

The Store package maps research to built-in Web search and Code Interpreter & Data Analysis when those capabilities are available to the current user. Capability absence must produce an explicit limitation rather than fabricated tool use.

## 3. Store Package

The publication-ready repository package is defined by:

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
docs/GPT_STORE_PACKAGE.md
```

The package state is:

```text
ready_for_manual_publication_test
```

This state means the repository package and static validation are complete. It does not mean the GPT has already been published in the GPT Store.

## 4. Free and Paid User Behavior

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

## 5. No Developer Secret in the Store Edition

The GPT Store edition does not require:

```text
OPENAI_API_KEY
SEARCH_API_KEY
DATABASE_URL
```

These environment variables remain supported only by optional standalone/server integrations.

A Store release must not embed developer secrets in GPT instructions, knowledge files, configuration text, or user-visible artifacts.

The core Store manifest keeps Apps and Actions disabled, so no third-party API or Action privacy-policy dependency is required by the package.

## 6. Persistence and Memory Boundary

Custom GPT conversations do not use previous GPT conversations, saved memory, or user custom instructions as workflow state.

The Store edition therefore uses conversation-local state plus explicit checkpoint/recovery artifacts for continuity across chats.

Checkpoint marker:

```text
K_SUPERVISOR_CHECKPOINT
```

Checkpoint schema version:

```text
1.0
```

Only safe orchestration boundaries may be checkpointed. Ambiguous mid-agent states are not replayed automatically.

The existing SQLite persistence layer remains part of the optional standalone/API edition and local engineering/test environment.

## 7. Optional Standalone/API Edition

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

The OpenAI provider adapter implemented in Phase 11.3 remains an optional adapter for standalone/server execution, development, integration testing, and future external products.

## 8. Architecture Invariants

Both editions preserve:

- Supervisor orchestration semantics;
- explicit CriticProfile user approval;
- approved profile immutability;
- Research-Critic revision loop;
- evidence and source discipline;
- PASS/REVISE separation from execution status;
- explicit failure/limitation states;
- no hidden chain-of-thought persistence.

The Store Edition implements Research and Critic as separated logical passes inside one ChatGPT runtime. It does not claim process-isolated or model-isolated agent instances.

Deployment-specific infrastructure must not change the workflow contracts.

## 9. Publication Requirements

Before GPT Store publication:

- use the approved manifest and instruction package;
- enable Web search and Code Interpreter & Data Analysis;
- keep Apps and Actions disabled for the core package;
- leave Recommended model unset;
- do not require an external backend for the free core experience;
- run the GPT Builder Preview test matrix;
- verify the workflow on a Free account and at least one paid account;
- verify that model switching does not break workflow semantics;
- verify fresh-chat behavior and checkpoint recovery;
- complete Builder Profile/category/policy requirements when prompted;
- review current OpenAI GPT Store publication requirements immediately before release.

Actual Store publication and live plan-account validation are manual release operations. Repository CI cannot substitute for those ChatGPT UI/account checks.

## 10. Platform Assumptions

Platform assumptions were re-verified on 2026-08-13 against current OpenAI Help Center documentation:

```text
https://help.openai.com/en/articles/8554407-gpts-in-chatgpt
https://help.openai.com/en/articles/8554397-create-a-gpt
https://help.openai.com/en/articles/8798878
```

Current relevant facts include:

- signed-in users can use GPTs they have access to;
- creating/editing GPTs requires an eligible paid plan and is performed on the web;
- Recommended model is optional and users may switch when additional models are available;
- public Store publishing can require Builder Profile/category/policy checks;
- public Actions require a valid Privacy Policy URL;
- GPT builders cannot view individual user conversations;
- GPTs start fresh across separate conversations and do not use saved memory, custom instructions, or previous GPT conversations.

OpenAI may change plan availability, model names, model picker behavior, capabilities, or GPT Store rules. These platform facts must be re-verified immediately before public release.

## 11. Validation

Static package validation:

```text
python -m scripts.validate_store_package
python -m pytest
```

Phase 11.7 implementation validation:

```text
Validated head: fb0d84468dddab88f15f425fda217cbabe1b057f
GitHub Actions: 31666028204
156 tests passed
```

Manual publication/Free-plan/paid-model-switch tests remain release gates and are intentionally not represented as completed repository CI checks.
