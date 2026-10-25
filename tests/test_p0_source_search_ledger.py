import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.source_search_ledger import SearchRun, validate_search_run, reconcile_source_record

def test_dated_recorded_search():
    x=validate_search_run(SearchRun("PubMed","silicon graphite", "2026-10-25T12:00:00+02:00",11,11))
    assert x["status"]=="REPRODUCIBLE_LOG"

def test_missing_hit_count_not_fabricated():
    x=validate_search_run(SearchRun("Publisher","Si/C","2026-10-25T12:00:00+02:00",None,None))
    assert x["status"]=="PARTIAL_LOG" and x["hit_count"]=="COUNT_UNAVAILABLE"

def test_unzoned_time_rejected():
    with pytest.raises(ValueError):
        validate_search_run(SearchRun("PubMed","silicon","2026-10-25T12:00:00",1,1))

def test_inconsistent_count_rejected():
    with pytest.raises(ValueError):
        validate_search_run(SearchRun("PubMed","silicon","2026-10-25T12:00:00+02:00",1,4))

def test_doi_metadata_not_full_text_evidence():
    rec=reconcile_source_record({"doi":"https://doi.org/10.1038/s41467-021-22662-7",
        "title":"Article","url":"https://nature.com/","access_status":"METADATA_ONLY"})
    assert rec["verification_status"]=="REVIEW_REQUIRED"
    assert not rec["methods_results_reinspected"]

def test_missing_identity_fails():
    with pytest.raises(ValueError):
        reconcile_source_record({"doi":"10.1038/s41467-021-22662-7","title":"Article"})
