"""
NEXAH Demo — Maze Navigation

A simple maze navigation example using the NEXAH kernel.
"""

from ENGINE.nexah_kernel import StructuralGraph
from ENGINE.nexah_kernel import NexahKernel


# --------------------------------------------------
# Define a simple maze graph
# --------------------------------------------------

maze_graph = StructuralGraph(
    nodes={
        "start": {},
        "A": {},
        "B": {},
        "C": {},
        "goal": {},
    },
    edges=[
        ("start", "A"),
        ("A", "B"),
        ("B", "goal"),
        ("A", "C"),
        ("C", "goal"),
    ],
    weights={}
)


# --------------------------------------------------
# Define regime landscape
# --------------------------------------------------

landscape_data = {
    "attractors": ["goal"],
    "basins": {
        "stable": ["C", "goal"],
        "unstable": ["start"]
    },
    "thresholds": ["B"]
}


# --------------------------------------------------
# Initialize kernel
# --------------------------------------------------

kernel = NexahKernel(maze_graph, landscape_data)


# --------------------------------------------------
# Analyze navigation
# --------------------------------------------------

result = kernel.analyze_system()


print("\nNEXAH Maze Navigation\n")

print("Possible trajectories:")
print(result.trajectories)


# --------------------------------------------------
# Simulate structural change
# --------------------------------------------------

action = {
    "type": "add_edge",
    "edge": ("start", "goal")
}

modified = kernel.simulate_action(action)

print("\nAfter structural intervention:")
print(modified)
