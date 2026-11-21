"""Crossref and Europe PMC source-only readiness, NO live network."""
from io import BytesIO
from urllib.error import HTTPError
import pytest
from krc_research.stage131_bibliography_adapter import lookup_doi_metadata
from krc_research.stage131_bibliography_http import fetch_json_metadata, ProviderHTTPError

DOI="10.1088/1757-899X/365/3/032058"

def test_disabled_gate_never_calls_injected_provider():
    def forbidden(*args,**kwargs):
        raise AssertionError("NETWORK_MUST_NOT_RUN")
    assert lookup_doi_metadata(DOI,fetch_json=forbidden)["status"]=="PROVIDER_DISABLED"

def test_metadata_two_providers_only_is_not_scientific_approval():
    seen=[]
    def fake(url,timeout):
        seen.append(url)
        assert timeout==5
        if "crossref" in url:
            return {"message":{"DOI":DOI,"title":["test"]}}
        return {"resultList":{"result":[{"doi":DOI,"isOpenAccess":"Y"}]}}
    result=lookup_doi_metadata(DOI,fetch_json=fake,allow_network=True)
    assert len(seen)==2
    assert result["status"]=="TWO_PROVIDER_DOI_MATCH_METADATA_ONLY"
    assert result["full_text_verified"] is False
    assert result["experimental_independence_verified"] is False

def test_metadata_provider_mismatch_never_promotes_clearance():
    def fake(url,timeout):
        if "crossref" in url:
            return {"message":{"DOI":"10.1000/other"}}
        return {"resultList":{"result":[]}}
    result=lookup_doi_metadata(DOI,fetch_json=fake,allow_network=True)
    assert result["status"]=="REVIEW_REQUIRED"

def test_http_refuses_non_allowlisted_urls_before_opener():
    def forbidden(*args,**kwargs):
        raise AssertionError("UNSAFE_URL_FETCH")
    with pytest.raises(ValueError,match="PROVIDER_URL_DENIED"):
        fetch_json_metadata("https://invalid.example/metadata",opener=forbidden)

def test_429_is_provider_error_not_not_found():
    attempts=[]
    def throttled(request,timeout):
        attempts.append(timeout)
        raise HTTPError(request.full_url,429,"rate limited",None,None)
    with pytest.raises(ProviderHTTPError) as exc:
        fetch_json_metadata("https://api.crossref.org/works/10.1000%2Fdemo",opener=throttled,sleeper=lambda _:None,max_attempts=2)
    assert exc.value.status==429 and len(attempts)==2
