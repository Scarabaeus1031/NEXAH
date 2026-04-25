# V31 — Shape Extraction (Clusters + Triangulation + IOTA)

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from sklearn.cluster import DBSCAN
import os

# =========================
# LOAD DATA (fallback)
# =========================
data_path = "NEXAH_CORE/outputs/ieee_gates/v28_data.npz"

if os.path.exists(data_path):
    print("Loading V28 data...")
    data = np.load(data_path)
    theta = data["theta"]
    r_vals = data["r"]
else:
    print("No data found → using test data")

    np.random.seed(0)
    N = 1000
    theta = np.linspace(0, 300, N)
    r_vals = 0.5 + 0.5 * np.sin(theta * 0.2)
    transition = 600
    r_vals[transition:] += np.random.normal(0, 0.5, N - transition)

N = len(theta)

# =========================
# DERIVATIVES → IOTA
# =========================
dr_dtheta = np.gradient(r_vals) / np.gradient(theta)
IOTA_THRESHOLD = np.percentile(np.abs(dr_dtheta), 98)
iota_indices = np.where(np.abs(dr_dtheta) > IOTA_THRESHOLD)[0]

# =========================
# CLUSTERING (DBSCAN)
# =========================
X = np.column_stack((theta, r_vals))

# wichtig: eps anpassen je nach Skalierung
clustering = DBSCAN(eps=5, min_samples=10).fit(X)
labels = clustering.labels_

# =========================
# TRIANGULATION (nur stabile Region optional)
# =========================
tri = Delaunay(X)

# =========================
# VISUALIZATION
# =========================
plt.figure(figsize=(12, 6))

# all points
plt.scatter(theta, r_vals, s=5, c="lightgrey", alpha=0.5)

# clusters
unique_labels = set(labels)
colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))

for lab, col in zip(unique_labels, colors):
    if lab == -1:
        continue  # noise skip

    mask = labels == lab
    plt.scatter(
        theta[mask],
        r_vals[mask],
        s=10,
        color=col,
        label=f"cluster {lab}"
    )

# triangulation lines (subsample für clarity)
for simplex in tri.simplices[::20]:
    plt.plot(
        theta[simplex],
        r_vals[simplex],
        color="black",
        alpha=0.1
    )

# IOTA events
plt.scatter(
    theta[iota_indices],
    r_vals[iota_indices],
    c="red",
    s=80,
    label="IOTA"
)

# transition line
plt.axvline(x=120, linestyle="--", color="black", label="transition")

plt.xlabel("theta")
plt.ylabel("r")
plt.title("V31 — Shape Extraction (Clusters + Triangulation)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig("v31_shape_extraction.png", dpi=150)
plt.show()

# =========================
# OUTPUT
# =========================
print("\n--- V31 RESULTS ---")
print(f"Total clusters (excl noise): {len(unique_labels) - (1 if -1 in labels else 0)}")
print(f"IOTA events: {len(iota_indices)}")
