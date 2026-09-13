# KRC MEDIA — Current Access Paths

Date: 2026-09-13
Status: CURRENT

## Primary project automation

```text
GitHub Actions OIDC -> Tailscale -> Tailscale SSH -> krcops -> bounded helpers
```

Accepted authority ceiling:

```text
tier0
tier1
tier2_restart
```

## Supplemental development access

RDC under `krcops` remains available as supplemental development access. It does not expand the bounded-helper authority ceiling.

## OCI infrastructure observation

OCI instance-principal authentication is available for read-only infrastructure observation from the KRC Cobalt host.

Persistent OCI authority is read-only. No reusable OCI user credential is stored in the repository.

Canonical detailed record:

`docs/KRC_MEDIA_OCI_CONTROLPLANE_READONLY_ACCESS_2026_09_13.md`

## Boundary

These access paths do not grant arbitrary root, unrestricted container control, deployment authority, secret reads, or general cloud mutation.
