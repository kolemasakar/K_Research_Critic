# Request Log Public Disablement Runtime Acceptance

Date: 2026-08-23
Status: ACCEPTED
Scope: public K-Research & Critic

## Test objective

Verify that after removing the public `logRequest` Action and synchronizing the no-logging Builder Instructions, a new user request proceeds directly to the standard CriticProfile gate without an external `script.google.com` consent screen.

## Runtime test

NEW-chat request:

```text
Досліди, чи справді регулярні прогулянки покращують якість сну.
```

Observed first response:

```text
Профіль збору і критики успішно створено.
1 - виконати аналіз одразу.
2 - переглянути і відредагувати профіль збору і критики.
3 - скасувати дослідження.
```

No `script.google.com` Action consent prompt appeared before the gate.

## Acceptance checks

```text
Public `logRequest` Action removed                 PASS
Public Builder Instructions synchronized          PASS
Public GPT updated                                PASS
NEW-chat smoke test                               PASS
script.google.com consent screen absent           PASS
CriticProfile gate appears directly               PASS
Active public Actions disabled                    PASS
Repository/public Builder synchronization         PASS
Historical request-log prototype retained         PASS
```

## Accepted markers

```text
REQUEST_LOG_PUBLIC = DISABLED
PUBLIC_ACTIONS = DISABLED
REQUEST_LOG_DISABLEMENT_RUNTIME = ACCEPTED
BUILDER_SYNC = ACCEPTED
```

## Boundary

The retained Google Sheet, Apps Script deployment, OpenAPI schema and historical acceptance artifacts remain reference/test resources only. They are not part of the active public Builder configuration.

Do not re-enable the public request-log Action without explicit owner approval of the consent UX or an alternative telemetry architecture.
