# ============================================================
# v54_multi_attractor_navigation.py
# NEXAH – Multi Attractor Navigation Engine
# ============================================================

import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandapower as pp

# ============================================================
# PATHS
# ============================================================
OUTDIR = Path("./results")
OUTDIR.mkdir(parents=True, exist_ok=True)

TS_PATH = OUTDIR / "v54_timeseries.png"
POLAR_PATH = OUTDIR / "v54_polar.png"
REPORT_PATH = OUTDIR / "v54_report.txt"

print(f"\n📁 v54 running → {OUTDIR.resolve()}\n")

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

# residue anchor / lift levels inspired by your -1/12 structure
residue_floor = -1.0 / 12.0
lift_levels = np.array([
    residue_floor * np.sqrt(2),
    residue_floor * np.sqrt(3),
    residue_floor * np.sqrt(5),
    residue_floor * np.sqrt(7),
])

def olgo_proximity(z, sharpness=80.0):
    d = np.min(np.abs(shells - z))
    return np.exp(-sharpness * d)

def nearest_shell(z):
    idx = np.argmin(np.abs(shells - z))
    return shells[idx], idx

def wrap_angle(a):
    return (a + np.pi) % (2 * np.pi) - np.pi

def safe_mean(x):
    return float(np.mean(x)) if len(x) else 0.0

def safe_max(x):
    return float(np.max(x)) if len(x) else 0.0

def phase_to_sector(theta):
    a = (theta + 2 * np.pi) % (2 * np.pi)
    return int(np.floor(a / (2 * np.pi / N_SECTORS))) % N_SECTORS

def softmax(x, temperature=1.0):
    x = np.asarray(x) / temperature
    z = x - np.max(x)
    ez = np.exp(z)
    s = np.sum(ez)
    if s <= 0:
        return np.ones_like(ez) / len(ez)
    return ez / s

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
    "u": [],
    "u_ieee": [],
    "u_theta": [],
    "u_lock": [],
    "u_breath": [],
    "u_attractor": [],
    "u_drift": [],
    "u_memory": [],
    "closure": [],
    "target_angle": [],
    "target_radius": [],
    "sector": [],
    "switch_event": [],
    "residue_target": [],
    "memory_bias": [],
}

# ============================================================
# SETTINGS
# ============================================================
T = 400

theta_ref = -np.pi / 2

# boundary attractor shell
target_radius_base = 0.86

k_r = 0.16
k_theta = 0.035
k_lock = 0.08
k_attractor = 0.055
k_drift = 0.015
k_memory = 0.030

u_clip = 0.14
load_gain = 0.08

# navigation / switching
switch_cooldown_steps = 18
switch_closure_threshold = 0.60
switch_angle_window = 0.16

# ============================================================
# INTERNAL STATE
# ============================================================
current_sector = 4
cooldown = 0

# sector memory: preferred revisits / persistence
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

    # --------------------------------------------------------
    # Multi-attractor evaluation
    # --------------------------------------------------------
    angle_errors = np.array([abs(wrap_angle(theta - a)) for a in sector_angles])

    # dynamic residue / lift target
    lift_idx = (t // 100) % len(lift_levels)
    residue_target = lift_levels[lift_idx]

    # per-sector boundary radii with small breathing offsets
    sector_radii = np.array([
        target_radius_base
        + 0.05 * np.sin(0.018 * t + i * 0.8)
        + 0.02 * np.cos(0.011 * t + i * 0.5)
        for i in range(N_SECTORS)
    ])

    # score each sector:
    # smaller angle error better
    # radius fit better
    # memory can bias revisits
    radial_costs = np.abs(r - sector_radii)
    angle_scores = -4.5 * angle_errors
    radial_scores = -3.0 * radial_costs
    memory_scores = 0.30 * sector_memory

    sector_scores = angle_scores + radial_scores + memory_scores

    # choose sector probabilistically when allowed
    switch_event = 0

    closure_probe = (
        0.45 * prox
        + 0.30 * np.exp(-4.0 * np.abs(r - sector_radii[current_sector]))
        + 0.25 * np.exp(-5.0 * abs(wrap_angle(theta - sector_angles[current_sector])))
    )

    can_switch = (
        cooldown <= 0
        and closure_probe > switch_closure_threshold
        and abs(wrap_angle(theta - sector_angles[current_sector])) < switch_angle_window
    )

    if can_switch:
        probs = softmax(sector_scores, temperature=0.55)

        # avoid trivial staying only
        stay_boost = 0.55
        probs = probs * (1.0 - stay_boost)
        probs[current_sector] += stay_boost
        probs = probs / probs.sum()

        new_sector = int(np.random.choice(np.arange(N_SECTORS), p=probs))
        if new_sector != current_sector:
            current_sector = new_sector
            cooldown = switch_cooldown_steps
            switch_event = 1

    if cooldown > 0:
        cooldown -= 1

    attractor_angle = sector_angles[current_sector]
    attractor_radius = sector_radii[current_sector]

    # --------------------------------------------------------
    # Memory field
    # --------------------------------------------------------
    # decay all, reinforce current
    sector_memory *= 0.985
    sector_memory[current_sector] += 0.05 * prox
    sector_memory = np.clip(sector_memory, 0.0, 2.0)

    sector_visits[current_sector] += 1

    # --------------------------------------------------------
    # Control terms
    # --------------------------------------------------------
    # pull to selected boundary attractor, not center
    u_ieee = -k_r * (r - attractor_radius)

    # weak structural axis
    u_theta = -k_theta * np.sin(wrap_angle(theta - theta_ref))

    # shell lock
    shell_target = shells[1] if prox < 0.9 else shells[0]
    u_lock = -k_lock * (z - shell_target)

    # weak breathing inside chosen shell
    u_breath = -0.008 * (r - attractor_radius) * (0.3 + 0.7 * prox)

    # attractor pull
    u_attractor = k_attractor * np.sin(wrap_angle(attractor_angle - theta))

    # hook / tooth / beak asymmetry
    u_drift = k_drift * np.sign(wrap_angle(theta - attractor_angle))
    if abs(wrap_angle(theta - attractor_angle)) < 0.14:
        u_drift *= 0.35

    # memory term: reinforces chosen sector once discovered
    u_memory = k_memory * np.tanh(sector_memory[current_sector] - 0.25)

    u = u_ieee + u_theta + u_lock + u_breath + u_attractor + u_drift + u_memory

    # warmup
    if t < 10:
        u = 0.0

    # micro-slip inside closure
    if prox > 0.20:
        u *= (0.92 + 0.06 * np.sin(0.025 * t))

    u = np.clip(u, -u_clip, u_clip)

    # --------------------------------------------------------
    # Apply
    # --------------------------------------------------------
    factor = 1.0 + u * load_gain
    factor = np.clip(factor, 0.94, 1.06)

    net.load.p_mw = base_p * factor
    net.load.q_mvar = base_q * factor

    # --------------------------------------------------------
    # Closure metric
    # --------------------------------------------------------
    closure = (
        0.42 * prox
        + 0.28 * np.exp(-4.0 * abs(r - attractor_radius))
        + 0.20 * np.exp(-5.0 * abs(wrap_angle(theta - attractor_angle)))
        + 0.10 * np.tanh(sector_memory[current_sector])
    )

    # --------------------------------------------------------
    # Store
    # --------------------------------------------------------
    data["voltage"].append(v_mean)
    data["coherence"].append(coh)
    data["radius"].append(r)
    data["theta"].append(theta)
    data["z"].append(z)
    data["prox"].append(prox)

    data["u"].append(u)
    data["u_ieee"].append(u_ieee)
    data["u_theta"].append(u_theta)
    data["u_lock"].append(u_lock)
    data["u_breath"].append(u_breath)
    data["u_attractor"].append(u_attractor)
    data["u_drift"].append(u_drift)
    data["u_memory"].append(u_memory)

    data["closure"].append(closure)
    data["target_angle"].append(attractor_angle)
    data["target_radius"].append(attractor_radius)
    data["sector"].append(current_sector)
    data["switch_event"].append(switch_event)
    data["residue_target"].append(residue_target)
    data["memory_bias"].append(sector_memory[current_sector])

# ============================================================
# REPORT
# ============================================================
sector_counts = {
    f"sector_{i}": int(np.sum(np.array(data["sector"]) == i))
    for i in range(N_SECTORS)
}

report = f"""NEXAH v54 – Multi Attractor Navigation

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

Switch count: {int(np.sum(data['switch_event']))}

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
fig, axs = plt.subplots(8, 1, figsize=(12, 18), sharex=True)

axs[0].plot(data["voltage"])
axs[0].set_title("Voltage")

axs[1].plot(data["coherence"])
axs[1].set_title("Coherence")

axs[2].plot(data["radius"], label="radius")
axs[2].plot(data["target_radius"], label="target radius", alpha=0.8)
axs[2].set_title("Radius")
axs[2].legend()

axs[3].plot(data["prox"])
axs[3].set_title("OLGO Proximity")

axs[4].plot(data["closure"])
axs[4].set_title("Closure Metric")

axs[5].plot(data["sector"])
axs[5].set_title("Active Sector")

axs[6].plot(data["memory_bias"])
axs[6].set_title("Memory Bias")

axs[7].plot(data["u"], label="u")
axs[7].plot(data["u_ieee"], label="u_ieee", alpha=0.7)
axs[7].plot(data["u_lock"], label="u_lock", alpha=0.7)
axs[7].plot(data["u_breath"], label="u_breath", alpha=0.7)
axs[7].plot(data["u_attractor"], label="u_attractor", alpha=0.7)
axs[7].plot(data["u_drift"], label="u_drift", alpha=0.7)
axs[7].plot(data["u_memory"], label="u_memory", alpha=0.7)
axs[7].legend(ncol=4)

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

ax.plot(theta_vals, r_vals, color="steelblue", alpha=0.75, label="IEEE trajectory")
ax.plot(target_angles, target_radii, color="magenta", alpha=0.65, label="target path")

sc = ax.scatter(theta_vals, r_vals, c=prox_vals, cmap="plasma", s=18, label="OLGO prox")

if len(switch_idx) > 0:
    ax.scatter(theta_vals[switch_idx], r_vals[switch_idx], color="green", s=28, label="switch")

for a in sector_angles:
    ax.plot([a, a], [0, 1.2], color="gray", alpha=0.18)

ax.set_title("v54 Multi Attractor Navigation Polar")
ax.legend(loc="upper right")
fig.colorbar(sc, pad=0.12)
fig.savefig(POLAR_PATH, dpi=150, bbox_inches="tight")
plt.close(fig)

print("✅ v54 finished")
print(f"📊 Saved: {TS_PATH}")
print(f"📊 Saved: {POLAR_PATH}")
print(f"📄 Saved: {REPORT_PATH}")
