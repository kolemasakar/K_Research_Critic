# Stage131 ↔ K_Sentinel transport reconciliation — 2026-10-28
**STAGING ONLY / FREE_ONLY / Production NO-GO.**

## Source of authoritative correction
Sentinel Draft PR #38 head `77177352be4a8fa7c3b965b5d5b95e07939a7c82` and `docs/STAGE127_SIMPLIFY_REUSE_EXISTING_TRANSPORT_PIVOT_2026-10-28.md` state owner direction to **REUSE existing authenticated transport**, separate all scientific validation, and STOP inventing transport layers/ports. K_Science main now contains **minimal network-only** workflow at commit `a43d2919e73581381d8839cd2b8bbb3c4c9ad804`. Draft PR #6 not merged; same workflow path collision must be reconciled before merge.

## Reconciled responsibility
- Sentinel/existing gateways: signed OIDC RS256 JWKS, exact workflow/audience/owner/repo/ref claims, Tailscale whois of real TCP peer and tag, durable token jti and request replay, bounded authenticated transport and strict explicit allowlist. No Science HMAC key, bibliography, CriticProfile or author consent decisions in transport.
- KRC Stage131: isolated local-only Unix-domain backend; four scientific operations, request/task scope, science consent provenance, internal signer, durable science replay, bibliography metadata and bounded artifact storage. Does NOT expose HTTP/Tailscale and does NOT duplicate OIDC.
- K_Science: narrowly scoped prepared workflows, explicit manual pilot, exact fixtures and 29 NOT_RUN E2E cases; signed scientific success must never be inferred from transport success.

## Existing transport candidates, NO automatic modification
- :19015 `kscience-krc-gateway.service`: already authenticates OIDC + Tailnet + persistent replay; deployed LIVE_ALLOWED limited to `krc_capabilities` / `krc_tools_list` and MCP_CALL_ALLOWED only `krc_capabilities`; cannot dispatch arbitrary research today. Inspect and regression-test a **narrow explicit** new adapter from that transport to Stage131 UDS; never broaden a wildcard MCP backend or modify active gateway before isolated review.
- :19016 `krc-stage114.service`: similar authenticated path but science logic currently embedded. Candidate for extraction into KRC, not a second long-term ingress.
- :19017 `krc-sentinel-stage127.service`: existing isolated staging pilot is active; keep only for bounded no-bearer network diagnostics, not proposed canonical new transport.
- Stage131 UDS `/run/krc-stage131/backend.sock` is a **local application boundary**, not a new remote transport. Distinct UID988/GID984 permission checks and transport caller UID/keys need explicit peer adapter contract. Nothing shall repoint :19015 automatically.

## Concrete gaps before integration
1. Decide supported transport (:19015 preferred evaluation) by side-by-side read-only code/security/behavior tests, then design explicit fixed operation dispatch adapter and local UDS peer credentials. Record expected `client,principal,repository,workflow_ref` exactly after verified OIDC projection. Avoid using untrusted caller-supplied fields.
2. Secure Stage131 config paths and root-controlled distinct `/etc/krc-stage131/approvals`; existing `ConsentCustody128` defaults to Stage126 path and **must not** be enabled unchanged. Explicit owner ticket and independently audited issuance remain absent; synthetic grant does not count.
3. Match identity projection with Sentinel verified `K_Science` canonical claims; durable token replay and science consent replay remain separate.
4. Approve final four-operation schema/envelope, exact errors/idempotency/artifact GET/rate/quotas. Public DOI metadata read only, no independent scientific proof.
5. Verify minimal main network-only probe :19017 when owner runs it. It checks HTTP403 without bearer; positive OIDC/E2E still NOT_RUN. Never merge PR #6 wholesale over the smaller main workflow.
6. Run E2E-01–05 only after backend consent/signer and canonical authenticated transport are independently accepted, with all three pinned SHAs and evidence.

## Superseded planning assertions
Any Stage131 plan saying a **new** Sentinel v2 transport must be built before progressing is superseded by the reuse-first decision. An **isolated local Stage131 backend** and its manual-only unit remain valid. No root install, activation, PR merge, public/production promotion or new port is authorized here.
