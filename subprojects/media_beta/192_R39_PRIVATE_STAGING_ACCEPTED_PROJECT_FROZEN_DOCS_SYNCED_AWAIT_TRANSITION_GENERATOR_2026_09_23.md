# KRC MEDIA — R3.9 private staging accepted; project frozen for transition handoff

Date: 2026-09-23  
Status: **AUTHORITATIVE CHECKPOINT / R39_PRIVATE_STAGING_ACCEPTED / S1_TO_S4_PASS / 92_TESTS_PASS / NATIVE_PLUGIN_MIGRATION_AVAILABLE / PUBLIC_GPT_UNCHANGED / PUBLIC_ROLLBACK_SNAPSHOT_NEXT / PROJECT_FROZEN_FOR_HANDOFF / FREE_ONLY**

## Current authoritative state

```text
R3_9_UNIFIED_KRC_GPT=ACTIVE
PRIVATE_STAGING=ACCEPTED
S1_CORE_GATE=PASS
S2_MEDIA_PREAPPROVAL_GATE=PASS
S3_READONLY_AND_GEMINI_CONSENT_BOUNDARY=PASS
S4_CONSEQUENTIAL_CONFIRMATION_BOUNDARY=PASS
SELECTED_REGRESSION_TESTS=92/92 PASS
FREE_ONLY=PASS
PROVIDER_WORK_DURING_S4=0
PUBLIC_GPT_MUTATION=NO
NATIVE_PLUGIN_MIGRATION_TRIGGER=CONFIRMED
NATIVE_PLUGIN_MIGRATION_EXECUTION=DEFERRED
```

## Unified artifacts

```text
instructions=prompts/GPT_STORE_UNIFIED_R39_INSTRUCTIONS.md
instructions_size=7404/8000
action_schema=gpt_store/actions/media_public_r39_openapi.yaml
action_schema_version=0.9.1-r39-unified-candidate
operations=13
read_nonconsequential=9
execution_consequential=4
routing_contract=contracts/krc_unified_media_routing.yaml
staging_manifest=gpt_store/unified_r39_manifest.yaml
builder_package=gpt_store/UNIFIED_R39_BUILDER_PACKAGE.md
```

## Private staging state

Target:

```text
K-Research & Critic - MEDIA BETA
sharing=ONLY_ME
instructions=Unified R3.9
action_schema=R3.9
action_transport=PASS
action_auth=PASS
```

A dedicated R3.9 staging credential is configured server-side. Its value is not stored in project documentation.

Important release rule:

```text
STAGING_CREDENTIAL_PROMOTION_TO_PUBLIC=FORBIDDEN
PUBLIC_ACTIVATION_REQUIRES_FRESH_PRODUCTION_CREDENTIAL=YES
```

The staging credential was exposed during interactive setup and therefore must not become the long-term public production credential.

## VoiceBridge state

```text
service=voicebridge-krc-media-beta-kolemasakar
service_id=srv-da1kic5bedkc73d6fk60
current_deployed_commit=fc6a967911c5c2a549df065762a185fc5f6c900b
dedicated_R39_auth_support=YES
dedicated_R39_backend_auth_test=HTTP_200
```

The prior read-only admission fix remains part of the runtime history. Current deployed commit additionally wires the dedicated R3.9 Action token into AppConfig.

## Native Plugin migration

Owner account UI now exposes:

```text
Перенести в плагін
displayed_deadline=2026-12-11
```

This supersedes earlier observations where no migrate control was visible.

Decision:

```text
NATIVE_MIGRATION_AVAILABLE=YES
MIGRATE_NOW=NO
```

First finish and accept the unified public GPT. Then reconsider native migration.

## Public GPT boundary

Current public `K-Research & Critic` remains unchanged and published.

Next work item:

```text
PUBLIC_ROLLBACK_BASELINE_SNAPSHOT
```

Capture before any public mutation:

- current Instructions;
- Knowledge;
- capabilities;
- Actions and authentication state;
- sharing/publication state.

Only after the rollback snapshot is accepted may the exact R3.9 Builder delta be proposed/applied.

## Explicit holds

```text
PUBLIC_GPT_MUTATION=NO
NATIVE_PLUGIN_MIGRATION_EXECUTION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
PR22_MERGE=NO
PR45_MERGE=NO
NEW_MEDIA_PROVIDER_WORK=NO
MAIN_MUTATION=NO
```

## Resume after chat transition

Resume from:

```text
RESUME_FROM=CHECKPOINT_192_R39_PRIVATE_STAGING_ACCEPTED
NEXT_GATE=PUBLIC_GPT_ROLLBACK_BASELINE_SNAPSHOT
```

Do not repeat S1-S4 unless product/runtime drift is detected.

Wait for the owner's transition generator and use it to create the next-chat bootstrap package.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_192_R39_PRIVATE_STAGING_ACCEPTED_PROJECT_FROZEN_AWAIT_TRANSITION_GENERATOR_2026_09_23`
