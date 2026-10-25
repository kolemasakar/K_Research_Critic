import os,sys,tempfile
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.reviewer_issuer import issue_review_attestation,read_reviewer_key
def receipt():
    return dict(source_id="S1",origin_id="O1",doi="10.1234/demo",document_sha256="a"*64,
       inspected_sections=("METHODS","RESULTS"),passage_locators=("method-paragraph","result-paragraph"),
       checked_at="2026-10-25T12:00:00+00:00",inspector_id="reviewer-X",method="FULL_TEXT",
       evidence_relation="SUPPORTS",external_trace_id="trace-1",trace_verified=True)
def notes():
    return dict(explicit_reviewer_approval=True,reviewer_id="reviewer-X",
                document_sha256="a"*64,source_id="S1",methods_notes="Method checked",
                results_notes="Outcome limits recorded")
def key(tmp_path):
    p=tmp_path/"key";p.write_bytes(b"k"*32);p.chmod(0o600);return p
def test_review_issue_explicit_approval(tmp_path):
    x=issue_review_attestation(receipt(),reviewer_id="reviewer-X",
         researcher_id="author-Y",inspection_record=notes(),key_path=key(tmp_path))
    assert x["signature"] and x["scientific_truth_verified"] is False
def test_no_explicit_approval(tmp_path):
    n=notes();n["explicit_reviewer_approval"]=False
    with pytest.raises(ValueError):issue_review_attestation(receipt(),reviewer_id="reviewer-X",
         researcher_id="author-Y",inspection_record=n,key_path=key(tmp_path))
def test_self_review_denied(tmp_path):
    with pytest.raises(ValueError):issue_review_attestation(receipt(),reviewer_id="reviewer-X",
         researcher_id="reviewer-X",inspection_record=notes(),key_path=key(tmp_path))
def test_wrong_document_denied(tmp_path):
    n=notes();n["document_sha256"]="b"*64
    with pytest.raises(ValueError):issue_review_attestation(receipt(),reviewer_id="reviewer-X",
         researcher_id="author-Y",inspection_record=n,key_path=key(tmp_path))
def test_weak_filesystem_permission_denied(tmp_path):
    p=key(tmp_path);p.chmod(0o644)
    with pytest.raises(ValueError):read_reviewer_key(p)
def test_symlink_key_denied(tmp_path):
    p=key(tmp_path);link=tmp_path/"link";link.symlink_to(p)
    with pytest.raises(ValueError):read_reviewer_key(link)
def test_missing_method_notes_denied(tmp_path):
    n=notes();n["methods_notes"]=""
    with pytest.raises(ValueError):issue_review_attestation(receipt(),reviewer_id="reviewer-X",
         researcher_id="author-Y",inspection_record=n,key_path=key(tmp_path))
