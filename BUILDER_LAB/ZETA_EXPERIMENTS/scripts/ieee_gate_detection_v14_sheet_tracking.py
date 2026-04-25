# BUILDER_LAB/ZETA_EXPERIMENTS/scripts/ieee_gate_detection_v14_sheet_tracking.py
#
# v14: Sheet Tracking + Mode Switching
#
# Goal:
# Track which "sheet" the system is on over time
# Detect transitions BETWEEN sheets (mode switching)
#

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

np.random.seed(42)

OUTPUT_PATH = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/ieee_gate_detection_v14_sheet_tracking.png"


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

# Phase space
points = np.column_stack((x, dx))

# --------------------------------------------------
# CLUSTER → SHEETS
# --------------------------------------------------
n_sheets = 4
kmeans = KMeans(n_clusters=n_sheets, random_state=42)
labels = kmeans.fit_predict(points)

# --------------------------------------------------
# TRACK SHEET OVER TIME
# --------------------------------------------------
sheet_over_time = labels

# detect transitions
transitions = np.zeros_like(sheet_over_time)
for i in range(1, len(sheet_over_time)):
    if sheet_over_time[i] != sheet_over_time[i - 1]:
        transitions[i] = 1

transition_indices = np.where(transitions == 1)[0]


# --------------------------------------------------
# PLOT 1: Phase Space + Sheets
# --------------------------------------------------
plt.figure(figsize=(10, 8))

colors = ["red", "green", "blue", "orange"]

for i in range(n_sheets):
    mask = labels == i
    plt.scatter(x[mask], dx[mask], s=10, color=colors[i], label=f"sheet {i}", alpha=0.6)

plt.plot(x, dx, color="gray", alpha=0.2, label="trajectory")

# highlight transitions
plt.scatter(
    x[transition_indices],
    dx[transition_indices],
    s=60,
    color="yellow",
    edgecolor="black",
    label="sheet switches"
)

plt.xlabel("x(t)")
plt.ylabel("dx/dt")
plt.title("v14 — Sheet Structure + Switching Points")
plt.legend()
plt.grid(True)


# --------------------------------------------------
# PLOT 2: Sheet Index over Time
# --------------------------------------------------
plt.figure(figsize=(10, 4))

plt.plot(t, sheet_over_time, color="black", linewidth=1)
plt.scatter(
    t[transition_indices],
    sheet_over_time[transition_indices],
    color="red",
    label="switch"
)

plt.xlabel("time")
plt.ylabel("sheet index")
plt.title("v14 — Sheet Tracking over Time")
plt.legend()
plt.grid(True)


# --------------------------------------------------
# PLOT 3: Switching Density
# --------------------------------------------------
window = 20
switch_density = np.convolve(transitions, np.ones(window)/window, mode='same')

plt.figure(figsize=(10, 4))
plt.plot(t, switch_density, color="purple")
plt.title("v14 — Switching Density (mode switching intensity)")
plt.xlabel("time")
plt.ylabel("density")
plt.grid(True)


# --------------------------------------------------
# SAVE
# --------------------------------------------------
plt.savefig(OUTPUT_PATH, dpi=150)

print("\n--- NEXAH IEEE Gate Detection v14 ---")
print(f"Total switches: {len(transition_indices)}")
print(f"Saved to: {OUTPUT_PATH}")

plt.show()
