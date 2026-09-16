# KRC MEDIA — OCI Control-Plane Read-Only Access
Підтверджений канал читання OCI control plane для інфраструктури KRC MEDIA.

Date: 2026-09-13
Status: ACTIVE / READ-ONLY / VERIFIED

A dedicated OCI instance-principal access path is available to the KRC MEDIA Cobalt host for control-plane observation.

## Purpose

The channel is used only to read live OCI network state needed for recovery, consistency checks, and infrastructure verification.

## Read scope

Permanent authority is read-only. Base virtual-network reads are supplemented by the single additional read permission required to list NSG security rules.

Required recovery reads are verified, including NSG rule-list access.

Earlier wording `OCI_CONTROLPLANE_READ=PASS` was too broad before this additional read was verified. That consistency warning is now closed.

## Mutation boundary

Temporary write permissions used during an owner-authorized network change were removed after verification.

Final negative verification confirmed that OCI network mutation is denied through the instance-principal path.

The existing KRC automation ceiling remains unchanged:

```text
tier0
tier1
tier2_restart
```

RDC remains supplemental development access and does not expand that ceiling.

## Credential handling

No reusable OCI user API credential, application secret, or private key is stored in this repository. Authentication uses OCI instance principals.

## Result

```text
OCI_CONTROLPLANE_BASE_READ=PASS
OCI_NSG_RULES_READ=PASS
OCI_CONTROLPLANE_MUTATION=DENIED
RECOVERY_CONSISTENCY_WARNING=CLOSED
COMBINED_PROJECT_VERIFICATION=PASS
RECOVERY=COMPLETE
```
