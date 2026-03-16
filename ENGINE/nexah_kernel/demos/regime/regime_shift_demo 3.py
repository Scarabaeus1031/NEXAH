"""
Regime Shift Demo

This example illustrates how a system can move across
regime boundaries and how structural intervention can
shift the system into a more stable region.

The demo uses a small abstract network where one node
acts as a regime threshold.
"""

from ..models import StructuralGraph
from ..nexah_kernel import NexahKernel


# --------------------------------------------------
# Define system graph
# --------------------------------------------------

graph = StructuralGraph(
    nodes={
        "Source": {},
        "A": {},
        "B": {},
        "C": {},
        "Sink": {},
    },
    edges=[
        ("Source", "A"),
        ("A", "B"),
        ("B", "C"),
        ("C", "Sink"),
    ],
    weights={}
)


# --------------------------------------------------
# Define regime landscape
# --------------------------------------------------

landscape = {
    "attractors": ["Sink"],
    "basins": {
        "stable": ["C", "Sink"],
        "unstable": ["A"]
    },
    "thresholds": ["B"]
}


kernel = NexahKernel(graph, landscape)


# --------------------------------------------------
# Analyze navigation
# --------------------------------------------------

analysis = kernel.analyze_system()

print("\nRegime Shift Analysis\n")

print("Navigation trajectories:")
print(analysis.trajectories)


# --------------------------------------------------
# Simulate threshold disruption
# --------------------------------------------------

print("\nSimulating threshold disruption at node B\n")

threshold_break = {
    "type": "remove_node",
    "node": "B"
}

broken_graph = kernel.simulate_action(threshold_break)

print("System after regime disruption:")
print(broken_graph)


# --------------------------------------------------
# Structural intervention
# --------------------------------------------------

print("\nCreating alternative path A -> C\n")

intervention = {
    "type": "add_edge",
    "edge": ("A", "C")
}

stabilized_graph = kernel.simulate_action(intervention)

print("System after stabilization intervention:")
print(stabilized_graph)
