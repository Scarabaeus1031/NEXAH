import numpy as np
import matplotlib.pyplot as plt
import os

# =========================
# PARAMETERS
# =========================
steps = 180
dt = 0.08

# damping
damping = 0.15

# target system
target_distance = 0.45
k_target = 0.8   # 🔥 NEW: strength of goal pull

# =========================
# INITIAL STATE
# =========================
lam = 0.58
psi = 0.46

# storage
lam_hist = []
psi_hist = []
risk_hist = []
dist_hist = []
field_lam_hist = []
field_psi_hist = []

# =========================
# SYSTEM MODEL
# =========================
def compute_distance(lam, psi):
    return np.sqrt((lam - 0.3)**2 + (psi - 0.2)**2)

def compute_risk(lam, psi):
    return 0.02 * lam**2 + 0.015 * psi**2

def field(lam, psi):
    # natural flow field (unchanged core)
    f_lam = 0.25 * (1 - lam) - 0.1 * psi
    f_psi = 0.18 * lam - 0.22 * psi
    return f_lam, f_psi

# =========================
# SIMULATION LOOP
# =========================
for step in range(steps):

    distance = compute_distance(lam, psi)
    risk = compute_risk(lam, psi)

    # gradient approx
    grad = risk

    # base field
    f_lam, f_psi = field(lam, psi)

    # =========================
    # 🔥 NEW: TARGET FORCE
    # =========================
    target_force = k_target * (distance - target_distance)

    # direction toward "center"
    dir_lam = (lam - 0.3)
    dir_psi = (psi - 0.2)

    norm = np.sqrt(dir_lam**2 + dir_psi**2) + 1e-8
    dir_lam /= norm
    dir_psi /= norm

    # =========================
    # FULL DYNAMICS
    # =========================
    dlam = (
        f_lam
        - damping * lam
        - target_force * dir_lam
    )

    dpsi = (
        f_psi
        - damping * psi
        - target_force * dir_psi * 0.8
    )

    # update
    lam += dt * dlam
    psi += dt * dpsi

    # store
    lam_hist.append(lam)
    psi_hist.append(psi)
    risk_hist.append(risk)
    dist_hist.append(distance)
    field_lam_hist.append(dlam)
    field_psi_hist.append(dpsi)

    print(
        f"[STEP {step}] lambda={lam:.4f} psi={psi:.4f} "
        f"risk={risk:.4f} dist={distance:.4f} "
        f"field=({dlam:.4f},{dpsi:.4f})"
    )

# =========================
# OUTPUT
# =========================
out_dir = "APPLICATIONS/power_systems/nexah_ieee9/results/controller_v10_4"
os.makedirs(out_dir, exist_ok=True)

# =========================
# PLOT 1: TIME SERIES
# =========================
plt.figure(figsize=(10,6))
plt.plot(lam_hist, label="lambda")
plt.plot(psi_hist, label="psi")
plt.plot(risk_hist, label="risk")
plt.plot(dist_hist, label="distance")
plt.legend()
plt.title("NEXAH v10.4 Controlled Navigation")
plt.xlabel("Step")
plt.ylabel("Value")
plt.grid()

plt.savefig(f"{out_dir}/output_v10_4_plot.png")
plt.close()

# =========================
# PLOT 2: LAMBDA vs PSI
# =========================
plt.figure(figsize=(6,6))
plt.scatter(lam_hist, psi_hist, c=range(len(lam_hist)))
plt.plot(lam_hist, psi_hist, alpha=0.4)
plt.xlabel("lambda")
plt.ylabel("psi")
plt.title("Phase: lambda vs psi")

plt.savefig(f"{out_dir}/output_v10_4_phase_lambda_psi.png")
plt.close()

# =========================
# PLOT 3: RISK vs DISTANCE
# =========================
plt.figure(figsize=(6,6))
plt.scatter(risk_hist, dist_hist, c=range(len(risk_hist)))
plt.plot(risk_hist, dist_hist, alpha=0.4)
plt.axhline(target_distance, linestyle="--", label="target")
plt.xlabel("risk")
plt.ylabel("distance")
plt.legend()
plt.title("Phase: risk vs distance")

plt.savefig(f"{out_dir}/output_v10_4_phase_risk_distance.png")
plt.close()

print("\nSaved results to:", out_dir)
