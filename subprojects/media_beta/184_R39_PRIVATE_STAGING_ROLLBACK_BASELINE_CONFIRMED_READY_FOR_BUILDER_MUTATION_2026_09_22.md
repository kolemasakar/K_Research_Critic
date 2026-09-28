# KRC MEDIA — R3.9 private staging rollback baseline confirmed

Date: 2026-09-22
Status: **AUTHORITATIVE CHECKPOINT / R39_PRIVATE_STAGING_BASELINE_CONFIRMED / READY_FOR_PRIVATE_BUILDER_MUTATION / PUBLIC_GPT_UNCHANGED / FREE_ONLY**

## Target staging GPT

```text
K-Research & Critic - MEDIA BETA
sharing=ONLY_ME
```

## Current Builder state confirmed from owner screenshots

Capabilities:

```text
Web Search=ON
Image Generation=OFF
Code Interpreter/Data Analysis=ON
```

Action:

```text
server=voicebridge-krc-media-beta-kolemasakar.onrender.com
authentication=API_KEY
authorization_type=BEARER
credential_value=HIDDEN / NOT CAPTURED
privacy_policy=https://github.com/kolemasakar/K_Research_Critic/blob/main/docs/PRIVACY_POLICY.md
visible_action_count=13
```

## Exact rollback instructions

Current private staging instructions match:

```text
prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md
version=0.2.0-r2-gemini-youtube-canary
blob_sha=bf551f244d6b638b8142583a58f796b230f2d1f1
```

## Exact rollback Action schema

Current Builder Action schema matches:

```text
gpt_store/actions/media_public_free_openapi.yaml
version=0.8.0-r2-gemini-youtube
blob_sha=8b1e1ce8c566cf26b0db14627a79ebaf0fe1c0e7
```

The screenshots confirm the same version marker and backend server.

## R3.9 replacement artifacts

```text
instructions=prompts/GPT_STORE_UNIFIED_R39_INSTRUCTIONS.md
instructions_blob_sha=aa92fcfe2d7950e0ded294c3d21f23c0602b8b68
instructions_chars=7404/8000

action_schema=gpt_store/actions/media_public_r39_openapi.yaml
action_schema_blob_sha=b03004e413720740bcdda72d3a9424d9270cf3c5
action_schema_version=0.9.1-r39-unified-candidate
```

R3.9 action confirmation split:

```text
read_nonconsequential=9
execution_consequential=4
total=13
```

## Mutation authorization scope

Owner previously approved R3.9 unification and explicitly continued the merge.

Allowed next on private staging GPT only:

1. replace Instructions with the exact R3.9 instructions artifact;
2. replace Action schema with the exact R3.9 schema artifact;
3. preserve existing hidden Bearer authentication unchanged;
4. preserve Only Me sharing;
5. preserve current capabilities unless explicitly required;
6. save/update private staging GPT;
7. run zero-provider-work smoke.

Not allowed:

```text
PUBLIC_GPT_MUTATION=NO
PUBLICATION_CHANGE=NO
AUTH_SECRET_DISCLOSURE=NO
NEW_PROVIDER_WORK=NO
NATIVE_PLUGIN_MIGRATION_EXECUTION=NO
PR22_MERGE=NO
PR45_MERGE=NO
```

## Rollback

If Builder validation or smoke fails:

1. restore `prompts/GPT_STORE_MEDIA_R2_GEMINI_YOUTUBE_CANARY_INSTRUCTIONS.md`;
2. restore `gpt_store/actions/media_public_free_openapi.yaml`;
3. keep the existing hidden Bearer authentication;
4. keep sharing Only Me;
5. retest the prior private canary baseline.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_184_R39_PRIVATE_STAGING_ROLLBACK_BASELINE_READY_2026_09_22`
