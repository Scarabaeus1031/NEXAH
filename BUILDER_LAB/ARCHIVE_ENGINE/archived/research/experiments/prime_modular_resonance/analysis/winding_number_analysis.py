import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
import os

# =========================
# CONFIG
# =========================
MOD = 23
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
# PRIME SEQUENCE
# =========================
primes = list(primerange(2, 300000))[:N_PRIMES]
residues = np.array([p % MOD for p in primes])

# =========================
# PHASE
# =========================
theta = 2 * np.pi * residues / MOD
theta_unwrapped = np.unwrap(theta)

# =========================
# WINDING NUMBER
# =========================
theta0 = theta_unwrapped[0]
winding = (theta_unwrapped - theta0) / (2 * np.pi)

# =========================
# LOCAL WINDING RATE
# =========================
dw = np.diff(winding)

# =========================
# PLOTS
# =========================
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(winding, linewidth=1)
plt.title(f"Winding Number W(n) (mod {MOD})")
plt.ylabel("W(n)")

plt.subplot(2, 1, 2)
plt.plot(dw, linewidth=0.5)
plt.axhline(np.mean(dw), linestyle='--', label=f"mean={np.mean(dw):.4f}")
plt.title("Local Winding Increment ΔW")
plt.xlabel("n")
plt.ylabel("ΔW")
plt.legend()

plt.tight_layout()
out_path = os.path.join(OUTPUT_DIR, f"winding_number_mod{MOD}.png")
plt.savefig(out_path)
plt.close()

# =========================
# METRICS
# =========================
total_windings = winding[-1]
mean_dw = np.mean(dw)

print("\n=== WINDING ANALYSIS ===")
print(f"Total windings: {total_windings:.4f}")
print(f"Mean ΔW: {mean_dw:.6f}")

print("\n=== INTERPRETATION ===\n")
print("If W(n) grows linearly:")
print("→ persistent rotation on phase manifold")

print("If ΔW has structure:")
print("→ non-uniform rotational increments")

print("\n[OK] saved →", out_path)
