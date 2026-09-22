# KRC MEDIA — R3.9 Unified KRC GPT routing contract and staging candidate ready

Date: 2026-09-22  
Status: **AUTHORITATIVE CHECKPOINT / R39_UNIFIED_KRC_GPT_ACTIVE / ROUTING_CONTRACT_READY / STAGING_MANIFEST_READY / STATIC_READBACK_PASS / PUBLIC_GPT_UNCHANGED / R4_C_PAUSED / FREE_ONLY**

## Owner authorization

Owner approved the interim architecture:

```text
R3_9=UNIFIED_KRC_GPT
USER_FACING_PRODUCT=ONE_K_RESEARCH_AND_CRITIC
CORE=AUTHORITATIVE
MEDIA=EVIDENCE_ACQUISITION_LAYER
R4_C=REMAINS_PAUSED
```

Goal: unify current KRC + KRC MEDIA semantics now without creating a monolith and without increasing future GPT-to-Plugin migration cost.

## New canonical R3.9 artifacts

Created:

```text
contracts/krc_unified_media_routing.yaml
gpt_store/unified_r39_manifest.yaml
tests/test_krc_unified_r39.py
```

Existing canonical sources reused unchanged:

```text
prompts/GPT_STORE_INSTRUCTIONS.md
prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md
gpt_store/actions/media_public_r3_openapi.yaml
plugins/krc_migration_candidate/contracts/media_tools.yaml
plugins/krc_migration_candidate/contracts/media_adapter.yaml
plugins/krc_r4_candidate/.app.json
```

## Architecture

```text
K-Research & Critic
  Core:
    CriticProfile -> Research -> Critic -> Final Report
  MEDIA:
    intent/routing -> transcript acquisition -> evidence input to Core
  Backend:
    existing R3C/E1-E4 + VoiceBridge
```

MEDIA is not a second verdict engine.

Transcript semantics:

```text
transcript proves = what the media source says
transcript does not prove = external factual truth
material claims still require Core cross-check rules
```

## Routing order

```text
1 detect media intent without provider work
2 create CriticProfile
3 obtain explicit CriticProfile approval
4 perform relevant read-only MEDIA preflight/lookup
5 reuse existing completed/processing jobs
6 request execution consent only if new provider work is required
7 retrieve transcript segments
8 use transcript as evidence
9 independently corroborate material factual claims
10 Critic -> one final report
```

Before CriticProfile approval:

```text
platform classification=ALLOWED
media relevance detection=ALLOWED
provider work=FORBIDDEN
transcript content retrieval=FORBIDDEN
MEDIA *_start=FORBIDDEN
independent web research=FORBIDDEN
```

## Frozen MEDIA parity

```text
READ_OPERATIONS=9
EXECUTION_OPERATIONS=4
TOTAL_OPERATIONS=13
READ_ONLY_EXECUTION_LEAKAGE=0
REGISTERED_R4_APPS=5
```

Execution remains isolated:

```text
E1=media_youtube_start
E2=media_instagram_start
E3=media_facebook_start
E4=media_telegram_start
```

## FREE_ONLY

Preserved:

```text
paid_retrieval_fallback=false
paid_stt_fallback=false
paid_proxy_fallback=false
automatic_paid_retry=false
supadata_public_active=false
scrapecreators_public_active=false
cookie_or_login_fallback=false
```

## Static readback validation

Repository readback after file creation:

```text
CORE_SHA=ff80e444bc41414984f84b493f0e92b1cf06c0c9
CORE_UNCHANGED_FROM_PRE_R39=PASS
CORE_PLUS_MEDIA_ADDENDUM_CHARS=7404
BUILDER_8000_CHAR_LIMIT=PASS

ROUTING_9_READ=PASS
ROUTING_4_EXECUTION=PASS
ROUTING_TOTAL_13=PASS
PREAPPROVAL_PROVIDER_BLOCK=PASS
CORE_AUTHORITY_PRESERVED=PASS
MEDIA_EVIDENCE_ONLY=PASS
FREE_ONLY_FAIL_CLOSED=PASS

R4_APP_COUNT=5
R4_APP_IDS_UNCHANGED=PASS
R4_C_PAUSED=PASS
PUBLIC_GPT_MUTATION_HOLD=PASS

NEW_R39_TESTS_AUTHORED=8
```

## Test execution limitation

A local exact-branch pytest attempt could not start because the current execution container could not resolve github.com, so it could not clone the repository.

GitHub Actions remain unavailable under the current project constraint.

Therefore:

```text
R39_STATIC_READBACK=PASS
R39_PYTEST_EXECUTION=NOT_RUN
R39_RUNTIME_ACCEPTANCE=NOT_YET_RUN
```

Do not overstate this as a full test-suite pass.

## Migration compatibility

The current GPT transport and future Plugin transport intentionally share semantics:

```text
current GPT:
  Core instructions + MEDIA addendum + 13-op Action schema

future Plugin:
  krc-core Skill + existing R3C/E1/E2/E3/E4 apps

VoiceBridge/business logic:
  unchanged
```

The GPT custom Action is treated as a disposable transport adapter. Future removal during Plugin migration must not change MEDIA business semantics.

## Release boundary

No production mutation at this checkpoint:

```text
PUBLIC_GPT_MUTATION=NO
PUBLIC_GPT_ACTION_CHANGE=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
R4_C_RESUME=NO
PR22_MERGE=NO
PR45_MERGE=NO
NEW_MEDIA_STARTS=0
PROVIDER_WORK=0
```

## Next gate

R3.9 repository/runtime validation before applying the unified package to the public GPT:

```text
R39_CORE_REGRESSION
R39_UNIFIED_ROUTING_TESTS
R39_13_OPERATION_PARITY
R39_FREE_ONLY_FAIL_CLOSED
R39_EXECUTION_CONFIRMATION_BOUNDARY
R39_MEDIA_FAILURE_ISOLATION
R39_FUTURE_PLUGIN_MAPPING_PARITY
```

After these gates pass, prepare the exact Builder delta for the existing public GPT. Keep the current public GPT as rollback anchor until post-update smoke acceptance.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_182_R39_UNIFIED_ROUTING_STAGING_STATIC_PASS_PUBLIC_GPT_UNCHANGED_2026_09_22`
