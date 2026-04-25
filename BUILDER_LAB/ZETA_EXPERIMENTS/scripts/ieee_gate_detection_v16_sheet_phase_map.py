# BUILDER_LAB/ZETA_EXPERIMENTS/scripts/ieee_gate_detection_v16_sheet_phase_map.py
#
# v16 — Sheet → Phase Mapping + Transition Matrix
#
# Goal:
# 1. Map sheets into (r, θ) phase space
# 2. Identify stable regions
# 3. Compute transition probabilities between sheets

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

np.random.seed(42)

OUTPUT_PHASE = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/ieee_gate_detection_v16_phase_map.png"
OUTPUT_TRANS = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/ieee_gate_detection_v16_transition_matrix.png"


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

# phase + radius
theta = np.arctan2(dx, x)
r = np.sqrt(x**2 + dx**2)

# flow direction (for sheet classification)
angle = np.arctan2(np.gradient(dx), np.gradient(x))

# --------------------------------------------------
# SHEET CLASSIFICATION (flow sectors)
# --------------------------------------------------
num_sheets = 6
sheet_ids = ((angle + np.pi) / (2 * np.pi) * num_sheets).astype(int)
sheet_ids = np.clip(sheet_ids, 0, num_sheets - 1)

# --------------------------------------------------
# PHASE SPACE MAP
# --------------------------------------------------
plt.figure(figsize=(8, 6))

for s in range(num_sheets):
    mask = sheet_ids == s
    plt.scatter(theta[mask], r[mask], s=5, label=f"sheet {s}", alpha=0.6)

plt.xlabel("θ (phase)")
plt.ylabel("r (radius)")
plt.title("v16 — Sheet Regions in (r, θ)")
plt.legend(markerscale=3)
plt.tight_layout()
plt.savefig(OUTPUT_PHASE, dpi=150)


# --------------------------------------------------
# TRANSITION MATRIX
# --------------------------------------------------
transitions = np.zeros((num_sheets, num_sheets))

for i in range(len(sheet_ids) - 1):
    a = sheet_ids[i]
    b = sheet_ids[i + 1]
    transitions[a, b] += 1

# normalize
row_sums = transitions.sum(axis=1, keepdims=True)
row_sums[row_sums == 0] = 1
P = transitions / row_sums


# --------------------------------------------------
# PLOT MATRIX
# --------------------------------------------------
plt.figure(figsize=(6, 5))
plt.imshow(P, cmap="viridis")
plt.colorbar(label="Transition Probability")

plt.xlabel("Next Sheet")
plt.ylabel("Current Sheet")
plt.title("v16 — Sheet Transition Matrix")

for i in range(num_sheets):
    for j in range(num_sheets):
        val = P[i, j]
        if val > 0.05:
            plt.text(j, i, f"{val:.2f}", ha='center', va='center', color='white', fontsize=8)

plt.tight_layout()
plt.savefig(OUTPUT_TRANS, dpi=150)


# --------------------------------------------------
# STATS
# --------------------------------------------------
unique, counts = np.unique(sheet_ids, return_counts=True)

print("\n--- NEXAH IEEE Gate Detection v16 ---")
print("Sheet occupancy:")
for u, c in zip(unique, counts):
    print(f"Sheet {u}: {c}")

print("\nTransition matrix (rows sum to 1):")
print(np.round(P, 3))

plt.show()
