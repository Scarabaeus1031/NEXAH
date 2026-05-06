# NEXAH_CORE/scripts/ieee_gate_detection_v13_sheets.py
#
# v13: Sheet Reconstruction in Phase Space
#
# Goal:
# Identify multiple local flow directions ("sheets")
# and detect intersections → gate regions

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

np.random.seed(42)

OUTPUT_PATH = "NEXAH_CORE/outputs/ieee_gates/ieee_gate_detection_v13_sheets.png"


# --------------------------------------------------
# SIGNAL
# --------------------------------------------------
def generate_signal(t):
    x = np.zeros_like(t)

    for i, ti in enumerate(t):
        if ti < 30:
            x[i] = 0.3 * np.sin(0.5 * ti)

        elif ti < 75:
            x[i] = (1 + 0.02 * ti) * np.sin(1.5 * ti)

        else:
            x[i] = np.random.normal(0, 1.0)

    return x


# --------------------------------------------------
# MAIN
# --------------------------------------------------
t = np.linspace(0, 100, 1000)
x = generate_signal(t)
dx = np.gradient(x, t)

# phase space
X = np.column_stack([x, dx])

# --------------------------------------------------
# CLUSTER LOCAL DYNAMICS
# --------------------------------------------------
n_clusters = 4
kmeans = KMeans(n_clusters=n_clusters, n_init=10)
labels = kmeans.fit_predict(X)

centers = kmeans.cluster_centers_

# --------------------------------------------------
# COMPUTE LOCAL FLOW (direction vectors)
# --------------------------------------------------
flow_vectors = []

for k in range(n_clusters):
    mask = labels == k

    # mean derivative direction
    mean_dx = np.mean(dx[mask])
    mean_ddx = np.mean(np.gradient(dx[mask])) if np.sum(mask) > 5 else 0

    flow_vectors.append((centers[k], np.array([mean_dx, mean_ddx])))

# --------------------------------------------------
# DETECT SHEET INTERSECTIONS
# --------------------------------------------------
intersection_points = []

for i in range(n_clusters):
    for j in range(i + 1, n_clusters):
        c1, v1 = flow_vectors[i]
        c2, v2 = flow_vectors[j]

        # angle between flows
        dot = np.dot(v1, v2)
        norm = np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-12
        angle = np.arccos(np.clip(dot / norm, -1, 1))

        # if directions strongly differ → potential crossing
        if angle > np.pi / 4:
            midpoint = (c1 + c2) / 2
            intersection_points.append(midpoint)

intersection_points = np.array(intersection_points) if len(intersection_points) > 0 else np.zeros((0,2))

# --------------------------------------------------
# PLOT
# --------------------------------------------------
plt.figure(figsize=(8, 8))

# full trajectory
plt.plot(x, dx, color="lightgray", alpha=0.5, label="trajectory")

# clusters
colors = ["red", "green", "blue", "orange", "purple"]

for k in range(n_clusters):
    mask = labels == k
    plt.scatter(
        x[mask],
        dx[mask],
        s=10,
        color=colors[k % len(colors)],
        alpha=0.6,
        label=f"sheet {k}"
    )

# flow vectors
for center, vec in flow_vectors:
    plt.arrow(
        center[0], center[1],
        vec[0]*0.5, vec[1]*0.5,
        color="black",
        head_width=0.1,
        length_includes_head=True
    )

# intersections
if len(intersection_points) > 0:
    plt.scatter(
        intersection_points[:,0],
        intersection_points[:,1],
        color="yellow",
        s=120,
        edgecolors="black",
        label="sheet intersections (gates)"
    )

plt.xlabel("x(t)")
plt.ylabel("dx/dt")
plt.title("v13 — Sheet Reconstruction in Phase Space")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=150)

print("\n--- NEXAH IEEE Gate Detection v13 ---")
print(f"Clusters (sheets): {n_clusters}")
print(f"Detected intersections: {len(intersection_points)}")
print(f"Saved to: {OUTPUT_PATH}")

plt.show()
