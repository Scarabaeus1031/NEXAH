# ============================================================
# v55_aperture_crossing_engine.py
# NEXAH – Aperture Crossing Engine
# ============================================================

import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp

# ============================================================
# SCRIPT NAME
# ============================================================
SCRIPT_NAME = "v55_aperture_crossing_engine.py"

# ============================================================
# PATHS
# ============================================================
OUTDIR = Path("./results")
OUTDIR.mkdir(parents=True, exist_ok=True)

TS_PATH = OUTDIR / "v55_timeseries.png"
POLAR_PATH = OUTDIR / "v55_polar.png"
REPORT_PATH = OUTDIR / "v55_report.txt"

print(f"\n📁 v55 running → {OUTDIR.resolve()}\n")
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

residue_floor = -1.0 / 12.0
lift_levels = np.array([
    residue_floor * np.sqrt(2),
    residue_floor * np.sqrt(3),
    residue_floor * np.sqrt(5),
    residue_floor * np.sqrt(7),
])

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

def softmax(x, temperature=1.0):
    x = np.asarray(x) / temperature
    z = x - np.max(x)
    ez = np.exp(z)
    s = np.sum(ez)
    if s <= 0:
        return np.ones_like(ez) / len(ez)
    return ez / s

def aperture_kernel(theta, center, width):
    err = wrap_angle(theta - center)
    return np.exp(-(err ** 2) / (2.0 * width ** 2))

def sector_name(i):
    return f"sector_{i}"

# ============================================================
# GRID
# ============================================================
np.random.seed(42)
rng = np.random.default_rng(42)

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
    "u_explore": [],
    "target_angle": [],
    "target_radius": [],
    "sector": [],
    "switch_event": [],
    "aperture_event": [],
    "aperture_strength": [],
    "memory_bias": [],
    "residue_target": [],
    "cooldown": [],
}

# ============================================================
# SETTINGS
# ============================================================
T = 400

theta_ref = -np.pi / 2
target_radius_base = 0.86

k_r = 0.14
k_theta = 0.030
k_lock = 0.075
k_attractor = 0.050
k_drift = 0.012
k_memory = 0.020
k_aperture = 0.060

u_clip = 0.14
load_gain = 0.08

switch_cooldown_steps = 12
switch_closure_threshold = 0.56
base_switch_window = 0.20
aperture_width = 0.22

# exploration
explore_amp = 0.012

# memory
memory_decay = 0.97
memory_gain = 0.020
memory_cap = 1.0

# aperture location between sectors 4 and 5
aperture_center = wrap_angle(0.5 * (sector_angles[4] + sector_angles[5]))

# ============================================================
# INTERNAL STATE
# ============================================================
current_sector = 4
cooldown = 0
sector_memory = np.zeros(N_SECTORS)
sector_visits = np.zeros(N_SECTORS, dtype=int)

# ============================================================
# LOOP
# ============================================================
for t in range(T):
    print(f"step {t}")

    try:
        pp.runpp(net, max_iteration=20)
    except Exception:
        print("⚠️ PF failed → reset/damp")
        net.load.p_mw = base_p * 0.97
        net.load.q_mvar = base_q * 0.97
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

    lift_idx = (t // 100) % len(lift_levels)
    residue_target = lift_levels[lift_idx]

    sector_radii = np.array([
        target_radius_base
        + 0.05 * np.sin(0.018 * t + i * 0.8)
        + 0.02 * np.cos(0.011 * t + i * 0.5)
        for i in range(N_SECTORS)
    ])

    angle_errors = np.array([abs(wrap_angle(theta - a)) for a in sector_angles])
    radial_costs = np.abs(r - sector_radii)

    angle_scores = -4.0 * angle_errors
    radial_scores = -2.7 * radial_costs
    memory_scores = 0.22 * sector_memory

    sector_scores = angle_scores + radial_scores + memory_scores

    current_angle = sector_angles[current_sector]
    current_radius = sector_radii[current_sector]

    aperture_strength = aperture_kernel(theta, aperture_center, aperture_width)
    aperture_event = 1 if aperture_strength > 0.60 else 0

    closure_probe = (
        0.40 * prox
        + 0.25 * np.exp(-4.0 * np.abs(r - current_radius))
        + 0.20 * np.exp(-4.5 * abs(wrap_angle(theta - current_angle)))
        + 0.15 * aperture_strength
    )

    switch_event = 0

    # wider switching window near aperture
    dynamic_switch_window = base_switch_window + 0.12 * aperture_strength

    can_switch = (
        cooldown <= 0
        and closure_probe > switch_closure_threshold
        and (
            abs(wrap_angle(theta - current_angle)) < dynamic_switch_window
            or aperture_strength > 0.65
        )
    )

    if can_switch:
        probs = softmax(sector_scores, temperature=0.65)

        # lower stay bias than v54
        stay_boost = 0.15
        probs = probs * (1.0 - stay_boost)
        probs[current_sector] += stay_boost

        # explicit aperture crossing preference:
        # when close to aperture and in sector 4 or 5, boost the neighbor
        if aperture_strength > 0.55:
            if current_sector == 4:
                probs[5] += 0.30 * aperture_strength
            elif current_sector == 5:
                probs[4] += 0.30 * aperture_strength
            else:
                # weak global boost toward nearest aperture-adjacent sectors
                probs[4] += 0.10 * aperture_strength
                probs[5] += 0.10 * aperture_strength

        probs = np.clip(probs, 1e-9, None)
        probs = probs / probs.sum()

        new_sector = int(rng.choice(np.arange(N_SECTORS), p=probs))
        if new_sector != current_sector:
            current_sector = new_sector
            cooldown = switch_cooldown_steps
            switch_event = 1

    if cooldown > 0:
        cooldown -= 1

    current_angle = sector_angles[current_sector]
    current_radius = sector_radii[current_sector]

    # ========================================================
    # MEMORY
    # ========================================================
    sector_memory *= memory_decay
    sector_memory[current_sector] += memory_gain * prox
    sector_memory = np.clip(sector_memory, 0.0, memory_cap)
    sector_visits[current_sector] += 1

    # ========================================================
    # CONTROL TERMS
    # ========================================================
    u_ieee = -k_r * (r - current_radius)
    u_theta = -k_theta * np.sin(wrap_angle(theta - theta_ref))

    shell_target = shells[1] if prox < 0.88 else shells[0]
    u_lock = -k_lock * (z - shell_target)

    u_breath = -0.008 * (r - current_radius) * (0.3 + 0.7 * prox)
    u_attractor = k_attractor * np.sin(wrap_angle(current_angle - theta))

    u_drift = k_drift * np.sign(wrap_angle(theta - current_angle))
    if abs(wrap_angle(theta - current_angle)) < 0.14:
        u_drift *= 0.35

    u_memory = k_memory * np.tanh(sector_memory[current_sector] - 0.20)

    # the new piece
    aperture_pull_direction = np.sign(wrap_angle(aperture_center - theta))
    u_aperture = k_aperture * aperture_strength * aperture_pull_direction

    # exploration term
    u_explore = explore_amp * np.sin(0.035 * t + 1.7)

    u = (
        u_ieee
        + u_theta
        + u_lock
        + u_breath
        + u_attractor
        + u_drift
        + u_memory
        + u_aperture
        + u_explore
    )

    if t < 10:
        u = 0.0

    if prox > 0.20:
        u *= (0.92 + 0.06 * np.sin(0.025 * t))

    u = np.clip(u, -u_clip, u_clip)

    factor = 1.0 + u * load_gain
    factor = np.clip(factor, 0.94, 1.06)

    net.load.p_mw = base_p * factor
    net.load.q_mvar = base_q * factor

    closure = (
        0.35 * prox
        + 0.22 * np.exp(-4.0 * abs(r - current_radius))
        + 0.18 * np.exp(-4.5 * abs(wrap_angle(theta - current_angle)))
        + 0.10 * np.tanh(sector_memory[current_sector])
        + 0.15 * aperture_strength
    )

    # ========================================================
    # STORE
    # ========================================================
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
    data["u_explore"].append(u_explore)

    data["target_angle"].append(current_angle)
    data["target_radius"].append(current_radius)
    data["sector"].append(current_sector)
    data["switch_event"].append(switch_event)
    data["aperture_event"].append(aperture_event)
    data["aperture_strength"].append(aperture_strength)
    data["memory_bias"].append(sector_memory[current_sector])
    data["residue_target"].append(residue_target)
    data["cooldown"].append(cooldown)

# ============================================================
# REPORT
# ============================================================
sector_counts = {
    sector_name(i): int(np.sum(np.array(data["sector"]) == i))
    for i in range(N_SECTORS)
}

report = f"""NEXAH v55 – Aperture Crossing Engine
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
Mean explore term: {safe_mean(data['u_explore']):.4f}

Switch count: {int(np.sum(data['switch_event']))}
Aperture events: {int(np.sum(data['aperture_event']))}

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
fig, axs = plt.subplots(10, 1, figsize=(13, 22), sharex=True)

axs[0].plot(data["voltage"])
axs[0].set_title("Voltage")

axs[1].plot(data["coherence"])
axs[1].set_title("Coherence")

axs[2].plot(data["radius"], label="radius")
axs[2].plot(data["target_radius"], label="target radius", alpha=0.8)
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
axs[8].plot(data["aperture_event"], label="aperture event")
axs[8].legend()
axs[8].set_title("Events")

axs[9].plot(data["u"], label="u")
axs[9].plot(data["u_ieee"], label="u_ieee", alpha=0.7)
axs[9].plot(data["u_lock"], label="u_lock", alpha=0.7)
axs[9].plot(data["u_breath"], label="u_breath", alpha=0.7)
axs[9].plot(data["u_attractor"], label="u_attractor", alpha=0.7)
axs[9].plot(data["u_drift"], label="u_drift", alpha=0.7)
axs[9].plot(data["u_memory"], label="u_memory", alpha=0.7)
axs[9].plot(data["u_aperture"], label="u_aperture", alpha=0.7)
axs[9].plot(data["u_explore"], label="u_explore", alpha=0.7)
axs[9].legend(ncol=5)

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
ap_idx = np.where(np.array(data["aperture_event"]) > 0)[0]

ax.plot(theta_vals, r_vals, color="steelblue", alpha=0.75, label="IEEE trajectory")
ax.plot(target_angles, target_radii, color="magenta", alpha=0.65, label="target path")

sc = ax.scatter(theta_vals, r_vals, c=prox_vals, cmap="plasma", s=18, label="OLGO prox")

if len(switch_idx) > 0:
    ax.scatter(theta_vals[switch_idx], r_vals[switch_idx], color="green", s=35, label="switch")
if len(ap_idx) > 0:
    ax.scatter(theta_vals[ap_idx], r_vals[ap_idx], color="red", s=18, alpha=0.7, label="aperture")

for a in sector_angles:
    ax.plot([a, a], [0, 1.2], color="gray", alpha=0.18)

ax.plot([aperture_center, aperture_center], [0, 1.2], color="red", alpha=0.35, linestyle="--")

ax.set_title("v55 Aperture Crossing Engine Polar")
ax.legend(loc="upper right")
fig.colorbar(sc, pad=0.12)
fig.savefig(POLAR_PATH, dpi=150, bbox_inches="tight")
plt.close(fig)

print("✅ v55 finished")
print(f"📊 Saved: {TS_PATH}")
print(f"📊 Saved: {POLAR_PATH}")
print(f"📄 Saved: {REPORT_PATH}")
