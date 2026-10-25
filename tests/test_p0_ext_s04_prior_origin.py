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
    assert x["overlap"]["REF27_vs_REF26"]=="OFFICIAL_RTU_REF27_PDF_AND_PUBLISHER_INDEXED_REF26_TABLE1_SHOW_EXACT_SAME_NINE_SAMPLE_IDS"
    assert x["prior"][1]["experiment_origin"]=="REUSED_ELEVATED_TEMPERATURE_2013_COHORT_9_OF_27_SUSPECTED"
    assert x["overlap"]["REF27_confidence"]=="EXACT_NINE_ID_COHORT_MATCH_REF26_PUBLISHER_INDEXED_TABLE_AND_REF27_OFFICIAL_PDF"

def test_ref27_reports_nine_reused_samples_not_new_independent_cohort():
    x=data()
    assert x["prior"][1]["sample_count_reported_transcription"]==9
    assert x["prior"][1]["prior_study_reuse_reported_transcription"]
    assert x["overlap"]["REF27_independent_experiment_count_policy"].startswith("DO_NOT_DOUBLE_COUNT")
    assert x["prior"][1]["direct_document_digest"]=="4bca8f7614ea2cf4681524edb39220dc52fd871203c225a19957e060e623289c"

def test_official_rtu_ref27_is_hash_anchored_but_not_peer_attested():
    x=data()
    p=x["prior"][1]
    assert p["access"]=="FULL_TEXT_ORIGINAL_RTU_PDF_SHA256_AND_PAGE_VERIFIED"
    assert p["pdf_page_count"]==8
    assert p["inspection"]["status"]=="TEXT_MATCH_WITH_METHODS_RESULTS"
    assert p["inspection"]["found"]==3
    assert p["inspection"]["independent_reviewer_signed"] is False

def test_ref26_ref27_same_nine_identified_specimens():
    x=data()
    ids=x["overlap"]["REF27_overlap_sample_ids"]
    assert len(ids)==9 and len(set(ids))==9
    assert ids==["N-1.28","N-2.28","N-7.28","K-9.28","K-11.28","K-12.28","KV-19.28","KV-21.28","KV-24.28"]
    assert x["overlap"]["REF26_primary_pdf_original_sha256"] is None
    assert x["overlap"]["REF27_independent_experiment_count_policy"].startswith("SAME_NINE_SPECIMENS_AS_REF26")
