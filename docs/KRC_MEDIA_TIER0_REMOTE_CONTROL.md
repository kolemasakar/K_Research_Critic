# KRC MEDIA — Project-Isolated Tier-0 Remote Control

Status: **PHASE 6 AUTHORIZED / REPOSITORY IMPLEMENTATION PREPARED / LIVE TRUST SETUP PENDING**

## Purpose

Phase 6 connects the already accepted local Tier-0 substrate on `krc-cobalt` to an ephemeral GitHub-hosted runner without granting backend mutation, Docker, secret, owner-account, or arbitrary-root authority.

Accepted local substrate from Sentinel Remote Phase 5:

```text
krcops
  -> exact bounded sudo
  -> /usr/local/sbin/krc-tier0-status
  -> sanitized read-only host facts
```

Phase 6 adds only the remote transport/control identity around that existing boundary.

## Canonical workflow

`.github/workflows/krc-media-tier0-control.yml`

The workflow:

- is `workflow_dispatch` only;
- runs only from `refs/heads/main` in `kolemasakar/K_Research_Critic`;
- requests only `contents: read` and `id-token: write` GitHub permissions;
- uses a dedicated KRC workload identity, never the KGM identity;
- requests only `tag:krc-media-github-actions`;
- resolves exactly `krc-media-node1` at `100.118.132.8`;
- connects only as `krcops` for the accepted Tier-0 helper;
- validates a strict allow-list of helper output keys;
- negative-tests arbitrary root, helper arguments, Docker, `ubuntu`, `root`, and KGM TCP/22 access;
- performs no service restart, deploy, package installation, Docker mutation, secret read, firewall change, or backend operation.

## Dedicated GitHub repository secrets required

The KRC repository must receive separate values:

```text
TS_KRC_OAUTH_CLIENT_ID
TS_KRC_AUDIENCE
```

Do not copy or reuse KGM's `TS_OAUTH_CLIENT_ID` / `TS_AUDIENCE` values.

The secret values themselves must never be committed or recorded in documentation.

## Required Tailscale trust boundary

The owner must create a dedicated Tailscale workload-identity/OAuth trust for the KRC repository/workflow and authorize only the source tag:

```text
tag:krc-media-github-actions
```

The trust must be constrained to the exact KRC GitHub repository and, where supported by the Tailscale trust configuration, the exact workflow/ref/event:

```text
repository: kolemasakar/K_Research_Critic
workflow: .github/workflows/krc-media-tier0-control.yml
ref: refs/heads/main
event: workflow_dispatch
```

No KGM repository/workflow claim may be accepted by the KRC trust.

## Required tailnet network/SSH policy outcome

The final global tailnet policy must produce exactly this effective authority for the KRC automation source:

```text
source: tag:krc-media-github-actions
network destination: tag:krc-media-node1
network port: tcp:22 only
Tailscale SSH destination user: krcops only
```

And it must deny:

```text
KGM destination tag: tag:kgm
KGM TCP/22
KRC SSH user ubuntu
KRC SSH user root
any other KRC port
```

Because the tailnet policy is global and already contains accepted owner and KGM rules, Phase 6 must be added as a narrow delta. Do not replace the whole ACL/grants/SSH document with a standalone snippet.

## Repository-side fail-closed behavior

Until both dedicated repository secrets and the exact Tailscale trust exist, manual workflow execution must fail before any KRC SSH command is accepted.

This is intentional. A failed token exchange or missing secret is not a reason to broaden an existing KGM trust credential.

## Acceptance gates

Live Phase-6 acceptance requires one successful manual run from canonical `main` with all of these terminal markers:

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

A single failed negative test means Phase 6 remains unaccepted.

## Explicitly not authorized by Phase 6

- Cobalt restart/reload/deploy;
- `docker exec`, Docker socket, or Docker group access;
- reads of `/opt/krc-cobalt`, `.env*`, `keys.json`, API keys, cookies, login state, provider credentials, or TLS keys;
- owner `ubuntu` automation;
- root SSH automation;
- firewall, OCI NSG, SSH daemon, or Tailscale owner-path changes;
- reverse proxy/public HTTPS work;
- VoiceBridge/Render/Neon/media-provider changes;
- Phase-4B hardening changes;
- Phase 7 or Tier-2 lifecycle mutation.

## Cross-project invariant

```text
K-Trader -> SentinelX only
KGM      -> its accepted KGM OIDC/Tailscale/Ansible identity
KRC      -> dedicated KRC OIDC/Tailscale/Tier-0 identity
```

No project may inherit another project's automation tag or trust credential.
