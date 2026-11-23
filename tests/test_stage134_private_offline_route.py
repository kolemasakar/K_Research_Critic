"""Stage134 private signed, one-shot offline-only route tests (no live providers)."""
import copy
import hashlib
import json
import os
from urllib.parse import quote

import pytest

from krc_research.stage131_project_research_route import ProjectResearchRoute, RouteDenied
from krc_research.stage131_n39_single_owner_chat_consent import canonical
from krc_research.stage131_science_semantic_contract import validate_operation_result
from krc_research.stage134_bibliography_provenance import Stage134Denied
from krc_research.stage134_offline_bibliography_route import (
    audit_offline_bundles, validate_stage134_offline_payload,
)

DOI = "10.1000/demo"


@pytest.fixture(autouse=True)
def private_umask():
    old = os.umask(0o077)
    try:
        yield
    finally:
        os.umask(old)


def bundle(doi=DOI, *, coverage_gap=True):
    cross = {"message": {"DOI": doi, "title": ["Concrete test"],
                         "published": {"date-parts": [[2024]]}}}
    pmc = {"resultList": {"result": [] if coverage_gap else [
        {"doi": doi, "title": "Concrete test", "pubYear": "2024"}]}}
    captures = []
    for provider, payload in (("crossref", cross), ("europe_pmc", pmc)):
        url = ("https://api.crossref.org/works/" + quote(doi, safe="")
               if provider == "crossref" else
               "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="
               + quote("DOI:" + doi, safe="") + "&format=json&pageSize=1")
        captures.append({
            "provider": provider, "url": url,
            "captured_at": "2026-11-23T12:00:00Z",
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
        })
    return {
        "version": "KRC-STAGE134-BIBLIOGRAPHY-PROVENANCE/1",
        "policy": "FREE_ONLY_OFFLINE", "doi": doi,
        "captures": captures,
        "sources": [{"source_id": "S1", "origin_id": "O1",
                     "document_sha256": "0" * 64,
                     "access": "METADATA_ONLY", "derived_from": []}],
    }


def profile(payload=None):
    return {"purpose": "Synthetic Stage134 private offline inspection; no providers",
            "operation": "research.bibliography.audit",
            "policy": "FREE_ONLY_OFFLINE",
            "payload": payload if payload is not None else {
                "offline_bundles": [bundle()]}}


def test_default_project_route_does_not_enable_stage134(tmp_path):
    r = ProjectResearchRoute(tmp_path / "state")
    with pytest.raises(RouteDenied, match="OFFLINE_OPERATION_NOT_ENABLED"):
        r.propose(profile())


def test_explicit_opt_in_requires_approved_immutable_hash(tmp_path, monkeypatch):
    def no_network(*_args, **_kwargs):
        raise AssertionError("PROVIDER_NETWORK_FORBIDDEN")
    import urllib.request
    import krc_research.public_metadata_adapters as old_provider
    monkeypatch.setattr(urllib.request, "urlopen", no_network)
    monkeypatch.setattr(old_provider, "urlopen", no_network)
    r = ProjectResearchRoute(tmp_path / "state", enable_stage134_offline=True)
    p = r.propose(profile())
    rid, digest = p["request_id"], p["profile_sha256"]
    assert p["status"] == "PROPOSED"
    with pytest.raises(RouteDenied, match="APPROVAL_REQUIRED"):
        r.run(rid, digest)
    with pytest.raises(RouteDenied, match="PROFILE_MISMATCH"):
        r.decide(rid, "a" * 64, "APPROVE")
    assert r.decide(rid, digest, "APPROVE")["status"] == "APPROVED"
    with pytest.raises(RouteDenied, match="OFFLINE_OPERATION_NOT_ENABLED"):
        ProjectResearchRoute(r.root).run(rid, digest)
    out = r.run(rid, digest)
    received = r.read(rid)
    assert received["descriptor"] == out
    assert hashlib.sha256(canonical(received["result"])).hexdigest() == out["artifact"]["sha256"]
    result = received["result"]
    assert result["status"] == "PENDING"
    assert result["scientific_approval"] is False
    assert validate_operation_result(
        result, task_id=rid + "-task",
        operation="research.bibliography.audit") == (
            "SEMANTIC_SHAPE_VALID_ONLY_NOT_SCIENTIFIC_APPROVAL")
    engine = result["engine_result"]
    assert engine["schema"] == "KRC-BIB-PROV-1"
    assert engine["count"] == 1 and engine["network_requests"] == 0
    assert engine["records"][0]["metadata_status"] == "COVERAGE_GAP_METADATA_ONLY"
    assert engine["records"][0]["scientific_independence"]["verified_origin_count"] == 0
    with pytest.raises(RouteDenied, match="APPROVAL_REQUIRED"):
        r.run(rid, digest)


def test_legacy_dois_only_never_allowed_even_in_opted_in_route(tmp_path):
    r = ProjectResearchRoute(tmp_path / "state", enable_stage134_offline=True)
    with pytest.raises((RouteDenied, Stage134Denied)):
        r.propose(profile({"dois": [DOI]}))


@pytest.mark.parametrize("mutation", [
    lambda b: b["captures"][0]["payload"]["message"].update(DOI="10.1000/other"),
    lambda b: b["captures"][0].update(payload_sha256="a" * 64),
    lambda b: b.update(policy="FREE_ONLY_METADATA"),
    lambda b: b["captures"][1].update(url="https://example.org/query"),
    lambda b: b["sources"][0].update(document_sha256="not-a-sha"),
])
def test_invalid_approved_bundle_cannot_be_proposed(tmp_path, mutation):
    r = ProjectResearchRoute(tmp_path / "state", enable_stage134_offline=True)
    b = bundle()
    mutation(b)
    with pytest.raises((RouteDenied, Stage134Denied)):
        r.propose(profile({"offline_bundles": [b]}))


def test_deny_ambiguous_and_duplicate_bundles(tmp_path):
    r = ProjectResearchRoute(tmp_path / "state", enable_stage134_offline=True)
    for payload in (
        {"offline_bundles": []},
        {"offline_bundles": [bundle()] * 2},
        {"offline_bundles": [bundle()] * 5},
        {"dois": [DOI], "offline_bundles": [bundle()]},
        {"offline_bundles": [bundle()], "allow_network": True},
    ):
        with pytest.raises((RouteDenied, Stage134Denied)):
            r.propose(profile(payload))


def test_two_provider_metadata_match_does_not_verify_research():
    result = audit_offline_bundles([bundle(coverage_gap=False)])
    assert result["records"][0]["metadata_status"] == (
        "TWO_PROVIDER_FIELDS_MATCH_METADATA_ONLY")
    assert result["independent_experimental_origins_verified"] == 0
    assert result["full_texts_inspected"] == 0
    assert result["retraction_clearance"] == "NOT_ESTABLISHED"


def test_profile_is_immutable_before_broker_dispatch(tmp_path):
    r = ProjectResearchRoute(tmp_path / "state", enable_stage134_offline=True)
    p = r.propose(profile())
    d = p["profile_sha256"]
    assert r.decide(p["request_id"], d, "APPROVE")["status"] == "APPROVED"
    with r.consent._db() as db:
        db.execute("UPDATE project_profiles SET profile_json=? WHERE request_id=?",
                   (json.dumps(profile({"offline_bundles": [bundle(coverage_gap=False)]})),
                    p["request_id"]))
    with pytest.raises(RouteDenied, match="PROFILE_MISMATCH"):
        r.run(p["request_id"], d)


def test_approved_bundle_has_zero_provider_network_scope():
    x = {"offline_bundles": [bundle()]}
    digest = validate_stage134_offline_payload(x)
    assert digest == hashlib.sha256(canonical(x)).hexdigest()
    result = audit_offline_bundles(x["offline_bundles"])
    assert result["network_requests"] == 0
    assert result["records"][0]["decision"] == "HUMAN_EVIDENCE_REVIEW_REQUIRED"
