# Stage131 K6 response schema / K7 integration handoff — 2026-10-28
**STAGING ONLY / FREE_ONLY / Production NO-GO; DRAFT not a frozen external contract.**

New strict response schema at schemas/stage131/science_response_v1.schema.json. Success and error messages are separate, known error codes only, unknown keys denied, and every error demands scientific_approval=false. This is a design candidate: actual KRC Stage123/131 on-wire responses are not yet proven to conform, and transport HTTP status mapping remains for joint review with K_Sentinel. Do NOT route live traffic to this schema without a compatibility bridge and integration regression.

Paired strict request schema remains schemas/stage131/science_request_envelope_v1.schema.json. Neither schema by itself authenticates OIDC, grants consent, enforces a byte-size limit or provides per-operation scientific payload constraints. Source-of-truth authority remains KRC backend with explicit grants only.

On krc-cobalt pinned source HEAD 70062c54ea286e30c78a79c1edee9dada41005e5, targeted request/response schema, Stage131 configuration, consent, Artifact Stage117/Stream116 tests **27/27 PASS**. Stage126 and Sentinel Stage127 ACTIVE NRestarts=0. No installations/starts.

K7 protected local HardenedExchange enforces principal/request scoping, TTL, SHA256 and read chunk limits. Authenticated artifact GET external route is NOT implemented or frozen. No public GET or broad MCP backend allowed.

Next KRC-only engineering gates: capture actual UDS response fixtures for four operations, compare to this DRAFT schema; formalize request-response versioning and error mapping without exposing science credentials; test artifact GET via authenticated boundary with replay and timeout. All live owner approval and scientific E2E gates remain outstanding.
