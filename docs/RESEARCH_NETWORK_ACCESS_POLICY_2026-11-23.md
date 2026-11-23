# Owner policy: public internet research is a core KRC capability

Effective: 2026-11-23
Priority: owner architectural directive
Status: PUBLIC_RESEARCH_NETWORK_ALLOWED_BY_DEFAULT
Scope: K-Research & Critic core research, discovery, DOI/bibliography,
source comparison, primary-source retrieval and fact-checking.

## Mandatory default

The KRC research system MUST be able to search, browse, retrieve and verify
public internet information as a regular built-in capability. Do not impose
a general ban, blanket offline-only policy, or separate owner consent for
each normal public source, DOI, search query, Crossref/OpenAlex/Europe PMC
lookup, or independent fact-check.

Ordinary public research should proceed when the owner requests a study,
review, literature search, citation check or scientific fact-check.
The owner's instruction to conduct that research already authorizes
the normal public read-only information-gathering steps for the task.

The former Stage134 eight-GET profile was a one-time engineering acceptance
fixture, NOT a standing quota or global KRC browsing prohibition.
Its consumption does not disable subsequent ordinary public research.

Provider coverage is extensible. Crossref, OpenAlex, Europe PMC, academic
publisher pages and other lawful publicly reachable sources may be used
when supported by an appropriate safe provider/browser adapter.
A source not being indexed by one catalog is not evidence of invalidity.
The system must report real source or network limitations transparently.

## Separation from execution and publication

Public read-only research is NOT the same operation as:
- An immutable, owner-approved inter-project KRC/K_Science signed task.
- Granting a client the ability to issue arbitrary network requests via KRC.
- Mutating KRC records, changing service configuration, publication, sending
  user content or unpublished manuscripts to external providers.
- Automatic paid API usage, account-based access or bypass of paywalls.

Existing Stage127/132/133 signed transport, identity, consent, durable replay,
artifact integrity, project policy and production release gates remain
independently enforceable. They must never be misrepresented as a general
prohibition on the KRC research engine's own public internet access.

The Stage134 offline snapshot engine remains a useful reproducible mode and
is never a substitute for the internet-capable primary research workflow.
The signed external bibliography.audit operation is a separately reviewed
API surface and does not have to be exposed before public research can work.

## Security, provenance and economics

- Read-only public research uses FREE_ONLY resources and no paid fallback,
  subscriptions, additional credentialed provider access or unapproved cost.
- Preserve HTTPS/TLS verification, redirect/SSRF protections, timeouts,
  bounded response sizes, rate-limit handling and sensible request pacing.
  These are transport safeguards, not permission to disable research.
- Honor robots/access rules, copyright and source licensing.
  Do not publish copyrighted full texts or private provider responses to
  public GitHub without appropriate authorization and rights.
- Preserve DOI, retrieval time, provider, exact public URL, content hash or
  stable reference and any corrections/retractions/coverage gaps.
- Distinguish provider-reported metadata from authenticated full-text source
  custody, independently inspected methods and verified scientific truth.
- No unsanctioned personal or manuscript uploads to third-party AI services.
- Owner local-computer disks remain prohibited without a separate, direct
  owner instruction under docs/OWNER_STORAGE_POLICY_2026-11-23.md.
- Future product improvements must not silently convert this open public
  research default back into opt-in, provider_approved=True, NO_SEND or
  blanket OFFLINE-only.

## Implementation status (not deployment claim)

Source branch research/stage134-bibliography-hardening-20261121 changes
the Stage131 public metadata adapter and composition gate to allow normal
FREE_ONLY DOI lookup by default. Explicit allow_network=False is reserved
for unit tests and deliberate offline/reproducibility calls, not a global
research prohibition.

The installed KRC private signed operation gateway is unchanged until a
separately verified deployment. Do not claim a production rollout from
source-only implementation and tests.
