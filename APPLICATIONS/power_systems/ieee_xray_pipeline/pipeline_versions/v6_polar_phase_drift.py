"""
ieee57_pipeline_v6_polar_phase_drift.py
======================================

Goal:
- visualize the FULL trajectory (not just event windows)
- detect whether the system forms:
    → closed loops (oscillation)
    → inward drift (collapse spiral)
    → outward drift (recovery / instability expansion)

Mapping:
- angle  = time phase (continuous)
- radius = contraction depth (1 - coherence)
- color  = switch intensity

This reveals:
→ spiral vs loop behavior
→ drift direction
→ energy injection patterns

Outputs:
- ieee57_pipeline_v6_polar_phase_drift.png
"""

import pandapower as pp
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# =========================
# 1. Load system
# =========================

net = pp.networks.case57()

time_steps = 300
np.random.seed(42)

load_factor = 1.0 + 0.25 * np.sin(np.linspace(0, 6 * np.pi, time_steps))
noise = np.random.normal(0, 0.02, time_steps)

voltage_history = []
coherence_history = []
switch_signal = []


# =========================
# 2. Simulation
# =========================

for t in range(time_steps):

    # perturb loads
    for load in net.load.index:
        net.load.at[load, "p_mw"] *= (load_factor[t] + noise[t])

    # power flow
    try:
        pp.runpp(net, enforce_q_lims=True)
        voltages = net.res_bus.vm_pu.values
    except Exception:
        voltages = np.ones(len(net.bus)) * 0.95

    v_mean = voltages.mean()
    v_std = voltages.std()
    coherence = 1.0 - v_std

    voltage_history.append(v_mean)
    coherence_history.append(coherence)

    # switch signal (gradient)
    if len(voltage_history) > 2:
        sw = np.gradient(voltage_history)[-1]
    else:
        sw = 0.0

    switch_signal.append(sw)


# =========================
# 3. Build polar trajectory
# =========================

coh = np.array(coherence_history)
sw = np.array(switch_signal)

# contraction depth
radius = 1.0 - coh

# normalize radius for visualization
radius = (radius - radius.min()) / (radius.max() - radius.min() + 1e-8)

# continuous phase
theta = np.linspace(0, 2 * np.pi * 3, time_steps)  # 3 rotations


# =========================
# 4. Drift analysis
# =========================

# compute slow drift trend
window = 20
smooth_radius = np.convolve(radius, np.ones(window)/window, mode='same')

# estimate drift direction
drift = np.gradient(smooth_radius)

mean_drift = np.mean(drift)

print("\n===== PHASE DRIFT ANALYSIS =====")
print(f"Mean radial drift: {mean_drift:.6f}")

if mean_drift > 0.001:
    print("→ OUTWARD drift (instability expansion)")
elif mean_drift < -0.001:
    print("→ INWARD drift (collapse spiral)")
else:
    print("→ CLOSED LOOP (oscillatory system)")


# =========================
# 5. Plot
# =========================

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="polar")

# main trajectory
sc = ax.scatter(
    theta,
    radius,
    c=np.abs(sw),
    cmap="plasma",
    s=30,
    alpha=0.9,
)

# smoothed path
ax.plot(theta, smooth_radius, linewidth=2.5, alpha=0.7, label="Smoothed trajectory")

# mark start & end
ax.scatter(theta[0], radius[0], color="green", s=120, label="Start")
ax.scatter(theta[-1], radius[-1], color="red", s=120, label="End")

# reference circles
ax.set_title("NEXAH Phase Drift — Spiral vs Loop Analysis")
ax.legend(loc="upper right")

cbar = plt.colorbar(sc, pad=0.1)
cbar.set_label("Switch intensity")


# =========================
# 6. Save
# =========================

save_dir = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
save_dir.mkdir(parents=True, exist_ok=True)

fig.savefig(save_dir / "ieee57_pipeline_v6_polar_phase_drift.png", dpi=200)
plt.close(fig)

print("\nSaved:")
print("  • ieee57_pipeline_v6_polar_phase_drift.png")
