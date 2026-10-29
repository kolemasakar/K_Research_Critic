import pytest
from krc_research.stage131_bibliography_adapter import lookup_doi_metadata

DOI="10.1088/1757-899X/365/3/032058"

def test_disabled_default_never_fetches():
    def forbidden(*args): raise AssertionError("called network")
    assert lookup_doi_metadata(DOI,fetch_json=forbidden)["status"]=="PROVIDER_DISABLED"

def test_both_doi_matches_metadata_only():
    def fake(url,timeout):
        assert timeout==5
        if "crossref" in url:return {"message":{"DOI":DOI,"title":["test"]}}
        return {"resultList":{"result":[{"doi":DOI,"isOpenAccess":"Y"}]}}
    d=lookup_doi_metadata(DOI,fetch_json=fake,allow_network=True)
    assert d["status"]=="TWO_PROVIDER_DOI_MATCH_METADATA_ONLY"
    assert not d["full_text_verified"] and not d["experimental_independence_verified"]

def test_503_not_conflated_with_not_found():
    def fail(url,timeout):
        if "crossref" in url:raise OSError("503")
        return {"resultList":{"result":[{"doi":DOI}]}}
    d=lookup_doi_metadata(DOI,fetch_json=fail,allow_network=True)
    assert d["status"]=="REVIEW_REQUIRED"
    assert d["sources"]["crossref"]["status"]=="PROVIDER_UNAVAILABLE"

def test_wrong_doi_fails_closed():
    def wrong(url,timeout):
        if "crossref" in url:return {"message":{"DOI":"10.1000/other"}}
        return {"resultList":{"result":[{"doi":"10.1000/other"}]}}
    assert lookup_doi_metadata(DOI,fetch_json=wrong,allow_network=True)["status"]=="REVIEW_REQUIRED"

def test_bad_input_and_timeout():
    with pytest.raises(ValueError):lookup_doi_metadata("invalid")
    with pytest.raises(ValueError):lookup_doi_metadata(DOI,fetch_json=lambda *_:{},allow_network=True,timeout_seconds=0)
