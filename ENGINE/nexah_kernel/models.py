from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class SystemArchitecture:
    """
    Representation of a generated architecture.
    """
    nodes: List[Any]
    edges: List[Any]
    parameters: Dict[str, Any]


@dataclass
class StructuralGraph:
    """
    Graph representation of the system architecture.
    """
    nodes: Dict[str, Any]
    edges: List[Any]
    weights: Dict[str, float]


@dataclass
class RegimeLandscape:
    """
    Representation of stability regimes within architecture space.
    """
    attractors: List[Any]
    basins: Dict[str, Any]
    thresholds: List[Any]


@dataclass
class NavigationResult:
    """
    Output of navigation analysis.
    """
    trajectories: List[Any]
    leverage_points: List[Any]
