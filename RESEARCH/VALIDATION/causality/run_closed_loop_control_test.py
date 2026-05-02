import numpy as np
import matplotlib.pyplot as plt

print("⚡ NEXAH — Closed-Loop Control Test")

# =========================
# LOAD CONTROL LAW
# =========================

data = np.load("RESEARCH/validation/causality/control_law_data.npz")
phi_grid = data["phi"]
s_star = data["s_star"]

# =========================
# PARAMETERS
# =========================

dt = 0.01
n_steps = 3000

target = np.array([15.0, 15.0])  # same as before

# =========================
# LORENZ SYSTEM
# =========================

def lorenz(x, sigma=10.0, rho=28.0, beta=8/3):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])

# =========================
# GATE USING s*(φ)
# =========================

def apply_control(x, t):
    theta = np.arctan2(x[1], x[0]) % (2 * np.pi)
    s = np.interp(theta, phi_grid, s_star)

    # same logic as resonance scan
    if np.linalg.norm(x[:2]) < 20:
        direction = target - x[:2]
        direction = direction / (np.linalg.norm(direction) + 1e-8)

        modulation = np.sin(t)

        x[0] += s * modulation * direction[0]
        x[1] += s * modulation * direction[1]

    return x

# =========================
# SIMULATION FUNCTION
# =========================

def simulate(control=False):
    x = np.array([1.0, 1.0, 20.0])

    trajectory = []
    instability_series = []

    for i in range(n_steps):
        t = i * dt

        dx = lorenz(x)

        if control:
            x = apply_control(x, t)

        x = x + dt * dx

        trajectory.append(x.copy())

        instability = np.linalg.norm(dx[:2])
        instability_series.append(instability)

    return np.array(trajectory), np.array(instability_series)

# =========================
# RUN BOTH CASES
# =========================

traj_base, inst_base = simulate(control=False)
traj_ctrl, inst_ctrl = simulate(control=True)

# =========================
# IOTA DETECTION
# =========================

threshold_base = np.percentile(inst_base, 95)
threshold_ctrl = np.percentile(inst_ctrl, 95)

iota_base = inst_base > threshold_base
iota_ctrl = inst_ctrl > threshold_ctrl

n_iota_base = np.sum(iota_base)
n_iota_ctrl = np.sum(iota_ctrl)

# =========================
# RESULTS
# =========================

print("\n📊 IOTA Comparison:")
print(f"Baseline IOTA count: {n_iota_base}")
print(f"Controlled IOTA count: {n_iota_ctrl}")
print(f"Δ: {n_iota_ctrl - n_iota_base}")

# =========================
# PLOT 1 — INSTABILITY
# =========================

plt.figure(figsize=(14, 6))

plt.plot(inst_base, label="baseline", alpha=0.7)
plt.plot(inst_ctrl, label="controlled", alpha=0.7)

plt.legend()
plt.title("Instability: Baseline vs Controlled")
plt.xlabel("time")
plt.ylabel("|dθ/dt|")
plt.grid(True)
plt.tight_layout()

plt.savefig("RESEARCH/validation/causality/results/closed_loop_instability.png", dpi=200)
plt.close()

# =========================
# PLOT 2 — TRAJECTORY
# =========================

plt.figure(figsize=(6, 6))

plt.plot(traj_base[:, 0], traj_base[:, 1], alpha=0.4, label="baseline")
plt.plot(traj_ctrl[:, 0], traj_ctrl[:, 1], alpha=0.6, label="controlled")

plt.legend()
plt.title("Trajectory Projection (xy)")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.tight_layout()

plt.savefig("RESEARCH/validation/causality/results/closed_loop_trajectory.png", dpi=200)
plt.close()

print("✅ Saved: closed_loop_instability.png")
print("✅ Saved: closed_loop_trajectory.png")
