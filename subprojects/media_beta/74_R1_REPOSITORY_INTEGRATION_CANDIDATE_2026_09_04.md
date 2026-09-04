# R1 Public KRC + MEDIA Repository Integration Candidate

Date: 2026-09-04
Status: R1_INTEGRATION_CANDIDATE / CI_REQUIRED / NO_LIVE_GPT_CHANGE

## Authority

R0 Public KRC Update Safety Preflight: PASS by owner-provided current Builder evidence.

This record authorizes and describes repository integration only. It does not authorize Render/Neon mutation, backend promotion, ChatGPT Builder Update, new GPT publication, Gemini prerecorded activation, Hybrid C/D implementation, paid fallback, external testers, or public MEDIA rollout.

## Integration strategy

The historical MEDIA PR #8 is not merged directly because it is divergent/dirty. R1 uses a clean forward-port from the verified public `main` baseline:

`ad56f3e3318e0b28eabc8ba6263bbbc462ccdcb6`

Target integration branch:

`agent/public-krc-media-r1-integration`

The active public Core package remains authoritative and unchanged during R1.

## Selected MEDIA forward-port

The following current MEDIA artifacts are staged additively in the public repository without activating them for the published GPT:

- `gpt_store/media_beta_manifest.yaml`
- `gpt_store/actions/media_managed_beta_openapi.yaml`
- `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md`
- `prompts/GPT_STORE_MEDIA_MANAGED_BETA_INSTRUCTIONS.md`
- `docs/PRIVACY_POLICY.md`
- current checkpoint/roadmap/decision/handoff records under `subprojects/media_beta/`
- focused MEDIA package regression tests

## Core preservation boundary

R1 must not modify these active public Core files:

- `gpt_store/manifest.yaml`
- `prompts/GPT_STORE_INSTRUCTIONS.md`
- `docs/GPT_STORE_PACKAGE.md`
- `docs/GPT_STORE_DEPLOYMENT.md`

Required preserved runtime/package state:

```text
public Core publication state: published
public Core Actions: false
public Core external backend dependency: false
Web search: enabled
Code Interpreter/Data Analysis: enabled
Image generation: disabled
Knowledge: empty
```

MEDIA artifacts remain staging/private-beta material and are not the active public Builder package.

## Safety invariants

```text
MEDIA unavailable/fails -> MEDIA unavailable/fails closed
Core KRC              -> remains usable
```

```text
Facebook Cobalt failure -> unavailable -> STOP
ScrapeCreators -> reserved/inactive
NO automatic paid fallback
Telegram public-only -> retrieval credits 0
Local attachment -> retrieval credits 0
AssemblyAI universal-2 -> current KRC prerecorded provider
Gemini prerecorded normal activation -> FALSE
```

## R1 acceptance gate

R1 candidate can be merged only if:

- full repository CI is green;
- focused MEDIA package tests are green;
- comparison against `main` shows no active Core file change;
- MEDIA remains additive/inactive for the current public package;
- no VoiceBridge, Render, Neon or Builder live change occurs.

After successful merge, create a final R1 closure checkpoint and move continuation to R2 readiness planning. R2/R3/R4 remain separately gated.
