import copy, json, hashlib, os
import pytest
from krc_research.stage131_project_research_route import ProjectResearchRoute
from krc_research.replay_registry import ReplayRegistry
from krc_research.stage131_project_signed_read import ProjectArtifactAuthority
from krc_research.stage132_project_post_contract import ProjectPostBoundary, IDENTITY
from krc_research.stage132_project_post_wire import OP, PREFLIGHT, INSPECTION, BIBLIOGRAPHY, OFFLINE_OPS
from krc_research.stage132_project_post_relay import PilotGatewayBoundary
from krc_research.stage131_science_semantic_contract import validate_operation_result
from test_stage132_project_post_contract import count
@pytest.fixture(autouse=True)
def private_umask():
 old=os.umask(0o077)
 try: yield
 finally: os.umask(old)

GATE=dict.fromkeys(("journal_policy_checked","search_audit_reproducible","primary_sources_inspected","novelty_reviewed","citations_validated","scientific_methods_audited","rights_and_ai_disclosure_done","human_author_approved"),False)
PAYLOADS={
 PREFLIGHT:{"manuscript_gate":GATE,"claims":[],"search_runs":[]},
 INSPECTION:{"receipt":{"source_id":"S01","origin_id":"O01","doi":"10.0000/synthetic","document_sha256":"a"*64,"inspected_sections":["methods"],"passage_locators":["p1"],"checked_at":"2026-11-20T00:00:00Z","inspector_id":"synthetic","method":"METHODS_RESULTS_EXCERPT","evidence_relation":"INSUFFICIENT","external_trace_id":"synthetic","trace_verified":False}}
}
@pytest.mark.parametrize("op",list(PAYLOADS))
def test_authorized_offline_operation(tmp_path,op):
 route=ProjectResearchRoute(tmp_path/"private")
 ReplayRegistry(route.root/"science-replay.sqlite")
 payload=copy.deepcopy(PAYLOADS[op])
 p=route.propose({"operation":op,"payload":payload,"purpose":"Synthetic isolated fixture","policy":"FREE_ONLY_OFFLINE"})
 rid=p["request_id"]
 e={"version":"krc-transport/2","identity":IDENTITY,"request_id":rid,"operation":op,"payload":payload}
 b=ProjectPostBoundary(route.root,enabled=True,enabled_operations=OFFLINE_OPS)
 call=lambda value:b.execute(value,trusted_principal="K_Science")
 assert call(e)[0]==403 and count(route)==0
 route.decide(rid,p["profile_sha256"],"APPROVE")
 assert ProjectPostBoundary(route.root,enabled=True).execute(e,trusted_principal="K_Science")[0]==403
 bad=copy.deepcopy(e)
 if op==PREFLIGHT:bad["payload"]["user_profile_approved"]=True
 else:bad["payload"]["receipt"]["trace_verified"]=True
 assert call(bad)[0]==403 and count(route)==0
 changed=copy.deepcopy(e)
 if op==PREFLIGHT:changed["payload"]["manuscript_gate"]["citations_validated"]=True
 else:changed["payload"]["receipt"]["source_id"]="other"
 assert call(changed)[0]==409 and count(route)==0
 status,d=call(e)
 assert status==200
 a=d["artifact"]
 scope={"request_id":rid,"artifact_id":a["artifact_id"],"principal":"K_Science"}
 f,descriptor=ProjectArtifactAuthority(route.root).spool(scope)
 with f:raw=f.read()
 assert descriptor=={**a,"request_id":rid}
 assert hashlib.sha256(raw).hexdigest()==a["sha256"] and len(raw)==a["size_bytes"]
 result=json.loads(raw)
 assert validate_operation_result(result,task_id=rid+"-task",operation=op)=="SEMANTIC_SHAPE_VALID_ONLY_NOT_SCIENTIFIC_APPROVAL"
 assert result["scientific_approval"] is False
 if op==PREFLIGHT:assert result["engine_result"]["final_publication_status"]=="NO_GO"
 else:assert result["engine_result"]["eligible_for_independent_claim_review"] is False
 assert call(e)[0]==409 and count(route)==1

def test_disabled_operations_never_fall_through():
 class Legacy:
  exchange=None
  def execute(self,*a,**k):raise AssertionError("legacy fallback")
 class Relay:
  enabled_operations=frozenset((OP,))
  def execute(self,*a,**k):raise AssertionError("relay fallback")
 gateway=PilotGatewayBoundary(Legacy(),Relay())
 for op in (PREFLIGHT, INSPECTION, BIBLIOGRAPHY):
  assert gateway.execute({"operation":op},trusted_principal="K_Science")=={"error":"OPERATION_DENIED"}
 with pytest.raises(ValueError):ProjectPostBoundary("/unused",enabled=True,enabled_operations={BIBLIOGRAPHY})

