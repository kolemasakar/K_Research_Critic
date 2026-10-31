"""Source-generated UDS error fixtures; no server or external transport."""
import json
from krc_research.research_boundary120 import ResearchBoundary

class Ledger:
    def __init__(self, decision="NEW"): self.decision=decision
    def admit(self, **_):return {"decision":self.decision}
    def complete(self,**_):return None

def failure(*a,**k):
    raise RuntimeError("synthetic-handler-failure")

def fixtures():
    request={"version":"krc-transport/2","request_id":"R-SYN","operation":"research.profile.validate","payload":{"task_id":"T-SYN"}}
    invalid=ResearchBoundary(ledger=Ledger(),exchange=None,dispatch=failure).execute({"version":"bad"},trusted_principal="K_Science")
    handler=ResearchBoundary(ledger=Ledger(),exchange=None,dispatch=failure).execute(request,trusted_principal="K_Science")
    ambiguous=ResearchBoundary(ledger=Ledger("AMBIGUOUS"),exchange=None,dispatch=failure).execute(request,trusted_principal="K_Science")
    return [
      {"case":"INVALID_REQUEST_EARLY","http_status":409,"body":invalid},
      {"case":"HANDLER_ERROR","http_status":409,"body":handler},
      {"case":"AMBIGUOUS_REQUEST","http_status":409,"body":ambiguous},
      {"case":"OPERATION_DENIED_EARLY","http_status":403,"body":{"error":"OPERATION_DENIED"},"origin":"literal VerifiedStage123Handler branch"},
      {"case":"RESPONSE_TOO_LARGE","http_status":507,"body":{"status":"error","error":{"code":"RESPONSE_TOO_LARGE"}},"origin":"literal Stage123Handler.send_json fallback"}
    ]

if __name__=="__main__":
    print(json.dumps(fixtures(),ensure_ascii=False,indent=2,sort_keys=True))
