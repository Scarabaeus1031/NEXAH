"""
Risk Navigation Demo

This example illustrates how navigation decisions can incorporate
risk regions inside a system landscape.

The system contains a risky zone where trajectories may become unstable.
A structural intervention introduces a safer navigation path.
"""

from ..models import StructuralGraph
from ..nexah_kernel import NexahKernel


# --------------------------------------------------
# Define system graph
# --------------------------------------------------

graph = StructuralGraph(
    nodes={
        "Start": {},
        "SafeA": {},
        "RiskZone": {},
        "SafeB": {},
        "Goal": {},
    },
    edges=[
        ("Start", "SafeA"),
        ("SafeA", "RiskZone"),
        ("RiskZone", "Goal"),
        ("Start", "SafeB"),
        ("SafeB", "Goal"),
    ],
    weights={}
)


# --------------------------------------------------
# Define regime landscape
# --------------------------------------------------

landscape = {
    "attractors": ["Goal"],
    "basins": {
        "stable": ["SafeA", "SafeB", "Goal"],
        "risky": ["RiskZone"]
    },
    "thresholds": ["RiskZone"]
}


kernel = NexahKernel(graph, landscape)


# --------------------------------------------------
# Analyze navigation
# --------------------------------------------------

analysis = kernel.analyze_system()

print("\nRisk Navigation Analysis\n")

print("Possible trajectories:")
print(analysis.trajectories)


# --------------------------------------------------
# Highlight risk zone
# --------------------------------------------------

print("\nRisk zone detected at node: RiskZone\n")


# --------------------------------------------------
# Structural intervention
# --------------------------------------------------

print("Creating safer bypass: SafeA -> SafeB\n")

intervention = {
    "type": "add_edge",
    "edge": ("SafeA", "SafeB")
}

safer_graph = kernel.simulate_action(intervention)

print("System after risk mitigation:")
print(safer_graph)
