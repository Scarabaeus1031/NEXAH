"""
v8_basin_escape_direction.py
============================

Goal:
- estimate local basin structure around the observed orbit
- detect escape-prone regions
- visualize escape direction in phase space and polar space

State space:
- x = coherence
- y = switch signal

Concept:
- stability center = max coherence, zero switch
- basin = region of low speed + low radial instability
- escape = region where motion is both:
    * locally fast
    * radially outward
    * off the dense orbit core

Outputs:
- ieee57_v8_basin_escape_cartesian.png
- ieee57_v8_basin_escape_polar.png
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
# 3. Phase-space quantities
# =========================

x = np.array(coherence_history)
y = np.array(switch_signal)

dx = np.gradient(x)
dy = np.gradient(y)

speed = np.sqrt(dx**2 + dy**2)
eps = 1e-8

# stability center
x0 = np.max(x)
y0 = 0.0

rx = x - x0
ry = y - y0
r = np.sqrt(rx**2 + ry**2)

# radial / tangential velocity
radial_velocity = (rx * dx + ry * dy) / (r + eps)
tangential_velocity = (rx * dy - ry * dx) / (r + eps)

# orbit core estimate = dense radial band
r_med = np.median(r)
r_std = np.std(r)

# local basin score:
# high when speed is low and radial outward push is low
speed_n = (speed - speed.min()) / (speed.max() - speed.min() + eps)
rv_n = (radial_velocity - radial_velocity.min()) / (radial_velocity.max() - radial_velocity.min() + eps)

basin_score = 1.0 - (0.6 * speed_n + 0.4 * np.clip(rv_n, 0, 1))
basin_score = np.clip(basin_score, 0, 1)

# escape score:
# high when point is fast + outward + away from orbit core
outward = np.maximum(radial_velocity, 0)
outward_n = outward / (np.max(outward) + eps)
off_core = np.abs(r - r_med) / (r_std + eps)
off_core_n = np.clip(off_core / (np.max(off_core) + eps), 0, 1)

escape_score = 0.45 * speed_n + 0.35 * outward_n + 0.20 * off_core_n
escape_score = np.clip(escape_score, 0, 1)

# escape candidates
escape_mask = escape_score > 0.65

mean_radial = np.mean(radial_velocity[np.isfinite(radial_velocity)])
mean_tangential = np.mean(tangential_velocity[np.isfinite(tangential_velocity)])

print("\n===== BASIN / ESCAPE ANALYSIS =====")
print(f"Classical events: {classical_events}")
print(f"Mean radial velocity: {mean_radial:.6f}")
print(f"Mean tangential velocity: {mean_tangential:.6f}")
print(f"Escape candidate count: {int(np.sum(escape_mask))}")

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
# 4. Cartesian basin / escape plot
# =========================

fig1, ax1 = plt.subplots(figsize=(11, 8))

# trajectory backbone
ax1.plot(x, y, color="lightsteelblue", linewidth=1.5, alpha=0.7, label="Trajectory")

# basin points
sc1 = ax1.scatter(
    x,
    y,
    c=basin_score,
    cmap="Greens",
    s=26,
    alpha=0.85,
    label="Basin score"
)

# quiver for every nth point
step = 5
ax1.quiver(
    x[::step],
    y[::step],
    dx[::step],
    dy[::step],
    escape_score[::step],
    angles="xy",
    scale_units="xy",
    scale=1.0,
    cmap="plasma",
    width=0.003,
    alpha=0.75
)

# escape candidates highlighted
ax1.scatter(
    x[escape_mask],
    y[escape_mask],
    facecolors="none",
    edgecolors="black",
    s=120,
    linewidths=1.5,
    label="Escape candidates"
)

# event markers
for ev in classical_events:
    if 0 <= ev < len(x):
        ax1.scatter(x[ev], y[ev], color="red", s=55, marker="x")

# start / end / center
ax1.scatter(x[0], y[0], color="green", s=100, label="Start")
ax1.scatter(x[-1], y[-1], color="red", s=100, label="End")
ax1.scatter(x0, y0, color="gold", s=160, marker="*", label="Stability center")

ax1.set_title("NEXAH Basin + Escape Direction (Cartesian)")
ax1.set_xlabel("Coherence")
ax1.set_ylabel("Switch signal")
ax1.grid(True)
ax1.legend(loc="best")

cbar1 = plt.colorbar(sc1, ax=ax1)
cbar1.set_label("Basin score")


# =========================
# 5. Polar basin / escape plot
# =========================

radius = 1.0 - x
radius = (radius - radius.min()) / (radius.max() - radius.min() + eps)
theta = np.linspace(0, 2 * np.pi * 3, len(radius))

fig2 = plt.figure(figsize=(10, 10))
ax2 = fig2.add_subplot(111, projection="polar")

# all points colored by escape score
sc2 = ax2.scatter(
    theta,
    radius,
    c=escape_score,
    cmap="magma",
    s=30,
    alpha=0.9
)

# smoothed orbit
ax2.plot(theta, radius, color="steelblue", linewidth=1.6, alpha=0.5)

# mark escape candidates
ax2.scatter(
    theta[escape_mask],
    radius[escape_mask],
    facecolors="none",
    edgecolors="cyan",
    s=120,
    linewidths=1.5,
    label="Escape candidates"
)

# arrow annotations at escape points
for i in np.where(escape_mask)[0][::2]:
    th0 = theta[i]
    r0 = radius[i]
    th1 = th0 + 0.10 * np.sign(tangential_velocity[i] if tangential_velocity[i] != 0 else 1.0)
    r1 = max(0.0, r0 + 0.10 * np.sign(radial_velocity[i] if radial_velocity[i] != 0 else 1.0))
    ax2.annotate(
        "",
        xy=(th1, r1),
        xytext=(th0, r0),
        arrowprops=dict(arrowstyle="->", lw=1.2, alpha=0.8, color="cyan"),
    )

# markers
ax2.scatter(theta[0], radius[0], color="green", s=120, label="Start")
ax2.scatter(theta[-1], radius[-1], color="red", s=120, label="End")

for ev in classical_events:
    if 0 <= ev < len(theta):
        ax2.scatter(theta[ev], radius[ev], color="black", s=55, marker="x")

ax2.set_title("NEXAH Basin + Escape Direction (Polar)")
ax2.legend(loc="upper right")

cbar2 = plt.colorbar(sc2, pad=0.1)
cbar2.set_label("Escape score")


# =========================
# 6. Save
# =========================

save_dir = Path("APPLICATIONS/power_systems/ieee_xray_pipeline/results")
save_dir.mkdir(parents=True, exist_ok=True)

fig1.savefig(save_dir / "ieee57_v8_basin_escape_cartesian.png", dpi=200)
fig2.savefig(save_dir / "ieee57_v8_basin_escape_polar.png", dpi=200)

plt.close(fig1)
plt.close(fig2)

print("\nSaved:")
print("  • ieee57_v8_basin_escape_cartesian.png")
print("  • ieee57_v8_basin_escape_polar.png")
