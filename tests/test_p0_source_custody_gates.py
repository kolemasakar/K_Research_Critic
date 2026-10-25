import hashlib
import pytest
from krc_research.source_custody_gates import verify_source_bytes,review_methods_novelty

def test_exact(tmp_path):
 p=tmp_path/'a';p.write_bytes(b'actual');r=verify_source_bytes(p,hashlib.sha256(b'actual').hexdigest());assert r['status']=='PASS' and not r['scientific_claim_verified']
def test_mutation(tmp_path):
 p=tmp_path/'a';p.write_bytes(b'a');d=hashlib.sha256(b'a').hexdigest();p.write_bytes(b'b');assert verify_source_bytes(p,d)['status']=='HASH_MISMATCH'
def test_bad_hash(tmp_path):
 p=tmp_path/'a';p.write_bytes(b'a')
 with pytest.raises(ValueError):verify_source_bytes(p,'wrong')
def test_symlink(tmp_path):
 p=tmp_path/'a';p.write_bytes(b'a');l=tmp_path/'b';l.symlink_to(p)
 with pytest.raises(ValueError):verify_source_bytes(l,hashlib.sha256(b'a').hexdigest())
def test_method_shortfall():
 r=review_methods_novelty({});assert r['methodology']=='SHORTFALL' and r['novelty']=='SHORTFALL'
def test_method_not_scientific_proof():
 p={k:'documented' for k in ('research_question','methods','sampling_plan','uncertainty_plan','prior_art_search_log','novelty_claim','closest_prior_work')};r=review_methods_novelty(p);assert r['methodology']=='DOCUMENTED_FOR_REVIEW' and not r['independent_novelty_established']
def test_invalid_package():
 with pytest.raises(ValueError):review_methods_novelty([])
