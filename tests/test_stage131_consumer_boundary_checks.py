from krc_research.stage131_consumer_boundary_checks import validate_science_result,validate_artifact_descriptor
OP="research.profile.validate"
RESULT={"task_id":"science-task-0001","operation":OP,"status":"PENDING","engine_result":{},"scientific_approval":False}
ART={"artifact_id":"a"*48,"filename":"result.json","media_type":"application/json","size_bytes":42,"sha256":"b"*64,"expires_at_epoch":2000}

def test_science_correlation_success_and_mismatches():
    assert validate_science_result(RESULT,expected_task_id=RESULT["task_id"],expected_operation=OP)=="VALID_SHAPE_ONLY"
    assert validate_science_result({**RESULT,"task_id":"other"},expected_task_id=RESULT["task_id"],expected_operation=OP)=="CORRELATION_MISMATCH"
    assert validate_science_result({**RESULT,"operation":"research.inspection.review"},expected_task_id=RESULT["task_id"],expected_operation=OP)=="CORRELATION_MISMATCH"

def test_science_malformed_and_approval():
    assert validate_science_result({**RESULT,"scientific_approval":True},expected_task_id=RESULT["task_id"],expected_operation=OP)=="INVALID_SCIENCE_RESULT"
    assert validate_science_result({**RESULT,"engine_result":[]},expected_task_id=RESULT["task_id"],expected_operation=OP)=="INVALID_SCIENCE_RESULT"
    assert validate_science_result({k:v for k,v in RESULT.items() if k!="task_id"},expected_task_id=RESULT["task_id"],expected_operation=OP)=="INVALID_SCIENCE_RESULT"

def test_artifact_ttl_boundary_and_missing_expiry():
    assert validate_artifact_descriptor(ART,now_epoch=1999)=="DESCRIPTOR_VALID_NOT_AUTHORIZED"
    assert validate_artifact_descriptor(ART,now_epoch=2000)=="EXPIRED"
    assert validate_artifact_descriptor(ART,now_epoch=2001)=="EXPIRED"
    assert validate_artifact_descriptor({k:v for k,v in ART.items() if k!="expires_at_epoch"},now_epoch=1000)=="INVALID_ARTIFACT"

def test_artifact_invalid_types():
    assert validate_artifact_descriptor({**ART,"size_bytes":True},now_epoch=1000)=="INVALID_ARTIFACT"
    assert validate_artifact_descriptor({**ART,"expires_at_epoch":True},now_epoch=1000)=="INVALID_ARTIFACT"
    assert validate_artifact_descriptor({**ART,"sha256":"!"*64},now_epoch=1000)=="INVALID_ARTIFACT"
