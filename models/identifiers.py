from __future__ import annotations

from enum import StrEnum
from uuid import uuid4


class IdPrefix(StrEnum):
    TASK = "TASK"
    RUN = "RUN"
    WORKFLOW = "WF"
    TRANSITION = "TRANSITION"
    PROFILE = "PROFILE"
    CLAIM = "CLAIM"
    SOURCE = "SOURCE"
    REVIEW = "REVIEW"
    ARTIFACT = "ARTIFACT"
    ASSESSMENT = "ASSESSMENT"
    APPROVAL = "APPROVAL"
    REQUEST = "REQUEST"
    AGENT = "AGENT"
    ERROR = "ERROR"


def generate_id(prefix: IdPrefix | str) -> str:
    """Return a collision-resistant, human-traceable identifier."""
    prefix_value = prefix.value if isinstance(prefix, IdPrefix) else str(prefix)
    normalized = prefix_value.strip().upper()
    if not normalized or not normalized.replace("_", "").isalnum():
        raise ValueError("Identifier prefix must be non-empty ASCII alphanumeric text")
    return f"{normalized}_{uuid4().hex[:16].upper()}"
