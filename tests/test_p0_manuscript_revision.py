import copy,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.manuscript_revision import audit_manuscript_revisions
from test_p0_integrated_research import fixture
def steps():
    p=fixture();q=copy.deepcopy(p);q["claims"][0]["required"]=2
    return [{"revision_id":"v1","manuscript":"Intro\\nUntested universal claim","package":p,"attestations":[],"change_note":"baseline"},
            {"revision_id":"v2","manuscript":"Intro\\nClaim limited to measured samples","package":q,"attestations":[],"change_note":"scope correction"}]
def test_two_real_manuscript_and_research_revisions():
    x=audit_manuscript_revisions(steps())
    assert x["actual_manuscript_revisions"]==1 and x["research_review"]["rounds_executed"]==2
    assert x["manuscripts"][1]["diff"]["changed"] and not x["publication_ready"]
def test_unchanged_manuscript_denied():
    x=steps();x[1]["manuscript"]=x[0]["manuscript"]
    with pytest.raises(ValueError):audit_manuscript_revisions(x)
def test_unchanged_research_denied_even_if_manuscript_changed():
    x=steps();x[1]["package"]=copy.deepcopy(x[0]["package"])
    with pytest.raises(ValueError):audit_manuscript_revisions(x)
def test_missing_change_log_denied():
    x=steps();x[1]["change_note"]=""
    with pytest.raises(ValueError):audit_manuscript_revisions(x)
def test_empty_text_denied():
    x=steps();x[1]["manuscript"]=""
    with pytest.raises(ValueError):audit_manuscript_revisions(x)
def test_one_revision_only_denied():
    with pytest.raises(ValueError):audit_manuscript_revisions(steps()[:1])
