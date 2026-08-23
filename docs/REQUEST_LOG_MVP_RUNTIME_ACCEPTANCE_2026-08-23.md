# Request Log MVP Runtime Acceptance

Date: 2026-08-23
Status: ACCEPTED
Scope: public K-Research & Critic only

## Runtime test

Published NEW-chat request:

```text
Досліди, чи справді регулярні прогулянки покращують якість сну.
```

The public GPT requested consent for the `script.google.com` Action and sent only the generalized topic:

```text
Вплив регулярних прогулянок на якість сну
```

The Action completed and the Google Sheet was independently read after the user continued with the CriticProfile reply `1`.

Observed rows:

| request_number | date | time | user_name | request_topic |
|---:|---|---|---|---|
| 1 | 23.08.2026 | 17:45:37 | none | API operation invocation request |
| 2 | 23.08.2026 | 17:56:59 | none | Вплив регулярних прогулянок на якість сну |

No row 3 existed after standalone workflow reply `1`.

## Acceptance checks

```text
Builder Action schema valid                       PASS
Builder direct Action write                       PASS
Published NEW-chat Action invocation              PASS
One substantive request -> exactly one row        PASS
Standalone `1` -> no extra row                    PASS
Server-generated Kyiv date/time                   PASS
user_name stored as none                          PASS
Generalized topic stored instead of full prompt   PASS
Research/Critic flow continued                    PASS
Owner-visible Google Sheet register               PASS
```

## Accepted markers

```text
REQUEST_LOG_MVP_RUNTIME = ACCEPTED
PUBLIC_CORE_ACTIONS = ENABLED
REQUEST_LOG_WORKFLOW_REPLY_DEDUP = ACCEPTED
```

The request-log Action is optional observability. Failure or denial must remain non-blocking for the Research/Critic workflow.
