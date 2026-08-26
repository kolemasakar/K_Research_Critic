# Request Log Public Disablement Decision
Рішення про вимкнення публічного журналу запитів у K-Research & Critic.

Date: 2026-08-23
Status: ACCEPTED / RUNTIME VERIFIED
Scope: public K-Research & Critic

## Decision

Disable the automatic Request Log Action in the public Custom GPT.

## Reason

The request-log implementation worked technically, but ChatGPT displays an external Action consent prompt before sharing the generalized request topic with `script.google.com`.

For a non-essential owner analytics function, this consent interruption materially degrades the first-request UX. The GPT owner cannot pre-authorize this consent for every public user.

## Product target

```text
Public request -> CriticProfile gate -> Research -> Critic -> report
```

No automatic request-log Action occurs before the CriticProfile gate.

## Retained prototype

Do not delete the tested implementation:

```text
integrations/request_log/google_apps_script/Code.gs
integrations/request_log/openapi.yaml
prompts/GPT_STORE_REQUEST_LOG_ADDENDUM.md
docs/PRIVACY_POLICY_REQUEST_LOG.md
docs/REQUEST_LOG_MVP.md
docs/REQUEST_LOG_MVP_RUNTIME_ACCEPTANCE_2026-08-23.md
Google Sheet: K-Research & Critic - Request Log
Apps Script deployment
```

Historical runtime acceptance remains valid as evidence that the prototype worked.

## Active Builder state

```text
Actions: disabled
REQUEST LOGGING instruction block: absent
privacy-policy URL required by active package: no
```

## Runtime completion

Completed on 2026-08-23:

```text
remove `logRequest` Action from public Builder       PASS
synchronize Builder Instructions with repository     PASS
save/update public GPT                               PASS
NEW-chat substantive request                         PASS
script.google.com consent screen absent              PASS
CriticProfile gate appears directly                  PASS
repository/public Builder synchronization            PASS
```

The observed first response in the post-disable NEW chat was the standard CriticProfile gate. No external Action consent screen appeared before that gate.

## Markers

```text
REQUEST_LOG_PROTOTYPE = IMPLEMENTED_TESTED_RETAINED
REQUEST_LOG_PUBLIC = DISABLED
DISABLE_REASON = USER_CONSENT_UX
PUBLIC_ACTIONS = DISABLED
BUILDER_SYNC = ACCEPTED
REQUEST_LOG_DISABLEMENT_RUNTIME = ACCEPTED
```

## Reactivation rule

Do not re-enable request logging in the public GPT unless the owner explicitly approves the resulting consent UX or a different telemetry architecture avoids that interruption.
