# GPT_STORE_PACKAGE
Документ визначає production-пакет K-Research & Critic, перевірки релізу та maintenance-gates для GPT Store.

Version: 2.3
Status: MAINTENANCE / CURRENT PUBLIC CORE SYNCED / ACTIONS DISABLED
Updated: 2026-08-26

## 1. Purpose

This document is the operator-facing packaging specification for the published K-Research & Critic Custom GPT.

Repository:

```text
kolemasakar/K_Research_Critic
```

Current public Core invariants:

```text
no developer API key
no mandatory external backend
no active Actions
no Apps
no pinned model
user-plan model policy
built-in ChatGPT capabilities for the core path
Ukrainian user-facing language by default
```

The previously accepted request-log Action is disabled because the platform-controlled external Action consent screen interrupts the normal public UX.

## 2. Active Package Files

```text
gpt_store/manifest.yaml
prompts/GPT_STORE_INSTRUCTIONS.md
gpt_store/checkpoint.py
gpt_store/checkpoint_example.json
scripts/validate_store_package.py
docs/GPT_STORE_PACKAGE.md
```

Retained historical request-log prototype resources:

```text
integrations/request_log/openapi.yaml
integrations/request_log/google_apps_script/Code.gs
prompts/GPT_STORE_REQUEST_LOG_ADDENDUM.md
docs/PRIVACY_POLICY_REQUEST_LOG.md
docs/REQUEST_LOG_MVP.md
docs/REQUEST_LOG_MVP_RUNTIME_ACCEPTANCE_2026-08-23.md
docs/REQUEST_LOG_DISABLEMENT_DECISION_2026-08-23.md
```

These retained resources are not part of the active public Builder configuration.

## 3. Current Builder Configuration

### Name

```text
K-Research & Critic
```

### Default language

```text
uk-UA
```

### Capabilities

Enable:

```text
Web search
Code Interpreter & Data Analysis
```

Disable:

```text
Image generation
Apps
Actions
```

No external backend or privacy-policy URL is required by the active public package.

## 4. Current Public Workflow

```text
new substantive request
 -> CriticProfile created internally
 -> first gate: direct run / profile review-edit / cancel
 -> explicit profile approval
 -> Research
 -> Critic
 -> REVISE when required
 -> final report
 -> review protocol
```

The request-log call is not part of the public workflow.

## 5. Risk and Claim-Level Cross-Check Contract

Risk floors:

```text
LOW >= 0
MEDIUM >= 1
HIGH >= 2
CRITICAL >= 3
```

For every material factual claim the runtime maintains:

```text
required
achieved_independent
exception = NONE | SHORTFALL
```

Independence is based on underlying evidence origins, not URL count. Duplicate/derivative reporting does not increase `achieved_independent`. A systematic review/meta-analysis counts as one evidence origin unless specific underlying studies were independently inspected and cited.

## 6. Traceability and Critic Contract

Every evidence origin counted in `achieved_independent` must be visible and traceable to the relevant material claim. A PASS count cannot exceed the number of visibly traceable independent evidence origins.

Critic checks claim-level ledgers, source authority, independence, freshness, support, contradictions, missing topics, evidence/conclusion consistency and traceability. Maximum revision loop: three iterations. Unresolved issues finish as `COMPLETED_WITH_LIMITATIONS`.

## 7. User-Visible Language Contract

Ukrainian is the default user-facing language unless the user explicitly requests another language.

Canonical localized headings, table columns and CriticProfile labels are defined in the active Store instructions and regression tests. Exact non-ASCII user-facing labels are intentionally not duplicated in this ASCII-constrained repository document.

## 8. Historical Request Log Result

The Request Log MVP was implemented and runtime-accepted on 2026-08-23. The implementation itself worked correctly, including one substantive request -> one row and workflow-reply de-duplication.

It is disabled for product UX reasons, not because of technical failure.

Current markers:

```text
historical request-log runtime acceptance: PRESERVED
public request-log: DISABLED
prototype resources: RETAINED
request-log disablement runtime: ACCEPTED
```

## 9. Disablement Runtime Acceptance

On 2026-08-23 the owner removed the public `logRequest` Action, synchronized the no-logging Builder Instructions, saved/updated the GPT, and opened a NEW chat.

Observed:

```text
script.google.com consent screen            ABSENT
CriticProfile gate appears directly         PASS
Actions                                     DISABLED
repository/public Builder synchronization   COMPLETE
```

## 10. Static Validation

```text
python -m scripts.validate_store_package
python -m pytest
```

## 11. Current Synchronization State

```text
actions: false
REQUEST LOGGING removed from Builder instructions
privacy-policy URL not required by active package
repository_matches_current_public_builder: true
request_log_disablement_runtime_accepted: true
```

## 12. Maintenance Boundary

Any later Builder change is a product update and must be revalidated before being treated as the public baseline.

Do not re-enable the public request-log Action without explicit owner approval of the resulting consent UX or an alternative telemetry architecture.
