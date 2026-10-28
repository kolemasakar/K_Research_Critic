"""Check actual Stage123 UDS response and protected GET implementation (no live services)."""
import inspect
from krc_research.artifact_exchange import deliver_result
from krc_research.uds_stage123 import Stage123Handler
from krc_research.uds_verified123b import VerifiedStage123Handler

def test_actual_inline_wire_contract_not_proposed_response_v1():
    class E:
        @staticmethod
        def _assert_scope(principal,request_id):
            assert principal=="K_Science"
    actual=deliver_result({"status":"synthetic"},exchange=E(),principal="K_Science",request_id="KS-"+"1"*32)
    assert actual["version"]=="krc-transport/2"
    assert actual["status"]=="completed"
    assert actual["delivery"]=="inline"
    assert "scientific_approval" not in actual
    assert "operation" not in actual

def test_get_is_private_local_only_and_scoped():
    source=inspect.getsource(Stage123Handler.do_GET)
    assert 'self.principal()' in source
    assert 'X-KRC-Request-ID' in source
    assert "exchange.read_stream" in source
    assert 'X-Content-SHA256' in source
    assert inspect.getattr_static(VerifiedStage123Handler,"do_GET") is Stage123Handler.do_GET
