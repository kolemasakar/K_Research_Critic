import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from krc_research.ref27_percent_alternatives import alternatives
def sample():
 return json.loads((Path(__file__).parent/"fixtures"/"ref27_upv_table_i.json").read_text())
def test_two_methods_fit_all_groups_not_one():
 r=alternatives(sample())
 assert len(r["methods_matching_all_groups"])==2
 assert "ratio_of_group_means" in r["methods_matching_all_groups"]
 assert "mean_of_unrounded_individual_pct" in r["methods_matching_all_groups"]
 assert not r["unique_original_method_inferable"]
def test_rounded_first_differs_for_group_k():
 r=alternatives(sample())
 k=next(x for x in r["groups"] if x["group"]=="K")
 assert k["mean_of_rounded_individual_pct"]==[18,11,6]
 assert k["source_reported_pct"]==[18,12,5]
def test_no_author_method_proof():
 assert not alternatives(sample())["authors_original_rounding_method_proven"]
