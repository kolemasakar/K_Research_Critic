# Public Request Log MVP

Version: 1.1
Status: RUNTIME_ACCEPTED
Updated: 2026-08-23

## Goal

Record a minimal owner-visible register of public K-Research & Critic requests without storing full conversations.

## Accepted implementation

```text
Public K-Research & Critic
  -> GPT Action `logRequest` (best effort, non-blocking)
  -> Google Apps Script Web App
  -> Google Sheet: K-Research & Critic — Request Log
```

Google Sheet ID:

```text
1icDvAkPx43s7568iZkANBCriz8UaanB4kMITO-icLaU
```

Sheet tab: `Звернення`.
Timezone: `Europe/Kyiv`.
Authentication: `None`.

Columns:

```text
Номер звернення
Дата
Час
Ім'я користувача
Коротка узагальнена тема запиту
```

## Privacy/data-minimization contract

- user name is currently always `none`;
- never infer identity from the prompt;
- send only a short generalized topic, maximum 160 characters;
- do not send the full prompt, response, CriticProfile, credentials, hidden reasoning, or unrelated personal details;
- logging failure or user denial must never block the Research/Critic workflow.

## Canonical files

```text
integrations/request_log/google_apps_script/Code.gs
integrations/request_log/openapi.yaml
prompts/GPT_STORE_REQUEST_LOG_ADDENDUM.md
prompts/GPT_STORE_INSTRUCTIONS.md
docs/PRIVACY_POLICY_REQUEST_LOG.md
```

## Runtime behavior

For each NEW substantive research request:

1. create a short generalized topic;
2. call `logRequest` exactly once before the CriticProfile gate;
3. continue the normal Research/Critic workflow regardless of logging success;
4. do not log standalone workflow replies such as `1`, `2`, `3`, approve/edit/cancel responses, or ordinary follow-ups continuing the same request.

## Security decision for MVP

Authentication: `None`.

This is intentionally the simplest MVP. Anyone who learns the Apps Script endpoint URL could submit rows. The table therefore must contain no sensitive data. A later revision may add a proxy/API-key layer if abuse becomes material.

## Runtime acceptance — 2026-08-23

Builder direct Action test:

```text
request_number: 1
request_topic: API operation invocation request
result: PASS
```

Published NEW-chat test:

```text
user request: Досліди, чи справді регулярні прогулянки покращують якість сну.
logged request_number: 2
logged topic: Вплив регулярних прогулянок на якість сну
user_name: none
result: PASS
```

After the CriticProfile gate, the user sent standalone `1`. Direct spreadsheet verification showed no third row. Therefore:

```text
one new substantive request -> one row       PASS
standalone workflow reply -> no new row      PASS
server-side Kyiv date/time                   PASS
user_name=none                               PASS
generalized topic only                       PASS
full prompt absent                           PASS
Core workflow continues after logging        PASS
owner review through Google Sheets           PASS
```

Final marker:

```text
REQUEST_LOG_MVP_RUNTIME = ACCEPTED
```
