# KRC MEDIA — Current Access Paths
Поточні підтверджені шляхи доступу до KRC MEDIA.

Date: 2026-09-13
Status: CURRENT / VERIFIED

## Primary project automation

```text
GitHub Actions OIDC
  -> OCI dynamic-group policy
  -> OCI control-plane read-only access
```

Purpose:
- inspect instance and network state;
- verify KRC MEDIA infrastructure without reusable OCI user credentials.

## Host operation

```text
GitHub Actions OIDC
  -> Tailscale
  -> Tailscale SSH
  -> krcops
  -> bounded sudo helper
```

Allowed tiers:
- tier0: read-only observation;
- tier1: bounded media-service status/diagnostics;
- tier2_restart: bounded restart-only control.

No general shell/root automation is granted.

## Supplemental development access

RDC remains available as a supplemental operator/development path. It is not the canonical project automation authority.

## Security boundary

- OCI control-plane access is read-only.
- Runtime mutations remain bounded by explicit helper/sudo policy.
- Secrets are not stored in repository documentation.
- Broad OCI user credentials are not part of the accepted path.
