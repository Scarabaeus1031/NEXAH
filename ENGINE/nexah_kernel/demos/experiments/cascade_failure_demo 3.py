"""
Cascade Failure Demo

This example illustrates how local failures can propagate
through a network and how structural intervention can
stabilize the system.

The example models a small infrastructure network.
"""

from ..models import StructuralGraph
from ..nexah_kernel import NexahKernel


# --------------------------------------------------
# Define network
# --------------------------------------------------

graph = StructuralGraph(
    nodes={
        "PowerPlant": {},
        "SubstationA": {},
        "SubstationB": {},
        "City": {},
        "Hospital": {},
    },
    edges=[
        ("PowerPlant", "SubstationA"),
        ("PowerPlant", "SubstationB"),
        ("SubstationA", "City"),
        ("SubstationB", "City"),
        ("City", "Hospital"),
    ],
    weights={}
)


# --------------------------------------------------
# Define regime landscape
# --------------------------------------------------

landscape = {
    "attractors": ["Hospital"],
    "basins": {
        "stable": ["City", "Hospital"],
        "fragile": ["SubstationA", "SubstationB"],
    },
    "thresholds": ["PowerPlant"]
}


kernel = NexahKernel(graph, landscape)


# --------------------------------------------------
# Analyze navigation
# --------------------------------------------------

analysis = kernel.analyze_system()

print("\nCascade Failure Analysis\n")
print("Navigation trajectories:")
print(analysis.trajectories)


# --------------------------------------------------
# Simulate node failure
# --------------------------------------------------

print("\nSimulating failure: PowerPlant\n")

failure_action = {
    "type": "remove_node",
    "node": "PowerPlant"
}

failed_graph = kernel.simulate_action(failure_action)

print("Network after failure:")
print(failed_graph)


# --------------------------------------------------
# Add redundancy intervention
# --------------------------------------------------

print("\nAdding redundancy: SubstationA -> Hospital\n")

intervention = {
    "type": "add_edge",
    "edge": ("SubstationA", "Hospital")
}

stabilized_graph = kernel.simulate_action(intervention)

print("Network after intervention:")
print(stabilized_graph)
