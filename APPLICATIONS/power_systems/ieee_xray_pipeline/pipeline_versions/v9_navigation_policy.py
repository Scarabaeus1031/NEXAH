"""
v9_navigation_policy.py
=======================

Goal:
- move from observation to a first intervention logic
- detect when the system approaches an escape-prone region
- compute a simple counter-vector that pushes the system back toward the basin
- visualize:
    1. observed trajectory
    2. escape sector / candidate points
    3. suggested navigation / stabilization direction

IMPORTANT:
This is still a policy prototype.
It does NOT modify the actual power-flow model yet.
It computes a navigation policy in the extracted NEXAH state space.

State space:
- x = coherence
- y = switch signal
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
classical_events = []

# =========================
# 2. Simulation
# =========================

for t in range(time_steps):
    for load in net.load.index:
        net.load.at[load, "p_mw"] *= (load_factor[t] + noise[t])

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

    if len(voltage_history) > 2:
        sw = np.gradient(voltage_history)[-1]
    else:
        sw = 0.0
    switch_signal.append(sw)

    # classical collapse detection
    if coherence < 0.90 and t > 10:
        classical_events.append(t)

# =========================
# 3. State space
# =========================

x = np.array(coherence_history)
y = np.array(switch_signal)

# center of stable basin (empirical)
center_x = np.mean(x[:50])
center_y = np.mean(y[:50])

# =========================
# 4. Polar representation
# =========================

dx = x - center_x
dy = y - center_y

r = np.sqrt(dx**2 + dy**2)
theta = np.arctan2(dy, dx)

# =========================
# 5. Escape region detection
# =========================

# empirical thresholds from your observations
escape_mask = (
    (theta < -np.pi/4) &  # ~270°–315° sector
    (theta > -3*np.pi/4) &
    (r > np.percentile(r, 75))
)

# =========================
# 6. Navigation policy
# =========================

nav_dx = []
nav_dy = []

for i in range(len(x)):
    # vector to center (stabilizing)
    to_center_x = center_x - x[i]
    to_center_y = center_y - y[i]

    # radial outward component
    radial_x = dx[i]
    radial_y = dy[i]

    if escape_mask[i]:
        # strong counter-force
        fx = -1.5 * radial_x + 0.8 * to_center_x
        fy = -1.5 * radial_y + 0.8 * to_center_y
    else:
        # mild orbit-following stabilization
        fx = 0.3 * to_center_x
        fy = 0.3 * to_center_y

    nav_dx.append(fx)
    nav_dy.append(fy)

nav_dx = np.array(nav_dx)
nav_dy = np.array(nav_dy)

# =========================
# 7. Visualization (Cartesian)
# =========================

fig, ax = plt.subplots(figsize=(8, 6))

# trajectory
ax.plot(x, y, color="lightblue", alpha=0.6, label="Trajectory")

# points
sc = ax.scatter(x, y, c=np.abs(y), cmap="plasma", s=20)

# escape points
ax.scatter(x[escape_mask], y[escape_mask],
           facecolors="none", edgecolors="cyan", s=80,
           label="Escape region")

# vectors
for i in range(0, len(x), 5):
    ax.arrow(x[i], y[i], nav_dx[i], nav_dy[i],
             head_width=0.002, alpha=0.5, color="black")

# center
ax.scatter(center_x, center_y, color="gold", s=120, marker="*",
           label="Stability center")

ax.set_xlabel("Coherence")
ax.set_ylabel("Switch signal")
ax.set_title("NEXAH Navigation Policy (Cartesian)")
ax.legend()
plt.colorbar(sc, label="Switch intensity")

# =========================
# 8. Visualization (Polar)
# =========================

fig2 = plt.figure(figsize=(8, 8))
ax2 = plt.subplot(111, projection='polar')

sc2 = ax2.scatter(theta, r, c=np.abs(y), cmap="plasma", s=25)

# escape
ax2.scatter(theta[escape_mask], r[escape_mask],
            facecolors="none", edgecolors="cyan", s=80)

# vectors
for i in range(0, len(theta), 5):
    new_theta = np.arctan2(nav_dy[i], nav_dx[i])
    new_r = np.sqrt(nav_dx[i]**2 + nav_dy[i]**2)

    ax2.arrow(theta[i], r[i],
              new_theta - theta[i],
              new_r,
              alpha=0.4, color="black")

ax2.set_title("NEXAH Navigation Policy (Polar)")
plt.colorbar(sc2, label="Switch intensity")

# =========================
# 9. Report
# =========================

report = f"""
===== NEXAH NAVIGATION POLICY REPORT =====

Detected classical events: {classical_events}

Escape region count: {np.sum(escape_mask)}

Mean radial distance: {np.mean(r):.6f}
Max radial distance: {np.max(r):.6f}

Stability center:
  coherence = {center_x:.6f}
  switch    = {center_y:.6f}

Interpretation:
- escape region concentrated in lower sector (~270°–315°)
- policy applies counter-radial force
- system shows orbit-like stability with localized escape vectors
"""

# =========================
# 10. Save outputs
# =========================

output_dir = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
output_dir.mkdir(parents=True, exist_ok=True)

plt.figure(1)
plt.savefig(output_dir / "ieee57_v9_navigation_policy_cartesian.png", dpi=150)

plt.figure(2)
plt.savefig(output_dir / "ieee57_v9_navigation_policy_polar.png", dpi=150)

with open(output_dir / "ieee57_v9_navigation_policy_report.txt", "w") as f:
    f.write(report)

print(report)
