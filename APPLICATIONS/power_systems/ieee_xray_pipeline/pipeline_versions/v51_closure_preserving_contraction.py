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

TS_PATH = OUTDIR / "v51_timeseries.png"
REPORT_PATH = OUTDIR / "v51_report.txt"

print(f"\n📁 v51 running → {OUTDIR.resolve()}\n")

# ============================================================
# OLGO / SHELL
# ============================================================
phi = (1 + np.sqrt(5)) / 2
pi = np.pi

f0 = (phi ** 3) / (pi ** 2)
epsilon = 0.029
shells = np.array([f0, f0 + epsilon, f0 + 2 * epsilon])

def olgo_proximity(z, sharpness=80.0):
    d = np.min(np.abs(shells - z))
    return np.exp(-sharpness * d)

def wrap_angle(a):
    return (a + np.pi) % (2 * np.pi) - np.pi

def safe_mean(x):
    return float(np.mean(x)) if len(x) else 0.0

def safe_max(x):
    return float(np.max(x)) if len(x) else 0.0

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
    "closure": [],
}

# ============================================================
# SETTINGS
# ============================================================
T = 400
theta_ref = -np.pi / 2
target_radius = 0.22

k_r = 0.24
k_theta = 0.05
k_lock = 0.10

u_clip = 0.10
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

    # --------------------------------------------------------
    # CONTROLLER CORE
    # --------------------------------------------------------
    u_ieee = -k_r * (r - target_radius)
    u_theta = -k_theta * np.sin(theta - theta_ref)

    # soft shell lock toward inner shell
    shell_target = shells[0]
    u_lock = -k_lock * (z - shell_target)

    # --------------------------------------------------------
    # v51 CORE:
    # contraction only when closure/binding is present
    # --------------------------------------------------------
    u_breath = -0.03 * (r - target_radius) * (prox ** 2)

    u = u_ieee + u_theta + u_lock + u_breath

    # warmup
    if t < 10:
        u = 0.0

    # preserve closure instead of damping too much
    if prox > 0.20:
        u *= 0.96

    u = np.clip(u, -u_clip, u_clip)

    # --------------------------------------------------------
    # APPLY
    # --------------------------------------------------------
    factor = 1.0 + u * load_gain
    factor = np.clip(factor, 0.94, 1.06)

    net.load.p_mw = base_p * factor
    net.load.q_mvar = base_q * factor

    # --------------------------------------------------------
    # CLOSURE METRIC
    # --------------------------------------------------------
    closure = (
        0.55 * prox
        + 0.45 * np.exp(-5.0 * abs(r - target_radius))
    )

    # --------------------------------------------------------
    # STORE
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
    data["closure"].append(closure)

# ============================================================
# REPORT
# ============================================================
report = f"""NEXAH v51 – Closure-preserving contraction

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
Mean breathing term: {safe_mean(data['u_breath']):.4f}
"""

REPORT_PATH.write_text(report, encoding="utf-8")
print("\n" + report)

# ============================================================
# PLOTS
# ============================================================
fig, axs = plt.subplots(6, 1, figsize=(12, 14), sharex=True)

axs[0].plot(data["voltage"])
axs[0].set_title("Voltage")

axs[1].plot(data["coherence"])
axs[1].set_title("Coherence")

axs[2].plot(data["radius"])
axs[2].axhline(target_radius, linestyle="--")
axs[2].set_title("Radius")

axs[3].plot(data["prox"])
axs[3].set_title("OLGO Proximity")

axs[4].plot(data["closure"])
axs[4].set_title("Closure Metric")

axs[5].plot(data["u"], label="u")
axs[5].plot(data["u_ieee"], label="u_ieee", alpha=0.7)
axs[5].plot(data["u_lock"], label="u_lock", alpha=0.7)
axs[5].plot(data["u_breath"], label="u_breath", alpha=0.7)
axs[5].legend()
axs[5].set_title("Control Terms")

plt.tight_layout()
plt.savefig(TS_PATH, dpi=150)
plt.close()

print("✅ v51 finished")
print(f"📊 Saved: {TS_PATH}")
print(f"📄 Saved: {REPORT_PATH}")
