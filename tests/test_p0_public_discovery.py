import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.public_discovery import discover_metadata,fetch_public_json
def cross(_):return {"status":"ok","message":{"total-results":13,"items":[{"DOI":"10.1234/test","title":["Test Concrete Study"],"URL":"https://doi.org/10.1234/test"}]}}
def alex(_):return {"meta":{"count":9},"results":[{"id":"https://openalex.org/W123","doi":"https://doi.org/10.1234/test","display_name":"Another concrete study","primary_location":{"landing_page_url":"https://example.org/paper"}}]}
def test_crossref_results_are_metadata_only():
    x=discover_metadata("concrete ultrasonic velocity",provider="Crossref",fetch=cross)
    assert x["status"]=="METADATA_RETRIEVED" and x["results_total"]==13
    assert x["records"][0]["evidence_access"]=="METADATA_ONLY"
    assert not x["scientific_evidence_verified"]
def test_openalex_results():
    x=discover_metadata("concrete ultrasound",provider="OpenAlex",fetch=alex)
    assert x["records"][0]["provider_id"]=="https://openalex.org/W123"
def test_provider_failure_not_empty_success():
    x=discover_metadata("concrete ultrasound",provider="OpenAlex",fetch=lambda _: (_ for _ in ()).throw(TimeoutError()))
    assert x["status"]=="PROVIDER_FAILURE" and x["results_total"] is None
def test_invalid_provider_denied():
    with pytest.raises(ValueError):discover_metadata("concrete ultrasound",provider="Other")
def test_result_cap_denied():
    with pytest.raises(ValueError):discover_metadata("concrete ultrasound",provider="Crossref",limit=100)
def test_malformed_result_denied_as_provider_failure():
    x=discover_metadata("concrete ultrasound",provider="Crossref",fetch=lambda _:{"status":"ok","message":{"items":[]}})
    assert x["status"]=="PROVIDER_FAILURE"
def test_bad_urls_denied():
    with pytest.raises(ValueError):fetch_public_json("https://evil.example/works")
    with pytest.raises(ValueError):fetch_public_json("https://api.openalex.org/users")

from krc_research.public_discovery import reconcile_discovery
def test_two_provider_same_doi_is_one_bibliographic_work_not_two_experiments():
    a=discover_metadata("concrete ultrasound",provider="Crossref",fetch=cross)
    b=discover_metadata("concrete ultrasound",provider="OpenAlex",fetch=alex)
    z=reconcile_discovery([a,b])
    assert z["matching_dois"]==["10.1234/test"]
    assert z["unique_matched_works"]==1
    assert z["independent_experimental_origins_verified"]==0
def test_provider_failure_cannot_be_presented_as_reconciled_success():
    a=discover_metadata("concrete ultrasound",provider="Crossref",fetch=cross)
    b=discover_metadata("concrete ultrasound",provider="OpenAlex",fetch=lambda _: (_ for _ in ()).throw(TimeoutError()))
    assert reconcile_discovery([a,b])["status"]=="PARTIAL"
def test_only_one_catalog_is_rejected():
    with pytest.raises(ValueError):reconcile_discovery([discover_metadata("concrete ultrasound",provider="Crossref",fetch=cross)])
