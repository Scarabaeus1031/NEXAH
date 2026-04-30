"""
NEXAH Experiment 3.3 — False Positive Analysis

Goal:
Evaluate how often high G(x) indicates a transition vs false alarm.

Output:
- Precision / Recall metrics
- Visualization of TP / FP / FN
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# ------------------------------------------------------------
# LOAD DATA (adapt if needed)
# ------------------------------------------------------------

# assume you already have:
# G_values (array)
# transition_indices (list of ints)

# Example placeholders:
# G_values = np.load("G_values.npy")
# transition_indices = np.load("transitions.npy")

# ------------------------------------------------------------
# PARAMETERS
# ------------------------------------------------------------

THRESHOLD = 0.7       # what is "high G"
WINDOW = 50           # time window for matching

# ------------------------------------------------------------
# DETECT HIGH G EVENTS
# ------------------------------------------------------------

high_g_indices = np.where(G_values > THRESHOLD)[0]

# compress to peaks (avoid duplicates)
peaks, _ = find_peaks(G_values, height=THRESHOLD, distance=20)

# ------------------------------------------------------------
# MATCH EVENTS
# ------------------------------------------------------------

TP = []  # true positives
FP = []  # false positives
FN = []  # missed transitions

used_transitions = set()

# classify peaks
for p in peaks:
    found_match = False
    
    for t in transition_indices:
        if abs(p - t) < WINDOW:
            TP.append(p)
            used_transitions.add(t)
            found_match = True
            break
    
    if not found_match:
        FP.append(p)

# find missed transitions
for t in transition_indices:
    if t not in used_transitions:
        FN.append(t)

# ------------------------------------------------------------
# METRICS
# ------------------------------------------------------------

precision = len(TP) / (len(TP) + len(FP) + 1e-9)
recall = len(TP) / (len(TP) + len(FN) + 1e-9)

print("---- Experiment 3.3 Results ----")
print(f"TP: {len(TP)}")
print(f"FP: {len(FP)}")
print(f"FN: {len(FN)}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")

# ------------------------------------------------------------
# VISUALIZATION
# ------------------------------------------------------------

plt.figure(figsize=(16, 5))

plt.plot(G_values, label="G(x)", color="blue", alpha=0.8)

# true positives
plt.scatter(TP, G_values[TP], color="green", label="TP", zorder=3)

# false positives
plt.scatter(FP, G_values[FP], color="red", label="FP", zorder=3)

# missed transitions
plt.scatter(FN, G_values[FN], color="orange", label="FN", zorder=3)

# ground truth transitions
plt.scatter(transition_indices, G_values[transition_indices],
            color="black", label="Transitions", s=20)

plt.axhline(THRESHOLD, linestyle="--", color="gray")

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
