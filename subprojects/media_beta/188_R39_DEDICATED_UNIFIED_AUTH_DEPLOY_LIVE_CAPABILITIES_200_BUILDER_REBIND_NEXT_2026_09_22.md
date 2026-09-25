# KRC MEDIA — R3.9 dedicated unified auth deployed and live

Date: 2026-09-22
Status: **AUTHORITATIVE CHECKPOINT / R39_PRIVATE_STAGING_ACTIVE / S1_PASS / S2_PASS / S3_AUTH_ROOT_CAUSE_CONFIRMED / DEDICATED_R39_AUTH_DEPLOY_LIVE / BUILDER_REBIND_NEXT / PUBLIC_GPT_UNCHANGED / FREE_ONLY**

## Root cause

The private Builder Action retained a Bearer credential that no longer matched the active VoiceBridge general Action token.

Builder diagnostic:

```text
getPublicMediaCapabilities
AUTHENTICATION_FAILED
bearer token invalid or revoked
retryable=false
```

This confirms the schema and endpoint were reachable but the retained credential was stale/mismatched.

## Safety decision

Do not rotate the existing general or R3C/E1-E4 credentials.

Instead add a dedicated additive credential:

```text
KRC_MEDIA_R39_ACTION_TOKEN
```

The secret value is runtime-only and is NOT stored in this repository or project documentation.

## VoiceBridge change

Branch:

```text
agent/krc-media-gemini-migration
```

Exact deployed SHA:

```text
fc6a967911c5c2a549df065762a185fc5f6c900b
```

Behavior:

- R3.9 token accepted on Gemini YouTube routes;
- R3.9 token accepted on Cobalt Instagram routes and scoped to Instagram;
- R3.9 token accepted on accepted managed Facebook/Telegram routes;
- R3.9 token blocked from legacy/general managed surfaces;
- existing Action/R3E1/R3E2/R3E3/R3E4 tokens remain accepted;
- provider admission/rate/concurrency controls also recognize R3.9 token;
- no FREE_ONLY policy relaxation.

## Validation

Exact-branch TypeScript build: PASS.

Targeted auth / routing / FREE_ONLY tests:

```text
tests=35
pass=35
fail=0
```

## Render deploy

```text
service=voicebridge-krc-media-beta-kolemasakar
service_id=srv-da1kic5bedkc73d6fk60
deploy_id=dep-dapf4fu0tbcc73amk1f0
commit=fc6a967911c5c2a549df065762a185fc5f6c900b
status=LIVE
```

Post-deploy direct read-only validation using the new dedicated R3.9 credential:

```text
GET /api/v1/media/public-capabilities
HTTP=200
configured=true
platforms=youtube,instagram,facebook,telegram
youtube_retrieval_provider=gemini_youtube_url
instagram_retrieval_provider=cobalt
facebook_free_retrieval_provider=cobalt
telegram_retrieval_provider=telegram_public_web
automatic_paid_fallback=false
paid_retrieval_fallback=false
paid_stt_fallback=false
```

No provider work was required for this validation.

## Next gate

Rebind the private `K-Research & Critic - MEDIA BETA` Action authentication to the dedicated R3.9 Bearer token, save authentication, update the private GPT, then run only:

```text
getPublicMediaCapabilities
```

Expected: HTTP 200 / capabilities object.

Do not run any `start...` operation.

## Boundaries

```text
PUBLIC_GPT_MUTATION=NO
PUBLICATION_CHANGE=NO
NATIVE_PLUGIN_MIGRATION_EXECUTION=NO
OLD_MEDIA_CREDENTIAL_ROTATION=NO
NEW_PROVIDER_WORK=NO
PR22_MERGE=NO
PR45_MERGE=NO
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_188_R39_DEDICATED_AUTH_DEPLOY_LIVE_BUILDER_REBIND_NEXT_2026_09_22`
