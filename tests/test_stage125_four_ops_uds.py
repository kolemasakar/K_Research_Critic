import json,os,threading
from datetime import datetime,timezone
import pytest
from krc_research.staging_service123c import make_staging_server
from test_staging_service123c import IDENTITY,KEY,SECRET,post
from krc_research.interproject_contract import envelope,sign_envelope
from krc_research.transport_auth123b import canonical
import hashlib,hmac

OPS=("research.profile.validate","research.evidence.preflight","research.bibliography.audit","research.inspection.review")
def payload(op):
 if op==OPS[0]:return {"critic_profile":{"profile_id":"p","version":"v1","protocol":"KRC Core","topic":"offline"}}
 if op==OPS[1]:
  fields=("journal_policy_checked","search_audit_reproducible","primary_sources_inspected","novelty_reviewed","citations_validated","scientific_methods_audited","rights_and_ai_disclosure_done","human_author_approved")
  return {"user_profile_approved":True,"manuscript_gate":{k:False for k in fields},"claims":[],"search_runs":[]}
 if op==OPS[2]:return {"dois":["10.1234/synthetic"]}
 return {"receipt":{"source_id":"s","origin_id":"o","doi":"10.1234/x","document_sha256":"a"*64,"inspected_sections":["Methods"],"passage_locators":["p1"],"checked_at":datetime.now(timezone.utc).isoformat(),"inspector_id":"i","method":"FULL_TEXT","evidence_relation":"SUPPORTS","external_trace_id":"synthetic","trace_verified":False}}
def signed(op,seq):
 inner=envelope(task_id=f"stage125-task-{seq:04}",operation=op,payload=payload(op),created_at=datetime.now(timezone.utc).isoformat())
 body={"version":"krc-transport/2","request_id":f"stage125-request-{seq:04}","operation":op,"identity":IDENTITY,"payload":{"science_envelope":inner,"science_signature":sign_envelope(inner,SECRET)}}
 stamp=datetime.now(timezone.utc).isoformat()
 binding={"domain":"KRC-TRANSPORT-IDENTITY/2","key_id":"stage","issued_at":stamp,"envelope":body}
 body["transport_auth"]={"alg":"HMAC-SHA256","key_id":"stage","issued_at":stamp,"mac":hmac.new(KEY,canonical(binding),hashlib.sha256).hexdigest()}
 return body
@pytest.mark.parametrize("op",OPS)
def test_verified_operation(tmp_path,op):
 server=make_staging_server(tmp_path/"backend.sock",tmp_path/"state",peer_principals={os.getuid():"K_Science"},uid_keys={os.getuid():{"stage":KEY}},claim_allowlist={tuple(IDENTITY.values())},science_secret=SECRET,bibliography_fn=lambda dois:{"count":len(dois),"network_used":False})
 t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
 try:
  msg=signed(op,OPS.index(op)+1)
  res=post(tmp_path/"backend.sock",msg)
  assert b"200 OK" in res,res[:500]
  answer=json.loads(res.partition(b"\r\n\r\n")[2])
  assert answer["result"]["operation"]==op
  assert answer["result"]["scientific_approval"] is False
  msg["payload"]["science_signature"]="0"*64
  assert b"403 Forbidden" in post(tmp_path/"backend.sock",msg)
 finally:server.shutdown();server.server_close();t.join()
