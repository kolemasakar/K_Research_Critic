# KRC MEDIA — Generated Skill source parity PASS; Plugin transport wording requires minimal revision

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / GENERATED_SKILL_SOURCE_PARITY_PASS / PLUGIN_NATIVE_TRANSPORT_WORDING_REVISE / APPS_EMPTY / FREE_ONLY**

## Inspected migrated Plugin

```text
PLUGIN_NAME=K-Research & Critic
PLUGIN_VERSION=0.19.1+bundle.537edef6e9b2291f8ee718897254ce9b
SKILL_PATH=skills/instructions/SKILL.md
SKILL_NAME=instructions
APPS_ATTACHED=0
PLUGIN_VISIBILITY=PRIVATE
```

## Source parity result

The body of the generated `skills/instructions/SKILL.md` matches the accepted public Unified R3.9 instruction artifact:

```text
canonical=prompts/GPT_STORE_UNIFIED_R39_INSTRUCTIONS.md
core_body_parity=PASS
media_addendum_body_parity=PASS
migration_fidelity=PASS
```

The generated YAML front matter/name differs from the repository R4 design Skill, which is expected for native migration and is not itself a semantic defect.

## Plugin-native semantic review

Two phrases are transport-specific to the legacy Custom Action surface:

1. `For supported public media URLs use the MEDIA Action`
2. `only then send the required gemini_free_consent object`

The accepted Plugin/MCP adapter contract instead routes through the KRC MEDIA Apps/tools and defines consent at the MCP adapter/tool boundary.

Therefore:

```text
SOURCE_MIGRATION_FIDELITY=PASS
PLUGIN_NATIVE_SEMANTIC_PARITY=REVISE
REASON=LEGACY_ACTION_TRANSPORT_WORDING
BUSINESS_LOGIC_DRIFT=NO
CORE_DRIFT=NO
FREE_ONLY_DRIFT=NO
```

## Required minimal revision

Preserve the entire migrated Skill except for these transport-normalization replacements:

```text
OLD:
For supported public media URLs use the MEDIA Action; MEDIA failure never blocks Core.

NEW:
For supported public media URLs use the available KRC MEDIA apps/tools; MEDIA failure never blocks Core.
```

and:

```text
OLD:
YouTube: preflight first; before new provider work show the returned Gemini Free data-use notice and require explicit approval; only then send the required gemini_free_consent object. No consent=no start.

NEW:
YouTube: preflight first; before new provider work show the returned Gemini Free data-use notice and require explicit approval; only then call the YouTube execution tool with the consent fields required by that tool. No consent=no start.
```

No other Skill text should change.

## Hard boundary

```text
APP_ATTACHMENT=HOLD
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MEDIA_PROVIDER_WORK=NO
CORE_TEXT_OTHER_THAN_TWO_TRANSPORT_LINES=NO_CHANGE
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_198_GENERATED_SKILL_SOURCE_PARITY_PASS
NEXT_GATE=APPLY_MINIMAL_PLUGIN_TRANSPORT_NORMALIZATION
AFTER_GATE=ATTACH_FIVE_CANONICAL_APPS
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_198_GENERATED_SKILL_SOURCE_PARITY_PASS_PLUGIN_TRANSPORT_WORDING_REVISE_NEXT_2026_09_24`
