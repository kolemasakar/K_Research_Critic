import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.canonical_evidence_ledger import Evidence,assess
ROOT=Path(__file__).resolve().parent
def data():
    return json.loads((ROOT/"fixtures/kscience_ext_s04_2013_origin_review.json").read_text(encoding="utf-8"))
def test_2013_2024_reused_cohort_is_not_independent():
    x=data()
    assert x["central"]["new_data_reported"] is False
    assert x["overlap"]["REF26_vs_2024"]=="HIGH_CONFIDENCE_SAME_REPORTED_27_SPECIMEN_COHORT"
    row=Evidence(source_id="REF26",origin_id="LENCIS_2013_COHORT_27",access="FULL_TEXT",support="SUPPORTED",inspected_methods_results=True,scope_matched=True,provenance_verified=True,primary_url=x["prior"][0]["original_publisher_full_text_search_index"])
    copy=Evidence(**{**row.__dict__,"source_id":"EXT-S04"})
    result=assess("C01",2,[row,copy])
    assert result["achieved_independent"]==1 and result["verdict"]=="SHORTFALL"
def test_unverified_2013_sources_do_not_pass():
    x=data()
    result=assess("C02",1,[Evidence(source_id="REF26",origin_id=x["prior"][0]["experiment_origin"],access="UNKNOWN",support="SUPPORTED",inspected_methods_results=False,scope_matched=True,provenance_verified=False,primary_url=x["prior"][0]["original_publisher_full_text_search_index"])])
    assert result["verdict"]=="SHORTFALL"
def test_ref27_remains_not_independent():
    x=data()
    assert x["overlap"]["REF27_vs_REF26"]=="POSSIBLE_SHARED_COHORT_NOT_PROVEN"
    assert x["prior"][1]["experiment_origin"]=="UNRESOLVED"
