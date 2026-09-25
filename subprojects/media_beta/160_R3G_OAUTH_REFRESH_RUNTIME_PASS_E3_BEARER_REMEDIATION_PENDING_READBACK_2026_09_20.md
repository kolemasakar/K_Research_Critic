# KRC MEDIA — R3-G OAuth runtime refresh continuity PASS / E3 route bearer remediation pending readback

Date: 2026-09-20
Status: **R3_G_OAUTH_REFRESH_RUNTIME_PASS / INTERNAL_E3_VOICEBRIDGE_AUTH_REMEDIATED_PENDING_READBACK**

## Runtime OAuth refresh acceptance

The already connected ChatGPT E3 private MCP was invoked after the original 3600-second access-token TTL had expired.

Render evidence:

```text
2026-09-20T01:30:20Z POST /oauth/token = 200
2026-09-20T01:30:21Z POST /mcp = 200
reconnect_required=false
```

Therefore:

```text
R3_G_REFRESH_TOKEN_RUNTIME_CONTINUITY=PASS
R3_G_ACCESS_TOKEN_REFRESH_AFTER_TTL=PASS
R3_G_CHATGPT_RECONNECT_REQUIRED=NO
```

This complements the existing CI coverage for:

```text
DCR_CLIENT_SURVIVES_RESTART=PASS
ACCESS_TOKEN_SURVIVES_RESTART=PASS
REFRESH_TOKEN_SURVIVES_RESTART=PASS
AUTH_CODE_SINGLE_USE=PASS
AUTH_CODE_IN_MEMORY_ONLY=PASS
WRONG_SIGNING_KEY_FAIL_CLOSED=PASS
TAMPERED_TOKEN_FAIL_CLOSED=PASS
EXPIRED_ACCESS_FAIL_CLOSED=PASS
EXPIRED_REFRESH_FAIL_CLOSED=PASS
```

## Separate internal-auth finding

The read-only E3 call reached the authenticated MCP surface successfully but VoiceBridge returned:

```text
voicebridge_http_error
http_status=401
retryable=false
```

This is a separate E3-to-VoiceBridge server-side bearer issue and does not invalidate the OAuth refresh evidence above.

The E3 route-scoped credential was rotated and synchronized only between:

```text
VoiceBridge KRC_MEDIA_R3E3_ACTION_TOKEN
E3 KRC_VOICEBRIDGE_BEARER
```

No secret value was written to the repository or exposed in documentation.

Post-rotation deploys:

```text
VoiceBridge deploy=dep-danjf6h42hec73en3jc0 status=live
E3 deploy=dep-danjf7bm8hqs73bhj870 status=live
VoiceBridge health=PASS
E3 health=PASS
E3 confirmation_probe_only=true
E3 provider_work_started=false
```

## Next gate

Repeat exactly one read-only `media_non_youtube_status` call for the already completed Facebook job.

Expected:

```text
MCP authentication succeeds
VoiceBridge internal auth succeeds
job_id=KRCM_2dbbe3ba-c2da-49c4-9941-f64b22630880
status=COMPLETED
no provider work
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_160_R3G_OAUTH_REFRESH_RUNTIME_PASS_E3_BEARER_REMEDIATION_PENDING_READBACK_2026_09_20`
