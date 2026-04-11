# ============================================================
# v53_attractor_engine.py
# NEXAH – Boundary Attractor Engine
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

TS_PATH = OUTDIR / "v53_timeseries.png"
POLAR_PATH = OUTDIR / "v53_polar.png"
REPORT_PATH = OUTDIR / "v53_report.txt"

print(f"\n📁 v53 running → {OUTDIR.resolve()}\n")

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
    "closure": [],
    "target_angle": [],
    "target_radius": [],
    "sector": [],
}

# ============================================================
# SETTINGS
# ============================================================
T = 400

theta_ref = -np.pi / 2

# NEW: not center-seeking, but boundary-seeking
target_radius_base = 0.86

k_r = 0.18
k_theta = 0.04
k_lock = 0.08
k_attractor = 0.05
k_drift = 0.015

u_clip = 0.14
load_gain = 0.08

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
    # Boundary attractor logic
    # --------------------------------------------------------
    angle_errors = np.array([abs(wrap_angle(theta - a)) for a in sector_angles])
    nearest_idx = int(np.argmin(angle_errors))
    attractor_angle = sector_angles[nearest_idx]

    # slight dynamic breathing of attractor radius
    attractor_radius = target_radius_base + 0.04 * np.sin(0.02 * t + nearest_idx)

    # --------------------------------------------------------
    # Control terms
    # --------------------------------------------------------
    # radial pull to boundary shell, not center
    u_ieee = -k_r * (r - attractor_radius)

    # keep relation to structural axis, but weaker than before
    u_theta = -k_theta * np.sin(wrap_angle(theta - theta_ref))

    # shell lock
    shell_target = shells[1] if prox < 0.9 else shells[0]
    u_lock = -k_lock * (z - shell_target)

    # closure-preserving contraction but only weak
    u_breath = -0.01 * (r - attractor_radius) * (0.3 + 0.7 * prox)

    # NEW: attractor anchoring
    u_attractor = k_attractor * np.sin(wrap_angle(attractor_angle - theta))

    # NEW: asymmetrical drift = hook / tooth / beak
    u_drift = k_drift * np.sign(wrap_angle(theta - theta_ref))
    if abs(wrap_angle(theta - attractor_angle)) < 0.18:
        u_drift *= 0.35

    u = u_ieee + u_theta + u_lock + u_breath + u_attractor + u_drift

    # warmup
    if t < 10:
        u = 0.0

    # micro slip inside closure
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
        0.45 * prox
        + 0.30 * np.exp(-4.0 * abs(r - attractor_radius))
        + 0.25 * np.exp(-5.0 * abs(wrap_angle(theta - attractor_angle)))
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

    data["closure"].append(closure)
    data["target_angle"].append(attractor_angle)
    data["target_radius"].append(attractor_radius)
    data["sector"].append(nearest_idx)

# ============================================================
# REPORT
# ============================================================
sector_counts = {
    f"sector_{i}": int(np.sum(np.array(data["sector"]) == i))
    for i in range(N_SECTORS)
}

report = f"""NEXAH v53 – Boundary Attractor Engine

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
fig, axs = plt.subplots(7, 1, figsize=(12, 16), sharex=True)

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
axs[5].set_title("Active Attractor Sector")

axs[6].plot(data["u"], label="u")
axs[6].plot(data["u_ieee"], label="u_ieee", alpha=0.7)
axs[6].plot(data["u_lock"], label="u_lock", alpha=0.7)
axs[6].plot(data["u_breath"], label="u_breath", alpha=0.7)
axs[6].plot(data["u_attractor"], label="u_attractor", alpha=0.7)
axs[6].plot(data["u_drift"], label="u_drift", alpha=0.7)
axs[6].legend(ncol=3)

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

ax.plot(theta_vals, r_vals, color="steelblue", alpha=0.75, label="IEEE trajectory")
ax.plot(target_angles, target_radii, color="magenta", alpha=0.65, label="attractor path")

sc = ax.scatter(theta_vals, r_vals, c=prox_vals, cmap="plasma", s=18, label="OLGO prox")

for a in sector_angles:
    ax.plot([a, a], [0, 1.2], color="gray", alpha=0.18)

ax.set_title("v53 Attractor Engine Polar")
ax.legend(loc="upper right")
fig.colorbar(sc, pad=0.12)
fig.savefig(POLAR_PATH, dpi=150, bbox_inches="tight")
plt.close(fig)

print("✅ v53 finished")
print(f"📊 Saved: {TS_PATH}")
print(f"📊 Saved: {POLAR_PATH}")
print(f"📄 Saved: {REPORT_PATH}")
