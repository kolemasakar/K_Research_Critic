import pytest
from krc_research.request_ledger119 import RequestLedger
from krc_research.artifact_exchange import ArtifactExchange, MIB
from krc_research.research_boundary120 import ResearchBoundary

def setup(tmp_path,dispatch=None):
 calls=[]
 def fn(op,payload,principal):
  calls.append((op,principal))
  return {"text":payload.get("text","ok")}
 return ResearchBoundary(ledger=RequestLedger(tmp_path/"ledger.sqlite3"),exchange=ArtifactExchange(tmp_path/"exchange"),dispatch=dispatch or fn),calls

def request(text="small",request_id="r"):
 return {"version":"krc-transport/2","request_id":request_id,"operation":"research.profile.validate","payload":{"text":text}}

def test_inline(tmp_path):
 b,c=setup(tmp_path)
 assert b.execute(request(),trusted_principal="K_Science")["delivery"]=="inline"
 assert len(c)==1

def test_replay(tmp_path):
 b,c=setup(tmp_path)
 a=b.execute(request(),trusted_principal="K_Science")
 assert b.execute(request(),trusted_principal="K_Science")==a and len(c)==1

def test_conflict(tmp_path):
 b,c=setup(tmp_path);b.execute(request(),trusted_principal="K_Science")
 assert b.execute(request("other"),trusted_principal="K_Science")["error"]["code"]=="IDEMPOTENCY_CONFLICT"

def test_large_artifact(tmp_path):
 b,c=setup(tmp_path)
 out=b.execute(request("x"*MIB),trusted_principal="K_Science")
 assert out["delivery"]=="artifact"
 assert len(b.exchange.get_bytes(out["artifact"]["artifact_id"],principal="K_Science",request_id="r"))>MIB

def test_foreign_fetch_denied(tmp_path):
 b,c=setup(tmp_path)
 out=b.execute(request("x"*MIB),trusted_principal="K_Science")
 with pytest.raises(Exception,match="NOT_FOUND"):
  b.exchange.get_bytes(out["artifact"]["artifact_id"],principal="other",request_id="r")

def test_untrusted_operation_error_reconciles(tmp_path):
 def fail(op,payload,p):raise RuntimeError("failure")
 b,_=setup(tmp_path,fail)
 assert b.execute(request(),trusted_principal="K_Science")["error"]["code"]=="HANDLER_ERROR"
 assert b.execute(request(),trusted_principal="K_Science")["error"]["code"]=="AMBIGUOUS_REQUEST"

def test_no_version(tmp_path):
 b,_=setup(tmp_path)
 assert b.execute({**request(),"version":"bad"},trusted_principal="K_Science")["error"]["code"]=="INVALID_REQUEST"
