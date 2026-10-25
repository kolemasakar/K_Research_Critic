import pytest
from krc_research.workflow_readiness import inspect_workflow, STAGES
BASE = {"user_profile_approved": True, "source_manifest_sha256": "a" * 64, "verified_primary_sources": 1}
def test_all_nine_accounted():
    r=inspect_workflow(BASE)
    assert len(r["stages"]) == 9 and set(r["stages"]) == set(STAGES)
def test_fail_closed_publication():
    r=inspect_workflow(BASE)
    assert r["publication_gate"] == "NO_GO" and not r["scientific_approval"] and not r["service_dispatch_ready"]
def test_unapproved_profile_fails():
    with pytest.raises(ValueError): inspect_workflow({**BASE, "user_profile_approved": False})
def test_spoofed_scientific_approval_fails():
    with pytest.raises(ValueError): inspect_workflow({**BASE, "scientific_approval": True})
def test_bad_manifest_fails():
    with pytest.raises(ValueError): inspect_workflow({**BASE, "source_manifest_sha256": "not-a-hash"})
def test_negative_count_fails():
    with pytest.raises(ValueError): inspect_workflow({**BASE, "verified_primary_sources": -1})
def test_digest_changes():
    assert inspect_workflow(BASE)["input_sha256"] != inspect_workflow({**BASE,"verified_primary_sources":2})["input_sha256"]
