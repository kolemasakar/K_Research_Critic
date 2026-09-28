# KRC MEDIA — R4-C local marketplace pilot authorized; bundle ready; app-access gate pending

Date: 2026-09-22  
Status: **AUTHORITATIVE CHECKPOINT / R4_C_LOCAL_MARKETPLACE_PILOT_AUTHORIZED / PILOT_BUNDLE_READY / TESTER_APP_ACCESS_GATE_PENDING / ZERO_PUBLICATION / SOURCE_GPT_UNCHANGED / FREE_ONLY**

## Authorization

Owner selected supported distribution mechanism:

```text
R4_C_DISTRIBUTION=LOCAL_MARKETPLACE_PILOT
R4_C_AUTHORIZED=YES / LOCAL_PILOT_ONLY
PUBLIC_DISCOVERY=NO
MANAGED_WORKSPACE_LINK=NO
```

## Pilot package

Prepared bounded local marketplace bundle:

```text
bundle=KRC_R4_LOCAL_PILOT_2026-09-22.zip
zip_sha256=e6cf16718183b3403179798b3e0ef7d5e5dfa703c1b160d6bfc16a56afea9868
marketplace=krc-r4-local
plugin=k-research-critic-r4-candidate
version=0.1.0
skills=1
registered_apps=5
canonical_operations=13
read_operations=9
execution_operations=4
```

The bundle contains:

```text
.agents/plugins/marketplace.json
plugins/krc_r4_candidate/plugin.json
plugins/krc_r4_candidate/.app.json
plugins/krc_r4_candidate/.codex-plugin/plugin.json
plugins/krc_r4_candidate/skills/krc-core/SKILL.md
PILOT_INSTALL.md
PILOT_MANIFEST.json
SHA256SUMS.txt
```

No plugin architecture or app mapping was changed.

## Distribution/install path

Official plugin tooling supports local marketplace roots with:

```text
codex plugin marketplace add <local-marketplace-root>
codex plugin marketplace list
codex plugin marketplace remove krc-r4-local
```

The extracted bundle root contains the required `.agents/plugins/marketplace.json`.

## Critical tester gate — existing app availability

The Candidate references five existing ChatGPT app IDs through `.app.json`.

Marketplace/plugin installation does not create those apps and does not grant access to them.

Therefore pilot acceptance must begin with:

```text
APP_1_R3C_AVAILABLE=?
APP_2_E1_YOUTUBE_AVAILABLE=?
APP_3_E2_INSTAGRAM_AVAILABLE=?
APP_4_E3_FACEBOOK_AVAILABLE=?
APP_5_E4_TELEGRAM_AVAILABLE=?

REQUIRED_FOR_FULL_PILOT=5/5 AVAILABLE
```

If any referenced app is unavailable to the pilot account:

- STOP;
- do not create substitute MCP apps;
- do not alter the app IDs;
- do not publish publicly;
- record the inaccessible app(s).

## Pilot acceptance order

```text
P0 install local marketplace
P1 install Candidate
P2 Core Skill visible/bound
P3 referenced apps availability 5/5
P4 13-operation visibility scan
P5 nine read-only MEDIA regression
P6 optional later execution only under separate explicit owner consent
```

No `*_start` is authorized by this local-pilot installation gate.

## Preserved boundaries

```text
SOURCE_PUBLIC_GPT_UNCHANGED=YES
PUBLIC_DIRECTORY=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
PR22_MERGE=NO
PR45_MERGE=NO
MEDIA_STARTS=0
PROVIDER_WORK=0
FREE_ONLY=YES
```

## Next gate

Provide the bundle to one pilot tester using ChatGPT Desktop or Codex with local marketplace support.

First return only:

```text
tester_environment=<OS + product/version>
marketplace_visible=PASS|FAIL
plugin_install=PASS|FAIL
core_skill=PASS|FAIL
app_availability=5/5 or blocked list
```

Do not proceed to MEDIA execution.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_180_R4C_LOCAL_MARKETPLACE_PILOT_BUNDLE_READY_APP_ACCESS_GATE_PENDING_2026_09_22`
