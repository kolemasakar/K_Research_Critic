# KRC MEDIA — Portable root manifest App binding fix applied; private Chat retest next

Date: 2026-09-24  
Status: **AUTHORITATIVE CHECKPOINT / CHAT_S3_FAIL_CONFIRMED / PORTABLE_ROOT_MANIFEST_ADDED / CANONICAL_APP_BINDING_APPLIED / PRIVATE_RETEST_NEXT / ZERO_PROVIDER**

## Failure confirmed before fix

Fresh Chat on version `0.19.5+appbinding.20260924` still reported:

```text
KRC MEDIA actions are not exposed as callable tools
```

and fell back to TinyFish.

Render correlation:

```text
R3C requests=0
E1 requests=0
provider_work=0
```

Therefore the compatibility-manifest-only binding was still insufficient for automatic natural routing in Chat.

## Official packaging clarification

Current OpenAI Plugin packaging guidance defines a portable root `plugin.json` as the canonical manifest. Registered Apps are referenced under:

```text
extensions.com.openai.apps="./.app.json"
```

A `.codex-plugin/plugin.json` remains a supported compatibility fallback.

## Fix applied

The private Plugin now contains both:

```text
plugin.json                         # canonical portable root manifest
.codex-plugin/plugin.json           # compatibility fallback
.app.json                            # five registered Apps
skills/instructions/SKILL.md        # existing Core + routing fix
```

Current Plugin:

```text
plugin_id=plugin_bb3595f295708191a3f9e145ba1ff2d5
version=0.19.6+portable.20260924
release=pluginrel_6ab57f1c11b88191bc1c02ee5391e7b7
scope=USER
discoverability=PRIVATE
```

Root `plugin.json`:

```text
$schema=https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
extensions.com.openai.apps=./.app.json
interface.capabilities=[Read,Write]
```

Compatibility manifest also retains:

```text
apps=./.app.json
skills=./skills
```

Canonical App refs remain unchanged 5/5.

## Readback

```text
root plugin.json=PRESENT
portable app binding=PRESENT
compatibility app binding=PRESENT
.app.json=5 canonical refs
Skill routing fix=PRESENT
provider_work=0
publication/share=unchanged PRIVATE
```

## Next gate

1. stop the currently running TinyFish test;
2. refresh the private Plugin page;
3. verify version `0.19.6+portable.20260924`;
4. launch **new Chat** from `Спробувати в чаті`;
5. repeat YouTube request -> CriticProfile -> `1`;
6. expected: R3C preflight/lookup before any TinyFish/web;
7. if no reusable transcript: Gemini Free Tier notice and explicit consent gate.

## Hard boundary

```text
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
MEDIA_PROVIDER_WORK=NO
EXECUTION_CONFIRMATION_APPROVAL=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
```

## Resume

```text
RESUME_FROM=CHECKPOINT_211_PORTABLE_ROOT_MANIFEST_APP_BINDING_FIX
NEXT_GATE=PRIVATE_CHAT_S2_S3_RETEST_ON_0_19_6
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_211_PORTABLE_ROOT_MANIFEST_APP_BINDING_FIX_APPLIED_PRIVATE_RETEST_NEXT_2026_09_24`
