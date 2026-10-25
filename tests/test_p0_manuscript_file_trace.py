import copy,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.manuscript_file_trace import audit_manuscript_files
from test_p0_integrated_research import fixture
def inputs(tmp_path):
    p=fixture();q=copy.deepcopy(p);q["claims"][0]["required"]=2
    a=tmp_path/"v1.md";b=tmp_path/"v2.md"
    a.write_text("# Report\n[C01] Unverified universal inference",encoding="utf-8")
    b.write_text("# Report\n[C01] Restricted observation-only inference",encoding="utf-8")
    return [{"revision_id":"v1","path":str(a),"package":p,"attestations":[],"change_note":"initial","claim_anchors":{"C01":"[C01] Unverified universal"}},
            {"revision_id":"v2","path":str(b),"package":q,"attestations":[],"change_note":"scope corrected","claim_anchors":{"C01":"[C01] Restricted observation"}}]
def test_real_two_file_revisions(tmp_path):
    x=audit_manuscript_files(inputs(tmp_path),approved_root=tmp_path)
    assert x["revision_audit"]["research_review"]["rounds_executed"]==2
    assert x["file_traces"][1]["claim_anchor_rows"][0]["line"]==2
    assert not x["publication_ready"]
def test_wrong_claim_anchor_rejected(tmp_path):
    steps=inputs(tmp_path);steps[1]["claim_anchors"]={"C01":"missing passage"}
    with pytest.raises(ValueError):audit_manuscript_files(steps,approved_root=tmp_path)
def test_no_missing_claim_id_allowed(tmp_path):
    steps=inputs(tmp_path);steps[1]["claim_anchors"]={}
    with pytest.raises(ValueError):audit_manuscript_files(steps,approved_root=tmp_path)
def test_path_escape_rejected(tmp_path):
    steps=inputs(tmp_path);sub=tmp_path/"sub";sub.mkdir()
    with pytest.raises(ValueError):audit_manuscript_files(steps,approved_root=sub)
def test_symlink_rejected(tmp_path):
    steps=inputs(tmp_path);alias=tmp_path/"link.md";alias.symlink_to(steps[1]["path"])
    steps[1]["path"]=str(alias)
    with pytest.raises(ValueError):audit_manuscript_files(steps,approved_root=tmp_path)
def test_multiple_anchor_locations_rejected(tmp_path):
    steps=inputs(tmp_path);p=Path(steps[1]["path"]);p.write_text(p.read_text()+"\n[C01] Restricted observation")
    with pytest.raises(ValueError):audit_manuscript_files(steps,approved_root=tmp_path)
