# KRC MEDIA — R3-C Capabilities Live Invocation PASS

Date: 2026-09-16
Status: **R3_C_CAPABILITIES_INVOCATION_PASS / R3_C_REMAINING_READ_ONLY_GATES_PENDING**

## Scope

This checkpoint records the first bounded live read-only R3-C invocation through the private ChatGPT OAuth MCP app `KRC MCP R3C Readonly`.

Only `media_get_capabilities` was invoked. No other MEDIA tool was called and no provider work was started.

## First attempt / transient edge condition

The first invocation reached the MCP adapter but returned a sanitized backend error:

```json
{
  "error": {
    "code": "voicebridge_http_error",
    "http_status": 429,
    "retryable": true
  },
  "status": "error",
  "is_error": true
}
```

The adapter performed no automatic retry.

Correlated service evidence showed VoiceBridge was not yet running at the time of the failed invocation and later emitted `service_started` after a read-only health wake. The VoiceBridge health endpoint then returned `status=ok`.

This is recorded as a Render free-service cold/wake edge condition, not an OAuth, MCP, bearer, or provider-work failure.

## Controlled manual retry

The owner repeated exactly the same single read-only tool invocation after VoiceBridge was awake.

The invocation completed successfully with the following structured result:

```json
{
  "automatic_paid_fallback": false,
  "configured": true,
  "duplicate_start_reuses_job": true,
  "durable_store": "postgres",
  "facebook_free_retrieval_configured": true,
  "facebook_free_retrieval_provider": "cobalt",
  "facebook_stt_configured": true,
  "facebook_stt_provider": "assemblyai",
  "instagram_retrieval_configured": true,
  "instagram_retrieval_credits": 0,
  "instagram_retrieval_provider": "cobalt",
  "instagram_stt_configured": true,
  "instagram_stt_provider": "assemblyai",
  "mode": "zero_client_managed_beta",
  "owner_access_injected_server_side": true,
  "paid_retrieval_fallback": false,
  "paid_stt_fallback": false,
  "platforms": ["youtube", "instagram", "facebook", "telegram"],
  "provider": "gemini_youtube_direct+cobalt_retrieval+assemblyai_stt",
  "restart_resilient_jobs": true,
  "supadata_public_active": false,
  "telegram_retrieval_credits": 0,
  "telegram_retrieval_provider": "telegram_public_web",
  "telegram_stt_configured": true,
  "telegram_stt_provider": "assemblyai",
  "user_beta_access_code_required": false,
  "youtube_gemini_consent_required": true,
  "youtube_gemini_free_tier_only": true,
  "youtube_gemini_model": "gemini-3.7-flash",
  "youtube_retrieval_configured": true,
  "youtube_retrieval_credits": 0,
  "youtube_retrieval_provider": "gemini_youtube_url",
  "youtube_stt_configured": true,
  "youtube_stt_provider": "gemini"
}
```

The response also contained a non-secret request identifier and the Gemini Free Tier data-use notice; those values are omitted from this checkpoint because they are not required for the acceptance marker.

## Acceptance

```text
MEDIA_GET_CAPABILITIES_LIVE=PASS
VOICEBRIDGE_SERVER_SIDE_BINDING=PASS
OWNER_ACCESS_INJECTED_SERVER_SIDE=true
CONFIGURED=true
DURABLE_STORE=postgres
RESTART_RESILIENT_JOBS=true
AUTOMATIC_PAID_FALLBACK=false
PAID_RETRIEVAL_FALLBACK=false
PAID_STT_FALLBACK=false
PROVIDER_WORK_STARTED=false
AUTOMATIC_RETRY=false
MANUAL_RETRY_AFTER_COLD_WAKE=PASS
```

## Remaining R3-C invocation gates

```text
preflight_without_provider_start=PENDING
durable_lookup_without_provider_start=PENDING
sanitized_error_behavior=PARTIAL_PASS   # 429 path observed and sanitized
execution_tools_absent=PASS
```

R3-C remains in progress and is not closed by this checkpoint.

Terminal marker:

`KRC_MEDIA_R3C_CAPABILITIES_LIVE_INVOCATION_PASS_2026_09_16`
