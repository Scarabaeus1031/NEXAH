from dataclasses import dataclass
from typing import Dict, List, Any


REQUIRED_FIELDS = [
    "nodes",
    "edges",
    "regimes",
    "transitions",
    "control_actions",
    "shock_events",
    "risk_target",
]


def validate_schema(data: Dict[str, Any]) -> None:
    """
    Validates a JSON system definition against the minimal
    NEXAH system schema.
    """

    for field in REQUIRED_FIELDS:
        if field not in data:
            raise ValueError(f"NEXAH schema error: missing required field '{field}'")

    if not isinstance(data["nodes"], list):
        raise TypeError("nodes must be a list")

    if not isinstance(data["edges"], list):
        raise TypeError("edges must be a list")

    if not isinstance(data["regimes"], dict):
        raise TypeError("regimes must be a dictionary")

    if not isinstance(data["transitions"], dict):
        raise TypeError("transitions must be a dictionary")


@dataclass
class NexahSystem:
    """
    Core system representation used by the NEXAH framework.
    """

    nodes: List[str]
    edges: List[List[str]]
    regimes: Dict[str, str]
    transitions: Dict[str, str]
    control_actions: Dict[str, Any]
    shock_events: Dict[str, Any]
    risk_target: str
    metadata: Dict[str, Any] | None = None
