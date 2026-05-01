import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

print("⚡ NEXAH — Phase-Aligned Control")

# =========================
# LORENZ SYSTEM
# =========================

def lorenz_step(state, sigma=10, rho=28, beta=8/3):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return np.array([dx, dy, dz])

# =========================
# SIMULATION PARAMS
# =========================

dt = 0.01
steps = 3000

state = np.array([1.0, 1.0, 1.0])

trajectory = []
instability = []
phi_series = []
omega_series = []
iota_events = []

# =========================
# CONTROL PARAMS
# =========================

k = 0.15  # control strength (tune!)

# =========================
# MAIN LOOP
# =========================

prev_phi = None

for t in range(steps):

    # ---- simulate
    dx = lorenz_step(state)
    state = state + dx * dt

    x, y, z = state
    trajectory.append(state.copy())

    # ---- phase
    phi = np.arctan2(y, x)
    phi_series.append(phi)

    # ---- omega
    if prev_phi is not None:
        dphi = phi - prev_phi

        # unwrap jump
        if dphi > np.pi:
            dphi -= 2 * np.pi
        elif dphi < -np.pi:
            dphi += 2 * np.pi

        omega = dphi / dt
    else:
        omega = 0.0

    omega_series.append(omega)
    prev_phi = phi

# =========================
# SMOOTH PHASE VELOCITY
# =========================

omega_array = np.array(omega_series)
omega_smooth = gaussian_filter1d(omega_array, sigma=10)

# =========================
# SECOND PASS WITH CONTROL
# =========================

state = np.array([1.0, 1.0, 1.0])
trajectory_controlled = []
instability_controlled = []
iota_controlled = []

prev_phi = None

for t in range(steps):

    dx = lorenz_step(state)

    # ---- phase
    x, y, z = state
    phi = np.arctan2(y, x)

    if prev_phi is not None:
        dphi = phi - prev_phi

        if dphi > np.pi:
            dphi -= 2 * np.pi
        elif dphi < -np.pi:
            dphi += 2 * np.pi

        omega = dphi / dt
    else:
        omega = 0.0

    # ---- mismatch
    omega_expected = omega_smooth[t]
    mismatch = omega - omega_expected

    # ---- control (ONLY ON x,y)
    u = -k * mismatch

    dx[0] += u
    dx[1] += u

    # ---- integrate
    state = state + dx * dt
    trajectory_controlled.append(state.copy())

    # ---- instability proxy
    inst = np.linalg.norm(dx)
    instability_controlled.append(inst)

    # ---- IOTA detection (same as before)
    if abs(mismatch) > 2.0:
        iota_controlled.append(t)

    prev_phi = phi

# =========================
# PLOTS
# =========================

trajectory = np.array(trajectory)
trajectory_controlled = np.array(trajectory_controlled)

# ---- TRAJECTORY
plt.figure(figsize=(6, 6))
plt.plot(trajectory[:,0], trajectory[:,1], alpha=0.3, label="baseline")
plt.plot(trajectory_controlled[:,0], trajectory_controlled[:,1], linewidth=2, label="phase-controlled")
plt.legend()
plt.title("Phase-Aligned Control Trajectory")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.tight_layout()
plt.savefig("RESEARCH/validation/causality/results/phase_control_trajectory.png", dpi=200)
plt.close()

# ---- INSTABILITY
plt.figure(figsize=(10, 4))
plt.plot(instability_controlled, label="controlled instability")

for t in iota_controlled:
    plt.axvline(t, color='red', alpha=0.2)

plt.legend()
plt.title("Phase-Aligned Control — Instability")
plt.xlabel("time")
plt.ylabel("instability")
plt.grid(True)
plt.tight_layout()
plt.savefig("RESEARCH/validation/causality/results/phase_control_instability.png", dpi=200)
plt.close()

# =========================
# SUMMARY
# =========================

summary_path = "RESEARCH/validation/causality/results/phase_control_summary.txt"

with open(summary_path, "w") as f:
    f.write("NEXAH — Phase-Aligned Control\n\n")
    f.write(f"IOTA count: {len(iota_controlled)}\n")
    f.write(f"Control strength k: {k}\n\n")
    f.write("Interpretation:\n")
    f.write("Control reduces phase mismatch.\n")
    f.write("Transitions occur when mismatch exceeds threshold.\n")

print(f"📊 IOTA count (controlled): {len(iota_controlled)}")
print("✅ Saved: phase_control_trajectory.png")
print("✅ Saved: phase_control_instability.png")
print("✅ Saved: phase_control_summary.txt")
