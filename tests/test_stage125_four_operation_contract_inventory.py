import pytest
from krc_research.private_contract_schemas import contracts
from krc_research.staging_backend114 import OPS

def test_four_operation_inventory():
    assert set(contracts()["operations"]) == set(OPS)

@pytest.mark.parametrize("operation",sorted(OPS))
def test_each_operation_has_input_and_output_schema(operation):
    spec=contracts()["operations"][operation]
    assert "inputSchema" in spec and "outputSchema" in spec
    assert spec["outputSchema"]["properties"]["scientific_approval"]["const"] is False
