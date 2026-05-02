import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

print("⚡ NEXAH — Phase Gate Control")

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
# PARAMS
# =========================

dt = 0.01
steps = 3000

k = 0.25          # control strength
threshold = 2.0   # mismatch threshold

# =========================
# BASELINE RUN (for omega reference)
# =========================

state = np.array([1.0, 1.0, 1.0])
phi_series = []
omega_series = []

prev_phi = None

for t in range(steps):

    dx = lorenz_step(state)
    state = state + dx * dt

    x, y, z = state
    phi = np.arctan2(y, x)
    phi_series.append(phi)

    if prev_phi is not None:
        dphi = phi - prev_phi

        if dphi > np.pi:
            dphi -= 2 * np.pi
        elif dphi < -np.pi:
            dphi += 2 * np.pi

        omega = dphi / dt
    else:
        omega = 0.0

    omega_series.append(omega)
    prev_phi = phi

omega_array = np.array(omega_series)
omega_smooth = gaussian_filter1d(omega_array, sigma=10)

# =========================
# CONTROL RUN
# =========================

state = np.array([1.0, 1.0, 1.0])

trajectory = []
instability = []
iota_events = []
control_active = []

prev_phi = None

for t in range(steps):

    dx = lorenz_step(state)

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

    omega_expected = omega_smooth[t]
    mismatch = omega - omega_expected

    # =========================
    # GATE CONTROL (KEY!)
    # =========================

    if abs(mismatch) > threshold:
        u = -k * mismatch
        control_active.append(1)
        iota_events.append(t)
    else:
        u = 0.0
        control_active.append(0)

    # apply control ONLY to x,y plane
    dx[0] += u
    dx[1] += u

    state = state + dx * dt
    trajectory.append(state.copy())

    inst = np.linalg.norm(dx)
    instability.append(inst)

    prev_phi = phi

trajectory = np.array(trajectory)

# =========================
# PLOTS
# =========================

# ---- TRAJECTORY
plt.figure(figsize=(6, 6))
plt.plot(trajectory[:,0], trajectory[:,1], linewidth=2, label="phase-gate control")
plt.title("Phase Gate Control Trajectory")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.tight_layout()
plt.savefig("RESEARCH/validation/causality/results/phase_gate_trajectory.png", dpi=200)
plt.close()

# ---- INSTABILITY
plt.figure(figsize=(12, 5))
plt.plot(instability, label="instability")

for t in iota_events:
    plt.axvline(t, color='red', alpha=0.2)

plt.title("Phase Gate Control — Instability")
plt.xlabel("time")
plt.ylabel("instability")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("RESEARCH/validation/causality/results/phase_gate_instability.png", dpi=200)
plt.close()

# ---- CONTROL ACTIVITY
plt.figure(figsize=(12, 3))
plt.plot(control_active)
plt.title("Control Activation (Gate)")
plt.xlabel("time")
plt.ylabel("active (1/0)")
plt.grid(True)
plt.tight_layout()
plt.savefig("RESEARCH/validation/causality/results/phase_gate_activation.png", dpi=200)
plt.close()

# =========================
# SUMMARY
# =========================

summary_path = "RESEARCH/validation/causality/results/phase_gate_summary.txt"

with open(summary_path, "w") as f:
    f.write("NEXAH — Phase Gate Control\n\n")
    f.write(f"IOTA events: {len(iota_events)}\n")
    f.write(f"Threshold: {threshold}\n")
    f.write(f"Control strength k: {k}\n\n")

    f.write("Interpretation:\n")
    f.write("Control is only active at phase mismatch peaks.\n")
    f.write("System is allowed to evolve freely otherwise.\n")

print(f"📊 IOTA events: {len(iota_events)}")
print("✅ Saved: phase_gate_trajectory.png")
print("✅ Saved: phase_gate_instability.png")
print("✅ Saved: phase_gate_activation.png")
print("✅ Saved: phase_gate_summary.txt")
