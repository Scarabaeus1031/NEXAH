"""
v7_navigation_vector.py
=======================

Goal:
- turn the current NEXAH phase-space view into a local navigation field
- estimate direction of motion in the structural state space
- visualize local navigation vectors on top of the trajectory
- distinguish between:
    * inward motion
    * outward motion
    * clockwise / counterclockwise drift
    * local stability / instability zones

State space used here:
- x = coherence
- y = switch signal

Optional derived interpretation:
- radius / phase in polar representation
- local navigation vectors = finite-difference motion field

This is still an analysis / visualization layer,
not yet an intervention controller.

Outputs:
- ieee57_v7_navigation_vector_field.png
- ieee57_v7_navigation_polar_vectors.png
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

    if t > 5:
        if voltage_history[-2] >= 0.90 and v_mean < 0.90:
            classical_events.append(t)


# =========================
# 3. Build phase trajectory
# =========================

x = np.array(coherence_history)
y = np.array(switch_signal)

# finite-difference navigation vectors
dx = np.gradient(x)
dy = np.gradient(y)

speed = np.sqrt(dx**2 + dy**2)

# normalize arrows for cleaner plotting
eps = 1e-8
dxn = dx / (speed + eps)
dyn = dy / (speed + eps)

# "stability center" = max coherence, zero switch
x0 = np.max(x)
y0 = 0.0

# radial direction relative to center
rx = x - x0
ry = y - y0
r = np.sqrt(rx**2 + ry**2)

# inward/outward flow:
# negative radial velocity = inward
radial_velocity = (rx * dx + ry * dy) / (r + eps)

# tangential velocity
tangential_velocity = (rx * dy - ry * dx) / (r + eps)

mean_radial = np.mean(radial_velocity[np.isfinite(radial_velocity)])
mean_tangential = np.mean(tangential_velocity[np.isfinite(tangential_velocity)])

print("\n===== NAVIGATION VECTOR ANALYSIS =====")
print(f"Classical events: {classical_events}")
print(f"Mean radial velocity: {mean_radial:.6f}")
print(f"Mean tangential velocity: {mean_tangential:.6f}")

if mean_radial < -1e-3:
    print("→ Global tendency: inward / contractive")
elif mean_radial > 1e-3:
    print("→ Global tendency: outward / expansive")
else:
    print("→ Global tendency: neutral / loop-like")

if mean_tangential > 1e-3:
    print("→ Global rotation: counterclockwise")
elif mean_tangential < -1e-3:
    print("→ Global rotation: clockwise")
else:
    print("→ Global rotation: weak / balanced")


# =========================
# 4. Cartesian navigation vector field plot
# =========================

fig1, ax1 = plt.subplots(figsize=(10, 8))

# trajectory
ax1.plot(x, y, alpha=0.5, linewidth=1.5, label="Trajectory")

# quiver every nth point
step = 5
q = ax1.quiver(
    x[::step],
    y[::step],
    dxn[::step],
    dyn[::step],
    speed[::step],
    angles="xy",
    scale_units="xy",
    scale=8,
    cmap="plasma",
    width=0.004,
)

# mark start / end
ax1.scatter(x[0], y[0], color="green", s=100, label="Start")
ax1.scatter(x[-1], y[-1], color="red", s=100, label="End")

# mark classical collapse events if in range
for ev in classical_events:
    if 0 <= ev < len(x):
        ax1.scatter(x[ev], y[ev], color="black", s=50, marker="x")

# stability center
ax1.scatter(x0, y0, color="gold", s=140, marker="*", label="Stability center")

ax1.set_title("NEXAH Navigation Vector Field (Coherence vs Switch)")
ax1.set_xlabel("Coherence")
ax1.set_ylabel("Switch signal")
ax1.grid(True)
ax1.legend(loc="best")

cbar1 = plt.colorbar(q, ax=ax1)
cbar1.set_label("Local speed")


# =========================
# 5. Polar navigation plot
# =========================

# radius = contraction depth
radius = 1.0 - x
radius = (radius - radius.min()) / (radius.max() - radius.min() + eps)

# phase from trajectory index
theta = np.linspace(0, 2 * np.pi * 3, len(radius))

# radial derivative in polar representation
dr = np.gradient(radius)
dtheta = np.gradient(theta)

# quiver in polar-like Cartesian embedding
xp = radius * np.cos(theta)
yp = radius * np.sin(theta)

dxp = np.gradient(xp)
dyp = np.gradient(yp)
sp = np.sqrt(dxp**2 + dyp**2)

dxpn = dxp / (sp + eps)
dypn = dyp / (sp + eps)

fig2 = plt.figure(figsize=(10, 10))
ax2 = fig2.add_subplot(111, projection="polar")

# trajectory points
sc = ax2.scatter(
    theta,
    radius,
    c=np.abs(y),
    cmap="plasma",
    s=28,
    alpha=0.9,
)

# smoothed line
ax2.plot(theta, radius, alpha=0.45, linewidth=1.5)

# quiver-like arrow segments in polar coordinates
for i in range(0, len(theta), 8):
    th0 = theta[i]
    r0 = radius[i]
    th1 = theta[i] + 0.12 * np.sign(dtheta[i])
    r1 = radius[i] + 0.08 * dr[i]
    ax2.annotate(
        "",
        xy=(th1, max(0.0, r1)),
        xytext=(th0, r0),
        arrowprops=dict(arrowstyle="->", lw=1.2, alpha=0.6),
    )

# mark start / end
ax2.scatter(theta[0], radius[0], color="green", s=120, label="Start")
ax2.scatter(theta[-1], radius[-1], color="red", s=120, label="End")

# mark collapse events
for ev in classical_events:
    if 0 <= ev < len(theta):
        ax2.scatter(theta[ev], radius[ev], color="black", s=50, marker="x")

ax2.set_title("NEXAH Polar Navigation Vectors")
ax2.legend(loc="upper right")

cbar2 = plt.colorbar(sc, pad=0.1)
cbar2.set_label("Switch intensity")


# =========================
# 6. Save
# =========================

save_dir = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
save_dir.mkdir(parents=True, exist_ok=True)

fig1.savefig(save_dir / "ieee57_v7_navigation_vector_field.png", dpi=200)
fig2.savefig(save_dir / "ieee57_v7_navigation_polar_vectors.png", dpi=200)

plt.close(fig1)
plt.close(fig2)

print("\nSaved:")
print("  • ieee57_v7_navigation_vector_field.png")
print("  • ieee57_v7_navigation_polar_vectors.png")
