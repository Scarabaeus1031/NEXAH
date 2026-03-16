from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class ArchyEnvironment:
    name: str
    outside: Dict[str, float]


ENVIRONMENTS = {

    "desert": ArchyEnvironment(
        name="desert",
        outside={
            "thermal": 40,
            "pressure": 1,
            "acoustic": 1,
            "humidity": 0.1,
        }
    ),

    "arctic": ArchyEnvironment(
        name="arctic",
        outside={
            "thermal": -20,
            "pressure": 1,
            "acoustic": 1,
            "humidity": 0.4,
        }
    ),

    "coastal": ArchyEnvironment(
        name="coastal",
        outside={
            "thermal": 25,
            "pressure": 1,
            "acoustic": 2,
            "humidity": 1.5,
        }
    ),

    "tropical": ArchyEnvironment(
        name="tropical",
        outside={
            "thermal": 32,
            "pressure": 1,
            "acoustic": 1,
            "humidity": 2.0,
        }
    ),

    "urban_heat": ArchyEnvironment(
        name="urban_heat",
        outside={
            "thermal": 38,
            "pressure": 1,
            "acoustic": 3,
            "humidity": 1.2,
        }
    ),
}


def get_environment(name: str) -> ArchyEnvironment:

    if name not in ENVIRONMENTS:
        raise ValueError(f"Unknown environment: {name}")

    return ENVIRONMENTS[name]
