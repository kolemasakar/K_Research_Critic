# K-Research & Critic - MEDIA BETA
## Checkpoint 71 - M4 Image Parity Ready / Owner Deployment-Canary Decision

Date: 2026-09-02
Status: M3_CLOSED / M4_IMAGE_PARITY_READY / OWNER_DEPLOYMENT_CANARY_DECISION
Release state: RELEASE_HOLD_OWNER_TESTING

## Current provider decision

```text
M3: CLOSED
current KRC prerecorded provider: AssemblyAI universal-2
Gemini prerecorded normal activation: FALSE
provider cutover now: FALSE
future Hybrid C/D: PLANNED / NOT_IMPLEMENTED
future Hybrid trigger: AssemblyAI free credits exhausted
```

The deferred Hybrid C/D plan remains governed by checkpoint 69 / D029 and is not part of the current M4 infrastructure change.

## M4 preflight and remediation

Checkpoint 70 recorded two final-image blockers:

```text
ffmpeg/ffprobe missing from VoiceBridge runtime image
psql missing from VoiceBridge runtime image
```

VoiceBridge feature-branch remediation added the minimum runtime packages and CI final-image validation.

VoiceBridge acceptance authority:

`docs/history/2026-09-02_KRC_MEDIA_M4_IMAGE_PARITY_REMEDIATION_ACCEPTANCE.md`

Acceptance commit:

`6a9491359795840ec9e79c9edc0ea82f595e9784`

Exact-head Validate run:

`33577022166`

Result:

```text
krc-image-parity: SUCCESS
cloud: SUCCESS
browser-extension: SUCCESS
repository-docs: SUCCESS
```

## What image parity now proves

The final Docker runtime image was built in CI and verified to contain working:

```text
ffmpeg
ffprobe
psql
```

The same final image passed a no-provider-call startup smoke:

```text
GET /api/v1/health -> ok
GET /api/v1/media/managed -> KRC managed capability route responds
mode = zero_client_managed_beta
local_attachment_transport = true
```

No provider credentials, provider calls, database operations, paid retrieval, or external deployment were used by the smoke.

## Current M4 state

```text
M4_PREFLIGHT: COMPLETE
M4_IMAGE_PARITY_REMEDIATION: COMPLETE
M4_IMAGE_PARITY: PASS
M4_CANARY_PREREQUISITE_IMAGE_PARITY: PASS
M4_DEPLOYMENT: NOT_PERFORMED
M4_CANARY: NOT_RUN
M4_CANARY_AUTHORIZATION: PENDING_OWNER_DECISION
```

## What is not yet proven

Repository/CI image parity does not prove the current deployed Render service has the same image/configuration or that external runtime dependencies are healthy.

Before an owner canary, deployment-time preflight must revalidate at least:

- exact target Render service / deployment source;
- exact branch/commit/image to deploy;
- KRC environment variable presence without revealing secret values;
- Neon/PostgreSQL connectivity and durable-store readiness;
- Cobalt configuration/health for free Facebook retrieval;
- AssemblyAI current configuration and remaining free-credit operating policy;
- rollback target and rollback procedure;
- current Action URL compatibility and no Builder/schema mutation unless separately authorized;
- no automatic paid fallback.

## Owner gate

The next step is no longer ordinary feature-branch engineering. It may affect an external backend deployment.

Therefore execution must STOP here until the owner separately authorizes the exact M4 deployment/canary scope.

Possible next decision:

```text
APPROVE M4 OWNER CANARY
HOLD
REJECT / REPLAN
```

Approval of an owner canary would still not authorize:

```text
R1 merge to public Core
R3 external testers
R4 public rollout
provider cutover
Hybrid C/D activation
automatic paid fallback
```

## Release boundary

```text
R1 merge: HOLD
R2 backend/production promotion: HOLD unless separately scoped for owner canary
R3 external testers: HOLD
R4 public rollout: HOLD
```

## Recovery command

`recover KRC MEDIA BETA checkpoint 71 M4 image parity ready owner canary decision 2026-09-02`
