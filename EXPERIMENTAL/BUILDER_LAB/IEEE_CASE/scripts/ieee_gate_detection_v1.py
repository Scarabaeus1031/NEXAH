import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# Historical synthetic coherence-threshold prototype
#
# Despite the historical filename, this script does not use an IEEE
# power-system model or the current NEXAH Gate Operator.
#
# Pipeline:
# Synthetic signal → lag-one autocorrelation → threshold candidates
# --------------------------------------------------

np.random.seed(42)

# --------------------------------------------------
# 1. TIME AXIS
# --------------------------------------------------
T = 1000
t = np.linspace(0, 100, T)

# --------------------------------------------------
# 2. SYNTHETIC SYSTEM SIGNAL
# stable → oscillatory → unstable
# --------------------------------------------------
x = np.zeros_like(t)

for i, ti in enumerate(t):
    if ti < 30:
        # stable regime (small noise)
        x[i] = 0.02 * np.sin(2 * np.pi * ti / 5)
    elif ti < 60:
        # transition (growing oscillation)
        amp = (ti - 30) / 30
        x[i] = amp * np.sin(2 * np.pi * ti / 3)
    else:
        # unstable regime
        amp = 1 + 0.5 * np.sin(ti / 5)
        x[i] = amp * np.sin(2 * np.pi * ti / 2) + 0.1 * np.random.randn()

# --------------------------------------------------
# 3. COHERENCE FUNCTION C(t)
# simple local autocorrelation proxy
# --------------------------------------------------
window = 30
C = np.zeros_like(x)

for i in range(window, len(x)):
    segment = x[i - window:i]
    if np.std(segment) > 1e-6:
        # normalized autocorrelation at lag 1
        C[i] = np.corrcoef(segment[:-1], segment[1:])[0, 1]
    else:
        C[i] = 1.0

# smooth slightly
C = np.convolve(C, np.ones(10)/10, mode='same')

# --------------------------------------------------
# 4. LOW-AUTOCORRELATION CANDIDATES
# --------------------------------------------------
epsilon = 0.1

gate_mask = np.abs(C) < epsilon

# cluster gates (avoid duplicates)
gate_indices = []
min_distance = 20

for i in range(len(gate_mask)):
    if gate_mask[i]:
        if len(gate_indices) == 0 or (i - gate_indices[-1]) > min_distance:
            gate_indices.append(i)

gate_times = t[gate_indices]

# --------------------------------------------------
# 5. VISUALIZATION
# --------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# --- LEFT: System Dynamics ---
axes[0].plot(t, x, linewidth=1.2)
axes[0].set_title("System Dynamics")
axes[0].set_xlabel("time")
axes[0].set_ylabel("x(t)")
axes[0].grid(True, alpha=0.3)

# --- CENTER: Coherence ---
axes[1].plot(t, C, linewidth=1.5)
axes[1].axhline(0, linestyle="--", linewidth=1)

# highlight near-zero zone
axes[1].fill_between(
    t, -epsilon, epsilon,
    alpha=0.2
)

axes[1].set_title("Coherence")
axes[1].set_xlabel("time")
axes[1].set_ylabel("C(t)")
axes[1].grid(True, alpha=0.3)

# --- RIGHT: Gate Detection ---
for gt in gate_times:
    axes[2].axvline(gt, linestyle="--", linewidth=1)

# background shading
axes[2].fill_between(t, 0, 1, where=C > 0.3, alpha=0.1)
axes[2].fill_between(t, 0, 1, where=C < 0.3, alpha=0.05)

axes[2].set_ylim(0, 1)
axes[2].set_title("Threshold Candidates")
axes[2].set_xlabel("time")
axes[2].set_yticks([])
axes[2].grid(True, alpha=0.3)

# --------------------------------------------------
# 6. CAPTION
# --------------------------------------------------
fig.text(
    0.5,
    -0.05,
    "Candidate points where the smoothed lag-one autocorrelation is near zero.",
    ha="center",
    fontsize=10
)

plt.tight_layout()

# --------------------------------------------------
# 7. SAVE OUTPUT
# --------------------------------------------------
plt.savefig("ieee_gate_detection_v1.png", dpi=200, bbox_inches="tight")
plt.show()

# --------------------------------------------------
# 8. RESULTS BLOCK
# --------------------------------------------------
print("---- RESULTS ----")
print(f"Candidates detected: {len(gate_times)}")
print(f"Candidate times: {np.round(gate_times, 2)}")
print(f"Mean |C| at candidates: {np.mean(np.abs(C[gate_indices])):.4f}")
