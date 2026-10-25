import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.scholar_screening import screen_studies
def record():
    return {"source_id":"EXT-S04","doi":"10.3390/buildings14030720",
       "title":"Methodology for Determining the Correct Ultrasonic Pulse Velocity in Concrete",
       "origin_id":"DOI:10.3390/buildings14030720","access":"FULL_TEXT",
       "decision":"INCLUDE","reason":"methods/UPV correction"}
LOG={"provider":"KScience owner registry","query":"ultrasound concrete correction",
     "executed_at":"2026-10-25T13:00:00+02:00","results_total":1}
def test_one_study_with_provenance():
    r=screen_studies([record()],search_log=LOG)
    assert r["screening_counts"]["INCLUDE"]==1 and not r["source_content_independently_verified"]
def test_deterministic_digest():
    assert screen_studies([record()],search_log=LOG)["screening_sha256"]==screen_studies([record()],search_log=LOG)["screening_sha256"]
def test_duplicate_ids_denied():
    with pytest.raises(ValueError):screen_studies([record(),record()],search_log={**LOG,"results_total":2})
def test_no_search_timestamp_denied():
    with pytest.raises(ValueError):screen_studies([record()],search_log={**LOG,"executed_at":"2026-10-25T13:00:00"})
def test_undercounted_search_denied():
    with pytest.raises(ValueError):screen_studies([record()],search_log={**LOG,"results_total":0})
def test_missing_reason_denied():
    x=record();x["reason"]=""
    with pytest.raises(ValueError):screen_studies([x],search_log=LOG)
def test_unresolved_remains_unverified():
    x=record();x["decision"]="UNRESOLVED";x["access"]="METADATA_ONLY"
    assert not screen_studies([x],search_log=LOG)["records"][0]["eligible_as_verified_scientific_evidence"]
