# phase_unwrapping.py

import os
import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange

# =========================
# CONFIG
# =========================

MOD = 23
N_PRIMES = 20000

# =========================
# PATH SETUP (ROBUST)
# =========================

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_PATH, "output", "plots")

os.makedirs(OUTPUT_PATH, exist_ok=True)

# =========================
# PRIMES
# =========================

primes = np.array(list(primerange(2, 300000)))[:N_PRIMES]
res = primes % MOD

# =========================
# ANGULAR PHASE
# =========================

theta = 2 * np.pi * res / MOD

# =========================
# UNWRAP PHASE
# =========================

theta_unwrapped = np.unwrap(theta)

# =========================
# STEP DIFFERENCES
# =========================

dtheta = np.diff(theta_unwrapped)

# =========================
# PLOT 1 — UNWRAPPED PHASE
# =========================

plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(theta_unwrapped, linewidth=1)
plt.title(f"Unwrapped Phase θ (mod {MOD})")
plt.ylabel("θ (continuous)")
plt.xlabel("n (prime index)")

# =========================
# PLOT 2 — PHASE STEPS
# =========================

plt.subplot(2, 1, 2)
plt.plot(dtheta, linewidth=0.8)
plt.axhline(np.mean(dtheta), linestyle='--',
            label=f"mean={np.mean(dtheta):.4f}")
plt.title("Phase Increment Δθ")
plt.ylabel("Δθ")
plt.xlabel("n")
plt.legend()

plt.tight_layout()

out1 = os.path.join(OUTPUT_PATH, f"phase_unwrapped_mod{MOD}.png")
plt.savefig(out1, dpi=300)
plt.close()

print(f"[OK] saved → {out1}")

# =========================
# PLOT 3 — HISTOGRAM
# =========================

plt.figure(figsize=(6, 4))
plt.hist(dtheta, bins=60)

plt.axvline(np.mean(dtheta),
            linestyle='--',
            label=f"mean={np.mean(dtheta):.4f}")

plt.title("Distribution of Δθ")
plt.xlabel("Δθ")
plt.ylabel("frequency")
plt.legend()

plt.tight_layout()

out2 = os.path.join(OUTPUT_PATH, f"phase_increment_hist_mod{MOD}.png")
plt.savefig(out2, dpi=300)
plt.close()

print(f"[OK] saved → {out2}")

# =========================
# SUMMARY
# =========================

mean_step = np.mean(dtheta)
std_step = np.std(dtheta)

print("\n=== PHASE ANALYSIS ===")
print(f"Mean Δθ: {mean_step:.6f}")
print(f"Std  Δθ: {std_step:.6f}")

print("\n=== INTERPRETATION ===")
print("""
If θ increases roughly linearly:
→ the system behaves like motion on a phase manifold

If Δθ shows peaks (not flat):
→ transitions are structured (not random)

If mean Δθ ≠ 0:
→ drift exists along the phase
""")
