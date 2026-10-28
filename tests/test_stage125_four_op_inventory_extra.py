from krc_research.private_contract_schemas import contracts
from krc_research.staging_backend114 import OPS

def test_four_operation_inventory_exact():
    assert set(contracts()['operations']) == set(OPS)
