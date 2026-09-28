# KRC MEDIA — R4-B read-only 429 leakage fixed; deploy LIVE; final authenticated B2 rerun pending

Date: 2026-09-22  
Status: **AUTHORITATIVE CHECKPOINT / R4_B_IN_PROGRESS / B1_PASS / B2_READONLY_429_FIX_DEPLOYED / B2_FINAL_AUTH_RERUN_PENDING / B3_PASS / FREE_ONLY / PUBLICATION_HOLD**

## Input

Checkpoint 174 established:

```text
B1=PASS
B3=PASS
VoiceBridge cold-start 429 remediation=PASS
B2 authenticated rerun=PENDING
```

The authenticated rerun then produced:

```text
media_get_capabilities=PASS
media_youtube_preflight=PASS
media_youtube_lookup=404 non-retryable
media_youtube_status=404 non-retryable
media_youtube_segments=404 non-retryable
media_instagram_preflight=PASS
media_instagram_lookup=429 retryable
media_non_youtube_status=429 retryable
media_non_youtube_segments=429 retryable
```

## Diagnosis

The remaining non-YouTube 429 was traced to `PublicMediaAdmissionController`.

Before remediation it applied free-tier admission rate/concurrency to every authenticated path under:

```text
/api/v1/media/managed/*
```

That included read-only operations:

```text
preflight
lookup
status
segments
```

The controller enforces a one-request-per-second minimum interval. Therefore a successful read-only preflight could immediately cause the next read-only lookup/status/segments call to return retryable 429 even though no provider work was requested.

This was a read-only admission leakage defect.

## Minimal remediation

VoiceBridge branch:

```text
repo=kolemasakar/VoiceBridge
branch=agent/krc-media-gemini-migration
```

Code commit:

```text
eda6fce7236eaa3d119864236078fbe45e5379f3
fix(media): exclude read-only routes from provider admission limits
```

Regression-test commit / deployed head:

```text
174174aae0635736f05d812094b555544623270c
test(media): keep read-only routes outside provider admission limits
```

New admission semantics:

```text
capabilities=NO provider admission budget
preflight=NO provider admission budget
lookup=NO provider admission budget
status=NO provider admission budget
segments=NO provider admission budget

POST /api/v1/media/managed/transcriptions
  = provider-start path
  = free-tier rate limit preserved
  = concurrency limit preserved
```

FREE_ONLY and authentication were not weakened.

## Validation

Static exact-branch validation:

```text
provider_start_classifier=PASS
read_only_bypass=PASS
start_rate_limit_preserved=PASS
start_concurrency_limit_preserved=PASS
regression_test_added=PASS
```

Container test execution was unavailable because the local container has no DNS/network access to GitHub. GitHub Actions remain unavailable. Render build therefore provides compile validation only, not the Node test suite.

Render deployment:

```text
service=voicebridge-krc-media-beta-kolemasakar
deploy=dep-dapb6f3m8hqs7395ntj0
exact_commit=174174aae0635736f05d812094b555544623270c
status=LIVE
typescript_build=PASS
post_deploy_health=200
service_version=0.6.0
job_ttl_seconds=3600
```

PR #45 remains open/draft/unmerged.

## YouTube 404 interpretation

VoiceBridge explicitly defines missing lookup/status/segments resources as:

```text
code=MEDIA_TRANSCRIPT_NOT_FOUND
http_status=404
retryable=false
```

The runtime retention TTL is currently 3600 seconds. Therefore old acceptance fixture jobs can legitimately expire and return 404.

For B2, a read-only operation is a contract PASS when it reaches authenticated runtime and returns its expected read semantic. A missing/expired fixture may therefore satisfy the negative read path with `404 non-retryable`; B2 must not require provider execution merely to manufacture a fresh job.

## Final B2 acceptance rule

Repeat only the nine authenticated Candidate read-only operations.

Acceptance:

```text
authentication=PASS
operations_attempted=9/9
infrastructure_429=0
execution_tools_called=0
provider_work_started=0

capabilities/preflight:
  expected=successful read result

lookup/status/segments:
  expected=either successful existing-job read
           OR MEDIA_TRANSCRIPT_NOT_FOUND / 404 / retryable=false
```

Any retryable 429 on a read-only managed operation after the deployed fix is a failure and must be investigated.

## State

```text
B1=PASS
B3=PASS
B2_READONLY_429_FIX=DEPLOYED_LIVE
B2_FINAL_AUTHENTICATED_RERUN=PENDING
R4_B_OVERALL=NOT_COMPLETE
R4_C_AUTHORIZED=NO

media_*_start=NOT_EXECUTED
provider_work=NOT_STARTED
publication=NO
sharing=NO
public_GPT_mutation=NO
PR22_merge=NO
PR45_merge=NO
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_175_R4B_READONLY_429_LEAKAGE_FIXED_DEPLOY_LIVE_B2_FINAL_AUTH_RERUN_PENDING_2026_09_22`
