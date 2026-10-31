import pytest
from krc_research.stage131_correlated_dispatch import execute_correlated,ScienceResultContractError
OP="research.profile.validate"
PAYLOAD={"task_id":"ks-task-00001"}
def good(op,payload,principal,*,request_id):
    return {"task_id":payload["task_id"],"operation":op,"status":"PENDING","engine_result":{},"scientific_approval":False}
def test_valid_result_released_after_validation():
    assert execute_correlated(good,operation=OP,payload=PAYLOAD,principal="K_Science",request_id="R")["scientific_approval"] is False
@pytest.mark.parametrize("mutation",[{"task_id":"wrong"},{"scientific_approval":True},{"operation":"research.inspection.review"},{"engine_result":[]},{"status":"APPROVED"}])
def test_unsafe_result_never_released(mutation):
    def invalid(*args,**kw):return {**good(OP,PAYLOAD,"K_Science",request_id="R"),**mutation}
    with pytest.raises(ScienceResultContractError):
        execute_correlated(invalid,operation=OP,payload=PAYLOAD,principal="K_Science",request_id="R")
def test_missing_trusted_task_denied_without_dispatch():
    def forbidden(*a,**k):raise AssertionError("dispatched")
    with pytest.raises(ScienceResultContractError,match="INVALID_REQUEST"):
        execute_correlated(forbidden,operation=OP,payload={},principal="K_Science",request_id="R")
