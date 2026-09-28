# KRC MEDIA — R3.9 private staging Action transport/auth PASS

Date: 2026-09-23
Status: **AUTHORITATIVE CHECKPOINT / R39_PRIVATE_STAGING_ACTIVE / ACTION_TRANSPORT_AUTH_PASS / GET_CAPABILITIES_PASS / S3_RETRY_READY / PUBLIC_GPT_UNCHANGED / FREE_ONLY**

## Builder diagnostic result

On the private staging GPT `K-Research & Critic - MEDIA BETA`, the read-only Builder test:

```text
getPublicMediaCapabilities
GET /api/v1/media/public-capabilities
```

completed successfully after rebinding the Action to the dedicated R3.9 Bearer credential.

Observed capability summary:

```text
configured=true
platforms=youtube,instagram,facebook,telegram
youtube=Gemini direct / Free Tier
youtube explicit data-use consent required before start
instagram/facebook=Cobalt + AssemblyAI
telegram=public web + AssemblyAI
paid fallback routes=disabled
durable jobs=enabled
duplicate start reuse=enabled
```

## Acceptance

```text
ACTION_TRANSPORT=PASS
ACTION_AUTH=PASS
GET_CAPABILITIES=PASS
PROVIDER_WORK=0
PUBLIC_GPT_MUTATION=NO
```

## Next gate

Retry S3 from a fresh private staging chat:

1. submit the supported YouTube URL analysis request;
2. verify CriticProfile gate;
3. approve with `1`;
4. allow read-only preflight/lookup;
5. expect the returned Gemini Free data-use notice before any new provider work;
6. do not approve consequential start during this smoke gate.

Expected:

```text
READONLY_BOUNDARY=PASS
GEMINI_DATA_USE_NOTICE=SHOWN
*_start completed=0
provider_work=0
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_189_R39_ACTION_TRANSPORT_AUTH_PASS_S3_RETRY_READY_2026_09_23`
