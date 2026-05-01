import numpy as np
import matplotlib.pyplot as plt

print("⚡ NEXAH — Closed-Loop Control Test (PHASE-LOCKED)")

# =========================
# PARAMETERS
# =========================

n_steps = 2000
dt = 0.01

target = np.array([15.0, 15.0])
target_radius = 3.0

# =========================
# LOAD CONTROL LAW
# =========================

data = np.load("RESEARCH/validation/causality/control_law_data.npz")

phi_grid = data["phi"]
s_star = data["s_star"]

# =========================
# INTERPOLATION FUNCTION
# =========================

def get_s_star(phi):
    return np.interp(phi, phi_grid, s_star)

# =========================
# LORENZ SYSTEM
# =========================

def lorenz(x, sigma=10.0, rho=28.0, beta=8/3):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])

# =========================
# CONTROL (PHASE-LOCKED)
# =========================

def apply_control(x):
    theta = np.arctan2(x[1], x[0]) % (2*np.pi)

    s = get_s_star(theta)

    # 🔥 KEY CHANGE: phase-locked modulation
    modulation = np.sin(theta)

    direction = target - x[:2]
    direction = direction / (np.linalg.norm(direction) + 1e-8)

    x[0] += s * modulation * direction[0]
    x[1] += s * modulation * direction[1]

    return x

# =========================
# SIMULATION
# =========================

def simulate(control=False):
    x = np.array([10.0, 10.0, 20.0])

    trajectory = []
    instability = []
    iota_events = []

    for i in range(n_steps):
        dx = lorenz(x)

        # instability measure
        inst = np.linalg.norm(dx[:2])
        instability.append(inst)

        # evolve
        x = x + dt * dx

        if control:
            x = apply_control(x)

        trajectory.append(x.copy())

        # IOTA condition (simple threshold)
        if inst > 20:
            iota_events.append(i)

    return np.array(trajectory), np.array(instability), np.array(iota_events)

# =========================
# RUN BOTH
# =========================

traj_base, inst_base, iota_base = simulate(control=False)
traj_ctrl, inst_ctrl, iota_ctrl = simulate(control=True)

# =========================
# STATS
# =========================

print("\n📊 IOTA Comparison:")
print(f"Baseline IOTA count: {len(iota_base)}")
print(f"Controlled IOTA count: {len(iota_ctrl)}")
print(f"Δ: {len(iota_ctrl) - len(iota_base)}")

# =========================
# PLOT — INSTABILITY
# =========================

plt.figure(figsize=(12, 6))

plt.plot(inst_base, label="baseline instability", alpha=0.6)
plt.plot(inst_ctrl, label="controlled instability", alpha=0.8)

plt.scatter(iota_base, inst_base[iota_base], color="red", label="baseline IOTA", s=30)
plt.scatter(iota_ctrl, inst_ctrl[iota_ctrl], color="green", label="controlled IOTA", s=30)

plt.xlabel("time")
plt.ylabel("instability")
plt.title("Closed-Loop Control (Phase-Locked)")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("RESEARCH/validation/causality/results/closed_loop_phase_locked_instability.png", dpi=200)
plt.close()

# =========================
# PLOT — TRAJECTORY
# =========================

plt.figure(figsize=(6, 6))

plt.plot(traj_base[:,0], traj_base[:,1], alpha=0.4, label="baseline")
plt.plot(traj_ctrl[:,0], traj_ctrl[:,1], alpha=0.7, label="controlled")

plt.xlabel("x")
plt.ylabel("y")
plt.title("Trajectory Comparison (Phase-Locked Control)")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("RESEARCH/validation/causality/results/closed_loop_phase_locked_trajectory.png", dpi=200)
plt.close()

print("✅ Saved: closed_loop_phase_locked_instability.png")
print("✅ Saved: closed_loop_phase_locked_trajectory.png")
