"""Isolated signed research preflight, without network operations."""
from .science_dispatch import handle_science_request
from .workflow_readiness import inspect_workflow

def execute_bounded_workflow(message, *, secret, signature, registry, now=None):
    if message.get('operation') != 'research.evidence.preflight':
        raise ValueError('Unsupported operation')
    payload = message.get('payload')
    if not isinstance(payload, dict):
        raise ValueError('Object payload required')
    readiness = inspect_workflow(payload)
    receipt = handle_science_request(message, secret=secret, signature=signature,
        seen=registry, permitted={'research.evidence.preflight'}, now=now)
    return {'schema': 'KRC-P0-BOUND-ENTRY-1', 'task_id': receipt['task_id'],
        'authenticated_operation': receipt['operation'], 'readiness': readiness,
        'critic': receipt['engine_result'], 'status': receipt['status'],
        'scientific_approval': False, 'publication_gate': 'NO_GO',
        'full_workflow_implemented': False}
