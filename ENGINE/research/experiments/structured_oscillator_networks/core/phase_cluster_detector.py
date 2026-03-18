import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

PHASE_FILE = "output/phase_history.npy"
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

N_INNER = 16
N_MIDDLE = 32

PHASE_THRESHOLD = 0.60
SMOOTH_WINDOW = 80


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def wrap_angle(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def moving_average(x, window):
    if window <= 1:
        return x.copy()

    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode="same")


def count_phase_clusters(theta, threshold=0.60):

    """
    Count clusters on circular phase space
    """

    phases = wrap_angle(theta)

    # sort phases
    phases_sorted = np.sort(phases)

    diffs = np.diff(phases_sorted)

    clusters = 1

    for d in diffs:
        if abs(d) > threshold:
            clusters += 1

    # wrap gap
    wrap_gap = abs((phases_sorted[0] + 2*np.pi) - phases_sorted[-1])

    if wrap_gap > threshold:
        clusters += 1

    return clusters


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

history = np.load(PHASE_FILE)

steps, nodes = history.shape

N_OUTER = nodes - N_INNER - N_MIDDLE


inner = history[:, :N_INNER]
middle = history[:, N_INNER:N_INNER + N_MIDDLE]
outer = history[:, N_INNER + N_MIDDLE:]


# ---------------------------------------------------------
# CLUSTER DETECTION
# ---------------------------------------------------------

cluster_counts = []
cluster_inner = []
cluster_middle = []
cluster_outer = []

for t in range(steps):

    theta = history[t]

    cluster_counts.append(
        count_phase_clusters(theta, PHASE_THRESHOLD)
    )

    cluster_inner.append(
        count_phase_clusters(inner[t], PHASE_THRESHOLD)
    )

    cluster_middle.append(
        count_phase_clusters(middle[t], PHASE_THRESHOLD)
    )

    cluster_outer.append(
        count_phase_clusters(outer[t], PHASE_THRESHOLD)
    )


cluster_counts = np.array(cluster_counts)
cluster_inner = np.array(cluster_inner)
cluster_middle = np.array(cluster_middle)
cluster_outer = np.array(cluster_outer)


cluster_counts_s = moving_average(cluster_counts, SMOOTH_WINDOW)


# ---------------------------------------------------------
# PLOT 1: GLOBAL CLUSTERS
# ---------------------------------------------------------

plt.figure(figsize=(10,4))

plt.plot(cluster_counts_s)

plt.xlabel("time")
plt.ylabel("cluster count")

plt.title("Global Phase Clusters")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "phase_cluster_count.png")

plt.close()


# ---------------------------------------------------------
# PLOT 2: LAYER CLUSTERS
# ---------------------------------------------------------

plt.figure(figsize=(10,4))

plt.plot(moving_average(cluster_inner, SMOOTH_WINDOW), label="inner")
plt.plot(moving_average(cluster_middle, SMOOTH_WINDOW), label="middle")
plt.plot(moving_average(cluster_outer, SMOOTH_WINDOW), label="outer")

plt.legend()

plt.xlabel("time")
plt.ylabel("clusters")

plt.title("Layer Phase Clusters")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "layer_phase_clusters.png")

plt.close()


# ---------------------------------------------------------
# PLOT 3: PHASE SNAPSHOT MAP
# ---------------------------------------------------------

plt.figure(figsize=(8,6))

plt.imshow(history.T, aspect="auto", cmap="twilight", origin="lower")

plt.colorbar(label="phase")

plt.xlabel("time")
plt.ylabel("node")

plt.title("Phase Evolution Map")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "phase_evolution_map.png")

plt.close()


# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

with open(OUTPUT_DIR / "phase_cluster_report.txt", "w") as f:

    f.write("Phase Cluster Report\n")
    f.write("====================\n\n")

    f.write(f"nodes: {nodes}\n")
    f.write(f"timesteps: {steps}\n\n")

    f.write("Global clusters\n")
    f.write("----------------\n")

    f.write(f"mean: {cluster_counts.mean():.2f}\n")
    f.write(f"max : {cluster_counts.max()}\n")
    f.write(f"min : {cluster_counts.min()}\n\n")

    f.write("Layer means\n")
    f.write("-----------\n")

    f.write(f"inner  : {cluster_inner.mean():.2f}\n")
    f.write(f"middle : {cluster_middle.mean():.2f}\n")
    f.write(f"outer  : {cluster_outer.mean():.2f}\n")


print("Phase cluster detection complete.")
