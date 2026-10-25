import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.public_metadata_adapters import crossref_doi,europepmc_doi,reconcile_doi

DOI="10.1038/s41467-021-22662-7"

def test_crossref_normalized_metadata():
    p=lambda u:{"status":"ok","message":{"DOI":DOI.upper(),"title":["Example"],"type":"journal-article"}}
    r=crossref_doi(DOI,fetch=p)
    assert r["status"]=="METADATA_ONLY" and r["retraction_status"]=="NOT_CLEARED"

def test_mismatching_doi_rejected():
    p=lambda u:{"status":"ok","message":{"DOI":"10.1111/fake","title":["Bad"]}}
    with pytest.raises(ValueError):crossref_doi(DOI,fetch=p)

def test_europepmc_only_exact_doi():
    p=lambda u:{"resultList":{"result":[{"doi":"10.9999/wrong","title":"Wrong"},
                                       {"doi":DOI,"title":"Actual","pmcid":"PMC123"}]}}
    r=europepmc_doi(DOI,fetch=p)
    assert r["title"]=="Actual" and r["status"]=="METADATA_ONLY"

def test_missing_europepmc_result_not_false_positive():
    r=europepmc_doi(DOI,fetch=lambda u:{"resultList":{"result":[]}})
    assert r["status"]=="NOT_FOUND"

def test_one_provider_error_does_not_forge_two_checks():
    good=lambda u:{"status":"ok","message":{"DOI":DOI,"title":["Example"]}}
    bad=lambda u:(_ for _ in ()).throw(TimeoutError("offline"))
    r=reconcile_doi(DOI,crossref_fetch=good,europepmc_fetch=bad)
    assert r["metadata_status"]=="PARTIAL"
    assert not r["methods_results_verified"] and r["independent_experiment_origins_verified"]==0
