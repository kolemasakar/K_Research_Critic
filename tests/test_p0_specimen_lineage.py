import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.specimen_lineage import audit_specimen_overlap,normalize_specimen_id
N=["N-1.28","N-2.28","N-7.28"]
K=["K-9.28","K-11.28","K-12.28"]
KV=["KV-19.28","KV-21.28","KV-24.28"]
def test_ref26_ref27_shared_nine_specimens():
    a=audit_specimen_overlap([{"source_id":"REF26","specimen_ids":N+K+KV+["N-10.7"]},
                              {"source_id":"REF27","specimen_ids":N+K+KV}])
    assert a["shared_sample_pairs"]==1 and a["pairs"][0]["common_count"]==9
    assert not a["pairs"][0]["independent_specimen_cohorts"]
def test_disjoint_specimens_not_claimed_scientifically_independent():
    a=audit_specimen_overlap([{"source_id":"a","specimen_ids":["N-1.28"]},
                              {"source_id":"b","specimen_ids":["N-2.28"]}])
    assert a["verdict"]=="NO_ID_OVERLAP_DETECTED"
    assert not a["scientific_independence_proven"]
def test_duplicate_source_id_denied():
    with pytest.raises(ValueError):audit_specimen_overlap([{"source_id":"a","specimen_ids":["N-1.28"]},{"source_id":"a","specimen_ids":["K-2.28"]}])
def test_duplicate_specimen_denied():
    with pytest.raises(ValueError):audit_specimen_overlap([{"source_id":"a","specimen_ids":["N-1.28","N-1.28"]},{"source_id":"b","specimen_ids":["K-2.28"]}])
def test_invalid_specimen_denied():
    with pytest.raises(ValueError):normalize_specimen_id("1.28")
def test_normalization():
    assert normalize_specimen_id(" kv-019.028 ")=="KV-19.28"
