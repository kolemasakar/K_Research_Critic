# KRC MEDIA Phase 8C — Bounded Cobalt Restart
Обмежений контрольований перезапуск Cobalt для KRC MEDIA без розширення інших повноважень.

Status: **REPOSITORY IMPLEMENTATION CANDIDATE / HOST BOOTSTRAP PENDING / LIVE ACCEPTANCE PENDING**

## Authorization

Project Owner authorized entry into Phase 8C on 2026-09-11.

Phase 8C is intentionally limited to one Tier-2 mutation:

```text
restart exact current Cobalt backend only
```

Not authorized by this phase:

- start or stop as standalone operations;
- deploy, pull, recreate, remove or exec;
- Docker socket/API access for `krcops`;
- arbitrary root;
- secret/env/key/log reads;
- firewall, OCI NSG, public-port or reverse-proxy changes;
- container hardening or provider/model/runtime changes;
- KGM or K-Trader changes.

## Accepted pre-Phase-8C baseline

```text
backend_name=krc-cobalt
backend_type=cobalt
backend_image_digest=sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
backend_running=true
backend_loopback_only=yes
backend_port=9000
backend_user=node
backend_read_only_rootfs=true
backend_privileged=false
```

## Tier-2 helper

Tracked source:

```text
ops/krc-media/phase8c/krc-tier2-cobalt-restart
```

Target host path:

```text
/usr/local/sbin/krc-tier2-cobalt-restart
```

The helper accepts no arguments, pins the exact container identity and image,
requires the accepted security/binding invariants before mutation, performs
exactly one `docker restart --time 10 krc-cobalt`, then re-validates the same
invariants before returning a fixed sanitized result.

Helper SHA-256:

```text
9ef17650c6eb0e94a55e80cac77b03c0eb0c98f37a913d1a9f38702c47acf27f
```

## Sudo boundary

Tracked rule:

```text
ops/krc-media/phase8c/92-krcops-tier2-cobalt-restart
```

Target:

```text
/etc/sudoers.d/92-krcops-tier2-cobalt-restart
```

The sudoers entry is SHA-256 pinned and uses the sudoers empty-argument
constraint (`""`), so `krcops` may invoke only the exact helper with no
arguments.

## Owner-side bootstrap

Tracked bootstrap:

```text
ops/krc-media/phase8c/bootstrap-tier2-restart.sh
```

It installs the root-owned helper (`0755`) and sudoers fragment (`0440`),
validates sudoers before activation, verifies the installed helper digest,
and performs negative privilege tests. It does **not** restart Cobalt.

Expected terminal marker:

```text
KRC_PHASE_8_P8_C_HOST_BOOTSTRAP=APPLIED
```

## Repository control path

The accepted trusted workflow identity is preserved:

```text
.github/workflows/krc-media-tier0-control.yml
```

Manual operations become:

```text
tier0          # existing read-only host observation
tier1          # existing bounded backend observation
tier2-restart  # new bounded Cobalt restart only
```

`tier0` remains the default. No separate workflow/OIDC identity is introduced.

For `tier2-restart`, the workflow must:

- pass exact repository/ref/node identity gates;
- pass Tier-1 sanitized preflight before mutation;
- invoke only `/usr/local/sbin/krc-tier2-cobalt-restart`;
- validate the helper's fixed output before emission;
- pass Tier-1 post-check;
- pass Tier-0 regression;
- retain arbitrary-root, direct-Docker, owner/root-user and KGM isolation denials.

## Acceptance gates

Phase 8C is not accepted until a live `main` workflow dispatch succeeds with:

```text
P8_C_REPOSITORY_BOUNDARY=PASS
P8_C_NODE_IDENTITY=PASS
P8_C_TIER1_PREFLIGHT=PASS
P8_C_TIER2_RESTART=PASS
P8_C_TIER1_REGRESSION=PASS
P8_C_TIER0_REGRESSION=PASS
P8_C_SECRET_VALUES=NOT_EXPOSED
P8_C_ARBITRARY_ROOT=DENIED
P8_C_TIER2_ARGUMENTS=DENIED
P8_C_DIRECT_DOCKER_ACCESS=DENIED
P8_C_OWNER_USER=DENIED
P8_C_ROOT_USER=DENIED
P8_C_KGM_ISOLATION=PASS
KRC_PHASE_8_P8_C_BOUNDED_RESTART=PASS
KRC_PHASE_8_OPERATION=TIER2_COBALT_RESTART_ONLY
```

Until then, canonical production authority remains the previously accepted
Tier-0/Tier-1 read-only boundary.
