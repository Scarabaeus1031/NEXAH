import json
from pathlib import Path

from .system_schema import NexahSystem, validate_schema


def load_system(path: str | Path) -> NexahSystem:
    """
    Loads a NEXAH system definition from a JSON file.
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"System file not found: {path}")

    with open(path, "r") as f:
        data = json.load(f)

    validate_schema(data)

    system = NexahSystem(
        nodes=data["nodes"],
        edges=data["edges"],
        regimes=data["regimes"],
        transitions=data["transitions"],
        control_actions=data.get("control_actions", {}),
        shock_events=data.get("shock_events", {}),
        risk_target=data["risk_target"],
        metadata=data.get("metadata"),
    )

    return system
