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
