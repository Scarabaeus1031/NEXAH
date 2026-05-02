import numpy as np
import matplotlib.pyplot as plt

print("⚡ NEXAH — YUGO Control Law Overlay")

# ======================================
# LOAD / IMPORT YOUR DATA
# ======================================

# 👉 Diese Arrays musst du ggf. anpassen
# (je nachdem wie dein v28 Script speichert)

# theta_unwrapped: shape (T,)
# iota_indices: list oder array von event indices

# Beispiel:
# data = np.load("RESEARCH/validation/causality/yugo_data.npz")
# theta_unwrapped = data["theta"]
# iota_indices = data["iota"]

# --- FALLBACK (wenn direkt im Script verfügbar) ---
from ieee_gate_detection_v28_yugo_flow_iota_coupling import (
    theta_unwrapped,
    iota_indices
)

# ======================================
# LOAD CONTROL LAW
# ======================================

# aus deinem vorherigen Schritt
control_data = np.load("RESEARCH/validation/causality/control_law_data.npz")

phi_grid = control_data["phi"]      # shape (N,)
s_star = control_data["s_star"]     # optimal control curve

# ======================================
# INTERPOLATION FUNCTION s*(φ)
# ======================================

def s_star_function(phi):
    # periodic interpolation
    return np.interp(
        phi,
        phi_grid,
        s_star,
        period=2*np.pi
    )

# ======================================
# MAP θ → φ
# ======================================

phi = np.mod(theta_unwrapped, 2*np.pi)

# evaluate control law
s_values = s_star_function(phi)

# ======================================
# OPTIONAL: YUGO INSTABILITY METRIC
# ======================================

# einfache Approximation:
# große Sprünge im Winkel → Instabilität
dtheta = np.diff(theta_unwrapped, prepend=theta_unwrapped[0])
instability = np.abs(dtheta)

# ======================================
# PLOT 1 — Control Law vs Phase
# ======================================

plt.figure(figsize=(12, 5))

plt.plot(phi, s_values, label="s*(φ)", linewidth=2)

# IOTA overlay
plt.scatter(
    phi[iota_indices],
    s_values[iota_indices],
    color="red",
    label="IOTA events",
    zorder=3
)

plt.xlabel("phase φ")
plt.ylabel("optimal control strength")
plt.title("NEXAH — Control Law applied to YUGO phase")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("RESEARCH/validation/causality/yugo_control_overlay.png")
print("✅ Saved: yugo_control_overlay.png")

plt.show()

# ======================================
# PLOT 2 — Time Series Overlay
# ======================================

plt.figure(figsize=(12, 5))

plt.plot(s_values, label="s*(θ(t))")
plt.plot(instability, label="instability proxy", alpha=0.7)

plt.scatter(
    iota_indices,
    s_values[iota_indices],
    color="red",
    label="IOTA events",
    zorder=3
)

plt.xlabel("time")
plt.ylabel("value")
plt.title("Control Law vs Instability (YUGO)")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("RESEARCH/validation/causality/yugo_control_timeseries.png")
print("✅ Saved: yugo_control_timeseries.png")

plt.show()

# ======================================
# OPTIONAL: STATISTICS
# ======================================

print("\n📊 Statistics:")

mean_s_iota = np.mean(s_values[iota_indices])
mean_s_all = np.mean(s_values)

print(f"Mean s*(φ) at IOTA: {mean_s_iota:.4f}")
print(f"Mean s*(φ) overall: {mean_s_all:.4f}")

print("\nΔ (IOTA vs baseline):", mean_s_iota - mean_s_all)
