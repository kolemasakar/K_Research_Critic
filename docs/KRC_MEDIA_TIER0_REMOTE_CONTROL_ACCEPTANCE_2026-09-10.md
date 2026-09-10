# KRC MEDIA — Tier-0 Remote Control Acceptance — 2026-09-10
Зафіксовано успішне live-приймання проектно-ізольованого Tier-0/read-only каналу GitHub OIDC → Tailscale → `krcops` для KRC MEDIA.

Status: **PHASE 6 COMPLETE / LIVE ACCEPTANCE PASS**

## Canonical acceptance run

Repository: `kolemasakar/K_Research_Critic`

Workflow: `.github/workflows/krc-media-tier0-control.yml`

Canonical repository SHA exercised by the live run:

`094f5b7297e1534a8654cbd471f511e7db50d42b`

GitHub Actions run:

`34435755146`

Event: `workflow_dispatch`

Branch: `main`

Conclusion: **success**

Run started: `2026-09-10T04:04:38Z`

Run completed: `2026-09-10T04:05:06Z`

## Proven path

```text
kolemasakar/K_Research_Critic
  -> GitHub OIDC
  -> dedicated KRC Tailscale federated identity
  -> ephemeral tag:krc-media-github-actions
  -> TCP/22 only
  -> tag:krc-media-node1
  -> Tailscale SSH
  -> krcops
  -> sudo -n /usr/local/sbin/krc-tier0-status
  -> sanitized Tier-0/read-only output
```

The run resolved exactly:

```text
hostname = krc-cobalt
Tailscale IPv4 = 100.118.132.8
```

The approved helper returned `KRC_TIER0_STATUS_VERSION=1` and sanitized host/service/listener facts only.

## Acceptance markers

All required markers were present in the successful job log:

```text
KRC_PHASE_6_REPOSITORY_BOUNDARY=PASS
KRC_PHASE_6_NODE_IDENTITY=PASS
KRC_PHASE_6_TIER0_OBSERVATION=PASS
KRC_PHASE_6_ARBITRARY_ROOT=DENIED
KRC_PHASE_6_HELPER_ARGUMENT_INJECTION=DENIED
KRC_PHASE_6_DOCKER_ACCESS=DENIED
KRC_PHASE_6_OWNER_USER=DENIED
KRC_PHASE_6_ROOT_USER=DENIED
KRC_PHASE_6_KGM_TCP22_ISOLATION=PASS
KRC_PHASE_6_PROJECT_ISOLATED_OIDC_CONTROL=PASS
KRC_PHASE_6_OPERATION=TIER0_READ_ONLY
```

## Runtime observations from accepted helper

The accepted run observed:

```text
hostname=krc-cobalt
kernel=6.17.0-1020-oracle
architecture=x86_64
cpu_count=2
tailscaled=active
ssh=active
docker=active
rpcbind=active
tailscale_ipv4=100.118.132.8
```

Cobalt remained loopback-only at `127.0.0.1:9000` in the sanitized listener set. No runtime mutation was performed.

## Isolation proof

The live run proved:

- arbitrary root through `krcops`: denied;
- helper argument injection: denied;
- Docker access through `krcops`: denied;
- automation SSH mapping to owner `ubuntu`: denied;
- automation SSH mapping to `root`: denied;
- KRC automation reachability to KGM TCP/22: denied;
- accepted operation remained Tier-0/read-only only.

## Credential and policy boundary

The accepted control path uses a dedicated KRC federated OIDC identity and source tag `tag:krc-media-github-actions`.

The KGM automation identity/tag/credentials are not reused.

The tailnet policy permits the KRC automation source only to `tag:krc-media-node1` on TCP/22, with Tailscale SSH user `krcops` only. Owner access remains a separate `kolemasakar@github -> ubuntu` path.

## Explicit exclusions retained

Phase 6 acceptance does not authorize:

- Cobalt restart/reload/deploy;
- Docker socket/group/exec authority;
- arbitrary root;
- owner `ubuntu` automation;
- secret reads or rotation;
- firewall, SSH daemon, OCI NSG, or owner Tailscale-path mutation;
- reverse proxy/public HTTPS work;
- MEDIA provider/model/runtime mutation;
- Phase-4B hardening changes;
- Tier-2/backend lifecycle operations;
- Phase 7+ capability.

## Terminal gate

```text
KRC_PHASE_6_PROJECT_ISOLATED_OIDC_CONTROL=PASS
KRC_PHASE_6_OPERATION=TIER0_READ_ONLY
KRC_PHASE_6_LIVE_ACCEPTANCE=PASS
PHASE_7_PLUS=NOT_AUTHORIZED
```
