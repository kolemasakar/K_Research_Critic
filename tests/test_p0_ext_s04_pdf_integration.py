import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.scientific_cycle_v3 import run_scientific_cycle
from krc_research.inspection_receipts import InspectionReceipt,audit_receipt

HERE=Path(__file__).resolve().parent
def fixture():
    return json.loads((HERE/"fixtures/kscience_ext_s04_real_article_pilot.json").read_text(encoding="utf-8"))
def manifest():
    return json.loads((HERE/"fixtures/kscience_ext_s04_pdf_snapshot_manifest.json").read_text(encoding="utf-8"))
def test_record_has_actual_pdf_hash_and_page_locators():
    m=manifest()
    assert len(m["pdf_sha256"])==64 and m["pdf_pages"]==15
    assert {x["section"] for x in m["source_inspection"]["verified_text_passages"]}=={"METHODS","RESULTS","LIMITATIONS"}
def test_source_binary_without_independent_review_is_not_accepted():
    m=manifest();p=fixture()
    p["inspection_receipts"]=[dict(source_id=m["source_id"],
        origin_id="DOI:"+m["doi"],doi=m["doi"],
        document_sha256=m["pdf_sha256"],
        inspected_sections=["METHODS","RESULTS","LIMITATIONS"],
        passage_locators=["PDF p3: devices","PDF p12: discussion","PDF p14: data availability"],
        checked_at="2026-10-25T15:00:00+02:00",
        inspector_id="KRC_AUTOMATED_PDF_READER",method="FULL_TEXT",
        evidence_relation="SUPPORTS",external_trace_id="krc-ext-s04-local-inspection",
        trace_verified=False)]
    output=run_scientific_cycle(p)
    assert [x["verdict"] for x in output["baseline"]["research"]["claim_verdicts"]]==["SHORTFALL"]*3
    assert not output["baseline"]["research"]["inspection_audit"][0]["usable"]
    assert output["baseline"]["critic"]["history"][0]["result"]["verdict"]=="REVISE"
    assert output["final_status"]=="NO_GO"
def test_historical_research_is_one_paper_origin():
    m=manifest()
    assert m["source_id"]=="EXT-S04"
    assert not m["independent_reviewer_attested"]
    assert len({m["doi"]})==1
