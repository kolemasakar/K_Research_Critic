# GPT_STORE_PACKAGE
Документ визначає пакет, налаштування та ручні release-gates для публікації K_Supervisor у GPT Store.

Version: 1.0
Status: ACTIVE

## 1. Purpose

This document is the operator-facing packaging specification for the public K_Supervisor Custom GPT.

The package is designed for the GPT Store-first product decision:

```text
no developer API key
no mandatory external backend
no Actions
no Apps
no pinned model
user-plan model policy
built-in ChatGPT capabilities only for the core path
```

## 2. Package Files

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
docs/GPT_STORE_PACKAGE.md
```

The manifest is the human/machine-readable builder configuration source. The instruction file is intended to be pasted into the GPT Builder Instructions field. The checkpoint contract provides a tested engineering representation of the cross-chat continuity format.

## 3. Builder Configuration

Use these values from `gpt_store/manifest.yaml`.

### Name

```text
K_Supervisor
```

### Description

```text
Research supervisor that plans evidence-based work, asks you to approve its critic criteria, independently verifies claims, revises weak drafts, and produces a final report with sources, uncertainty, and review status.
```

### Recommended model

Leave the recommended model unset.

The workflow must not depend on a named model. Users may use or switch among models available to their ChatGPT plan when the platform exposes alternatives.

### Capabilities

Enable:

```text
Web search
Code Interpreter & Data Analysis
```

Disable for the core package:

```text
Image generation
Apps
Actions
```

Web search is the preferred path for fresh public evidence. Data analysis is useful for calculations and structured evidence work. The instructions contain graceful-degradation behavior when a capability is not available to the current user.

### Knowledge

No uploaded Knowledge file is mandatory for the first Store release.

Behavioral rules belong in Instructions. This keeps the public core self-contained and avoids making publication depend on an uploaded private corpus.

## 4. Conversation Starters

Use the four starters from the manifest:

```text
Research this topic and build the CriticProfile for my approval before you start.
Compare two technologies using independent sources and show unresolved risks.
Verify this claim, including evidence that supports or contradicts it.
Resume a K_Supervisor task from a checkpoint I will paste.
```

## 5. Store Workflow Mapping

The Custom GPT is one ChatGPT runtime executing separated logical roles.

```text
Supervisor stage
  -> Domain/risk assessment
  -> CriticProfile proposal
  -> USER APPROVAL / EDIT / REJECT
  -> Research stage
  -> Critic stage
  -> autonomous REVISE/PASS loop
  -> Final report
  -> Review protocol
```

The Store Edition therefore provides logical multi-agent separation rather than process-isolated model instances. The Critic stage must perform a fresh verification pass and, when web search is available, should use independent verification searches rather than only reusing Research-stage source selection.

## 6. Checkpoint and Fresh-chat Recovery

Custom GPT conversations do not use previous GPT conversations, saved memory, or user custom instructions as cross-chat workflow state.

Cross-chat continuation therefore uses an explicit user-controlled checkpoint marked:

```text
K_SUPERVISOR_CHECKPOINT
```

Schema version:

```text
1.0
```

Safe checkpoint states:

```text
PROFILE_REVIEW_REQUIRED
PROFILE_APPROVED
REVISE_REQUIRED
APPROVED
FINALIZED
COMPLETED_WITH_LIMITATIONS
FAILED
```

Ambiguous mid-agent states are not valid checkpoint states.

Recovery rules:

- validate marker/version/required fields;
- never reconstruct missing critical state from guesswork;
- PROFILE_REVIEW_REQUIRED returns to the normal approval gate;
- PROFILE_APPROVED, REVISE_REQUIRED, and APPROVED require user confirmation to resume but do not require re-approval of an unchanged approved CriticProfile;
- terminal states are summarized rather than automatically restarted.

The engineering contract is in `gpt_store/checkpoint.py`. A synthetic example is in `gpt_store/checkpoint_example.json`.

## 7. Official OpenAI Requirements Snapshot

Verified on 2026-08-13 against current OpenAI Help Center documentation.

Primary references:

```text
https://help.openai.com/en/articles/8554407-gpts-in-chatgpt
https://help.openai.com/en/articles/8554397-create-a-gpt
https://help.openai.com/en/articles/8798878
```

Current platform facts relevant to this package:

- signed-in ChatGPT users can use GPTs they have access to, including public GPTs;
- creating/editing GPTs requires an eligible paid plan and is performed on the web;
- the Builder supports name, description, conversation starters, instructions, knowledge, capabilities, apps, actions, and an optional recommended model;
- if no recommended model is configured, users may choose a model available to them; model availability can change;
- public GPT Store publishing may require category selection and a completed Builder Profile;
- a public GPT using Actions requires a valid Privacy Policy URL for each public action;
- public publishing can be blocked by workspace settings, unsupported app connections, policy checks, or account restrictions;
- public GPTs may be automatically checked before broader sharing/publication;
- GPT builders cannot view individual user conversations with their GPT;
- GPTs do not use saved memory, user custom instructions, or previous conversations; each new GPT conversation starts fresh.

Because this package uses no Actions and no Apps, it does not require an Action privacy-policy URL and does not create a mandatory third-party data path.

## 8. Static Validation

Run before opening the GPT Builder:

```text
python -m scripts.validate_store_package
python -m pytest
```

Static validation checks:

- Store channel and user-plan model policy;
- no pinned recommended model;
- no developer secret requirement;
- no mandatory backend;
- Apps/Actions disabled;
- required built-in capabilities declared;
- instruction file present and containing the mandatory approval/review/checkpoint rules;
- checkpoint example conforms to the checkpoint contract.

## 9. Preview Test Matrix

Run in GPT Builder Preview before public sharing:

```text
P1 New low-risk research task
P2 High-risk domain task and conservative risk floor
P3 Explicit APPROVE gate
P4 EDIT then approve
P5 REJECT stops autonomous execution
P6 Research -> Critic -> PASS
P7 Forced REVISE then corrected second iteration
P8 Web-search-unavailable/freshness limitation behavior
P9 Generate checkpoint at PROFILE_APPROVED
P10 Paste checkpoint into a fresh GPT conversation and resume
P11 Malformed checkpoint rejection
P12 Final report plus review protocol without hidden reasoning
```

## 10. Account/Plan Release Matrix

These checks require real ChatGPT accounts and cannot be proven by repository CI alone.

Before public release, manually verify:

```text
Free account:
  - can open/use the public GPT;
  - workflow reaches the profile gate;
  - capability limits degrade explicitly rather than fabricating tool use.

Paid account:
  - can use the same workflow;
  - can switch to another available model when the account exposes alternatives;
  - workflow semantics and checkpoint format remain unchanged after switching.
```

Record the result in the release notes or release checklist. A live account test is a publication gate, not a reason to add developer-funded API calls to the free core.

## 11. Publication Checklist

Immediately before Store publication:

1. Re-run static validation and full CI.
2. Re-check the official OpenAI GPT publishing documentation because plan/model/Store rules can change.
3. Open GPT Builder on the web using an eligible creator account.
4. Configure name, description, starters, instructions, and capabilities exactly from the manifest/package.
5. Leave Recommended model unset.
6. Keep Apps and Actions disabled.
7. Complete Builder Profile requirements if prompted.
8. Run the Preview test matrix.
9. Run the Free and paid account release matrix.
10. Select an appropriate Store category when prompted.
11. Confirm policy/product requirements and publish to GPT Store.

Actual publication is a manual ChatGPT UI action. Repository automation does not claim to publish the GPT.

## 12. Release State

The repository package may be marked `ready_for_manual_publication_test` when:

- package files validate;
- CI is green;
- official OpenAI requirements have been re-checked;
- no developer secret/backend is required by the Store core.

`ready_for_manual_publication_test` does not mean `published`.
