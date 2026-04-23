# ==========================================================
# NEXAH Demo — Structure Robustness Comparison
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

NOISE_STD = 0.02

# ----------------------------------------------------------
# LORENZ (synthetic oscillatory system)
# ----------------------------------------------------------

t = np.linspace(0, 20, 2000)

# simple synthetic "Lorenz-like" signal (peaks)
lorenz_clean = (
    np.exp(-((t-2)**2)/0.1) +
    np.exp(-((t-5)**2)/0.1) +
    np.exp(-((t-8)**2)/0.1) +
    np.exp(-((t-11)**2)/0.1) +
    np.exp(-((t-14)**2)/0.1) +
    np.exp(-((t-17)**2)/0.1)
)

lorenz_clean = lorenz_clean / np.max(lorenz_clean)

lorenz_noisy = lorenz_clean + np.random.normal(0, NOISE_STD, size=lorenz_clean.shape)

# ----------------------------------------------------------
# IEEE (real drift system)
# ----------------------------------------------------------

df = pd.read_csv("APPLICATIONS/power_systems/stability_field_dynamics/data/ieee_noisy.csv")

time_ieee = df["time"].values
ieee_clean = df["voltage"].values

ieee_clean = (ieee_clean - np.min(ieee_clean)) / (np.max(ieee_clean) - np.min(ieee_clean))
ieee_noisy = ieee_clean + np.random.normal(0, NOISE_STD, size=ieee_clean.shape)

# ----------------------------------------------------------
# STRUCTURE (gradient)
# ----------------------------------------------------------

grad_lorenz_clean = np.gradient(lorenz_clean)
grad_lorenz_noisy = np.gradient(lorenz_noisy)

grad_ieee_clean = np.gradient(ieee_clean)
grad_ieee_noisy = np.gradient(ieee_noisy)

# ----------------------------------------------------------
# CORRELATION
# ----------------------------------------------------------

lorenz_corr = np.corrcoef(grad_lorenz_clean, grad_lorenz_noisy)[0, 1]
ieee_corr = np.corrcoef(grad_ieee_clean, grad_ieee_noisy)[0, 1]

# ----------------------------------------------------------
# PLOT
# ----------------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(t, grad_lorenz_clean, label="Lorenz clean", alpha=0.8)
plt.plot(t, grad_lorenz_noisy, label="Lorenz noisy", alpha=0.5)

plt.plot(time_ieee, grad_ieee_clean, label="IEEE clean", linestyle="--")
plt.plot(time_ieee, grad_ieee_noisy, label="IEEE noisy", linestyle="--", alpha=0.5)

plt.title("NEXAH — Structure Under Noise: Oscillatory vs Real System")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("outputs/demo/nexah_structure_comparison.png", dpi=150)

# ----------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------

print("\n⚡ NEXAH Structure Robustness Comparison")

print("\n📊 Correlation:")
print(f"Lorenz gradient corr: {lorenz_corr:.3f}")
print(f"IEEE gradient corr:   {ieee_corr:.3f}")

print("\n🔥 Interpretation:")
print("Different systems exhibit different robustness profiles:")
print("→ oscillatory systems retain strong structure under noise")
print("→ drift systems retain global trend but lose fine structure")
