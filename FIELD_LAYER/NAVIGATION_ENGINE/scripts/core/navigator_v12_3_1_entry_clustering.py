import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

PLOT_PATH = "FIELD_LAYER/outputs/plots/v12_3_1_entry_clustering.png"

# DBSCAN Parameter (sehr wichtig zum Spielen)
EPS = 1.5       # Radius für Cluster
MIN_SAMPLES = 2 # Mindestpunkte pro Cluster

# --------------------------------------------------
# DATA (ersetze später mit echten Entry Points)
# --------------------------------------------------

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
# CLUSTERING
# --------------------------------------------------

clustering = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit(entry_points)
labels = clustering.labels_

unique_labels = set(labels)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_facecolor("#2b0040")

colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))

for label, color in zip(unique_labels, colors):
    mask = labels == label
    points = entry_points[mask]

    if label == -1:
        # Noise (keine Gruppe)
        ax.scatter(points[:, 0], points[:, 1],
                   c="gray", s=80, label="noise")
    else:
        ax.scatter(points[:, 0], points[:, 1],
                   c=[color], s=100, label=f"cluster {label}")

        # Cluster-Zentrum
        center = points.mean(axis=0)
        ax.scatter(center[0], center[1],
                   c=[color], s=200, edgecolor="white", marker="X")

        # Verbindungslinien (visualisiert "Funnel")
        for p in points:
            ax.plot([p[0], center[0]], [p[1], center[1]],
                    color=color, alpha=0.5)

# Layout
ax.set_title("V12.3.1 Entry Clustering (Funnel Detection)")
ax.set_xlabel("α")
ax.set_ylabel("β")
ax.legend()

plt.tight_layout()
plt.savefig(PLOT_PATH, dpi=200)
print(f"Saved: {PLOT_PATH}")

# --------------------------------------------------
# DEBUG OUTPUT
# --------------------------------------------------

print("\nEntry Clusters:")
for label in unique_labels:
    if label == -1:
        continue
    cluster_points = entry_points[labels == label]
    print(f"  Cluster {label}: {len(cluster_points)} points")
    print(cluster_points)
