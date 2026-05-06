import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

PLOT_PATH = "FIELD_LAYER/outputs/plots/v12_3_entry_to_cycle_mapping.png"

# --------------------------------------------------
# MOCK / LOAD (hier ersetzt du später mit echten Daten)
# --------------------------------------------------

# Beispiel: Nodes (Cycle-Zentrum rechts)
nodes = np.array([
    [10.5, 25.5], [11.2, 26.3], [12.0, 24.8],
    [13.1, 26.0], [11.8, 23.7], [12.7, 27.2],
    [10.9, 27.8], [9.8, 25.2], [13.5, 25.5],
    [11.5, 28.5], [10.2, 24.3]
])

# Beispiel Entry Points (ersetzen durch echte aus V12.2)
entry_points = np.array([
    [8.5, 22.0],
    [9.2, 27.5],
    [12.5, 31.0],
    [7.5, 18.5],
    [13.0, 13.5],
    [10.8, 26.2],
    [11.3, 25.7],
    [9.9, 24.8]
])

# --------------------------------------------------
# CORE: ENTRY → NODE MAPPING
# --------------------------------------------------

def map_entries_to_nodes(entries, nodes):
    mappings = []

    for i, e in enumerate(entries):
        dists = np.linalg.norm(nodes - e, axis=1)
        nearest_idx = np.argmin(dists)
        mappings.append((i, nearest_idx, dists[nearest_idx]))

    return mappings

mappings = map_entries_to_nodes(entry_points, nodes)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 6))

# Background placeholder (optional: dein Feld reinladen)
ax.set_facecolor("#2b0040")

# Nodes
ax.scatter(nodes[:, 0], nodes[:, 1],
           c="yellow", edgecolor="black", s=200, zorder=3)

for i, (x, y) in enumerate(nodes):
    ax.text(x, y, f"N{i}", fontsize=8, ha='center', va='center')

# Entry points
ax.scatter(entry_points[:, 0], entry_points[:, 1],
           c="green", s=80, zorder=4)

# Draw mapping lines
for entry_idx, node_idx, dist in mappings:
    e = entry_points[entry_idx]
    n = nodes[node_idx]

    ax.plot([e[0], n[0]], [e[1], n[1]],
            color="cyan", linewidth=1.5, alpha=0.7)

# Layout
ax.set_title("V12.3 Entry → Cycle Mapping")
ax.set_xlabel("α")
ax.set_ylabel("β")

plt.tight_layout()
plt.savefig(PLOT_PATH, dpi=200)
print(f"Saved: {PLOT_PATH}")

# --------------------------------------------------
# DEBUG OUTPUT
# --------------------------------------------------

print("\nEntry → Node Mapping:")
for entry_idx, node_idx, dist in mappings:
    print(f"  Entry {entry_idx} → Node N{node_idx} | dist={dist:.3f}")
