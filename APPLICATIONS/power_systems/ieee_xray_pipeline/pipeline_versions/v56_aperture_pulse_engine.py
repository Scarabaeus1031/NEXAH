# ============================================================
# v56_aperture_pulse_engine.py
# NEXAH – Aperture Pulse Engine
# ============================================================

import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# ============================================================
# SCRIPT NAME
# ============================================================
SCRIPT_NAME = "v56_aperture_pulse_engine.py"

# ============================================================
# PATHS
# ============================================================
OUTDIR = Path("./results")
OUTDIR.mkdir(parents=True, exist_ok=True)

TS_PATH = OUTDIR / "v56_timeseries.png"
POLAR_PATH = OUTDIR / "v56_polar.png"
CUBE_PATH = OUTDIR / "v56_3d.png"
HEXA_PATH = OUTDIR / "v56_hexa_topology.png"
REPORT_PATH = OUTDIR / "v56_report.txt"

print(f"\n📁 v56 running → {OUTDIR.resolve()}\n")
print(f"▶ Script: {SCRIPT_NAME}\n")

# ============================================================
# HELPERS
# ============================================================
phi = (1 + np.sqrt(5)) / 2
pi = np.pi

f0 = (phi ** 3) / (pi ** 2)
epsilon = 0.029
shells = np.array([f0, f0 + epsilon, f0 + 2 * epsilon])
shell_names = ["Core", "Transition", "Expansion"]

N_SECTORS = 6
sector_angles = np.linspace(0, 2 * np.pi, N_SECTORS, endpoint=False)

def wrap_angle(a):
    return (a + np.pi) % (2 * np.pi) - np.pi

def olgo_proximity(z, sharpness=80.0):
    d = np.min(np.abs(shells - z))
    return np.exp(-sharpness * d)

def nearest_shell(z):
    idx = np.argmin(np.abs(shells - z))
    return shells[idx], idx

def safe_mean(x):
    return float(np.mean(x)) if len(x) else 0.0

def safe_max(x):
    return float(np.max(x)) if len(x) else 0.0

def aperture_kernel(theta, center, width):
    err = wrap_angle(theta - center)
    return np.exp(-(err ** 2) / (2.0 * width ** 2))

def sector_name(i):
    return f"sector_{i}"

def phase_to_sector(phase):
    a = (phase + 2 * np.pi) % (2 * np.pi)
    return int(np.floor(a / (2 * np.pi / N_SECTORS))) % N_SECTORS

# ============================================================
# GRID
# ============================================================
np.random.seed(42)

net = pp.networks.case57()
net.load.p_mw *= 0.85
net.load.q_mvar *= 0.85

base_p = net.load.p_mw.copy()
base_q = net.load.q_mvar.copy()

# ============================================================
# STORAGE
# ============================================================
data = {
    "voltage": [],
    "coherence": [],
    "radius": [],
    "theta": [],
    "z": [],
    "prox": [],
    "closure": [],
    "u": [],
    "u_ieee": [],
    "u_theta": [],
    "u_lock": [],
    "u_breath": [],
    "u_attractor": [],
    "u_drift": [],
    "u_memory": [],
    "u_aperture": [],
    "target_angle": [],
    "target_radius": [],
    "sector": [],
    "switch_event": [],
    "aperture_window": [],
    "aperture_pulse": [],
    "aperture_strength": [],
    "memory_bias": [],
    "cooldown": [],
    "x": [],
    "y": [],
    "hx": [],
    "hy": [],
    "hz": [],
}

# ============================================================
# SETTINGS
# ============================================================
T = 400

theta_ref = -np.pi / 2
target_radius_base = 0.86

# controller gains
k_r = 0.11
k_theta = 0.020
k_lock = 0.060
k_attractor = 0.038
k_drift = 0.008
k_memory = 0.010
k_aperture = 0.028

u_clip = 0.10
load_gain = 0.07

# switching / aperture
switch_closure_threshold = 0.595
aperture_center = wrap_angle(0.5 * (sector_angles[4] + sector_angles[5]))
aperture_width = 0.065
switch_window = 0.075
cooldown_steps = 28
pulse_steps = 4
pulse_decay = 0.78

# breathing / memory
memory_decay = 0.985
memory_gain = 0.010
memory_cap = 1.0

# ============================================================
# INTERNAL STATE
# ============================================================
current_sector = 4
cooldown = 0
pulse_timer = 0
pulse_sign = 0.0
sector_memory = np.zeros(N_SECTORS)
prev_theta = None

# ============================================================
# LOOP
# ============================================================
for t in range(T):
    print(f"step {t}")

    try:
        pp.runpp(net, max_iteration=30)
    except Exception:
        print("⚠️ PF failed → reset/damp")
        net.load.p_mw = base_p * 0.985
        net.load.q_mvar = base_q * 0.985
        continue

    vm = net.res_bus.vm_pu.values
    v_mean = np.mean(vm)

    coh = 1.0 - np.std(vm)
    sw = (v_mean - 1.0) * 10.0

    r = np.hypot(coh - 0.942913, sw - 0.000076)
    theta = wrap_angle(np.arctan2(sw - 0.000076, coh - 0.942913))

    z = 0.5 * coh + 0.5 * (1.0 - abs(sw))
    prox = olgo_proximity(z)
    _, shell_idx = nearest_shell(z)

    # --------------------------------------------------------
    # target shell / sector geometry
    # --------------------------------------------------------
    sector_radii = np.array([
        target_radius_base
        + 0.045 * np.sin(0.020 * t + i * 0.70)
        + 0.015 * np.cos(0.012 * t + i * 0.35)
        for i in range(N_SECTORS)
    ])

    current_angle = sector_angles[current_sector]
    current_radius = sector_radii[current_sector]

    # --------------------------------------------------------
    # aperture logic: local only
    # --------------------------------------------------------
    aperture_strength = aperture_kernel(theta, aperture_center, aperture_width)
    in_aperture_window = 1 if aperture_strength > 0.42 else 0

    theta_err_ap = abs(wrap_angle(theta - aperture_center))
    theta_err_sec = abs(wrap_angle(theta - current_angle))

    crossing_ready = (
        cooldown <= 0
        and theta_err_ap < switch_window
        and prox > 0.69
        and prev_theta is not None
    )

    crossed_direction = 0
    if prev_theta is not None:
        prev_side = np.sign(wrap_angle(prev_theta - aperture_center))
        curr_side = np.sign(wrap_angle(theta - aperture_center))
        if prev_side != 0 and curr_side != 0 and prev_side != curr_side:
            crossed_direction = 1

    closure = (
        0.36 * prox
        + 0.26 * np.exp(-4.0 * abs(r - current_radius))
        + 0.18 * np.exp(-6.0 * theta_err_sec)
        + 0.10 * np.tanh(sector_memory[current_sector])
        + 0.10 * aperture_strength
    )

    switch_event = 0
    aperture_pulse = 0

    if crossing_ready and crossed_direction and closure > switch_closure_threshold:
        if current_sector == 4:
            current_sector = 5
            pulse_sign = +1.0
        elif current_sector == 5:
            current_sector = 4
            pulse_sign = -1.0
        else:
            # fallback to nearest aperture-adjacent sector
            current_sector = 4 if wrap_angle(theta - aperture_center) < 0 else 5
            pulse_sign = np.sign(wrap_angle(aperture_center - theta))

        switch_event = 1
        aperture_pulse = 1
        cooldown = cooldown_steps
        pulse_timer = pulse_steps

    if cooldown > 0:
        cooldown -= 1

    # after a switch, recompute target
    current_angle = sector_angles[current_sector]
    current_radius = sector_radii[current_sector]

    # --------------------------------------------------------
    # memory
    # --------------------------------------------------------
    sector_memory *= memory_decay
    sector_memory[current_sector] += memory_gain * prox
    sector_memory = np.clip(sector_memory, 0.0, memory_cap)

    # --------------------------------------------------------
    # controller terms
    # --------------------------------------------------------
    u_ieee = -k_r * (r - current_radius)
    u_theta = -k_theta * np.sin(wrap_angle(theta - theta_ref))

    shell_target = shells[1] if prox < 0.86 else shells[0]
    u_lock = -k_lock * (z - shell_target)

    u_breath = -0.006 * (r - current_radius)
    u_attractor = k_attractor * np.sin(wrap_angle(current_angle - theta))
    u_drift = k_drift * np.sign(wrap_angle(theta - current_angle))
    if abs(wrap_angle(theta - current_angle)) < 0.10:
        u_drift *= 0.25

    u_memory = k_memory * np.tanh(sector_memory[current_sector] - 0.18)

    # pulse only, no permanent magnet
    if pulse_timer > 0:
        u_aperture = k_aperture * pulse_sign * (pulse_decay ** (pulse_steps - pulse_timer))
        pulse_timer -= 1
    else:
        u_aperture = 0.0

    u = (
        u_ieee
        + u_theta
        + u_lock
        + u_breath
        + u_attractor
        + u_drift
        + u_memory
        + u_aperture
    )

    if t < 10:
        u = 0.0

    if prox > 0.20:
        u *= 0.92

    u = np.clip(u, -u_clip, u_clip)

    factor = 1.0 + u * load_gain
    factor = np.clip(factor, 0.95, 1.05)

    net.load.p_mw = base_p * factor
    net.load.q_mvar = base_q * factor

    # --------------------------------------------------------
    # geometry for visuals
    # --------------------------------------------------------
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    hx = current_radius * np.cos(current_angle)
    hy = current_radius * np.sin(current_angle)
    hz = z

    # --------------------------------------------------------
    # store
    # --------------------------------------------------------
    data["voltage"].append(v_mean)
    data["coherence"].append(coh)
    data["radius"].append(r)
    data["theta"].append(theta)
    data["z"].append(z)
    data["prox"].append(prox)
    data["closure"].append(closure)

    data["u"].append(u)
    data["u_ieee"].append(u_ieee)
    data["u_theta"].append(u_theta)
    data["u_lock"].append(u_lock)
    data["u_breath"].append(u_breath)
    data["u_attractor"].append(u_attractor)
    data["u_drift"].append(u_drift)
    data["u_memory"].append(u_memory)
    data["u_aperture"].append(u_aperture)

    data["target_angle"].append(current_angle)
    data["target_radius"].append(current_radius)
    data["sector"].append(current_sector)

    data["switch_event"].append(switch_event)
    data["aperture_window"].append(in_aperture_window)
    data["aperture_pulse"].append(aperture_pulse)
    data["aperture_strength"].append(aperture_strength)
    data["memory_bias"].append(sector_memory[current_sector])
    data["cooldown"].append(cooldown)

    data["x"].append(x)
    data["y"].append(y)
    data["hx"].append(hx)
    data["hy"].append(hy)
    data["hz"].append(hz)

    prev_theta = theta

# ============================================================
# REPORT
# ============================================================
sector_counts = {
    sector_name(i): int(np.sum(np.array(data["sector"]) == i))
    for i in range(N_SECTORS)
}

report = f"""NEXAH v56 – Aperture Pulse Engine
Script: {SCRIPT_NAME}

Mean voltage: {safe_mean(data['voltage']):.4f}
Mean coherence: {safe_mean(data['coherence']):.4f}
Mean radius: {safe_mean(data['radius']):.4f}

Final voltage: {data['voltage'][-1] if data['voltage'] else 0.0:.4f}
Final coherence: {data['coherence'][-1] if data['coherence'] else 0.0:.4f}
Final radius: {data['radius'][-1] if data['radius'] else 0.0:.4f}

Mean OLGO proximity: {safe_mean(data['prox']):.4f}
Max OLGO proximity: {safe_max(data['prox']):.4f}

Mean closure metric: {safe_mean(data['closure']):.4f}
Max closure metric: {safe_max(data['closure']):.4f}

Mean control signal: {safe_mean(data['u']):.4f}
Mean attractor term: {safe_mean(data['u_attractor']):.4f}
Mean drift term: {safe_mean(data['u_drift']):.4f}
Mean memory term: {safe_mean(data['u_memory']):.4f}
Mean aperture term: {safe_mean(data['u_aperture']):.4f}

Switch count: {int(np.sum(data['switch_event']))}
Aperture windows: {int(np.sum(data['aperture_window']))}
Aperture pulses: {int(np.sum(data['aperture_pulse']))}

Sector occupancy:
  sector_0: {sector_counts['sector_0']}
  sector_1: {sector_counts['sector_1']}
  sector_2: {sector_counts['sector_2']}
  sector_3: {sector_counts['sector_3']}
  sector_4: {sector_counts['sector_4']}
  sector_5: {sector_counts['sector_5']}
"""

REPORT_PATH.write_text(report, encoding="utf-8")
print("\n" + report)

# ============================================================
# TIMESERIES
# ============================================================
fig, axs = plt.subplots(10, 1, figsize=(14, 24), sharex=True)

axs[0].plot(data["voltage"])
axs[0].set_title("Voltage")

axs[1].plot(data["coherence"])
axs[1].set_title("Coherence")

axs[2].plot(data["radius"], label="radius")
axs[2].plot(data["target_radius"], label="target radius")
axs[2].legend()
axs[2].set_title("Radius")

axs[3].plot(data["prox"])
axs[3].set_title("OLGO Proximity")

axs[4].plot(data["closure"])
axs[4].axhline(switch_closure_threshold, color="red", linestyle="--", alpha=0.5)
axs[4].set_title("Closure Metric")

axs[5].plot(data["sector"])
axs[5].set_title("Active Sector")

axs[6].plot(data["memory_bias"])
axs[6].set_title("Memory Bias")

axs[7].plot(data["aperture_strength"])
axs[7].set_title("Aperture Strength")

axs[8].plot(data["switch_event"], label="switch")
axs[8].plot(data["aperture_window"], label="aperture window")
axs[8].plot(data["aperture_pulse"], label="pulse")
axs[8].legend()
axs[8].set_title("Events")

axs[9].plot(data["u"], label="u")
axs[9].plot(data["u_ieee"], label="u_ieee", alpha=0.8)
axs[9].plot(data["u_lock"], label="u_lock", alpha=0.8)
axs[9].plot(data["u_breath"], label="u_breath", alpha=0.8)
axs[9].plot(data["u_attractor"], label="u_attractor", alpha=0.8)
axs[9].plot(data["u_drift"], label="u_drift", alpha=0.8)
axs[9].plot(data["u_memory"], label="u_memory", alpha=0.8)
axs[9].plot(data["u_aperture"], label="u_aperture", alpha=0.8)
axs[9].legend(ncol=4)

plt.tight_layout()
plt.savefig(TS_PATH, dpi=150)
plt.close()

# ============================================================
# POLAR
# ============================================================
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="polar")

theta_vals = np.array(data["theta"])
r_vals = np.array(data["radius"])
prox_vals = np.array(data["prox"])
target_angles = np.array(data["target_angle"])
target_radii = np.array(data["target_radius"])
switch_idx = np.where(np.array(data["switch_event"]) > 0)[0]
ap_idx = np.where(np.array(data["aperture_window"]) > 0)[0]

ax.plot(theta_vals, r_vals, color="steelblue", alpha=0.75, label="IEEE trajectory")
ax.plot(target_angles, target_radii, color="magenta", alpha=0.65, label="target path")
sc = ax.scatter(theta_vals, r_vals, c=prox_vals, cmap="plasma", s=18, label="OLGO prox")

if len(switch_idx) > 0:
    ax.scatter(theta_vals[switch_idx], r_vals[switch_idx], color="green", s=40, label="switch")
if len(ap_idx) > 0:
    ax.scatter(theta_vals[ap_idx], r_vals[ap_idx], color="red", s=12, alpha=0.6, label="aperture")

for a in sector_angles:
    ax.plot([a, a], [0, 1.2], color="gray", alpha=0.15)

ax.plot([aperture_center, aperture_center], [0, 1.2], color="red", linestyle="--", alpha=0.35)
ax.set_title("v56 Aperture Pulse Engine Polar")
ax.legend(loc="upper right")
fig.colorbar(sc, pad=0.12)
fig.savefig(POLAR_PATH, dpi=150, bbox_inches="tight")
plt.close(fig)

# ============================================================
# 3D
# ============================================================
fig = plt.figure(figsize=(11, 9))
ax = fig.add_subplot(111, projection="3d")

x = np.array(data["x"])
y = np.array(data["y"])
z = np.array(data["z"])
prox_vals = np.array(data["prox"])

sc = ax.scatter(x, y, z, c=prox_vals, cmap="plasma", s=10)

# aperture axis
ax.plot(
    [0.0, np.cos(aperture_center)],
    [0.0, np.sin(aperture_center)],
    [np.min(z), np.max(z)],
    color="red",
    linestyle="--",
    alpha=0.5,
)

# hexa target markers
hx = np.array(data["hx"])
hy = np.array(data["hy"])
hz = np.array(data["hz"])
ax.plot(hx, hy, hz, color="magenta", alpha=0.7, linewidth=1.2)

ax.set_title("v56 Aperture Pulse Engine 3D")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("OLGO z")
fig.colorbar(sc, pad=0.08)
fig.savefig(CUBE_PATH, dpi=150, bbox_inches="tight")
plt.close(fig)

# ============================================================
# HEXA STYLE TOPOLOGY
# ============================================================
fig, ax = plt.subplots(figsize=(8, 8))

hex_nodes = np.array([(np.cos(a), np.sin(a)) for a in sector_angles])

# outer hexagon
for i in range(N_SECTORS):
    j = (i + 1) % N_SECTORS
    ax.plot(
        [hex_nodes[i, 0], hex_nodes[j, 0]],
        [hex_nodes[i, 1], hex_nodes[j, 1]],
        color="gray",
        linewidth=2.0,
    )

# spokes
for i in range(N_SECTORS):
    ax.plot(
        [0.0, hex_nodes[i, 0]],
        [0.0, hex_nodes[i, 1]],
        color="lightgray",
        linewidth=1.5,
    )

# nodes
for i in range(N_SECTORS):
    ax.scatter(hex_nodes[i, 0], hex_nodes[i, 1], s=250, color="skyblue", edgecolor="none")
    ax.text(hex_nodes[i, 0] * 1.12, hex_nodes[i, 1] * 1.12, str(i), ha="center", va="center", fontsize=18)

# center
ax.scatter(0, 0, s=350, color="hotpink")
ax.text(0, 0, "Q°", color="white", ha="center", va="center", fontsize=16, fontweight="bold")

# sector 4<->5 aperture bridge
p4 = hex_nodes[4] * 0.52
p5 = hex_nodes[5] * 0.52
ax.plot([p4[0], p5[0]], [p4[1], p5[1]], color="magenta", linewidth=3, alpha=0.8)

# active visits
sector_array = np.array(data["sector"])
for i in range(N_SECTORS):
    count = np.sum(sector_array == i)
    size = 100 + 4 * count
    ax.scatter(hex_nodes[i, 0], hex_nodes[i, 1], s=size, facecolors="none", edgecolors="mediumpurple", linewidths=2)

ax.set_title("v56 Hexa Aperture Topology")
ax.set_aspect("equal")
ax.axis("off")
fig.savefig(HEXA_PATH, dpi=150, bbox_inches="tight")
plt.close(fig)

print("✅ v56 finished")
print(f"📊 Saved: {TS_PATH}")
print(f"📊 Saved: {POLAR_PATH}")
print(f"📊 Saved: {CUBE_PATH}")
print(f"📊 Saved: {HEXA_PATH}")
print(f"📄 Saved: {REPORT_PATH}")
