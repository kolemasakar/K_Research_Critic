# KRC MEDIA — R3.9 exact validation PASS; native migration trigger confirmed; private staging package ready

Date: 2026-09-22  
Status: **AUTHORITATIVE CHECKPOINT / R39_UNIFIED_KRC_GPT_ACTIVE / EXACT_BRANCH_VALIDATION_PASS / 91_TESTS_PASS / NATIVE_MIGRATION_TRIGGER_CONFIRMED / PRIVATE_MEDIA_BETA_STAGING_NEXT / PUBLIC_GPT_UNCHANGED / R4_C_DEFERRED_UNTIL_R39_ACCEPTANCE / FREE_ONLY**

## Product trigger update

Owner UI now shows:

```text
Перенесіть свої GPT у плагіни до 11 грудня
Перенести в плагін
```

Therefore:

```text
TRIGGER_1=NATIVE_MIGRATION_AVAILABLE_IN_PLUS_ACCOUNT / CONFIRMED
NATIVE_MIGRATION_BUTTON=AVAILABLE
DISPLAYED_DEADLINE=2026-12-11
```

Do not execute migration yet.

The migration step is deferred until the unified KRC product is accepted, so that the native migration receives the consolidated Core + MEDIA configuration rather than an older split state.

## Exact-branch validation

Validation host:

```text
device=krc-cobalt
repo=kolemasakar/K_Research_Critic
branch=agent/krc-public-media-r3-integration
```

Initial R3.9 validation found one stale historical test expecting the migration candidate README to still say:

```text
DESIGN_ONLY / NOT_INSTALLABLE / NOT_DEPLOYED
```

The candidate has legitimately advanced to:

```text
PRIVATE_MCP_IMPLEMENTATION_VALIDATED
R3-H_COMPLETE
PUBLICATION_HOLD
```

The stale test was reconciled without changing runtime behavior.

## Validation results

After reconciliation:

```text
R39 tests=PASS
migration candidate guards=PASS
public MEDIA integration guards=PASS
Core/store/profile/report/loop/E2E selected regressions=PASS

TOTAL_SELECTED_TESTS=91
PASSED=91
FAILED=0
```

Exact validated functional head before documentation-only package commit:

```text
b683e90a73a8a1f0fcc09670869d85087fe0aee1
```

## R3.9 Action confirmation correction

The historical R3 Action schema had:

```text
13 operations with x-openai-isConsequential=false
```

That is acceptable as historical repository evidence but not sufficient for the current Unified custom-GPT confirmation boundary.

Therefore R3.9 introduces a separate schema:

```text
gpt_store/actions/media_public_r39_openapi.yaml
```

R3.9 schema:

```text
READ / NON-CONSEQUENTIAL=9
EXECUTION / CONSEQUENTIAL=4
TOTAL=13
```

Consequential operations:

```text
startPublicGeminiYoutubeTranscription
startPublicInstagramCobaltTranscription
startPublicFacebookCobaltTranscription
startPublicTelegramTranscription
```

The historical R3 schema remains unchanged.

## Exact Builder instructions artifact

Created:

```text
prompts/GPT_STORE_UNIFIED_R39_INSTRUCTIONS.md
```

It is exactly:

```text
canonical Core
+ blank line
+ accepted MEDIA R3 public addendum
```

Validated:

```text
CORE_BYTE_PARITY=PASS
BUILDER_CHAR_COUNT=7404/8000
```

## Private-first staging decision

Before touching the existing published GPT, use:

```text
K-Research & Critic - MEDIA BETA
```

as the private staging surface.

Reason:

- already private/owner-only;
- existing VoiceBridge Action authentication is already configured;
- supports safe rollback;
- allows Core + MEDIA + confirmation smoke before public mutation.

Canonical manual package:

```text
gpt_store/UNIFIED_R39_BUILDER_PACKAGE.md
```

## Staging mutation boundary

Allowed next only on the private MEDIA BETA GPT:

```text
replace Instructions with prompts/GPT_STORE_UNIFIED_R39_INSTRUCTIONS.md
replace Action schema with gpt_store/actions/media_public_r39_openapi.yaml
keep existing bearer authentication unchanged
keep sharing private
```

Do not expose or paste the bearer secret.

## Smoke boundary

No provider execution is needed for acceptance.

Required:

```text
CORE_GATE=PASS
MEDIA_PREAPPROVAL_BLOCK=PASS
READONLY_BOUNDARY=PASS
EXECUTION_CONFIRMATION_PROMPT=PASS
CONFIRMATION_ACTION=CANCEL
PROVIDER_WORK=0
FREE_ONLY=PASS
MEDIA_FAILURE_ISOLATION=PASS
```

## Public and migration boundary

Still:

```text
PUBLIC_GPT_MUTATION=NO
PUBLIC_GPT_ACTION_CHANGE=NO
PUBLICATION_CHANGE=NO
NATIVE_PLUGIN_MIGRATION_EXECUTION=NO
R4_C=DEFERRED_UNTIL_R39_UNIFIED_ACCEPTANCE
PR22_MERGE=NO
PR45_MERGE=NO
```

## Next gate

Manual private Builder staging on `K-Research & Critic - MEDIA BETA`, followed by zero-provider-work smoke acceptance.

Only after PASS:

1. prepare/apply identical delta to public `K-Research & Critic`;
2. run public smoke;
3. then reconsider native `Перенести в плагін`.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_183_R39_91_PASS_NATIVE_MIGRATION_TRIGGER_CONFIRMED_PRIVATE_STAGING_READY_2026_09_22`
