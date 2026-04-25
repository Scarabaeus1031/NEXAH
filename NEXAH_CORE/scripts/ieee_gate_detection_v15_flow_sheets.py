# BUILDER_LAB/ZETA_EXPERIMENTS/scripts/ieee_gate_detection_v15_flow_sheets.py
#
# v15: Flow-Based Sheet Definition
#
# Goal:
# Define sheets based on local flow direction (NOT clustering)
#

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

OUTPUT_PATH = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/ieee_gate_detection_v15_flow_sheets.png"


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
ddx = np.gradient(dx, t)

# --------------------------------------------------
# FLOW VECTOR
# --------------------------------------------------
# v = (dx, ddx)
flow = np.column_stack((dx, ddx))

# normalize direction
norms = np.linalg.norm(flow, axis=1, keepdims=True) + 1e-12
flow_unit = flow / norms

# --------------------------------------------------
# SHEET ASSIGNMENT (by direction)
# --------------------------------------------------
# discretize angle
angles = np.arctan2(flow_unit[:, 1], flow_unit[:, 0])

# map angle to bins (like sectors)
n_sectors = 6
bins = np.linspace(-np.pi, np.pi, n_sectors + 1)

sheet_labels = np.digitize(angles, bins) - 1

# fix bounds
sheet_labels[sheet_labels == n_sectors] = n_sectors - 1


# --------------------------------------------------
# SHEET SWITCHING
# --------------------------------------------------
switches = np.zeros_like(sheet_labels)
for i in range(1, len(sheet_labels)):
    if sheet_labels[i] != sheet_labels[i - 1]:
        switches[i] = 1

switch_idx = np.where(switches == 1)[0]


# --------------------------------------------------
# PLOT 1 — Phase Space
# --------------------------------------------------
plt.figure(figsize=(10, 8))

colors = plt.cm.tab10(sheet_labels / np.max(sheet_labels))

plt.scatter(x, dx, c=sheet_labels, cmap='tab10', s=10, alpha=0.6)
plt.plot(x, dx, color="gray", alpha=0.2)

plt.scatter(
    x[switch_idx],
    dx[switch_idx],
    color="black",
    s=40,
    label="switch"
)

plt.xlabel("x")
plt.ylabel("dx/dt")
plt.title("v15 — Flow-Based Sheets (Direction Sectors)")
plt.legend()
plt.grid(True)


# --------------------------------------------------
# PLOT 2 — Sheet over time
# --------------------------------------------------
plt.figure(figsize=(10, 4))

plt.plot(t, sheet_labels, color="black")
plt.scatter(t[switch_idx], sheet_labels[switch_idx], color="red")

plt.xlabel("time")
plt.ylabel("sheet (flow sector)")
plt.title("v15 — Flow Sheet Tracking")
plt.grid(True)


# --------------------------------------------------
# PLOT 3 — Flow Angle
# --------------------------------------------------
plt.figure(figsize=(10, 4))

plt.plot(t, angles, color="purple")
plt.xlabel("time")
plt.ylabel("angle")
plt.title("v15 — Flow Direction Angle")
plt.grid(True)


# --------------------------------------------------
# SAVE
# --------------------------------------------------
plt.savefig(OUTPUT_PATH, dpi=150)

print("\n--- NEXAH IEEE Gate Detection v15 ---")
print(f"Flow sectors: {n_sectors}")
print(f"Total switches: {len(switch_idx)}")
print(f"Saved to: {OUTPUT_PATH}")

plt.show()
