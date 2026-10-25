# KRC ↔ K_Science / Sentinel-Remote: integration checkpoint 2026-10-25

## Approved order and invariants
Owner approved I1→I7. Full KRC Core/Scholarly Research P0 not yet accepted, so no false overall acceptance. KRC is shared scientific engine; K_Science owns the research, experiments and manuscript; Sentinel-Remote exclusively owns cross-project identity/route/ACL/recovery. FREE_ONLY, private, no publication-dependent design.

## Implemented code
- `src/krc_research/interproject_contract.py`: canonical versioned request envelope, origin/destination, bounded operation, timestamp, SHA256 of payload, HMAC-SHA256 signature check, age and replay validation interface.
- `src/krc_research/science_dispatch.py`: fail-closed isolated dispatcher for `research.evidence.preflight`, `research.bibliography.audit`, `research.inspection.review`. Requires explicit CriticProfile approval on preflight and has no remote listener/implicit host privileges. Operation `research.profile.validate` reserved, NOT_IMPLEMENTED in dispatch.
- `tests/test_p0_interproject_contract.py`, `tests/test_p0_science_dispatch.py`.
- K_Science `integrations/krc_exchange_v1.py`, `tests/test_krc_exchange_v1.py`, docs contract.
- Sentinel-Remote `docs/integrations/KSCIENCE_KRC_RESEARCH_ROUTE_V1_2026-10-25.md`: route and ACL **specification only**, not active implementation.

## Executed acceptance
On krc-cobalt, isolated /tmp fixture, dedicated pytest venv:
- KRC 58/58 PASS, including 7 contract and 4 dispatcher cases.
- K_Science 4/4 PASS.
- Local interop: K_Science make_request -> KRC signed validation with test key + replay check PASS. This is not production signing by K_Sentinel.
- No real scientific dataset, university thesis files or personal secrets transferred.

## Gaps / required next work
I1: KRC Core and Scholarly P0 acceptance still PARTIAL (science evidence, search log, originality/author gate not complete).
I2: Contract+dispatcher offline PASS, **no durable replay database or production identity**. HMAC test key is deterministic fixture, NEVER deploy it.
I3: Adapter offline PASS; **not yet a real client connected through K_Sentinel**.
I4: Sentinel contract registered in docs; no K_Science runtime identity/SSH/private transport or ACL provisioning verified, so **NOT CONNECTED**.
I5: Live K_Science→Sentinel→KRC→K_Science cycle NOT RUN. Synthetic local interop is not a scientific cycle.
I6: Isolated unit checks passed, frozen cross-project corpus and independent repeat acceptance PENDING.
I7: User direction: private ChatGPT plugin integration deferred until KRC completion; private plugin 0.19.14 unchanged.
Next prioritized engineering: discover K_Science runtime identity, implement authenticated transport and persisted replay cache through Sentinel-Remote, then run end-to-end test; do not expose current KRC localhost 19014 without controlled route and auth.
