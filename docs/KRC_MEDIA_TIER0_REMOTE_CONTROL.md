# KRC MEDIA — Project-Isolated Tier-0 Remote Control
Безпечний проектно-ізольований канал віддаленого Tier-0/read-only керування KRC MEDIA через GitHub OIDC, Tailscale та окрему системну ідентичність `krcops`.

Status: **PHASE 6 COMPLETE / LIVE ACCEPTANCE PASS**

Canonical live acceptance record: `docs/KRC_MEDIA_TIER0_REMOTE_CONTROL_ACCEPTANCE_2026-09-10.md`.

Canonical acceptance run: `34435755146` on repository SHA `094f5b7297e1534a8654cbd471f511e7db50d42b`.

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
- fails closed unless executed from `refs/heads/main` in `kolemasakar/K_Research_Critic`;
- requests only `id-token: write`; no repository contents permission or checkout is used;
- uses a dedicated KRC workload identity, never the KGM identity;
- requests only `tag:krc-media-github-actions`;
- resolves exactly `krc-media-node1` at `100.118.132.8`;
- connects only as `krcops` for the accepted Tier-0 helper;
- validates a strict allow-list of helper output keys;
- negative-tests arbitrary root, helper arguments, Docker, `ubuntu`, `root`, and KGM TCP/22 access;
- performs no service restart, deploy, package installation, Docker mutation, secret read, firewall change, or backend operation.

## Dedicated GitHub repository secrets

The KRC repository uses separate values:

```text
TS_KRC_OAUTH_CLIENT_ID
TS_KRC_AUDIENCE
```

These belong to the dedicated KRC federated identity. KGM's `TS_OAUTH_CLIENT_ID` / `TS_AUDIENCE` values are not reused.

The secret values themselves must never be committed or recorded in documentation.

## Accepted Tailscale trust boundary

The dedicated KRC workload-identity/federated trust authorizes only the source tag:

```text
tag:krc-media-github-actions
```

The trust is constrained to the KRC GitHub workload, including the canonical main-branch workflow identity and manual dispatch event.

No KGM repository/workflow identity is accepted by the KRC trust.

## Accepted tailnet network/SSH policy outcome

The effective authority for the KRC automation source is:

```text
source: tag:krc-media-github-actions
network destination: tag:krc-media-node1
network port: tcp:22 only
Tailscale SSH destination user: krcops only
```

The accepted negative boundaries deny:

```text
KGM destination tag: tag:kgm
KGM TCP/22
KRC SSH user ubuntu
KRC SSH user root
any other KRC port
```

Owner access remains a separate `kolemasakar@github -> tag:krc-media-node1 -> ubuntu` path.

## Repository-side fail-closed behavior

The workflow fails closed on repository/ref mismatch or missing dedicated KRC OIDC inputs. A failed token exchange is not a reason to broaden or reuse the KGM trust credential.

## Live acceptance

Canonical successful manual run:

```text
run_id=34435755146
event=workflow_dispatch
branch=main
repository_sha=094f5b7297e1534a8654cbd471f511e7db50d42b
conclusion=success
```

All required terminal markers were observed:

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

## Current terminal state

```text
KRC_PHASE_6_LIVE_ACCEPTANCE=PASS
KRC_PHASE_6_PROJECT_ISOLATED_OIDC_CONTROL=PASS
KRC_PHASE_6_OPERATION=TIER0_READ_ONLY
PHASE_7_PLUS=NOT_AUTHORIZED
```
