# KRC MEDIA — Free-only infrastructure policy clarification

Date: 2026-09-19  
Status: **AUTHORITATIVE POLICY CLARIFICATION / FREE_ONLY / RENDER_FREE_WEB_ALLOWED / RENDER_POSTGRES_REJECTED_FOR_DURABLE_STATE**

## Decision

The project goal is **not** to eliminate Render as a platform.

The authoritative infrastructure policy is:

```text
PROJECT_COST_POLICY=FREE_ONLY

RENDER_FREE_WEB_SERVICES=ACCEPTED
RENDER_ONRENDER_COM_ENDPOINTS=ACCEPTED
RENDER_POSTGRES=REJECTED_FOR_DURABLE_STATE
RENDER_PAID_UPGRADE=DENIED

NEON_FREE_POSTGRES=PRIMARY_DURABLE_DATABASE
OCI_ALWAYS_FREE=ACCEPTED
SELF_HOSTED_COBALT_ON_OCI=ACCEPTED

PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
UNEXPECTED_BILLING_RISK=DENIED
```

## Meaning

Render Free Web Services remain an accepted hosting layer for KRC MEDIA components, including VoiceBridge and isolated MCP sentinels, as long as they remain within the free plan and do not introduce a required paid dependency.

Addresses under `.onrender.com` are therefore expected and valid in the accepted architecture.

The rejected dependency is specifically **Render PostgreSQL as durable state**. The previous Render PostgreSQL instance expired/suspended and would require a paid upgrade, which conflicts with the FREE_ONLY policy.

Neon Free PostgreSQL is the accepted primary durable database.

## Current accepted architecture

```text
ChatGPT / KRC
    -> Render Free Remote MCP sentinels
    -> Render Free VoiceBridge
    -> Neon Free PostgreSQL
    -> OCI Always Free self-hosted Cobalt
    -> free-tier provider paths
```

This clarification does not alter R3-E1 or R3-E2 acceptance evidence and does not authorize any paid resource.

## Preserved boundaries

```text
PAID_DATABASE_UPGRADE=DENIED
PAID_RENDER_WEB_UPGRADE=DENIED
PAID_HOSTING_FALLBACK=DENIED
PAID_PROVIDER_FALLBACK=DENIED
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
MAIN_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_133_FREE_ONLY_INFRASTRUCTURE_POLICY_RENDER_WEB_ALLOWED_POSTGRES_REJECTED_2026_09_19`
