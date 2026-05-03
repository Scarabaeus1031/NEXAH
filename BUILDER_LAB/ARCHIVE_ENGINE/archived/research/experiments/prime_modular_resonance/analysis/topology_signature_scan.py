import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
import os

# =========================
# CONFIG
# =========================
MOD_LIST = [7, 11, 13, 17, 19, 23, 29]
N_PRIMES = 20000

OUTPUT_DIR = os.path.join(
    "BUILDER_LAB",
    "ARCHIVE_ENGINE",
    "archived",
    "research",
    "experiments",
    "prime_modular_resonance",
    "analysis",
    "output",
    "plots"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# PRIME SEQUENCE (shared)
# =========================
primes = list(primerange(2, 300000))[:N_PRIMES]

# =========================
# STORAGE
# =========================
mean_dtheta_list = []
mean_dw_list = []
linearity_list = []

# =========================
# SCAN
# =========================
for MOD in MOD_LIST:

    residues = np.array([p % MOD for p in primes])
    theta = 2 * np.pi * residues / MOD
    theta_unwrapped = np.unwrap(theta)

    # Δθ
    dtheta = np.diff(theta_unwrapped)
    mean_dtheta = np.mean(dtheta)

    # winding
    winding = (theta_unwrapped - theta_unwrapped[0]) / (2 * np.pi)
    dw = np.diff(winding)
    mean_dw = np.mean(dw)

    # linearity check (R² of linear fit)
    x = np.arange(len(winding))
    coeffs = np.polyfit(x, winding, 1)
    fit = np.polyval(coeffs, x)

    ss_res = np.sum((winding - fit)**2)
    ss_tot = np.sum((winding - np.mean(winding))**2)
    r2 = 1 - ss_res / ss_tot

    # store
    mean_dtheta_list.append(mean_dtheta)
    mean_dw_list.append(mean_dw)
    linearity_list.append(r2)

    print(f"\nMOD {MOD}")
    print(f"Mean Δθ: {mean_dtheta:.6f}")
    print(f"Mean ΔW: {mean_dw:.6f}")
    print(f"Linearity (R²): {r2:.6f}")

# =========================
# PLOTS
# =========================
plt.figure(figsize=(12, 6))

plt.subplot(3, 1, 1)
plt.plot(MOD_LIST, mean_dtheta_list, marker='o')
plt.title("Mean Phase Drift Δθ vs Modulus")
plt.ylabel("mean Δθ")

plt.subplot(3, 1, 2)
plt.plot(MOD_LIST, mean_dw_list, marker='o')
plt.title("Mean Winding Increment ΔW vs Modulus")
plt.ylabel("mean ΔW")

plt.subplot(3, 1, 3)
plt.plot(MOD_LIST, linearity_list, marker='o')
plt.title("Linearity of W(n) (R²) vs Modulus")
plt.xlabel("modulus")
plt.ylabel("R²")

plt.tight_layout()

out_path = os.path.join(OUTPUT_DIR, "topology_signature_scan.png")
plt.savefig(out_path)
plt.close()

print("\n[OK] saved →", out_path)

# =========================
# INTERPRETATION
# =========================
print("\n=== INTERPRETATION ===\n")

print("If mean Δθ consistently ≠ 0:")
print("→ drift exists across moduli")

print("If mean ΔW > 0:")
print("→ persistent rotation exists")

print("If R² ~ 1:")
print("→ motion is globally linear (stable rotation)")

print("\nThis defines the topology signature of the system.")
