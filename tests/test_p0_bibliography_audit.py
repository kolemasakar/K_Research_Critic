import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.bibliography_audit import audit_bibliography
DOI="10.1038/nmat2725"
def cross(url):
    return {"status":"ok","message":{"DOI":DOI,"title":["Test"]}}
def europe(url):
    return {"resultList":{"result":[{"doi":DOI,"title":"Test"}]}}
def updates(url):
    return {"status":"ok","message":{"items":[{"DOI":"10.1038/nmat2749","title":["Erratum"]}]}}

def test_metadata_never_turns_into_fulltext():
    x=audit_bibliography([DOI],crossref_fetch=cross,europepmc_fetch=europe,updates_fetch=updates)
    assert x["count"]==1 and x["two_provider_metadata_matches"]==1
    assert x["records"][0]["experimental_origins_verified"]==0
    assert not x["records"][0]["methods_results_verified"]

def test_erratum_is_not_cleared_retraction():
    x=audit_bibliography([DOI],crossref_fetch=cross,europepmc_fetch=europe,updates_fetch=updates)
    assert x["updates_detected"]==1 and x["retraction_clearance"]=="NOT_ESTABLISHED"

def test_duplicate_doi_rejected():
    with pytest.raises(ValueError):
        audit_bibliography([DOI,"https://doi.org/"+DOI])

def test_invalid_count_rejected():
    with pytest.raises(ValueError):
        audit_bibliography([])

def test_provider_failure_kept_as_error():
    def failing(url):
        raise TimeoutError("fail")
    x=audit_bibliography([DOI],crossref_fetch=failing,europepmc_fetch=europe,updates_fetch=updates)
    assert x["two_provider_metadata_matches"]==0
    assert x["records"][0]["providers"]["crossref"]["status"]=="ERROR"
