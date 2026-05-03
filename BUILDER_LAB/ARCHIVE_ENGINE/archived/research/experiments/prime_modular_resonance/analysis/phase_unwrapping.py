# phase_unwrapping.py

import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange

# =========================
# CONFIG
# =========================

MOD = 23
N_PRIMES = 20000

OUTPUT_PATH = "analysis/output/plots"

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
# PLOTS
# =========================

plt.figure(figsize=(12, 6))

plt.subplot(2,1,1)
plt.plot(theta_unwrapped, linewidth=1)
plt.title(f"Unwrapped Phase θ (mod {MOD})")
plt.ylabel("θ (continuous)")
plt.xlabel("n (prime index)")

plt.subplot(2,1,2)
plt.plot(dtheta, linewidth=0.8)
plt.axhline(np.mean(dtheta), linestyle='--', label=f"mean={np.mean(dtheta):.3f}")
plt.title("Phase Increment Δθ")
plt.ylabel("Δθ")
plt.xlabel("n")
plt.legend()

plt.tight_layout()
plt.savefig(f"{OUTPUT_PATH}/phase_unwrapped_mod{MOD}.png")
print(f"[OK] saved → {OUTPUT_PATH}/phase_unwrapped_mod{MOD}.png")

# =========================
# HISTOGRAM
# =========================

plt.figure(figsize=(6,4))
plt.hist(dtheta, bins=50)
plt.title("Distribution of Δθ")
plt.xlabel("Δθ")
plt.ylabel("frequency")

plt.tight_layout()
plt.savefig(f"{OUTPUT_PATH}/phase_increment_hist_mod{MOD}.png")
print(f"[OK] saved → {OUTPUT_PATH}/phase_increment_hist_mod{MOD}.png")

# =========================
# SUMMARY
# =========================

print("\n=== PHASE ANALYSIS ===")
print(f"Mean Δθ: {np.mean(dtheta):.5f}")
print(f"Std  Δθ: {np.std(dtheta):.5f}")

print("\n=== INTERPRETATION ===")
print("If θ grows roughly linearly:")
print("→ system behaves like motion along a phase manifold")

print("If Δθ has structure:")
print("→ transitions are not random steps on the circle")
