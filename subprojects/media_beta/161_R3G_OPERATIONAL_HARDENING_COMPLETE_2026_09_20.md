# KRC MEDIA — R3-G operational hardening COMPLETE

Date: 2026-09-20
Status: **R3_G_COMPLETE / OAUTH_REFRESH_RUNTIME_PASS / E3_VOICEBRIDGE_ROUTE_AUTH_PASS / FREE_ONLY**

## OAuth runtime acceptance

Already-connected ChatGPT E3 private MCP crossed the original 3600-second access-token TTL and refreshed without reconnect.

Runtime evidence:

```text
POST /oauth/token = 200
POST /mcp = 200
reconnect_required=false
```

Accepted:

```text
R3_G_REFRESH_TOKEN_RUNTIME_CONTINUITY=PASS
R3_G_ACCESS_TOKEN_REFRESH_AFTER_TTL=PASS
R3_G_CHATGPT_RECONNECT_REQUIRED=NO
```

## E3 -> VoiceBridge route-auth remediation

A route-scoped R3-E3 bearer override was synchronized between E3 and VoiceBridge without exposing the secret in repository or documentation.

Boolean integrity evidence:

```text
E3:
  voicebridge_override_configured=true
  voicebridge_override_matches_expected_sha256=true

VoiceBridge:
  override_configured=true
  override_matches_expected_sha256=true
  effective_token_configured=true
  effective_token_matches_expected_sha256=true
  auth_diagnostic_enabled=false
```

Final post-deploy read-only request using the scoped credential:

```text
GET /api/v1/media/managed/transcriptions/KRCM_2dbbe3ba-c2da-49c4-9941-f64b22630880
HTTP=404
error=MEDIA_TRANSCRIPT_NOT_FOUND
```

This is an authenticated application-level 404, not a 401/429 auth failure.

Therefore:

```text
E3_TO_VOICEBRIDGE_AUTH=PASS
ROUTE_SCOPED_BEARER_DELIVERY=PASS
401_REMEDIATION=PASS
429_GENERAL_ADMISSION_PATH_AVOIDED=PASS
PROVIDER_WORK_STARTED=false
ADDITIONAL_MEDIA_STARTS=0
```

## Durable job retention / 404 explanation

VoiceBridge runtime health:

```text
managed_media_retention.job_ttl_seconds=3600
```

Neon authoritative table after the elapsed retention window:

```text
public.krc_managed_media_jobs total_rows=0
```

Repository behavior:

```text
DELETE FROM krc_managed_media_jobs WHERE expires_at <= now()
read path requires expires_at > now()
default jobTtlSeconds=3600
```

Thus the Facebook/Telegram/Instagram canary rows expired by policy. The post-expiry 404 is expected and does not invalidate the earlier restart durability and idempotency acceptance performed inside the retention window.

## CI / deployed heads

```text
KRC code head=dbcebdff0201fd9240a7aeafa5f5d5dd46ca08f7
KRC tests run=35485995871 PASS

VoiceBridge code head=db9fb62c57fc731732f88ff5b417a0f15be178b6
VoiceBridge validate run=35492121039 PASS
VoiceBridge deploy=dep-dann2op42hec73f1s7s0 LIVE
```

## Phase result

```text
R3_A=PASS
R3_B=PASS
R3_C=PASS
R3_D=PASS
R3_E1=COMPLETE
R3_E2=COMPLETE
R3_E3=COMPLETE
R3_E4=COMPLETE
R3_F=COMPLETE
R3_G=COMPLETE
R3_H=READY_FOR_REVIEW
R4=HOLD
```

## Safety boundary

```text
PROJECT_COST_POLICY=FREE_ONLY
E2_CONFIRMATION_PROBE_ONLY=true
E3_CONFIRMATION_PROBE_ONLY=true
E4_CONFIRMATION_PROBE_ONLY=true
ADDITIONAL_LIVE_MEDIA_STARTS=NO
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
R4=HOLD
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_161_R3G_OPERATIONAL_HARDENING_COMPLETE_2026_09_20`
