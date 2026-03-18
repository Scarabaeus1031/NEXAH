"""
NEXAH Demo — Minimal Navigation Example

This demo shows how the NEXAH kernel can analyze a small system
and compute possible navigation trajectories.

The example system is a simple structural graph.
"""

from .models import StructuralGraph
from .nexah_kernel import NexahKernel


# --------------------------------------------------
# Define a small system graph
# --------------------------------------------------

graph = StructuralGraph(
    nodes={
        "A": {},
        "B": {},
        "C": {},
        "D": {},
    },
    edges=[
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
    ],
    weights={}
)


# --------------------------------------------------
# Define regime landscape
# --------------------------------------------------

landscape_data = {
    "attractors": ["D"],
    "basins": {
        "stable": ["C", "D"],
        "unstable": ["A"]
    },
    "thresholds": ["B"]
}


# --------------------------------------------------
# Initialize NEXAH kernel
# --------------------------------------------------

kernel = NexahKernel(graph, landscape_data)


# --------------------------------------------------
# Analyze system navigation
# --------------------------------------------------

result = kernel.analyze_system()


print("\nNEXAH Navigation Analysis\n")

print("Trajectories:")
print(result.trajectories)

print("\nLeverage Points:")
print(result.leverage_points)
