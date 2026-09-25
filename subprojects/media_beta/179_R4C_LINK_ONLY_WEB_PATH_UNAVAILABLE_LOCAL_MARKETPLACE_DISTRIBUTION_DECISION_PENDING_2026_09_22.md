# KRC MEDIA — R4-C link-only web path unavailable; local marketplace distribution decision pending

Date: 2026-09-22  
Status: **AUTHORITATIVE CHECKPOINT / R4_C_LINK_ONLY_PILOT_AUTHORIZED / WEB_LINK_ONLY_PATH_UNAVAILABLE_ON_CURRENT_PERSONAL_SURFACE / ZERO_MUTATION / DISTRIBUTION_DECISION_PENDING / SOURCE_GPT_UNCHANGED / FREE_ONLY**

## UI evidence

Manual UI inspection on the personal ChatGPT Plus account showed:

1. Plugins -> Personal -> Created by me lists the individual MCP apps (R3C/E1-E4 surfaces).
2. Search for `K-Research & Critic R4 Candidate` returns no result.
3. The top-right `+` opens the `New plugin` MCP connection form:
   - icon
   - name
   - description
   - server URL / tunnel
   - authentication / OAuth
   - MCP risk acknowledgement

This form creates a new standalone MCP plugin. It is not management UI for the existing local marketplace package.

No state change was made.

## Product-distribution interpretation

The R4 Candidate was installed from a Personal/Local marketplace package using:

```text
.agents/plugins/marketplace.json
plugins/krc_r4_candidate/
```

Current OpenAI plugin documentation distinguishes local marketplaces from the universal public directory. Local marketplace plugins are loaded by compatible local clients (including Codex/ChatGPT desktop paths) and can be distributed through repository/personal marketplaces.

Plugin sharing by link is documented for managed workspaces, where available sharing options can include workspace members with the link.

The current personal Plus web surface does not expose a link-only share control for this local marketplace package.

Therefore the previously proposed C2 web mutation:

```text
set Personal/Local Candidate -> anyone with link
```

is not available on the current account/surface.

## R4-C state

```text
R4_C_AUDIENCE_INTENT=LINK_ONLY_PILOT
R4_C_AUTHORIZED=YES / LINK_ONLY_PILOT_INTENT
C0_ROLLBACK_ANCHOR_FREEZE=PASS
C1_AUDIENCE_SELECTION=PASS
C2_WEB_LINK_ONLY_SHARE_MUTATION=UNAVAILABLE_ON_CURRENT_SURFACE
C3_ACCESS_VERIFICATION=PENDING
C4_USER_SWITCH=PENDING

PLUGIN_AUDIENCE_CHANGE=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
PUBLIC_DISCOVERY=NO
SOURCE_PUBLIC_GPT_MUTATION=NO
PR22_MERGE=NO
PR45_MERGE=NO
MEDIA_STARTS=0
PROVIDER_WORK=0
```

## Safe alternatives

The intended bounded pilot can proceed only by selecting a supported distribution mechanism:

```text
A=LOCAL_MARKETPLACE_PILOT
  distribute the existing local marketplace package to a specific pilot tester through a compatible local client / repository marketplace
  no public discovery
  no source GPT mutation

B=MANAGED_WORKSPACE_LINK_PILOT
  use a managed ChatGPT workspace where plugin sharing is enabled
  share with workspace members via link
  requires workspace/admin capability

C=PUBLIC_DIRECTORY
  publish through the universal/public plugin directory
  not equivalent to link-only pilot and requires separate explicit authorization
```

Because the reviewed link-only web control is absent, the stop condition applies: do not substitute another state-changing distribution mechanism without explicit owner approval.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_179_R4C_WEB_LINK_ONLY_UNAVAILABLE_DISTRIBUTION_DECISION_PENDING_2026_09_22`
