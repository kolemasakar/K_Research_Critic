# KRC MEDIA — R4-C cutover proposal ready; exact audience approval pending

Date: 2026-09-22  
Status: **AUTHORITATIVE CHECKPOINT / R4_B_COMPLETE / PRIVATE_REPLACEMENT_ACCEPTED / R4_C_PROPOSAL_READY / EXACT_AUDIENCE_APPROVAL_PENDING / NON_DESTRUCTIVE_CUTOVER / FREE_ONLY / PUBLICATION_HOLD**

## Starting state

```text
R4_A=COMPLETE
R4_B=COMPLETE
PRIVATE_REPLACEMENT_ACCEPTED=YES
R4_CUTOVER_READY=YES
R4_C_AUTHORIZED=NO
SOURCE_PUBLIC_GPT_UNCHANGED=YES
```

## R4-C governing contract

Checkpoint 167 defines R4-C as a separate final owner decision. Approval 3 must authorize the exact audience/share/publication/user-switch actions presented at that time.

Because the current account exposes no built-in migration control, R4-C remains non-destructive.

## Proposed R4-C sequence

### C0 — freeze rollback anchor

Before any sharing/publication mutation:

```text
existing K-Research & Critic GPT=KEEP PUBLISHED / UNCHANGED
source GPT audience=UNCHANGED
source GPT content=UNCHANGED
PR22=NO MERGE
PR45=NO MERGE
FREE_ONLY=REQUIRED
```

### C1 — set replacement audience

One exact owner-selected audience is required:

```text
OPTION_1=PRIVATE_OWNER_ONLY
OPTION_2=LINK_ONLY_PILOT
OPTION_3=PUBLIC_DISCOVERY / MARKETPLACE_OR_EQUIVALENT_IF_AVAILABLE
```

No audience is assumed by default.

### C2 — share/publish replacement only to approved audience

Perform only the UI/product mutation required for the chosen audience.

No source-GPT mutation is included.

### C3 — access verification

From the intended user context verify:

```text
replacement_visible=PASS
Core Skill available=PASS
registered apps=5
canonical operations visible=13
read operations=9
execution operations=4
confirmation boundary=PASS
FREE_ONLY=PASS
```

No live `*_start` is required for access verification.

### C4 — user switch

Only after C3 passes:

- direct the approved user/audience to the replacement Plugin;
- do not remove, edit, or unpublish the existing GPT;
- retain the source GPT as the rollback anchor.

### C5 — post-switch checkpoint

Record:

```text
R4_CUTOVER=PASS
APPROVED_AUDIENCE=<owner-selected>
SOURCE_PUBLIC_GPT_UNCHANGED=YES
ROLLBACK_ANCHOR=AVAILABLE
PUBLICATION_SCOPE=<exact approved scope>
```

## Explicitly excluded

```text
DELETE_SOURCE_GPT=NO
UNPUBLISH_SOURCE_GPT=NO
EDIT_SOURCE_GPT=NO
BUILTIN_MIGRATE=NO / unavailable
PR22_MERGE=NO
PR45_MERGE=NO
NEW_MEDIA_STARTS=NO
PROVIDER_WORK=NO
PAID_FALLBACK=NO
```

## Rollback

If replacement visibility/access/parity fails:

1. stop directing users to the replacement;
2. reduce replacement visibility to private where supported;
3. keep/restore the existing public GPT as the active user entry point;
4. retain accepted private runtime components for diagnosis;
5. do not merge PR #22/#45 as a rollback mechanism.

## Stop conditions

Immediate STOP if:

- audience/share controls differ materially from this plan;
- rollback anchor would be lost;
- the replacement loses 13-operation parity;
- any execution operation leaks onto the read-only surface;
- confirmation semantics become ambiguous;
- FREE_ONLY cannot be proven;
- an unapproved state-changing control is required.

## Authorization still required

The next mutation requires an explicit audience selection:

```text
1=PRIVATE_OWNER_ONLY
2=LINK_ONLY_PILOT
3=PUBLIC_DISCOVERY
```

Until one is selected:

```text
R4_C_AUTHORIZED=NO
PLUGIN_PUBLICATION=NO
PLUGIN_SHARING_CHANGE=NO
USER_SWITCH=NO
```

Terminal marker:

`KRC_MEDIA_CHECKPOINT_177_R4C_PROPOSAL_READY_EXACT_AUDIENCE_APPROVAL_PENDING_2026_09_22`
