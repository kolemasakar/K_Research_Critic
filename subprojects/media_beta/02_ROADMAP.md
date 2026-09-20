# MEDIA BETA Roadmap

Version: 7.4
Status: **PLUGIN_FIRST / R3-E1_COMPLETE / R3-E2_COMPLETE / R3-E3_COMPLETE / R3-E4_COMPLETE / R3-F_COMPLETE / R3-G_REFRESH_RUNTIME_PENDING / FREE_ONLY / PUBLICATION_HOLD**
Updated: 2026-09-20

## Current roadmap position

```text
R3-A Contract freeze/security baseline        PASS
R3-B Authentication/secret hardening          PASS
R3-C 9-tool read-only binding                 PASS
R3-D Consequential-action confirmation        PASS
R3-E1 YouTube execution                       PASS / COMPLETE
R3-E2 Instagram execution                     PASS / COMPLETE
R3-E3 Facebook execution                      PASS / COMPLETE
R3-E4 Telegram execution                      PASS / COMPLETE
R3-F Full 13-operation parity                 PASS / COMPLETE
R3-G Private operational hardening            ACCESS RESTART PASS / REFRESH RUNTIME PENDING
R3-H Migration/publication readiness          HOLD
R4 Owner-approved cutover/publication         HOLD
```

## R3-F accepted contract

```text
READ_OPERATIONS=9
EXECUTION_OPERATIONS=4
TOTAL_OPERATIONS=13
R3C_EXECUTION_TOOLS=0
E1_OTHER_EXECUTION_TOOLS=0
E2_OTHER_EXECUTION_TOOLS=0
E3_OTHER_EXECUTION_TOOLS=0
E4_OTHER_EXECUTION_TOOLS=0
RUNTIME_PARITY=PASS
```

## R3-G remaining work

Already demonstrated at runtime:

- OAuth DCR;
- initial token issuance;
- authenticated E3/E4 calls;
- authenticated calls after E3/E4 service redeploy;
- stable server-side signing keys.

Already covered in CI:

- client/access/refresh continuity across restart;
- reusable refresh token until expiry;
- authorization code single-use and in-memory;
- wrong signing key / rotation invalidation;
- tampered token fail-closed;
- expired access/refresh fail-closed.

Remaining runtime gate:

1. wait until the existing access token exceeds the 3600-second TTL;
2. invoke one read-only operation on an already connected private MCP;
3. require `POST /oauth/token -> 200`;
4. require subsequent authenticated `POST /mcp -> 200` without reconnect;
5. close R3-G.

## Safety invariant

```text
E2_CONFIRMATION_PROBE_ONLY=true
E3_CONFIRMATION_PROBE_ONLY=true
E4_CONFIRMATION_PROBE_ONLY=true
ADDITIONAL_LIVE_MEDIA_STARTS=NO
PROJECT_COST_POLICY=FREE_ONLY
AUTOMATIC_PAID_FALLBACK=DENIED
```

## Next phases

- close R3-G runtime refresh-token continuity;
- perform R3-H migration/publication readiness review;
- keep public mutation, plugin publication/sharing, main merges and R4 on HOLD until separately approved.

Recovery authority: `CURRENT_HANDOFF.md` v19.3 + checkpoint 159.
