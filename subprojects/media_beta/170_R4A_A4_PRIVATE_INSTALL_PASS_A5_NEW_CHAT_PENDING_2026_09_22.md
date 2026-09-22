# KRC MEDIA — R4-A private install PASS; A5 new-chat verification pending

Date: 2026-09-22  
Status: **AUTHORITATIVE CHECKPOINT / R4_A_IN_PROGRESS / A0_A1_A2_A3_PASS / A4_PRIVATE_INSTALL_PASS / A5_NEW_CHAT_VERIFICATION_PENDING / FREE_ONLY / PUBLICATION_HOLD**

## Scope

This checkpoint records successful private installation of the assembled R4 Candidate through the Personal / Local marketplace path.

No public publication, sharing, public GPT mutation, PR merge, main mutation, MEDIA `*_start`, provider work, or GitHub Actions execution occurred.

## A4 private installation result

Owner-reported Work validation:

```text
plugin=K-Research & Critic R4 Candidate
marketplace/source=Personal / Local
skills=1
registered_apps=5
FREE_ONLY=preserved
publication=NO
sharing=NO
MEDIA/provider/GitHub operations=NO
validation_errors_final=0
```

The installed candidate references the expected registered app mappings:

```text
R3C = asdk_app_6aaaf8ca113c8191a4ac53f8793833a4
E1  = asdk_app_6ab26b061fb4819180fa096638f1e4df
E2  = asdk_app_6aaeae197c9081918b90e46f5bb09615
E3  = asdk_app_6aaf262767d8819199146dc84b8e1ee8
E4  = asdk_app_6aaf292e653481918c75767dea004c5c
```

## Schema corrections discovered by real Work validation

Initial Work validation found exactly two package schema issues:

```text
1. unsupported field required in each .app.json mapping
2. missing required interface.defaultPrompt
```

Only those minimal schema corrections were applied in Work.

Repository package was reconciled to the accepted validated shape:

```text
.app.json:
  removed required from all five mappings

.codex-plugin/plugin.json:
  added interface.defaultPrompt
```

Repository reconciliation commits:

```text
ee1a0da52b146281d6d70337aef4cd05a854eb95
44bb0bd855de474af7429877a5e509df0f15dba5
```

The canonical Core Skill content and registered app IDs were not changed.

## R4-A state

```text
A0_FREEZE_PREFLIGHT=PASS
A1_E1_RESTART_SAFE_OAUTH_HARDENING=PASS
A1_RESTART_CONTINUITY=PASS
A2_E1_PRIVATE_CONNECTION=PASS
A3_CORE_SKILL_PRIVATE_INSTALL=PASS
A4_PACKAGE_STATIC_VALIDATION=PASS
A4_PRIVATE_INSTALL=PASS

A5_PRIVATE_ASSEMBLY_VERIFICATION=PENDING_NEW_CHAT
A6_STOP_CHECKPOINT=PENDING
```

## New-chat requirement

The installed Plugin becomes available only in a new chat.

A5 must therefore be performed in a fresh chat using the installed:

```text
K-Research & Critic R4 Candidate
```

A5 is non-execution verification only.

Required acceptance:

```text
PLUGIN_VISIBLE=YES
SKILL_COUNT=1
REGISTERED_APP_COUNT=5

Core Skill bound=PASS

MEDIA:
  read operations=9
  execution operations=4
  total operations=13
  read-only execution leakage=0

FREE_ONLY=PASS
SOURCE_PUBLIC_GPT_UNCHANGED=YES
PUBLICATION=NO
SHARING=NO

media_youtube_start=NO
media_instagram_start=NO
media_facebook_start=NO
media_telegram_start=NO
provider_work=NO
```

No R4-B regression is authorized by A5.

## Hard boundary

```text
R4_B_AUTHORIZED=NO
R4_C_AUTHORIZED=NO
PUBLIC_GPT_MUTATION=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
PR22_MERGE=NO
PR45_MERGE=NO
MAIN_MUTATION=NO
GITHUB_ACTIONS_CURRENTLY_AVAILABLE=NO
```

## Next gate

Open a new chat with the installed private `K-Research & Critic R4 Candidate` Plugin and perform A5 visibility/permission/parity verification only.

Terminal marker:

`KRC_MEDIA_CHECKPOINT_170_R4A_A4_PRIVATE_INSTALL_PASS_A5_NEW_CHAT_PENDING_2026_09_22`
