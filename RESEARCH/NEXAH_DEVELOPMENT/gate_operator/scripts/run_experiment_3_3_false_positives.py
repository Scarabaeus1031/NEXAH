"""
NEXAH Experiment 3.3 — False Positive Analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

G_values = np.load("../output_results/experiment_3_2_G_values.npy")
transition_indices = np.load("../output_results/experiment_3_2_transitions.npy")

# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------

THRESHOLD = 0.7
WINDOW = 50

# ------------------------------------------------------------
# DETECT HIGH G EVENTS
# ------------------------------------------------------------

peaks, _ = find_peaks(G_values, height=THRESHOLD, distance=20)

# ------------------------------------------------------------
# MATCH EVENTS
# ------------------------------------------------------------

TP = []
FP = []
FN = []

used_transitions = set()

for p in peaks:
    match = False
    for t in transition_indices:
        if abs(p - t) < WINDOW:
            TP.append(p)
            used_transitions.add(t)
            match = True
            break
    if not match:
        FP.append(p)

for t in transition_indices:
    if t not in used_transitions:
        FN.append(t)

# ------------------------------------------------------------
# METRICS
# ------------------------------------------------------------

precision = len(TP) / (len(TP) + len(FP) + 1e-9)
recall = len(TP) / (len(TP) + len(FN) + 1e-9)

print("\n---- Experiment 3.3 Results ----")
print(f"TP: {len(TP)}")
print(f"FP: {len(FP)}")
print(f"FN: {len(FN)}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")

# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------

plt.figure(figsize=(16, 5))

plt.plot(G_values, label="G(x)", alpha=0.8)

plt.scatter(TP, G_values[TP], color="green", label="TP", zorder=3)
plt.scatter(FP, G_values[FP], color="red", label="FP", zorder=3)
plt.scatter(FN, G_values[FN], color="orange", label="FN", zorder=3)

plt.scatter(
    transition_indices,
    G_values[transition_indices],
    color="black",
    label="Transitions",
    s=20
)

plt.axhline(THRESHOLD, linestyle="--")

plt.title("Experiment 3.3 — False Positive Analysis")
plt.xlabel("Time")
plt.ylabel("G(x)")
plt.legend()

plt.tight_layout()

plt.savefig(
    "../output_results/experiment_3_3_false_positive_analysis.png",
    dpi=300
)

plt.show()
