import numpy as np
import matplotlib.pyplot as plt

print("⚡ NEXAH — Adaptive Closed-Loop Control")

# =========================
# LOAD CONTROL LAW
# =========================

data = np.load("RESEARCH/validation/causality/control_law_data.npz")

phi_grid = data["phi"]
s_star = data["s_star"]

# =========================
# PARAMETERS
# =========================

n_steps = 2000
dt = 0.01

alpha = 1.5   # 🔥 adaptive strength (tune this!)

target = np.array([15.0, 15.0])
target_radius = 3.0

# =========================
# LORENZ
# =========================

def lorenz(x, sigma=10.0, rho=28.0, beta=8/3):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])

# =========================
# INTERPOLATE s*(φ)
# =========================

def get_s_star(phi):
    return np.interp(phi, phi_grid, s_star)

# =========================
# INSTABILITY (simple proxy)
# =========================

def instability(x):
    return np.linalg.norm(x[:2]) / 20.0

# =========================
# SIMULATION
# =========================

x = np.array([5.0, 5.0, 25.0])

trajectory = []
inst_series = []
iota_events = []

for i in range(n_steps):
    t = i * dt

    # phase
    phi = (t % (2*np.pi))

    # base control
    s_base = get_s_star(phi)

    # adaptive control
    s = s_base * (1 + alpha * instability(x))

    # direction to target
    direction = target - x[:2]
    direction = direction / (np.linalg.norm(direction) + 1e-8)

    # update
    x = x + dt * lorenz(x)
    x[0] += s * np.sin(t) * direction[0]
    x[1] += s * np.sin(t) * direction[1]

    # logging
    trajectory.append(x.copy())
    inst = instability(x)
    inst_series.append(inst)

    # IOTA detection (simple threshold)
    if inst > 1.2:
        iota_events.append(i)

trajectory = np.array(trajectory)

print(f"\n📊 IOTA count: {len(iota_events)}")

# =========================
# PLOTS
# =========================

plt.figure(figsize=(10, 5))
plt.plot(inst_series, label="instability")

for i in iota_events:
    plt.axvline(i, color='r', alpha=0.2)

plt.title("Adaptive Closed-Loop Instability")
plt.legend()
plt.tight_layout()

plt.savefig("RESEARCH/validation/causality/results/adaptive_instability.png", dpi=200)
plt.close()

plt.figure(figsize=(6, 6))
plt.plot(trajectory[:, 0], trajectory[:, 1], linewidth=1)
plt.scatter(target[0], target[1], c='red', label="target")

plt.title("Adaptive Closed-Loop Trajectory")
plt.legend()
plt.tight_layout()

plt.savefig("RESEARCH/validation/causality/results/adaptive_trajectory.png", dpi=200)
plt.close()

print("✅ Saved: adaptive_instability.png")
print("✅ Saved: adaptive_trajectory.png")
