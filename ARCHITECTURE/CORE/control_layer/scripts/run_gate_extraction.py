# ARCHITECTURE/CORE/control_layer/scripts/run_gate_extraction.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
import os

print("⚡ NEXAH Gate Extraction")


# --------------------------------
# Config
# --------------------------------
INPUT_PATH = "ARCHITECTURE/CORE/control_layer/outputs/demo/separatrix_points.npy"
OUTPUT_PATH = "ARCHITECTURE/CORE/control_layer/outputs/demo/"
N_GATES = 6


# --------------------------------
# Safety check
# --------------------------------
if not os.path.exists(INPUT_PATH):
    raise FileNotFoundError(
        "❌ separatrix_points.npy fehlt.\n"
        "→ bitte zuerst run_separatrix_extraction.py ausführen"
    )


# --------------------------------
# Load data
# --------------------------------
data = np.load(INPUT_PATH)

# falls mehr als 2 dims → nur x,y
points = data[:, :2]


# --------------------------------
# Vector field (gleich wie vorher)
# --------------------------------
def field(x, y):
    dx = y - 0.3 * x - x * (x**2 + y**2)
    dy = -x - 0.3 * y - y * (x**2 + y**2)
    return np.array([dx, dy])


# --------------------------------
# KD-Tree für lokale Struktur
# --------------------------------
tree = cKDTree(points)


def local_density(p, k=10):
    d, _ = tree.query(p, k=k)
    return np.mean(d)


def flow_alignment(p, target=np.array([0.0, 0.0])):
    f = field(p[0], p[1])
    direction = target - p

    return np.dot(f, direction) / (
        np.linalg.norm(f) * np.linalg.norm(direction) + 1e-6
    )


def curvature_estimate(p, k=6):
    d, idx = tree.query(p, k=k)
    neighbors = points[idx]

    cov = np.cov(neighbors.T)
    eigvals = np.linalg.eigvals(cov)

    return np.min(eigvals) / (np.max(eigvals) + 1e-6)


# --------------------------------
# Gate scoring
# --------------------------------
scores = []

for p in points:
    density = local_density(p)
    align = flow_alignment(p)
    curv = curvature_estimate(p)

    score = (
        1.0 / (density + 1e-3)   # sparse = sharper boundary
        + 2.0 * align            # flow Richtung Zentrum
        - 1.5 * curv             # vermeide chaotische Bereiche
    )

    scores.append(score)

scores = np.array(scores)


# --------------------------------
# Best Gates auswählen
# --------------------------------
idx = np.argsort(scores)[-N_GATES:]
gates = points[idx]


# --------------------------------
# Save
# --------------------------------
os.makedirs(OUTPUT_PATH, exist_ok=True)

np.save(
    os.path.join(OUTPUT_PATH, "gate_points.npy"),
    gates
)


# --------------------------------
# Plot
# --------------------------------
plt.figure(figsize=(8, 8))

# Field Hintergrund
xx, yy = np.meshgrid(
    np.linspace(-2, 2, 60),
    np.linspace(-2, 2, 60)
)

u, v = field(xx, yy)
plt.streamplot(xx, yy, u, v, color="black", density=1.2)


# Separatrix
plt.scatter(
    points[:, 0],
    points[:, 1],
    s=20,
    color="black",
    alpha=0.5,
    label="separatrix"
)


# Gates
plt.scatter(
    gates[:, 0],
    gates[:, 1],
    s=140,
    color="magenta",
    edgecolor="white",
    label="gates"
)


# Zentrum
plt.scatter(
    0, 0,
    s=180,
    color="yellow",
    edgecolor="black",
    label="core"
)


plt.title("NEXAH Gate Extraction")
plt.legend()
plt.grid(True)

plt.savefig(
    os.path.join(OUTPUT_PATH, "nexah_gate_extraction.png"),
    dpi=150
)

print(f"✔ Saved → {OUTPUT_PATH}nexah_gate_extraction.png")
print("✔ Gate Points:\n", gates)


# --------------------------------
# Interpretation
# --------------------------------
print("\n🧠 Interpretation:\n")
print("Magenta points = extracted transition gates")
print("→ lie on separatrix")
print("→ align with flow toward stable region")
print("→ represent optimal entry points between basins")
