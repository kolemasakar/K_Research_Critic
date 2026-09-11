# KRC MEDIA RDC Background Autostart Acceptance - 2026-09-11
Прийнято тимчасовий режим спрощеного RDC-доступу на період активної розробки.

Status: ACCEPTED FOR DEVELOPMENT / LOW-FRICTION MODE

## Decision

During active development, operator convenience is prioritized over final hardening. RDC keeps its persisted pairing and is started automatically after host reboot.

## Runtime identity

```text
host=krc-cobalt
user=krcops
uid=1002
rdc_version=0.2.50
node=v24.21.0
```

## Host change

Ubuntu cron was installed and enabled because the host did not have cron and the user systemd session was not suitable for unattended startup.

```text
cron=installed
cron_service=active
autostart=crontab @reboot
```

## Persistence model

```text
pairing=persistent
process=background
startup=crontab @reboot
service_account=krcops
root_rdc=not used
```

The crontab entry starts the user-local Node/RDC runtime from `/home/krcops` and writes logs under `/home/krcops/.local/state/desktop-commander/remote.log`.

## Live evidence

The persisted RDC session was reused. The background process was started as `krcops`. The owner SSH session was then closed and the device remained ONLINE and answered a remote ping.

```text
logout_survival=PASS
remote_ping=PASS
device_status=ONLINE
```

A deliberate host reboot was not performed solely for this acceptance. Therefore the `@reboot` path is configured but awaits confirmation at the next natural reboot.

## Authority boundary

This development convenience change does not modify the accepted KRC automation authority ceiling. GitHub OIDC/Tailscale Tier0, Tier1, and Tier2 restart-only controls remain unchanged. RDC runs as `krcops`; no root RDC daemon or direct Docker authority was added.

Final hardening and token lifecycle policy are deferred until active project development is substantially complete.