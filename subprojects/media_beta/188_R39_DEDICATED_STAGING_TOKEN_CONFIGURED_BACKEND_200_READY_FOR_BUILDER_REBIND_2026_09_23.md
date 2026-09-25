# KRC MEDIA — R3.9 dedicated staging token configured; backend auth PASS

Date: 2026-09-23
Status: **AUTHORITATIVE CHECKPOINT / R39_PRIVATE_STAGING_ACTIVE / DEDICATED_R39_TOKEN_CONFIGURED / BACKEND_AUTH_200_PASS / BUILDER_REBIND_NEXT / PUBLIC_GPT_UNCHANGED / FREE_ONLY**

## Diagnosis

Builder read-only Action test reached VoiceBridge but returned:

```text
AUTHENTICATION_FAILED
retryable=false
```

This proved the retained hidden Bearer credential in the private MEDIA BETA Builder no longer matched the backend.

## Safe isolation path

Current VoiceBridge runtime supports a dedicated R3.9 credential:

```text
KRC_MEDIA_R39_ACTION_TOKEN
```

This is separate from the general public MEDIA token and the scoped R3E1-R3E4 credentials.

A new dedicated R3.9 token was configured in Render. The token value is intentionally NOT recorded in repository documentation.

Render deploy:

```text
service=voicebridge-krc-media-beta-kolemasakar
deploy=dep-daphq1ijnfac73bpnvi0
commit=fc6a967911c5c2a549df065762a185fc5f6c900b
status=LIVE
```

## Direct backend validation

Using the dedicated R3.9 Bearer against:

```text
GET /api/v1/media/public-capabilities
```

returned:

```text
HTTP=200
configured=true
platforms=youtube,instagram,facebook,telegram
supadata_public_active=false
automatic_paid_fallback=false
paid_retrieval_fallback=false
paid_stt_fallback=false
youtube_gemini_free_tier_only=true
youtube_gemini_consent_required=true
```

No provider work was started.

## Next step

Rebind only the private `K-Research & Critic - MEDIA BETA` Builder Action to the new dedicated R3.9 Bearer.

Do not change:

- schema;
- server URL;
- public GPT;
- R3C/E1-E4 credentials;
- Plugin state.

After rebind, rerun only `getPublicMediaCapabilities`.

Expected:

```text
Builder Action test=HTTP 200 / capability object
provider work=0
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_188_R39_DEDICATED_STAGING_TOKEN_BACKEND_200_2026_09_23`
