import pytest
from krc_research.stage131_correlated_dispatch import execute_correlated, ScienceResultContractError
def test_mutating_dispatch_cannot_change_trusted_task_or_original_payload():
    payload={"task_id":"trusted-task","nested":{"value":"original"}}
    def mutate(operation,received,principal,*,request_id):
        received["task_id"]="attacker-task"
        received["nested"]["value"]="changed"
        return {"task_id":received["task_id"],"operation":operation,"status":"PENDING","engine_result":{},"scientific_approval":False}
    with pytest.raises(ScienceResultContractError,match="CORRELATION_MISMATCH"):
        execute_correlated(mutate,operation="research.profile.validate",payload=payload,principal="K_Science",request_id="R")
    assert payload=={"task_id":"trusted-task","nested":{"value":"original"}}
