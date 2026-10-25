# KRC №100 — REF-27 conditional closure and Research Engine readiness audit
Date: 2026-10-25

## 1. REF-27 acceptance boundary
**Conditional source acceptance, NOT scientific validation.**
REF-27 (Lencis/Udris/Korjakins; DOI 10.2478/cons-2013-0011) original institutional PDF SHA-256 `4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c` verified. The 9 printed sample rows and arithmetic of Table I are available; published group aggregates reproducible, but formula for percentage averages is ambiguous. Both figure raster images were extracted from original PDF and registered with SHA and real dimensions. Exact graph↔specimen/aggregate mapping and independent reproduction of the 270m/s first-2h narrative claim remain unverified. UK-1401 ±1% is source-reported maximum measurement error, NOT an experimentally established confidence interval. Raw readings and calibration certificate unavailable. The final approval remains **NO_GO**. Status: **CONDITIONAL_SOURCE_ACCEPTED / FIGURE_NUMERIC_SHORTFALL**, Critic **REVISE**. No fabricated graph observations or independent experiments.

## 2. KRC Research Engine readiness, scoped to K_Science
| Scope | Evidence | Gate |
|---|---|---|
| Original PDF hash, evidence provenance, bibliography DOI | Source/registry audit and isolated source workflows | PASS for bounded scope |
| Crossref/OpenAlex search, screening, checkpoint | P3 real provider tests; partial Crossref pages with count drift; not systematic completeness | PARTIAL |
| Source DOI/full text evidence and numerical tables | REF-27 exact source + arithmetic | PASS for *reported* numbers |
| Figure digitization and scientific plot validation | Affine gate, source raster inventory; no independently verified matching coordinates | SHORTFALL |
| Multi-revision Critic & manuscript change trace | Earlier isolated real revisions and audit | PASS internal / scientific NO_GO |
| Full isolated research suite | Fresh run at krc-cobalt, checkout /tmp/krc-p0-offline-20261025 | **253/253 PASS**, 1.72s, exit 0 |
| K_Science private access | Historical verified signed read-only krc_capabilities and replay rejection | PASS only bounded capability/replay, not research workflow |
| Complete service research_* workflow over route | Listed operations not fully implemented or accepted | NO_GO |
| K_Science physical/mathematical model + experimental validation | Not supplied/accepted by KRC test | NOT EVALUATED |
| Human external scientific review | Deferred to final acceptance per owner-approved combined model | PENDING |
| Public plugin / production / MEDIA | Explicit freeze | HOLD |

## 3. Technical and scientific debts, ordered
P0 (gate before broader private K_Science research):
- Ship minimally scoped service operations for research_start/source_search/source_verify/methodology_review/novelty_review/critic_review/manuscript_build/publication_gate/research_export with signed ACL and fail-closed provenance, without production change.
- End-to-end real, authorized K_Science request→KRC engine→results audit through Sentinel, with replay/timeout/failure tests. Do not use synthetic tests as live acceptance.
- Reconcile isolated checkout and repository branch and pin a reproducible test commit; tests PASS on host but are not proof the current branch/production coincide.
- Enforce source statuses FULL_TEXT/ABSTRACT_ONLY/METADATA_ONLY, primary-source independence counts and publication gate NO_GO for absent evidence.

P1 (scientific completion of REF-27):
- Request verified specimen-series metadata / raw time-series from authors only if needed for figure admission.
- Independently re-annotate tick labels and curve points; quantify actual pixel localization repeatability and combine uncertainty only with justified models.
- Resolve first-two-hour Figure2 reference and source figure mapping; otherwise maintain SHORTFALL.
- At final manuscript acceptance, obtain independent external human reviewer and author signoff.

P2 (research quality and operational hardening):
- Expand bounded database/catalog reproducibility and transparent provider pagination failure accounting.
- Add a K_Science domain-specific method/novelty/strength validation rubric using independent destructive-test references and calibrated measurement uncertainty.
- Review sustainable free-only capacity, security, observability, documentation; keep public/MEDIA/production on HOLD.

## 4. Acceptance decision
- REF-27 internal source/citation intake: ACCEPT **conditional restricted citation** only, not full scientific fact validation.
- KRC Research Engine isolated QA: PASS tested 253 tests.
- K_Science full live scholarly workflow: **NO_GO**.
- Scientific/publication signoff: **NO_GO**.

No manual owner action required at current development stage; future human review or original raw dataset requires additional owner/source involvement. FREE_ONLY, production/MEDIA/public freeze respected.
