import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.reproducible_discovery import audit_discovery_batch
def run(provider,doi="10.1234/test",status="METADATA_RETRIEVED"):
    return {"schema":"KRC-DISCOVERY-1","provider":provider,"query":"concrete velocity",
      "request_url":"https://example.org/"+provider,"executed_at":"2026-10-25T15:00:00+00:00",
      "response_digest":"a"*64,"status":status,"exported_records":1,
      "records":[{"provider_id":provider+"-1","doi":doi,"title":"Paper","evidence_access":"METADATA_ONLY"}]}
def test_same_doi_two_catalogs_one_record():
    x=audit_discovery_batch([run("Crossref"),run("OpenAlex","https://doi.org/10.1234/test")],
      {"10.1234/test":{"decision":"INCLUDE","reason":"Relevant testing setup"}})
    assert x["unique_doi_records"]==1
    assert x["records"][0]["providers"]==["Crossref","OpenAlex"]
    assert x["independent_experimental_origins_verified"]==0
def test_unscreened_stays_unresolved():
    x=audit_discovery_batch([run("Crossref"),run("OpenAlex")],{})
    assert x["status"]=="PARTIAL" and x["records"][0]["decision"]=="UNRESOLVED"
def test_provider_failure_is_not_successful_zero():
    r=run("OpenAlex",status="PROVIDER_FAILURE");r["error_type"]="TimeoutError"
    x=audit_discovery_batch([run("Crossref"),r],{})
    assert len(x["provider_failures"])==1 and x["status"]=="PARTIAL"
def test_invalid_decision_rejected():
    with pytest.raises(ValueError):audit_discovery_batch([run("Crossref"),run("OpenAlex")],{"10.1234/test":{"decision":"PASS","reason":"invalid"}})
def test_false_screening_record_rejected():
    with pytest.raises(ValueError):audit_discovery_batch([run("Crossref"),run("OpenAlex")],{"10.1234/other":{"decision":"INCLUDE","reason":"made up"}})
def test_duplicate_provider_run_rejected():
    with pytest.raises(ValueError):audit_discovery_batch([run("Crossref"),run("Crossref")],{},require_both=False)
def test_export_count_mismatch_rejected():
    r=run("Crossref");r["exported_records"]=2
    with pytest.raises(ValueError):audit_discovery_batch([r,run("OpenAlex")],{})
def test_deterministic_manifest():
    args=[run("Crossref"),run("OpenAlex")]
    assert audit_discovery_batch(args,{})["manifest_sha256"]==audit_discovery_batch(args,{})["manifest_sha256"]
