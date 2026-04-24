# zeta_nexah_demo.py
# NEXAH Zeta Demo:
# rotating contributions -> interference -> coherence -> gates

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# ------------------------------------------------------------
# 1. Parameters
# ------------------------------------------------------------
sigma = 0.5          # critical-line style slice: s = 1/2 + i t
N = 400             # number of terms
T = 1200            # time samples
tau = np.linspace(0, 60, T)

n = np.arange(1, N + 1)

# ------------------------------------------------------------
# 2. Zeta-like partial sum along s = sigma + i t
# ------------------------------------------------------------
Z = np.zeros(T, dtype=complex)
coherence = np.zeros(T)

for k, tt in enumerate(tau):
    s = sigma + 1j * tt

    terms = n ** (-s)
    Z[k] = np.sum(terms)

    # coherence proxy:
    # 1 = aligned / strong resultant
    # 0 = destructive interference / gate candidate
    coherence[k] = np.abs(Z[k]) / np.sum(np.abs(terms))

# ------------------------------------------------------------
# 3. Gate detection: low coherence minima
# ------------------------------------------------------------
threshold = np.percentile(coherence, 5)

gate_mask = coherence <= threshold

gate_indices = []
min_distance = 30

for i in np.where(gate_mask)[0]:
    if not gate_indices or i - gate_indices[-1] > min_distance:
        gate_indices.append(i)

gate_tau = tau[gate_indices]
gate_Z = Z[gate_indices]

# ------------------------------------------------------------
# 4. Pick one moment to show vector construction
# ------------------------------------------------------------
show_index = gate_indices[len(gate_indices) // 2] if gate_indices else T // 2
show_t = tau[show_index]
show_terms = n ** (-(sigma + 1j * show_t))

partial = np.cumsum(show_terms[:80])

# ------------------------------------------------------------
# 5. Plot
# ------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# --- Panel 1: rotating vector sum path ---
axes[0].plot(partial.real, partial.imag, linewidth=1.4)
axes[0].scatter(partial.real[-1], partial.imag[-1], s=50, zorder=5)
axes[0].axhline(0, linewidth=0.8, alpha=0.4)
axes[0].axvline(0, linewidth=0.8, alpha=0.4)
axes[0].set_title("Rotating Contributions")
axes[0].set_xlabel("Re")
axes[0].set_ylabel("Im")
axes[0].grid(True, alpha=0.25)
axes[0].set_aspect("equal", adjustable="box")

# --- Panel 2: zeta-like output path ---
axes[1].plot(Z.real, Z.imag, linewidth=1.0, alpha=0.8)
axes[1].scatter(gate_Z.real, gate_Z.imag, s=35, label="gate candidates")
axes[1].scatter(0, 0, s=80, marker="x", label="origin / cancellation")
axes[1].set_title("Output Path ζ-like(s)")
axes[1].set_xlabel("Re")
axes[1].set_ylabel("Im")
axes[1].grid(True, alpha=0.25)
axes[1].legend()
axes[1].set_aspect("equal", adjustable="box")

# --- Panel 3: coherence over t ---
axes[2].plot(tau, coherence, linewidth=1.4)
axes[2].axhline(threshold, linestyle="--", linewidth=1, label="low-coherence threshold")

for gt in gate_tau:
    axes[2].axvline(gt, linewidth=0.7, alpha=0.45)

axes[2].set_title("Coherence C(t) + Gates")
axes[2].set_xlabel("t / phase")
axes[2].set_ylabel("C(t)")
axes[2].grid(True, alpha=0.25)
axes[2].legend()

fig.suptitle(
    "NEXAH Zeta Demo — Rotating Contributions → Interference → Gate Candidates",
    fontsize=14
)

fig.text(
    0.5,
    -0.02,
    "Interpretation: gates appear where rotating contributions nearly cancel and coherence reaches local minima.",
    ha="center",
    fontsize=10
)

plt.tight_layout()
plt.savefig("zeta_nexah_demo.png", dpi=220, bbox_inches="tight")
plt.show()

# ------------------------------------------------------------
# 6. Results
# ------------------------------------------------------------
print("---- NEXAH ZETA DEMO RESULTS ----")
print(f"sigma: {sigma}")
print(f"N terms: {N}")
print(f"gate candidates: {len(gate_indices)}")
print("gate t values:", np.round(gate_tau, 3))
print(f"coherence threshold: {threshold:.6f}")
print("output saved: zeta_nexah_demo.png")
