# K-Research & Critic — Unified R3.9 Builder Package

Status: **STAGING_READY / PRIVATE_MEDIA_BETA_FIRST / PUBLIC_GPT_HOLD**

Validated exact branch head:

```text
b683e90a73a8a1f0fcc09670869d85087fe0aee1
```

Validation:

```text
R39 + Core + migration + public MEDIA selected regression suite
91 passed / 0 failed
```

## First target

Use the existing private GPT:

```text
K-Research & Critic - MEDIA BETA
```

Do **not** update the published `K-Research & Critic` yet.

The private MEDIA BETA already has the VoiceBridge Action authentication configured, so it is the safest staging surface.

## Builder Instructions

Replace the private staging GPT Instructions with the exact contents of:

```text
prompts/GPT_STORE_UNIFIED_R39_INSTRUCTIONS.md
```

This file is generated exactly as:

```text
prompts/GPT_STORE_INSTRUCTIONS.md
+
blank line
+
prompts/GPT_STORE_MEDIA_R3_PUBLIC_ADDENDUM.md
```

Validated size:

```text
7404 / 8000 characters
```

Do not hand-edit the combined text.

## Action schema

Replace only the Action schema with:

```text
gpt_store/actions/media_public_r39_openapi.yaml
```

R3.9 schema contract:

```text
operations=13
read-only/non-consequential=9
execution/consequential=4
```

Consequential operations:

```text
startPublicGeminiYoutubeTranscription
startPublicInstagramCobaltTranscription
startPublicFacebookCobaltTranscription
startPublicTelegramTranscription
```

These four must have:

```yaml
x-openai-isConsequential: true
```

All other nine operations remain:

```yaml
x-openai-isConsequential: false
```

## Authentication

Keep the existing MEDIA BETA Action authentication unchanged:

```text
type=Bearer/API key
server=https://voicebridge-krc-media-beta-kolemasakar.onrender.com
```

Do not expose, copy into chat, or commit the bearer secret.

If the Builder asks to re-enter authentication and the existing secret is no longer retained, STOP. Resolve it through the existing secure owner/admin configuration path; do not paste the secret into project documents or chat.

## Capabilities

Keep:

```text
Web Search=ON
Code Interpreter / Data Analysis=ON
Image Generation=unchanged
Knowledge=unchanged
Sharing=PRIVATE / owner-only during staging
```

Do not publish or widen audience.

## Staging smoke sequence

### S1 — Core-only gate

New chat:

```text
Досліди вплив регулярних прогулянок на якість сну.
```

Expected before any research:

```text
Профіль збору і критики успішно створено.
1 - виконати аналіз одразу.
2 - переглянути і відредагувати профіль збору і критики.
3 - скасувати дослідження.
```

No MEDIA tool should be called.

### S2 — Media URL gate

Provide a supported public media URL and ask for analysis.

Expected before any transcript/provider work:

- the same CriticProfile gate;
- no provider work;
- no `*_start`.

After explicit profile approval, allow the appropriate read-only preflight/lookup.

### S3 — Read-only boundary

Expected:

```text
read operations=9
execution operations=4
read-only execution leakage=0
```

Read-only calls must not show a consequential confirmation.

### S4 — Consequential confirmation boundary

Request a new MEDIA transcription after profile approval.

Expected before provider work:

- ChatGPT shows confirmation for the platform-specific start operation;
- do **not** approve during this smoke test;
- cancel the confirmation.

Expected result:

```text
*_start completed=0
provider work=0
confirmation boundary=PASS
```

### S5 — MEDIA failure isolation

If MEDIA is unavailable, Core must continue with available approved research paths and disclose the limitation.

## Acceptance

```text
CORE_GATE=PASS
MEDIA_PREAPPROVAL_BLOCK=PASS
READONLY_BOUNDARY=PASS
EXECUTION_CONFIRMATION_BOUNDARY=PASS
FREE_ONLY=PASS
MEDIA_FAILURE_ISOLATION=PASS
PROVIDER_WORK_DURING_SMOKE=0
PUBLICATION_CHANGE=0
```

Only after this private staging acceptance prepare the identical Builder delta for the existing public `K-Research & Critic`.

## Rollback

For the private staging GPT:

1. restore `prompts/GPT_STORE_MEDIA_BETA_BUILDER_INSTRUCTIONS.md`;
2. restore the previously accepted MEDIA BETA Action schema if changed;
3. keep existing authentication unchanged;
4. keep the GPT private.

For the public GPT, no rollback is currently required because it remains unchanged.
