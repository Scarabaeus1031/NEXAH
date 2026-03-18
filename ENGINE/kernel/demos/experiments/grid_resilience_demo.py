"""
NEXAH Demo — Grid Resilience

A simple infrastructure-style network example showing how
NEXAH can analyze structural systems and simulate interventions.
"""

from ENGINE.nexah_kernel import StructuralGraph
from ENGINE.nexah_kernel import NexahKernel


# --------------------------------------------------
# Define grid network
# --------------------------------------------------

grid = StructuralGraph(
    nodes={
        "A": {},
        "B": {},
        "C": {},
        "D": {},
        "E": {},
    },
    edges=[
        ("A","B"),
        ("B","C"),
        ("A","D"),
        ("D","E"),
        ("E","C"),
    ],
    weights={}
)


# --------------------------------------------------
# Define regime landscape
# --------------------------------------------------

landscape = {
    "attractors": ["C"],
    "basins": {
        "stable": ["B","D","E","C"],
        "unstable": ["A"]
    },
    "thresholds": ["B"]
}


# --------------------------------------------------
# Initialize kernel
# --------------------------------------------------

kernel = NexahKernel(grid, landscape)


# --------------------------------------------------
# Analyze system
# --------------------------------------------------

analysis = kernel.analyze_system()

print("\nNEXAH Grid Resilience Analysis\n")

print("Navigation trajectories:")
print(analysis.trajectories)


# --------------------------------------------------
# Simulate failure
# --------------------------------------------------

print("\nSimulating node failure: B")

failure_action = {
    "type": "remove_node",
    "node": "B"
}

failed_grid = kernel.simulate_action(failure_action)

print("Grid after failure:")
print(failed_grid)


# --------------------------------------------------
# Simulate resilience intervention
# --------------------------------------------------

print("\nAdding redundancy link: A -> C")

repair_action = {
    "type": "add_edge",
    "edge": ("A","C")
}

repaired_grid = kernel.simulate_action(repair_action)

print("Grid after intervention:")
print(repaired_grid)
