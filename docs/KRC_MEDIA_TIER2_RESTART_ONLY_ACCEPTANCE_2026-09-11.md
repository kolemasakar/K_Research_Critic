# KRC MEDIA — Tier-2 Restart-Only Acceptance — 2026-09-11

Status: **COMPLETE / LIVE ACCEPTANCE PASS / FROZEN**

## Accepted control path

```text
GitHub Actions workflow_dispatch on main
  -> dedicated KRC GitHub OIDC identity
  -> Tailscale tag:krc-media-github-actions
  -> tag:krc-media-node1:22
  -> Tailscale SSH
  -> krcops
  -> exact sudo helper
  -> restart-only accepted Cobalt backend
```

The workflow remains `.github/workflows/krc-media-tier0-control.yml` and exposes exactly:

```text
tier0
tier1
tier2_restart
```

## Canonical repository acceptance

```text
PR #19: merged by squash
main SHA: 1a61509ca925166d3a59c40d90fc671bd3027e55
exact-main CI run: 34617085456
exact-main CI conclusion: success
```

## Host layer

```text
/usr/local/sbin/krc-tier2-media-restart
root:root 0755

/etc/sudoers.d/92-krcops-tier2-media-restart
root:root 0440
visudo: PASS
```

The sudoers rule authorizes the exact helper with no arguments only.

Pre-live negative tests passed:

```text
P8_C_ARBITRARY_ROOT=DENIED
P8_C_ARGUMENTS=DENIED
P8_C_DIRECT_DOCKER_ACCESS=DENIED
```

Tier-1 precheck before live acceptance confirmed the accepted Cobalt identity and `tier1_backend_status=PASS`.

## Fail-closed restart contract

The helper requires exactly one running backend matching:

```text
image=ghcr.io/imputnet/cobalt@sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
port=127.0.0.1:9000 only
user=node
ReadOnlyRootfs=true
Privileged=false
```

It does not start a stopped backend. Identity mismatch, ambiguity, or missing backend causes failure before mutation.

Its sole mutation is an exact Docker restart of the resolved accepted running container. The same identity is revalidated after restart.

## Canonical live acceptance

```text
run_id=34618591919
job_id=103326586885
workflow=KRC MEDIA Tier-0 Tailscale Control
branch=main
operation=tier2_restart
repository_sha=1a61509ca925166d3a59c40d90fc671bd3027e55
conclusion=success
```

Restart helper output:

```text
P8_C_RESTART_VERSION=1
backend_type=cobalt
backend_identity_verified=yes
pre_restart_running=true
restart_requested=yes
post_restart_running=true
post_restart_identity_verified=yes
tier2_restart_status=PASS
```

Final acceptance markers:

```text
P8_C_REPOSITORY_BOUNDARY=PASS
P8_C_NODE_IDENTITY=PASS
P8_C_PRECHECK=PASS
P8_C_BACKEND_IDENTITY=PASS
P8_C_RESTART=PASS
P8_C_POSTCHECK=PASS
P8_C_ARBITRARY_ROOT=DENIED
P8_C_ARGUMENTS=DENIED
P8_C_DIRECT_DOCKER_ACCESS=DENIED
P8_C_OWNER_USER=DENIED
P8_C_ROOT_USER=DENIED
P8_C_KGM_ISOLATION=PASS
P8_C_SECRET_VALUES=NOT_EXPOSED
P8_C_TIER0_REGRESSION=PASS
P8_C_TIER1_REGRESSION=PASS
KRC_PHASE_8_P8_C_RESTART_ONLY=PASS
KRC_PHASE_8_OPERATION=TIER2_RESTART_ONLY
```

## Explicit authority ceiling

Tier-2 is **restart-only**. The following remain unauthorized:

- start or stop;
- reload;
- deploy;
- Docker pull or image change;
- container replacement;
- Docker exec or direct Docker access for `krcops`;
- Compose operations;
- configuration mutation;
- secret/env/key/log access;
- firewall or OCI NSG changes;
- public exposure changes;
- reverse proxy/TLS changes;
- owner `ubuntu` automation;
- root automation;
- KGM access.

Any expansion requires a new explicit authorization and acceptance phase.
