"""Stage120 in-process transport boundary. Staging only; principal comes from trusted caller."""
import json
from .request_ledger119 import RequestLedger, LedgerError
from .artifact_exchange import deliver_result, ExchangeError

class ResearchBoundary:
    def __init__(self, *, ledger, exchange, dispatch):
        self.ledger=ledger
        self.exchange=exchange
        self.dispatch=dispatch

    def execute(self, request, *, trusted_principal):
        if not isinstance(request,dict) or request.get("version")!="krc-transport/2":
            return {"status":"rejected","error":{"code":"INVALID_REQUEST"}}
        request_id=request.get("request_id")
        operation=request.get("operation")
        payload=request.get("payload")
        if not isinstance(operation,str) or not isinstance(payload,dict):
            return {"status":"rejected","error":{"code":"INVALID_REQUEST"}}
        try:
            claim=self.ledger.admit(principal=trusted_principal,request_id=request_id,operation=operation,payload=payload)
        except LedgerError as exc:
            return {"status":"rejected","request_id":request_id,"error":{"code":exc.code}}
        if claim["decision"]=="REPLAY":
            return claim["result"]
        if claim["decision"]=="AMBIGUOUS":
            return {"status":"pending_reconciliation","request_id":request_id,"error":{"code":"AMBIGUOUS_REQUEST"}}
        try:
            result=self.dispatch(operation,payload,trusted_principal)
            output=deliver_result(result,exchange=self.exchange,principal=trusted_principal,request_id=request_id)
            self.ledger.complete(principal=trusted_principal,request_id=request_id,operation=operation,payload=payload,result=output)
            return output
        except (ExchangeError,LedgerError) as exc:
            return {"status":"pending_reconciliation","request_id":request_id,"error":{"code":exc.code}}
        except Exception:
            return {"status":"pending_reconciliation","request_id":request_id,"error":{"code":"HANDLER_ERROR"}}
