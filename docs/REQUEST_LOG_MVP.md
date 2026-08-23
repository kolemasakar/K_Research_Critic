# Public Request Log MVP

Version: 1.3
Status: DISABLED_DUE_TO_USER_CONSENT_UX / RUNTIME ACCEPTED / PROTOTYPE RETAINED
Updated: 2026-08-23

## Decision

The Request Log MVP was implemented and runtime-tested successfully, but it is disabled in the public K-Research & Critic UX.

Reason:

```text
ChatGPT external Action consent is shown to users before `script.google.com` receives the generalized topic.
The builder cannot pre-authorize that consent for every public user.
The consent interruption is too costly for a non-essential analytics feature.
```

Current public workflow:

```text
User request
  -> CriticProfile gate
  -> Research
  -> Critic
  -> Final report
```

with no automatic request-log Action.

## Historical prototype

The tested prototype is retained in the repository for reference and possible future reuse outside the public Custom GPT consent path:

```text
GPT Action `logRequest`
  -> Google Apps Script Web App
  -> Google Sheet: K-Research & Critic — Request Log
```

Google Sheet ID:

```text
1icDvAkPx43s7568iZkANBCriz8UaanB4kMITO-icLaU
```

Sheet tab: `Звернення`.
Timezone: `Europe/Kyiv`.
Authentication used by prototype: `None`.

Stored fields were:

```text
Номер звернення
Дата
Час
Ім'я користувача
Коротка узагальнена тема запиту
```

## Privacy/data-minimization contract

The prototype intentionally used minimal data:

- `user_name=none`;
- identity was never inferred from the prompt;
- only a generalized topic up to 160 characters was sent;
- full prompt, response, CriticProfile, credentials and hidden reasoning were not intentionally stored;
- logging failure or denial never blocked Research/Critic.

## Canonical prototype files

```text
integrations/request_log/google_apps_script/Code.gs
integrations/request_log/openapi.yaml
prompts/GPT_STORE_REQUEST_LOG_ADDENDUM.md
docs/PRIVACY_POLICY_REQUEST_LOG.md
docs/REQUEST_LOG_MVP_RUNTIME_ACCEPTANCE_2026-08-23.md
docs/REQUEST_LOG_DISABLEMENT_DECISION_2026-08-23.md
```

These files are retained as historical/tested implementation artifacts. They are not part of the active public Builder configuration while request logging is disabled.

## Historical runtime acceptance — 2026-08-23

The prototype itself passed:

```text
Builder direct Action test                 PASS
Published NEW-chat request write           PASS
one substantive request -> one row         PASS
standalone `1` -> no additional row        PASS
server-side Kyiv timestamp                 PASS
user_name=none                             PASS
generalized topic only                     PASS
Core workflow continued after logging      PASS
```

Historical marker:

```text
REQUEST_LOG_MVP_RUNTIME = ACCEPTED
```

## Public disablement runtime acceptance — 2026-08-23

After the owner removed the Action and synchronized the no-logging Builder Instructions, a NEW-chat request produced the standard CriticProfile gate directly.

Verified:

```text
script.google.com consent screen            ABSENT
CriticProfile gate appears directly         PASS
public Actions                              DISABLED
repository/public Builder sync              COMPLETE
```

Current product marker:

```text
REQUEST_LOG_PUBLIC = DISABLED_DUE_TO_USER_CONSENT_UX
REQUEST_LOG_DISABLEMENT_RUNTIME = ACCEPTED
```

## Reactivation rule

Do not re-enable this Action in the public GPT unless the owner explicitly approves the resulting consent UX or a different telemetry architecture avoids that interruption.
