# KRC MEDIA — R3-E2 restart replay PASS / status+segments PASS

Date: 2026-09-19  
Status: **AUTHORITATIVE CHECKPOINT / R3-E2 RESTART REPLAY PASS / STATUS+SEGMENTS PASS / PROVIDER REPLAY ZERO / DUPLICATE-START IDEMPOTENCY PENDING**

## Scope

This checkpoint records the owner-authorized restart/replay acceptance for the successful R3-E2 Instagram live canary job.

Target durable job:

```text
job_id=KRCM_04e6d847-449c-4d0f-82c7-b494871d9322
status=COMPLETED
segment_count=1
```

No new `media_instagram_start` was executed during this checkpoint.

## Read-only replay probe

R3-E2 gained a bounded startup replay probe modeled on the previously accepted R3-E1 pattern:

```text
KRC_R3E2_REPLAY_PROBE_JOB_ID
```

The probe invokes only:

```text
media_non_youtube_status
media_non_youtube_segments
```

It never invokes `media_instagram_start`.

Implementation commits:

```text
c07e906411656996770900b347434e87abe84af9
03f60bcf9c7005cdf4436e18d3e54a086da835e2
```

Validation:

```text
Tests #1733=SUCCESS
Python 3.13=PASS
Python 3.14=PASS
Quality gates=PASS
```

## VoiceBridge restart proof

VoiceBridge was replaced using the accepted patched head:

```text
service=voicebridge-krc-media-beta-kolemasakar
commit=e7b8ebb2803f46656ed07483f87beb31b740f436
deploy=dep-danak4mk1f9s7382ou1g
status=LIVE
health=HTTP 200 / status=ok
```

After the VoiceBridge restart, Neon still contained:

```text
job_id=KRCM_04e6d847-449c-4d0f-82c7-b494871d9322
status=COMPLETED
segment_count=1
```

## R3-E2 restart / application-level replay

R3-E2 was then replaced with the replay probe enabled:

```text
service=krc-mcp-r3e2-instagram-sentinel-v2
commit=03f60bcf9c7005cdf4436e18d3e54a086da835e2
deploy=dep-danakn6gekts738aplj0
status=LIVE
```

Startup evidence:

```json
{"event":"r3e2_record_replay_probe","job_id":"KRCM_04e6d847-449c-4d0f-82c7-b494871d9322","job_status":"COMPLETED","next_cursor":null,"page_segment_count":1,"provider_work_started":false,"segment_count":1,"start_called":false,"status":"pass"}
```

Therefore:

```text
VOICEBRIDGE_RESTART_REPLAY=PASS
R3E2_RESTART_REPLAY=PASS
STATUS_READ_AFTER_RESTART=PASS
SEGMENTS_READ_AFTER_RESTART=PASS
PROVIDER_WORK_AFTER_RESTART=false
START_CALLED_DURING_REPLAY=false
```

## Cleanup

The temporary replay environment variable was disabled after evidence capture:

```text
KRC_R3E2_REPLAY_PROBE_JOB_ID=disabled
```

Final clean R3-E2 deployment:

```text
deploy=dep-danal3bbc2fs73do967g
commit=03f60bcf9c7005cdf4436e18d3e54a086da835e2
status=LIVE
health=HTTP 200 / status=ok
confirmation_probe_only=false
provider_work_started=false
tool_count=5
execution_tool_count=1
```

Neon after cleanup remains:

```text
job_id=KRCM_04e6d847-449c-4d0f-82c7-b494871d9322
status=COMPLETED
segment_count=1
```

## Error scan

For the restart/replay window beginning at 2026-09-19T15:28:10Z:

```text
VoiceBridge 5xx/error/exception scan=0
R3-E2 5xx/error/exception/traceback scan=0
ERROR_SCAN=PASS
```

## Gate status

```text
R3_E2_LIVE_CANARY=PASS
NEON_JOB_PERSISTENCE=PASS
VOICEBRIDGE_RESTART_REPLAY=PASS
R3E2_RESTART_REPLAY=PASS
STATUS_READ_AFTER_RESTART=PASS
SEGMENTS_READ_AFTER_RESTART=PASS
PROVIDER_REPLAY_AFTER_RESTART=NO
ERROR_SCAN=PASS

DUPLICATE_START_IDEMPOTENCY=PENDING
DUPLICATE_START_REUSED=PENDING
DUPLICATE_PROVIDER_WORK_ZERO=PENDING
R3_E2_FINAL_CLOSURE=PENDING
```

## OAuth consequence

R3-E2 OAuth client/token state remains in-memory, so the final clean redeploy invalidated the previous ChatGPT DCR session.

Before duplicate-start idempotency acceptance, a fresh private MCP DCR/reconnect is required.

## Preserved boundaries

```text
PROJECT_COST_POLICY=FREE_ONLY
PAID_DATABASE_UPGRADE=DENIED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
R3_E3_E4=HOLD
R4=HOLD
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_138_R3E2_RESTART_REPLAY_STATUS_SEGMENTS_PASS_2026_09_19`
