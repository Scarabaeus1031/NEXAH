import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# V12.4 — Exit → Target Mapping
# ============================================================

print("Running V12.4 Exit Target Mapping...")

# ------------------------------------------------------------
# Load / mock previous data (replace with real loaders if needed)
# ------------------------------------------------------------

# Nodes (example positions — replace with your real nodes)
nodes = np.array([
    [11.0, 26.0], [10.5, 25.5], [12.0, 24.8], [13.0, 26.0],
    [12.0, 23.5], [11.5, 24.0], [10.8, 27.8],
    [9.8, 25.2], [13.5, 25.5], [11.5, 28.5], [10.2, 24.2]
])

# Exit points (replace with actual extracted exits)
exit_points = np.array([
    [14.5, 22.0],
    [13.2, 13.5],
    [16.0, 44.5],
    [12.8, 26.0],
    [11.2, 18.5],
    [9.5, 25.0],
    [10.0, 19.0],
    [12.0, 31.0]
])

# ------------------------------------------------------------
# Map exits → nearest node (target)
# ------------------------------------------------------------

def map_exit_to_node(exit_points, nodes):
    mapping = []
    for i, e in enumerate(exit_points):
        dists = np.linalg.norm(nodes - e, axis=1)
        idx = np.argmin(dists)
        mapping.append((i, idx, dists[idx]))
    return mapping

mapping = map_exit_to_node(exit_points, nodes)

# ------------------------------------------------------------
# Build transition counts (Exit → Node frequency)
# ------------------------------------------------------------

transition_counts = {}

for _, node_idx, _ in mapping:
    transition_counts[node_idx] = transition_counts.get(node_idx, 0) + 1

# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------

plt.figure(figsize=(10, 8))

# Plot nodes
plt.scatter(nodes[:, 0], nodes[:, 1],
            s=300, c='yellow', edgecolor='black', zorder=3)

for i, (x, y) in enumerate(nodes):
    plt.text(x, y, f"N{i}", ha='center', va='center', fontsize=10)

# Plot exits
plt.scatter(exit_points[:, 0], exit_points[:, 1],
            s=80, c='red', label='exit points', zorder=2)

# Draw mapping arrows
for i, node_idx, dist in mapping:
    ex = exit_points[i]
    nd = nodes[node_idx]

    plt.plot([ex[0], nd[0]],
             [ex[1], nd[1]],
             color='cyan', linewidth=2)

# Highlight dominant targets
for node_idx, count in transition_counts.items():
    if count >= 2:  # threshold for dominance
        x, y = nodes[node_idx]
        plt.scatter(x, y, s=600,
                    facecolors='none',
                    edgecolors='white',
                    linewidths=2)

plt.title("V12.4 Exit → Target Mapping")
plt.xlabel("α")
plt.ylabel("β")
plt.legend()

plt.savefig("FIELD_LAYER/outputs/plots/v12_4_exit_target_mapping.png")
plt.close()

# ------------------------------------------------------------
# Print results
# ------------------------------------------------------------

print("\nExit → Target Mapping:")
for i, node_idx, dist in mapping:
    print(f"  Exit {i} → Node N{node_idx} | dist={dist:.3f}")

print("\nTarget Frequencies:")
for node_idx, count in sorted(transition_counts.items(), key=lambda x: -x[1]):
    print(f"  Node N{node_idx}: {count} hits")

print("\nSaved: FIELD_LAYER/outputs/plots/v12_4_exit_target_mapping.png")
