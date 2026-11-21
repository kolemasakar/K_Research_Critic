"""Strict offline Stage133 external scientific payload validation.

No network, disk, key, consent, source verification, or scientific approval.
The owner grant is checked separately by the private project route.
"""
from copy import deepcopy
from datetime import datetime
import re
from jsonschema import Draft202012Validator, FormatChecker

_TS = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})$")
_CHECKER = FormatChecker()
@_CHECKER.checks("date-time")
def _aware_rfc3339(value):
    if value is None:
        return True
    if not isinstance(value, str) or _TS.fullmatch(value) is None:
        return False
    try:
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return moment.utcoffset() is not None
    except ValueError:
        return False

from .private_contract_details import CLAIM, RECEIPT

GATE_FLAGS = (
    "journal_policy_checked", "search_audit_reproducible",
    "primary_sources_inspected", "novelty_reviewed",
    "citations_validated", "scientific_methods_audited",
    "rights_and_ai_disclosure_done", "human_author_approved"
)
TEXT = {"type": "string", "minLength": 1, "maxLength": 4096}
GATE = {
    "type": "object", "additionalProperties": False,
    "required": list(GATE_FLAGS),
    "properties": {
        **{name: {"type": "boolean"} for name in GATE_FLAGS},
        "detector_run_records": {
            "type": "array", "maxItems": 32,
            "items": {
                "type": "object", "additionalProperties": False,
                "required": ["provider", "checked_at", "input_hash"],
                "properties": {
                    "provider": TEXT,
                    "checked_at": {"type": "string", "format": "date-time"},
                    "input_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                },
            },
        },
        "detector_check_status": {
            "enum": ["NOT_RUN", "UNAVAILABLE", "COMPLETED"]
        },
        "detector_authorized": {"type": "boolean"},
    },
}
SEARCH = {
    "type": "object", "additionalProperties": False,
    "required": ["provider", "query", "executed_at", "hit_count", "exported_records"],
    "properties": {
        "provider": TEXT,
        "query": TEXT,
        "executed_at": {"type": ["string", "null"], "format": "date-time"},
        "hit_count": {"type": ["integer", "null"], "minimum": 0},
        "exported_records": {"type": ["integer", "null"], "minimum": 0},
        "filter_description": {"type": "string", "maxLength": 4096},
    },
}
CLAIM_STRICT = deepcopy(CLAIM)
CLAIM_STRICT["properties"]["evidence"]["maxItems"] = 64
CLAIM_STRICT["properties"]["required"]["maximum"] = 64
RECEIPT_STRICT = deepcopy(RECEIPT)
RECEIPT_STRICT["properties"]["trace_verified"] = {"const": False}
for name in ("inspected_sections", "passage_locators"):
    RECEIPT_STRICT["properties"][name]["maxItems"] = 128
    RECEIPT_STRICT["properties"][name]["items"] = TEXT

PREFLIGHT = "research.evidence.preflight"
INSPECTION = "research.inspection.review"
EXTERNAL_SCHEMAS = {
    PREFLIGHT: {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object", "additionalProperties": False,
        "required": ["manuscript_gate"],
        "properties": {
            "manuscript_gate": GATE,
            "claims": {"type": "array", "maxItems": 128, "items": CLAIM_STRICT},
            "search_runs": {"type": "array", "maxItems": 128, "items": SEARCH},
        },
    },
    INSPECTION: {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object", "additionalProperties": False,
        "required": ["receipt"],
        "properties": {"receipt": RECEIPT_STRICT},
    },
}
_VALIDATORS = {
    operation: Draft202012Validator(schema, format_checker=_CHECKER)
    for operation, schema in EXTERNAL_SCHEMAS.items()
}

def validate_external_science_payload(operation, payload):
    """Reject malformed content before authorization claim or science dispatch."""
    if not isinstance(payload, dict) or operation not in _VALIDATORS:
        return False
    if not _VALIDATORS[operation].is_valid(payload):
        return False
    if operation == PREFLIGHT:
        identifiers = [row["claim_id"] for row in payload.get("claims", [])]
        if len(identifiers) != len(set(identifiers)):
            return False
        for run in payload.get("search_runs", []):
            count, exported = run["hit_count"], run["exported_records"]
            if count is not None and exported is not None and exported > count:
                return False
        gate = payload["manuscript_gate"]
        if gate.get("detector_check_status") == "COMPLETED" and (
            gate.get("detector_authorized") is not True
            or not gate.get("detector_run_records")
        ):
            return False
    return True
