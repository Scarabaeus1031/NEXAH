"""
NEXAH Kernel Test

Minimal sanity test for the NEXAH kernel.
"""

from ENGINE.nexah_kernel import StructuralGraph
from ENGINE.nexah_kernel import NexahKernel


# --------------------------------------------------
# Test Graph
# --------------------------------------------------

graph = StructuralGraph(
    nodes={
        "A": {},
        "B": {},
        "C": {},
    },
    edges=[
        ("A", "B"),
        ("B", "C"),
    ],
    weights={}
)


# --------------------------------------------------
# Test Landscape
# --------------------------------------------------

landscape_data = {
    "attractors": ["C"],
    "basins": {
        "stable": ["B", "C"],
        "unstable": ["A"]
    },
    "thresholds": ["B"]
}


# --------------------------------------------------
# Initialize Kernel
# --------------------------------------------------

kernel = NexahKernel(graph, landscape_data)


# --------------------------------------------------
# Navigation Test
# --------------------------------------------------

analysis = kernel.analyze_system()

print("\nNavigation Test")
print("----------------")

print("Trajectories:", analysis.trajectories)
print("Leverage Points:", analysis.leverage_points)


# --------------------------------------------------
# Action Simulation Test
# --------------------------------------------------

action = {
    "type": "add_edge",
    "edge": ("A", "C")
}

modified = kernel.simulate_action(action)

print("\nAction Test")
print("-----------")

print("Modified Graph:", modified)
