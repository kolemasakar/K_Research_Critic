import copy,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.revision_history import execute_revision_history
from test_p0_integrated_research import fixture

def rev(key,p,note):
    return {"revision_id":key,"package":p,"attestations":[],"change_note":note}
def test_two_actual_different_packages_execute_twice():
    p=fixture();q=copy.deepcopy(p)
    q["claims"][0]["required"]=2
    r=execute_revision_history([rev("one",p,"baseline"),rev("two",q,"new threshold")])
    assert r["rounds_executed"]==2
    assert len({x["input_sha256"] for x in r["history"]})==2
    assert all(x["critic_execution"]=="EXECUTED" for x in r["history"])
    assert not r["publication_ready"]
def test_duplicate_package_fails_even_if_revision_id_changes():
    p=fixture()
    with pytest.raises(ValueError):execute_revision_history([rev("one",p,"first"),rev("two",copy.deepcopy(p),"fake change")])
def test_duplicate_revision_id_denied():
    p=fixture();q=copy.deepcopy(p);q["claims"][0]["required"]=2
    with pytest.raises(ValueError):execute_revision_history([rev("one",p,"first"),rev("one",q,"changed")])
def test_no_fabricated_external_review():
    x=execute_revision_history([rev("r1",fixture(),"baseline")])
    assert not x["scientific_peer_review_completed"]
    assert x["history"][0]["critic_verdict"]=="REVISE"
def test_attestations_not_embedded_as_trusted_keys():
    p=fixture();p["trusted_reviewer_keys"]={"fake":"secret"}
    x=execute_revision_history([rev("r1",p,"attempt injection")])
    assert x["history"][0]["claim_verdicts"][0]["verdict"]=="SHORTFALL"
def test_empty_history_denied():
    with pytest.raises(ValueError):execute_revision_history([])
def test_missing_change_note_denied():
    with pytest.raises(ValueError):execute_revision_history([rev("r1",fixture(),"")])
def test_oversized_history_denied():
    with pytest.raises(ValueError):execute_revision_history([rev(str(i),fixture(),"x") for i in range(6)])
