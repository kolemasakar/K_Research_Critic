"""Stage134 default-denied signed POST source boundary; no external issuer or grants.

An isolated synthetic owner decision is for tests only and does not approve
a real Stage127 E2E or authorize a production release.
"""
import copy
import hashlib
import json
import os
import stat
from pathlib import Path
from types import SimpleNamespace

import pytest

from krc_research.stage131_project_research_route import ProjectResearchRoute
from krc_research.stage131_project_signed_read import ProjectArtifactAuthority
from krc_research.stage132_project_post_contract import ProjectPostBoundary
from krc_research.stage132_project_post_wire import (
    BIBLIOGRAPHY, DEFAULT_OPS, IDENTITY, OFFLINE_OPS, OP, checked_ops,
)
from krc_research.stage132_project_post_relay import PilotGatewayBoundary, RelayClient
from krc_research.stage132_project_post_runtime import (
    reviewed_offline_operations,
)
from krc_research.replay_registry import ReplayRegistry
from test_stage134_private_offline_route import profile as sample_profile


@pytest.fixture(autouse=True)
def private_mode():
    previous = os.umask(0o077)
    try:
        yield
    finally:
        os.umask(previous)


@pytest.fixture
def case(tmp_path):
    route = ProjectResearchRoute(tmp_path / "state", enable_stage134_offline=True)
    ReplayRegistry(route.root / "science-replay.sqlite")
    p = sample_profile()
    proposed = route.propose(p)
    envelope = {
        "version": "krc-transport/2",
        "identity": dict(IDENTITY),
        "request_id": proposed["request_id"],
        "operation": BIBLIOGRAPHY,
        "payload": copy.deepcopy(p["payload"]),
    }
    enabled = ProjectPostBoundary(
        route.root, enabled=True,
        enabled_operations=OFFLINE_OPS | {BIBLIOGRAPHY},
        enable_stage134=True,
    )
    return route, proposed, envelope, enabled


def test_stage134_is_default_denied_even_when_stage133_is_enabled(case):
    route, proposal, envelope, _ = case
    for opts in (
        {},
        {"enabled_operations": OFFLINE_OPS},
    ):
        boundary = ProjectPostBoundary(route.root, enabled=True, **opts)
        assert boundary.execute(envelope, trusted_principal="K_Science") == (
            403, {"error": "OPERATION_DENIED"})
    with pytest.raises(ValueError, match="INVALID_OFFLINE_OPERATION_ALLOWLIST"):
        ProjectPostBoundary(
            route.root, enabled=True,
            enabled_operations=OFFLINE_OPS | {BIBLIOGRAPHY})
    assert checked_ops(DEFAULT_OPS) == DEFAULT_OPS
    assert BIBLIOGRAPHY not in checked_ops(OFFLINE_OPS)
    assert BIBLIOGRAPHY in checked_ops(
        OFFLINE_OPS | {BIBLIOGRAPHY}, enable_stage134=True)
    assert route.show(proposal["request_id"])["status"] == "PROPOSED"


def test_exact_approved_stage134_signed_post_and_real_artifact_get(case):
    route, proposal, envelope, boundary = case
    rid, digest = proposal["request_id"], proposal["profile_sha256"]
    assert boundary.execute(envelope, trusted_principal="K_Science")[0] == 403
    assert route.decide(rid, digest, "APPROVE")["status"] == "APPROVED"
    status, out = boundary.execute(envelope, trusted_principal="K_Science")
    assert status == 200 and out["request_id"] == rid
    assert out["version"] == "krc-transport/2"
    assert out["status"] == "completed"
    assert out["delivery"] == "artifact"
    a = out["artifact"]
    scope = {"request_id": rid, "artifact_id": a["artifact_id"],
             "principal": "K_Science"}
    file_handle, desc = ProjectArtifactAuthority(route.root).spool(scope)
    with file_handle:
        raw = file_handle.read()
    assert len(raw) == a["size_bytes"]
    assert hashlib.sha256(raw).hexdigest() == a["sha256"]
    assert desc == {**a, "request_id": rid}
    result = json.loads(raw)
    assert result["operation"] == BIBLIOGRAPHY
    assert result["status"] == "PENDING"
    assert result["scientific_approval"] is False
    engine = result["engine_result"]
    assert engine["schema"] == "KRC-BIB-PROV-1"
    assert engine["network_requests"] == 0
    assert engine["independent_experimental_origins_verified"] == 0
    assert engine["records"][0]["decision"] == "HUMAN_EVIDENCE_REVIEW_REQUIRED"
    assert boundary.execute(envelope, trusted_principal="K_Science")[0] == 409
    assert route.show(rid)["status"] == "COMPLETED"
    route.decide(rid, digest, "CANCEL")
    assert boundary.execute(envelope, trusted_principal="K_Science")[0] == 403


@pytest.mark.parametrize("mutation, expected", [
    (lambda e: e["identity"].update(repository="other/repo"), 403),
    (lambda e: e.update(operation="research.inspection.review"), 403),
    (lambda e: e["payload"]["offline_bundles"][0].update(doi="10.1000/other"), 403),
    (lambda e: e["payload"]["offline_bundles"][0]["captures"][0].update(
        payload_sha256="b" * 64), 403),
    (lambda e: e["payload"].update(dois=["10.1000/demo"]), 403),
    (lambda e: e.update(extra=True), 403),
])
def test_invalid_external_stage134_payload_never_uses_approval(case, mutation, expected):
    route, proposal, envelope, boundary = case
    route.decide(proposal["request_id"], proposal["profile_sha256"], "APPROVE")
    bad = copy.deepcopy(envelope)
    mutation(bad)
    code, _ = boundary.execute(bad, trusted_principal="K_Science")
    assert code == expected
    assert route.show(proposal["request_id"])["status"] == "APPROVED"


def test_same_valid_schema_modified_payload_is_conflict(case):
    route, proposal, envelope, boundary = case
    route.decide(proposal["request_id"], proposal["profile_sha256"], "APPROVE")
    changed = copy.deepcopy(envelope)
    changed["payload"]["offline_bundles"][0]["sources"][0]["origin_id"] = "O2"
    code, result = boundary.execute(changed, trusted_principal="K_Science")
    assert code == 409 and result["error"]["code"] == "IDEMPOTENCY_CONFLICT"
    assert route.show(proposal["request_id"])["status"] == "APPROVED"


def test_wrong_principal_or_unapproved_profile_does_not_dispatch(case):
    route, proposal, envelope, boundary = case
    assert boundary.execute(envelope, trusted_principal="K_Science")[0] == 403
    route.decide(proposal["request_id"], proposal["profile_sha256"], "APPROVE")
    assert boundary.execute(envelope, trusted_principal="OTHER")[0] == 403
    assert ProjectPostBoundary(
        route.root, enabled=False,
        enabled_operations=OFFLINE_OPS | {BIBLIOGRAPHY},
        enable_stage134=True,
    ).execute(envelope, trusted_principal="K_Science")[0] == 403
    assert route.show(proposal["request_id"])["status"] == "APPROVED"


def test_gateway_relays_only_when_explicitly_enabled():
    class Legacy:
        exchange = None
        def execute(self, *_a, **_kw):
            raise AssertionError("UNTRUSTED_LEGACY_FALLBACK")
    class Relay:
        def __init__(self, ops):
            self.enabled_operations = ops
        def execute(self, envelope):
            assert envelope["operation"] == BIBLIOGRAPHY
            return 200, {"valid": "RELAYED_TO_SIGNED_BROKER"}
    envelope = {"operation": BIBLIOGRAPHY}
    denied = PilotGatewayBoundary(Legacy(), Relay(OFFLINE_OPS))
    assert denied.execute(envelope, trusted_principal="K_Science") == {
        "error": "OPERATION_DENIED"}
    allowed = PilotGatewayBoundary(Legacy(), Relay(OFFLINE_OPS | {BIBLIOGRAPHY}))
    assert allowed.execute(envelope, trusted_principal="K_Science") == {
        "valid": "RELAYED_TO_SIGNED_BROKER"}


def test_stage134_root_owned_marker_is_an_independent_runtime_gate(monkeypatch, tmp_path):
    import krc_research.stage132_project_post_runtime as runtime
    assert reviewed_offline_operations(False) == DEFAULT_OPS
    with pytest.raises(ValueError, match="STAGE134_REQUIRES_STAGE133"):
        reviewed_offline_operations(False, stage134_requested=True)
    s133 = tmp_path / "stage133-marker"
    s134 = tmp_path / "stage134-marker"
    s133.write_text("synthetic", encoding="ascii")
    s134.write_text("synthetic", encoding="ascii")
    s133.chmod(0o600)
    s134.chmod(0o600)
    monkeypatch.setattr(runtime, "STAGE133_MARKER", s133)
    monkeypatch.setattr(runtime, "STAGE134_MARKER", s134)
    with pytest.raises(ValueError, match="STAGE133_MARKER_CUSTODY"):
        reviewed_offline_operations(True)
    prior_lstat = Path.lstat
    def fake_owner(path, *args, **kwargs):
        actual = prior_lstat(path, *args, **kwargs)
        if path == s133 or path == s134:
            return SimpleNamespace(st_mode=stat.S_IFREG | 0o600,
                                   st_uid=0, st_nlink=1)
        return actual
    monkeypatch.setattr(Path, "lstat", fake_owner)
    assert reviewed_offline_operations(True) == OFFLINE_OPS
    assert reviewed_offline_operations(True, stage134_requested=True) == (
        OFFLINE_OPS | {BIBLIOGRAPHY})
    s134.unlink()
    with pytest.raises(FileNotFoundError):
        reviewed_offline_operations(True, stage134_requested=True)
