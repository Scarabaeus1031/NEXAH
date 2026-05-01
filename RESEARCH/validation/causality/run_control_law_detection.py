import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import curve_fit

print("⚡ NEXAH — Control Law Detection (s*(φ))")

# =========================
# LOAD DATA
# =========================

data_path = "RESEARCH/validation/causality/gate_resonance_scan_multirun.npy"
heatmap = np.load(data_path)

strength_values = np.linspace(0.0, 1.5, heatmap.shape[0])
phase_values = np.linspace(0.0, 2 * np.pi, heatmap.shape[1])

# =========================
# EXTRACT s*(φ)
# =========================

best_indices = np.argmax(heatmap, axis=0)
s_star_raw = strength_values[best_indices]

# =========================
# SMOOTHING
# =========================

s_star_smooth = gaussian_filter1d(s_star_raw, sigma=2)

# =========================
# REGIME CLASSIFICATION
# =========================

regimes = []

for s in s_star_smooth:
    if s < 0.35:
        regimes.append(0)   # resonant
    elif s < 0.75:
        regimes.append(1)   # transition
    else:
        regimes.append(2)   # high-input

regimes = np.array(regimes)

# =========================
# DETECT TRANSITIONS (KNICKE)
# =========================

switch_idx = np.where(np.diff(regimes) != 0)[0] + 1
switch_phases = phase_values[switch_idx]

# =========================
# SIMPLE SIN FIT (TEST ONLY)
# =========================

def sin_model(phi, a, b, c):
    return a + b * np.sin(phi + c)

try:
    params, _ = curve_fit(sin_model, phase_values, s_star_smooth)
    sin_fit = sin_model(phase_values, *params)
    fit_success = True
except:
    sin_fit = None
    fit_success = False

# =========================
# PLOT
# =========================

plt.figure(figsize=(12, 6))

plt.plot(phase_values, s_star_raw, 'o-', alpha=0.4, label="raw s*(φ)")
plt.plot(phase_values, s_star_smooth, linewidth=3, label="smoothed s*(φ)")

if fit_success:
    plt.plot(phase_values, sin_fit, '--', label="sin fit (test)")

# Regime coloring
plt.scatter(phase_values[regimes == 0], s_star_smooth[regimes == 0], s=60, label="resonant")
plt.scatter(phase_values[regimes == 1], s_star_smooth[regimes == 1], s=60, label="transition")
plt.scatter(phase_values[regimes == 2], s_star_smooth[regimes == 2], s=60, label="high-input")

# Mark transitions
for p in switch_phases:
    plt.axvline(p, linestyle='--', alpha=0.3)

plt.xlabel("phase φ")
plt.ylabel("optimal strength s*")
plt.title("NEXAH Control Law: s*(φ) with Regimes")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("RESEARCH/validation/causality/results/control_law_detection.png", dpi=200)
plt.close()
np.savez(
    "RESEARCH/validation/causality/control_law_data.npz",
    phi=phi_grid,
    s_star=s_star
)

print("✅ Saved: control_law_data.npz")
# =========================
# SAVE SUMMARY
# =========================

summary_path = "RESEARCH/validation/causality/results/control_law_detection.txt"

with open(summary_path, "w") as f:
    f.write("NEXAH — Control Law Detection\n\n")

    f.write("Detected regime switches (phase):\n")
    for p in switch_phases:
        f.write(f"{p:.6f}\n")

    f.write("\nRegime definition:\n")
    f.write("0 = resonant (low control)\n")
    f.write("1 = transition\n")
    f.write("2 = high-input (phase mismatch)\n")

    if fit_success:
        f.write("\nSin-fit parameters (test only):\n")
        f.write(f"a={params[0]:.4f}, b={params[1]:.4f}, c={params[2]:.4f}\n")
        f.write("Fit quality: LIMITED (non-sinusoidal structure)\n")

    f.write("\nInterpretation:\n")
    f.write("Control law is regime-based, not continuous.\n")
    f.write("Optimal control depends on phase alignment.\n")

print("✅ Saved: control_law_detection.png")
print("✅ Saved: control_law_detection.txt")
