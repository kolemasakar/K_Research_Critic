# Public Request Log MVP

Version: 1.0
Status: IMPLEMENTED_PACKAGE_PENDING_APPS_SCRIPT_DEPLOYMENT_AND_BUILDER_WIRING
Updated: 2026-08-23

## Goal

Record a minimal owner-visible register of public K-Research & Critic requests without storing full conversations.

## Selected implementation

```text
Public K-Research & Critic
  -> GPT Action (best effort, non-blocking)
  -> Google Apps Script Web App
  -> Google Sheet: K-Research & Critic — Request Log
```

Google Sheet ID:

```text
1icDvAkPx43s7568iZkANBCriz8UaanB4kMITO-icLaU
```

Sheet tab: `Звернення`.
Timezone: `Europe/Kyiv`.

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
- logging failure must never block the Research/Critic workflow.

## Files

```text
integrations/request_log/google_apps_script/Code.gs
integrations/request_log/openapi.yaml
docs/PRIVACY_POLICY_REQUEST_LOG.md
```

## Manual deployment steps

1. Open the target Google Sheet.
2. Extensions -> Apps Script.
3. Replace the default script with `integrations/request_log/google_apps_script/Code.gs`.
4. Deploy -> New deployment -> Web app.
5. Execute as: yourself.
6. Access: Anyone.
7. Copy the deployment URL / deployment ID.
8. Replace `REPLACE_WITH_DEPLOYMENT_ID` in `integrations/request_log/openapi.yaml` with the real deployment ID.
9. In the public GPT Builder add an Action and import the resulting OpenAPI schema.
10. Authentication: None.
11. Set Privacy Policy URL to the public GitHub page for `docs/PRIVACY_POLICY_REQUEST_LOG.md`.
12. Add/synchronize the Builder instruction block that performs one best-effort `logRequest` call per new research request.
13. Run a fresh-chat smoke test and verify that exactly one row is appended.

## Logging behavior

For each new research request, create a short generalized topic such as:

```text
cold shower and immunity
RTK GNSS construction control
smartphone comparison
```

Call `logRequest` once. Do not log numeric profile-gate responses (`1`, `2`, `3`) as new requests. Do not retry repeatedly if the Action fails. Continue the normal workflow.

## Security decision for MVP

Authentication: `None`.

This is intentionally the simplest MVP. Anyone who learns the Apps Script endpoint URL could submit rows. The table therefore must contain no sensitive data. A later revision may add a proxy/API-key layer if abuse becomes material.

## Acceptance criteria

- one new user research request -> one table row;
- number is sequential under normal concurrency;
- date/time are generated server-side in Kyiv timezone;
- user name is `none`;
- topic is generalized and <=160 characters;
- full prompt is absent;
- request logging failure does not block CriticProfile/Research/Critic;
- owner can review/filter/export directly in Google Sheets.
