# Execution failure stage diagnostics — 2026-10-04

## Change

Allowlisted failure_stage=warmup/readiness/start with consequential_post_attempted boolean. Warmup/readiness=false means execution did not send a consequential POST. start=true only means an attempt was made, not provider acceptance or billing. Inconsistent/untrusted stage values are stripped at MCP egress. No retry-policy, timeout-budget, credentials, model or billing changes.

E2's existing45s health-only warmup now preserves failure location. The new r3c readiness gate marks its failure separately, and errors from the single start POST mark the attempted send. No automatic POST replay.

## Validation

Full KRC425PASS/9fixture-skipped18.18s. Follow-up includes final allowlist type validation plus9 real HTTPS cross-repository tests using isolated research fixtures:13PASS20.31s. Production fixture injection excluded. Tests verify each failure stage, no POST before readiness, no ambiguous replay, unsafe/inconsistent stage rejection.

## Gemini request review

Official https://ai.google.dev/gemini-api/docs/video-understanding REST YouTube example matches existing v1beta/interactions text+videoURI request. Official https://ai.google.dev/gemini-api/docs/pricing lists Gemini3.7Flash input/output FreeTier free. No verified request-shape or model-eligibility defect found. Keepgemini-3.7-flash; earlier400causeunresolved. Latestpriorproviderfailure503service_unavailable. No speculative model/mime_type change.

## Rollout

Deploy the tested KRC commit only to existing free E2. Activate bounded one-start test then restore probe-only. Recheck YouTube preflight/lookup before one separatelyauthorized freshstart. InitialreadonlyYouTubepreflight429; canonicalVoiceBridgehealth200/statusok request46c62010-5d3a-4812-81a1-8b1b34c6f321 afterwake.
