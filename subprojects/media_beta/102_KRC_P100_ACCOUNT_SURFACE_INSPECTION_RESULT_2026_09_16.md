# KRC — P100 Account Surface Inspection Result — 2026-09-16

Status: **P100_INSPECTION_ACCEPTED / REMOTE_CUSTOM_MCP_CANDIDATE / EXECUTION_UNVERIFIED / NO_LIVE_BINDING**

## Sentinel evidence

Read-only inspection through ChatGPT Work Cloud Browser completed against the owner's account.

Observed account surface:

```text
SENTINEL_P100_INSPECTION=RUN
KRC_GPT_IDENTITY=PASS
MIGRATION_CONTROL_PRESENT=NO
MIGRATION_CONTROL_VISIBLE_TEXT=NONE_IN_INSPECTED_SURFACES
PLUGIN_SURFACE_PRESENT=YES
CONNECTED_APP_OPTION=YES
CUSTOM_MCP_OPTION=YES
REMOTE_MCP_SUPPORTED=YES
REMOTE_MCP_CONNECTION_TESTED=NO
AUTH_OPTIONS=OAuth|No_authentication|Mixed
ACTION_CONFIRMATION_MODEL=GLOBAL_READ_ALLOWED_WRITES_ASK_WITH_PLUGIN_OVERRIDES
WEB_AVAILABILITY=YES
INSTALL_PERMISSION=YES_UI_CONTROL
SHARE_PERMISSION=UNKNOWN
PUBLISH_PERMISSION=UNKNOWN
MIGRATION_EXECUTED=NO
PLUGIN_INSTALLED=NO
APP_CONNECTED=NO
MCP_UPLOADED=NO
CREDENTIAL_MUTATION=NO
PUBLIC_GPT_MUTATION=NO
REPOSITORY_MUTATION=NO
RENDER_MUTATION=NO
```

The inspected custom-MCP form offered server URL and tunnel paths. The UI description indicated connectors may be capable of changing/deleting data, but no KRC MCP server was connected and no execution/write tool was scanned or invoked.

## OpenAI documentation cross-check

Current OpenAI Help Center documentation states that full MCP support including modify/write actions is rolling out in beta for ChatGPT Business, Enterprise and Edu. It also states that custom remote MCP servers can be configured in developer mode, OAuth can be used where supported, and write actions are subject to permissions/confirmation controls.

Therefore the account UI observation is useful but is not sufficient evidence that this specific account can execute KRC write/action tools. The project must fail closed until a real KRC-compatible MCP tool scan/canary proves the capability.

## Surface classification

Previous:

```text
SURFACE_CLASSIFICATION=SURFACE_AMBIGUOUS
```

Refined:

```text
SURFACE_CLASSIFICATION=REMOTE_CUSTOM_MCP_CANDIDATE
REMOTE_MCP_UI=PASS
REMOTE_MCP_TRANSPORT_VISIBLE=PASS
AUTH_SURFACE_VISIBLE=PASS
EXECUTION_WRITE_UI_DESCRIPTION=PASS
EXECUTION_WRITE_ACTUAL=UNVERIFIED
SHARE_PERMISSION=UNKNOWN
PUBLISH_PERMISSION=UNKNOWN
```

This is sufficient to select remote custom MCP as the preferred implementation candidate for KRC MEDIA, but not sufficient to authorize live connection or activation.

## Authentication consequence for KRC

The current VoiceBridge MEDIA API uses server-side bearer authentication. The inspected custom-MCP form did not expose a direct static Bearer/API-key option; visible choices were OAuth, no authentication and mixed.

Therefore ChatGPT must not connect directly to VoiceBridge by exposing its bearer secret.

Target boundary:

```text
ChatGPT Plugin/App
  -> authenticated remote MCP adapter
  -> server-side VoiceBridge bearer injection
  -> existing VoiceBridge MEDIA API
```

The VoiceBridge bearer remains server-side and must never appear in skill text, repository files, model-visible tool parameters, user-visible output, or Sentinel evidence.

OAuth is the preferred secure candidate for the ChatGPT-to-MCP edge if the account/tool surface and chosen deployment support it. `No authentication` is not accepted for a public remote production endpoint. `Mixed` remains TBD until its exact behavior is verified from the live supported surface/docs.

## Next executable phase — bounded canary

Prepare a repository-only MCP adapter implementation candidate with a **read-only canary tool** first. Do not deploy it yet.

Required first canary semantics:

```text
tool=krc_media_capabilities_canary
mutation=false
provider_work=false
voicebridge_secret_exposure=false
write=false
```

Purpose:
- prove MCP server packaging and tool discovery;
- prove the account can connect to the chosen remote MCP transport;
- prove auth handshake without exposing VoiceBridge bearer;
- determine whether actual execution/write tools are permitted before implementing the four start operations.

Only after the canary is accepted may the project stage the 13-operation MCP mapping and a separately authorized live deployment/connection test.

## Hard boundaries

```text
LIVE_MCP_DEPLOYMENT=DENIED
LIVE_MCP_CONNECTION=DENIED
VOICEBRIDGE_SECRET_EXPOSURE=DENIED
RENDER_CHANGE=DENIED
PUBLIC_GPT_CHANGE=DENIED
PLUGIN_INSTALLATION=DENIED
PLUGIN_PUBLICATION=DENIED
MIGRATION_EXECUTION=DENIED
MAIN_MUTATION=DENIED
PR22_MERGE=DENIED
PR45_MERGE=DENIED
```
