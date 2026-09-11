# KRC MEDIA — Project-Isolated Remote Control

Безпечний проектно-ізольований канал віддаленого керування KRC MEDIA через GitHub OIDC, Tailscale, Tailscale SSH та окрему системну ідентичність `krcops`.

Status: **PHASE 8C COMPLETE / LIVE ACCEPTANCE PASS / RESTART-ONLY CEILING**

Latest acceptance record:

`docs/KRC_MEDIA_TIER2_RESTART_ONLY_ACCEPTANCE_2026-09-11.md`

Historical Phase-6 Tier-0 acceptance record remains:

`docs/KRC_MEDIA_TIER0_REMOTE_CONTROL_ACCEPTANCE_2026-09-10.md`

## Current purpose

The KRC MEDIA control plane provides three bounded operations over one dedicated project identity:

```text
tier0          sanitized read-only host observation
tier1          sanitized read-only Cobalt backend observation
tier2_restart  restart-only exact accepted running Cobalt backend
```

No general root, Docker, deploy, configuration, secret, or cross-project authority is granted.

## Canonical workflow

`.github/workflows/krc-media-tier0-control.yml`

The workflow:

- is `workflow_dispatch` only;
- fails closed unless executed from `refs/heads/main` in `kolemasakar/K_Research_Critic`;
- uses the dedicated KRC OIDC workload identity;
- requests `tag:krc-media-github-actions` only;
- resolves exactly `krc-media-node1` at `100.118.132.8`;
- connects through Tailscale SSH as `krcops` only;
- validates strict sanitized output schemas;
- negative-tests arbitrary root, helper arguments, direct Docker, `ubuntu`, `root`, and KGM TCP/22 access;
- keeps project identity and authority separate from KGM and K-Trader.

## Dedicated GitHub repository secrets

```text
TS_KRC_OAUTH_CLIENT_ID
TS_KRC_AUDIENCE
```

Secret values must never be committed or documented. KGM trust credentials are not reused.

## Accepted Tailscale boundary

```text
source: tag:krc-media-github-actions
network destination: tag:krc-media-node1
network port: tcp:22 only
Tailscale SSH destination user: krcops only
```

Explicitly denied:

```text
KGM TCP/22
KRC SSH user ubuntu
KRC SSH user root
other KRC ports outside accepted policy
```

Owner access remains a separate recovery/admin path.

## Tier-0 — host observation

Helper:

```text
/usr/local/sbin/krc-tier0-status
```

Original canonical Phase-6 run:

```text
run_id=34435755146
repository_sha=094f5b7297e1534a8654cbd471f511e7db50d42b
conclusion=success
```

Accepted Phase-6 terminal markers included repository and node identity PASS, sanitized Tier-0 observation PASS, arbitrary root denied, helper argument injection denied, Docker denied, owner/root automation denied, and KGM TCP/22 isolation PASS.

## Tier-1 — backend observation

Helper:

```text
/usr/local/sbin/krc-tier1-media-status
root:root 0755
```

Sudoers:

```text
/etc/sudoers.d/91-krcops-tier1-media
root:root 0440
```

Canonical Phase-8B live acceptance:

```text
run_id=34601081712
job_id=103268260112
repository_sha=f14fc70bce5c907906a2c4365b83bbbdfa3c8c57
conclusion=success
```

Tier-1 exposes only bounded sanitized backend state and does not expose environment values, secrets, key contents, logs, compose contents, or arbitrary Docker output.

## Tier-2 — restart-only

Helper:

```text
/usr/local/sbin/krc-tier2-media-restart
root:root 0755
```

Sudoers:

```text
/etc/sudoers.d/92-krcops-tier2-media-restart
root:root 0440
exact no-argument helper authorization
```

The helper fails closed unless exactly one running backend matches the accepted identity:

```text
image=ghcr.io/imputnet/cobalt@sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62
binding=127.0.0.1:9000 only
runtime user=node
ReadOnlyRootfs=true
Privileged=false
```

A stopped backend is not started. Identity mismatch or ambiguity fails before mutation.

The sole authorized mutation is restart of the resolved accepted running container. Identity and running state are revalidated afterwards.

Canonical Phase-8C repository acceptance:

```text
PR #19: squash merged
main SHA=1a61509ca925166d3a59c40d90fc671bd3027e55
exact-main CI run=34617085456
conclusion=success
```

Canonical Phase-8C live acceptance:

```text
run_id=34618591919
job_id=103326586885
operation=tier2_restart
repository_sha=1a61509ca925166d3a59c40d90fc671bd3027e55
conclusion=success
```

Accepted restart output:

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

Final Phase-8C gates:

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

## Current authority ceiling

The accepted automation authority is exactly:

```text
tier0
tier1
tier2_restart
```

The following remain **not authorized**:

- start;
- stop;
- reload;
- deploy;
- image pull/update;
- container creation or replacement;
- `docker exec`;
- direct Docker/socket authority for `krcops`;
- Compose operations;
- application/configuration mutation;
- secret/env/key/log reads;
- firewall or OCI NSG changes;
- reverse proxy/public HTTPS changes;
- MEDIA provider/model changes;
- arbitrary sudo/root;
- automation as `ubuntu` or `root`;
- KGM access.

Any expansion above restart-only requires a new explicit owner authorization gate and a new acceptance phase.

## Cross-project invariant

```text
K-Trader -> SentinelX
KGM      -> independent KGM OIDC/Tailscale/Ansible identity
KRC      -> dedicated KRC OIDC/Tailscale/krcops bounded-helper identity
```

No project inherits another project's automation tag or trust credential.
