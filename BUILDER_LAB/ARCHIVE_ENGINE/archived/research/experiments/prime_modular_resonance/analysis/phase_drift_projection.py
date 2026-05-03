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
# PHASE MAPPING
# =========================
theta = 2 * np.pi * residues / MOD

# unwrap
theta_unwrapped = np.unwrap(theta)

# =========================
# PHASE INCREMENTS
# =========================
dtheta = np.diff(theta_unwrapped)

# =========================
# GLOBAL DRIFT VECTOR
# =========================
mean_dtheta = np.mean(dtheta)

# normalize drift direction
drift_dir = np.sign(mean_dtheta)

# projection
projection = dtheta * drift_dir

# =========================
# PLOTS
# =========================
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(projection, linewidth=1)
plt.title(f"Drift Projection Δθ_proj (mod {MOD})")
plt.ylabel("projected Δθ")

plt.subplot(2, 1, 2)
plt.hist(projection, bins=50)
plt.axvline(np.mean(projection), linestyle='--', label=f"mean={np.mean(projection):.4f}")
plt.title("Distribution of Projected Drift")
plt.xlabel("Δθ projection")
plt.ylabel("frequency")
plt.legend()

plt.tight_layout()
out_path = os.path.join(OUTPUT_DIR, f"phase_drift_projection_mod{MOD}.png")
plt.savefig(out_path)
plt.close()

# =========================
# METRICS
# =========================
positive_fraction = np.mean(projection > 0)
negative_fraction = np.mean(projection < 0)

print("\n=== PHASE DRIFT PROJECTION ===")
print(f"Mean projected Δθ: {np.mean(projection):.6f}")
print(f"Positive fraction: {positive_fraction:.4f}")
print(f"Negative fraction: {negative_fraction:.4f}")

print("\n=== INTERPRETATION ===\n")
print("If most projections are positive:")
print("→ motion aligns with a global drift direction")

print("If symmetric:")
print("→ no coherent directional motion")

print(f"\n[OK] saved → {out_path}")
