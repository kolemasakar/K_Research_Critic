import pytest
from krc_research.local_research_stages import execute_local_stage as run
BASE={"user_profile_approved":True, "source_manifest_sha256":"a"*64}
def test_search_manifest_not_live():
    r=run("source_search",{**BASE,"search_runs":[{"provider":"Crossref","query":"concrete","executed_at":None,"hit_count":None,"exported_records":None}]})
    assert r["mode"]=="OFFLINE_MANIFEST_ONLY" and r["records"][0]["status"]=="PARTIAL_LOG"
def test_source_metadata_not_verified():
    r=run("source_verify",{**BASE,"sources":[{"title":"A","url":"https://example.org/a","access_status":"FULL_TEXT"}]})
    assert r["records"][0]["verification_status"]=="REVIEW_REQUIRED"
def test_critic_fails_closed():
    r=run("critic_review",{**BASE,"claims":[{"claim_id":"C01","required":1,"evidence":[]}]})
    assert r["claims"][0]["verdict"]=="SHORTFALL" and r["publication_gate"]=="NO_GO"
def test_export_is_not_manuscript():
    r=run("research_export",BASE)
    assert r["mode"]=="STATUS_RECEIPT_ONLY" and not r["scientific_approval"]
def test_unknown_operation():
    with pytest.raises(ValueError):run("manuscript_build",BASE)
def test_approval_required():
    with pytest.raises(ValueError):run("source_search",{**BASE,"user_profile_approved":False})
def test_bound_source_count():
    with pytest.raises(ValueError):run("source_verify",{**BASE,"sources":[{}]*101})
