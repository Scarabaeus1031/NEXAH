import matplotlib.pyplot as plt
import numpy as np

# --------------------------------
# Experimental results
# --------------------------------

labels = [
    "Ring",
    "Random",
    "Star",
    "Symmetry (5+6+6)"
]

mean_times = [
    100,   # approx from experiments
    29.5,
    1.97,
    1.29
]

std_times = [
    95,
    68,
    0.53,
    0.42
]

# --------------------------------
# Plot
# --------------------------------

x = np.arange(len(labels))

plt.figure(figsize=(8,5))

plt.bar(
    x,
    mean_times,
    yerr=std_times,
    capsize=6
)

plt.xticks(x, labels, rotation=20)

plt.ylabel("Synchronization Time")
plt.title("Kuramoto Synchronization vs Graph Topology")

plt.tight_layout()

plt.savefig("sync_time_vs_topology.png", dpi=300)

print("Saved figure: sync_time_vs_topology.png")

plt.show()
