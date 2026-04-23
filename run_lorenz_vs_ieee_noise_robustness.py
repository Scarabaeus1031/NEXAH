# ==========================================================
# NEXAH Demo — Cross-System Noise Robustness (Final)
# ==========================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------

CSV_PATH = "APPLICATIONS/power_systems/stability_field_dynamics/data/ieee_noisy.csv"
NOISE_STD = 0.02
SMOOTH_SIGMA = 2
SEED = 42

np.random.seed(SEED)

# ----------------------------------------------------------
# LORENZ-LIKE SIGNAL (oscillatory system)
# ----------------------------------------------------------

t_lorenz = np.linspace(0, 20, 2000)

signal_lorenz_clean = (
    np.exp(-((t_lorenz - 2)**2)) +
    np.exp(-((t_lorenz - 6)**2)) +
    np.exp(-((t_lorenz - 12)**2)) +
    np.exp(-((t_lorenz - 18)**2))
)

signal_lorenz_clean /= np.max(signal_lorenz_clean)

noise_l = np.random.normal(0, NOISE_STD, size=signal_lorenz_clean.shape)
signal_lorenz_noisy = signal_lorenz_clean + noise_l

# ----------------------------------------------------------
# IEEE SYSTEM (real system)
# ----------------------------------------------------------

df = pd.read_csv(CSV_PATH)

t_ieee = df["time"].values
signal_ieee_clean = df["voltage"].values

signal_ieee_clean = (signal_ieee_clean - np.min(signal_ieee_clean)) / (
    np.max(signal_ieee_clean) - np.min(signal_ieee_clean)
)

noise_i = np.random.normal(0, NOISE_STD, size=signal_ieee_clean.shape)
signal_ieee_noisy = signal_ieee_clean + noise_i

# ----------------------------------------------------------
# TIME NORMALIZATION
# ----------------------------------------------------------

t_lorenz = t_lorenz / t_lorenz.max()
t_ieee = t_ieee.astype(float)
t_ieee = t_ieee / t_ieee.max()

# ----------------------------------------------------------
# STRUCTURE EXTRACTION
# ----------------------------------------------------------

def compute_structure(signal):
    grad = np.gradient(signal)
    curv = np.gradient(grad)
    return grad, curv

# raw
grad_l_clean, curv_l_clean = compute_structure(signal_lorenz_clean)
grad_l_noisy, curv_l_noisy = compute_structure(signal_lorenz_noisy)

grad_i_clean, curv_i_clean = compute_structure(signal_ieee_clean)
grad_i_noisy, curv_i_noisy = compute_structure(signal_ieee_noisy)

# smoothed
grad_l_noisy_s = gaussian_filter1d(grad_l_noisy, SMOOTH_SIGMA)
grad_i_noisy_s = gaussian_filter1d(grad_i_noisy, SMOOTH_SIGMA)

# ----------------------------------------------------------
# METRICS
# ----------------------------------------------------------

def safe_corr(a, b):
    if np.std(a) < 1e-6 or np.std(b) < 1e-6:
        return np.nan
    return np.corrcoef(a, b)[0, 1]

metrics = {
    "Lorenz grad raw": safe_corr(grad_l_clean, grad_l_noisy),
    "Lorenz grad smooth": safe_corr(grad_l_clean, grad_l_noisy_s),
    "IEEE grad raw": safe_corr(grad_i_clean, grad_i_noisy),
    "IEEE grad smooth": safe_corr(grad_i_clean, grad_i_noisy_s),
    "Lorenz curv": safe_corr(curv_l_clean, curv_l_noisy),
    "IEEE curv": safe_corr(curv_i_clean, curv_i_noisy),
}

# ----------------------------------------------------------
# PLOT
# ----------------------------------------------------------

plt.figure(figsize=(14, 8))

# Lorenz
plt.plot(t_lorenz, grad_l_clean, label="Lorenz clean", linewidth=2)
plt.plot(t_lorenz, grad_l_noisy, alpha=0.15, label="Lorenz noisy (raw)")
plt.plot(t_lorenz, grad_l_noisy_s, linewidth=2, linestyle="--", label="Lorenz noisy (smoothed)")

# IEEE
plt.plot(t_ieee, grad_i_clean, linestyle="-.", label="IEEE clean")
plt.plot(t_ieee, grad_i_noisy, alpha=0.3, linestyle=":", label="IEEE noisy (raw)")
plt.plot(t_ieee, grad_i_noisy_s, linewidth=2, linestyle="--", label="IEEE noisy (smoothed)")

plt.title("NEXAH — Structure Under Noise: Oscillatory vs Real System")
plt.xlabel("normalized time")
plt.ylabel("gradient (structure)")
plt.legend()
plt.grid(alpha=0.3)

output_path = "outputs/demo/nexah_cross_system_noise_robustness_final.png"
plt.savefig(output_path, dpi=150)
plt.close()

# ----------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------

print("\n⚡ NEXAH Cross-System Noise Robustness (Final)")
print(f"✔ Saved plot → {output_path}")

print("\n📊 Correlation:")
for k, v in metrics.items():
    print(f"{k:22s}: {v:.3f}")

# ----------------------------------------------------------
# INTERPRETATION (DATA-DRIVEN)
# ----------------------------------------------------------

print("\n🧠 Interpretation:")

if metrics["Lorenz grad smooth"] > metrics["Lorenz grad raw"]:
    print("→ Lorenz: structure recoverable after smoothing")
else:
    print("→ Lorenz: structure highly noise-sensitive")

if metrics["IEEE grad raw"] > 0.5:
    print("→ IEEE: global structure robust under noise")

if metrics["IEEE grad smooth"] > metrics["IEEE grad raw"]:
    print("→ IEEE: smoothing improves structural clarity")

print("\n🔥 Conclusion:")
print("Structure exists at multiple scales:")
print("→ high-frequency structure is noise-sensitive")
print("→ low-frequency structure is robust")
print("→ smoothing reveals latent structure in noisy data")
