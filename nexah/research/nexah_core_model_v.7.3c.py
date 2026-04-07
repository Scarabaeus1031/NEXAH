import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# NEXAH v7.3c — State Control System
# engage / lock / release / nexit
# ============================================================

# ------------------------------------------------------------
# GRID
# ------------------------------------------------------------
N = 80
x = np.linspace(-1.5, 1.5, N)
y = np.linspace(-1.5, 1.5, N)
X, Y = np.meshgrid(x, y)

# ------------------------------------------------------------
# CORE FIELDS
# ------------------------------------------------------------
def instability_measure(x, y):
    r = np.sqrt(x*x + y*y) + 1e-9
    return np.log(r) + 0.3 * np.sin(3.0 * x) * np.cos(3.0 * y)

def instability_gradient(x, y, eps=1e-4):
    dx = (instability_measure(x + eps, y) - instability_measure(x - eps, y)) / (2.0 * eps)
    dy = (instability_measure(x, y + eps) - instability_measure(x, y - eps)) / (2.0 * eps)
    return np.array([dx, dy], dtype=float)

def flow_field(x, y):
    r = np.sqrt(x*x + y*y) + 1e-9
    fx = -y / r + 0.5 * x
    fy =  x / r + 0.5 * y
    return np.array([fx, fy], dtype=float)

def current_field(x, y):
    g = instability_gradient(x, y)
    return np.linalg.norm(g)

def pressure_field(x, y):
    g = instability_gradient(x, y)
    return g[0]**2 + g[1]**2

def power_field(x, y):
    u = instability_measure(x, y)
    i = current_field(x, y)
    return u * i

# ------------------------------------------------------------
# STATE MACHINE
# ------------------------------------------------------------
STATE_NAMES = {
    0: "engage",
    1: "lock",
    2: "release",
    3: "nexit",
}

STATE_COLORS = {
    0: "tab:blue",
    1: "tab:orange",
    2: "tab:green",
    3: "tab:red",
}

# engage  = 0100
# lock    = 0010
# release = 0001
# nexit   = 1000

def decide_state(x, y):
    """
    Simple rule-based switching system from local field values.
    """
    u = instability_measure(x, y)
    i = current_field(x, y)
    p = power_field(x, y)
    q = pressure_field(x, y)

    r = np.sqrt(x*x + y*y)

    # RELEASE: strong sink / discharge core
    if (p < -5.0 and i > 2.0) or q > 20.0:
        return 2

    # LOCK: near a shell / orbit corridor
    if 0.55 < r < 1.05 and i < 2.0:
        return 1

    # NEXIT: outer region / escape tendency
    if r > 1.15 or u > 0.55:
        return 3

    # Default = ENGAGE
    return 0

def state_vector(x, y, state):
    """
    Hybrid control:
    - engage  : move into system and start coupling
    - lock    : follow orbit / shell
    - release : discharge out of high-pressure sink
    - nexit   : directed outward exit / transition
    """
    grad = instability_gradient(x, y)
    flow = flow_field(x, y)

    grad_norm = np.linalg.norm(grad) + 1e-9
    flow_norm = np.linalg.norm(flow) + 1e-9

    grad_u = grad / grad_norm
    flow_u = flow / flow_norm

    r = np.sqrt(x*x + y*y) + 1e-9
    radial_u = np.array([x / r, y / r], dtype=float)

    if state == 0:   # engage
        vec = -0.60 * grad_u + 0.80 * flow_u

    elif state == 1: # lock
        vec = 0.15 * radial_u + 1.10 * flow_u

    elif state == 2: # release
        vec = -1.10 * grad_u + 0.20 * flow_u

    else:            # nexit
        vec = 0.95 * radial_u + 0.25 * flow_u

    return vec

# ------------------------------------------------------------
# SIMULATION
# ------------------------------------------------------------
def simulate_state_trajectory(x0, y0, steps=260, dt=0.035, max_radius=1.8):
    x, y = float(x0), float(y0)

    traj = []
    states = []

    for _ in range(steps):
        if not np.isfinite(x) or not np.isfinite(y):
            break

        state = decide_state(x, y)
        vec = state_vector(x, y, state)

        # limit step
        norm = np.linalg.norm(vec) + 1e-9
        vec = vec / norm

        x = x + dt * vec[0]
        y = y + dt * vec[1]

        traj.append((x, y))
        states.append(state)

        if np.sqrt(x*x + y*y) > max_radius:
            break

    return np.array(traj, dtype=float), np.array(states, dtype=int)

# ------------------------------------------------------------
# FIELD MAPS
# ------------------------------------------------------------
U_map = np.zeros_like(X)
I_map = np.zeros_like(X)
P_map = np.zeros_like(X)
Q_map = np.zeros_like(X)
S_map = np.zeros_like(X)

for i in range(N):
    for j in range(N):
        xi = X[i, j]
        yi = Y[i, j]

        U_map[i, j] = instability_measure(xi, yi)
        I_map[i, j] = current_field(xi, yi)
        P_map[i, j] = power_field(xi, yi)
        Q_map[i, j] = pressure_field(xi, yi)
        S_map[i, j] = decide_state(xi, yi)

# ------------------------------------------------------------
# SAMPLE TRAJECTORIES
# ------------------------------------------------------------
start_points = [
    (-1.10, -1.10),
    (-1.10,  1.00),
    ( 1.10, -1.10),
    ( 1.10,  1.00),
    ( 0.00,  0.00),
    ( 0.55,  0.00),
    ( 0.00, -0.75),
    (-0.60,  0.20),
]

trajectories = []
state_sequences = []

for sx, sy in start_points:
    traj, states = simulate_state_trajectory(sx, sy)
    trajectories.append(traj)
    state_sequences.append(states)

# ------------------------------------------------------------
# PLOT 1 — FOUR CORE MAPS
# ------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

im0 = axs[0, 0].imshow(U_map, origin="lower", extent=[-1.5, 1.5, -1.5, 1.5], cmap="viridis")
axs[0, 0].set_title("Voltage / Instability (U)")
plt.colorbar(im0, ax=axs[0, 0])

im1 = axs[0, 1].imshow(I_map, origin="lower", extent=[-1.5, 1.5, -1.5, 1.5], cmap="viridis")
axs[0, 1].set_title("Current (I)")
plt.colorbar(im1, ax=axs[0, 1])

im2 = axs[1, 0].imshow(P_map, origin="lower", extent=[-1.5, 1.5, -1.5, 1.5], cmap="viridis")
axs[1, 0].set_title("Power (P = U * I)")
plt.colorbar(im2, ax=axs[1, 0])

im3 = axs[1, 1].imshow(Q_map, origin="lower", extent=[-1.5, 1.5, -1.5, 1.5], cmap="viridis")
axs[1, 1].set_title("Pressure / Gradient Energy")
plt.colorbar(im3, ax=axs[1, 1])

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# PLOT 2 — STATE MAP
# ------------------------------------------------------------
plt.figure(figsize=(7, 6))
im = plt.imshow(S_map, origin="lower", extent=[-1.5, 1.5, -1.5, 1.5], cmap="tab10", vmin=0, vmax=3)
plt.title("NEXAH v7.3c — State Map")
cbar = plt.colorbar(im, ticks=[0, 1, 2, 3])
cbar.ax.set_yticklabels([STATE_NAMES[i] for i in [0, 1, 2, 3]])
plt.xlabel("x")
plt.ylabel("y")
plt.show()

# ------------------------------------------------------------
# PLOT 3 — TRAJECTORIES OVER STATE MAP
# ------------------------------------------------------------
plt.figure(figsize=(7, 7))
plt.imshow(
    S_map,
    origin="lower",
    extent=[-1.5, 1.5, -1.5, 1.5],
    cmap="Pastel1",
    alpha=0.95,
    vmin=0,
    vmax=3
)

for traj, states in zip(trajectories, state_sequences):
    if len(traj) == 0:
        continue

    # draw full path faint
    plt.plot(traj[:, 0], traj[:, 1], color="black", linewidth=1.2, alpha=0.35)

    # draw state-colored points
    for st in range(4):
        mask = states == st
        if np.any(mask):
            plt.scatter(
                traj[mask, 0],
                traj[mask, 1],
                s=14,
                color=STATE_COLORS[st],
                label=STATE_NAMES[st]
            )

# deduplicate legend
handles, labels = plt.gca().get_legend_handles_labels()
seen = set()
new_handles = []
new_labels = []
for h, l in zip(handles, labels):
    if l not in seen:
        seen.add(l)
        new_handles.append(h)
        new_labels.append(l)

plt.legend(new_handles, new_labels, loc="upper right")
plt.title("Trajectory Navigation over State Field")
plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True, alpha=0.25)
plt.show()

# ------------------------------------------------------------
# PLOT 4 — TIMELINE OF STATES
# ------------------------------------------------------------
plt.figure(figsize=(12, 5))
for idx, states in enumerate(state_sequences):
    if len(states) == 0:
        continue
    plt.step(
        np.arange(len(states)),
        states + idx * 4.5,
        where="mid",
        linewidth=1.8,
        label=f"traj {idx}"
    )

for st in range(4):
    plt.text(-8, st, STATE_NAMES[st], color=STATE_COLORS[st], fontsize=10)

plt.title("Mode Timeline — engage / lock / release / nexit")
plt.xlabel("time step")
plt.ylabel("stacked state index")
plt.grid(True, alpha=0.25)
plt.legend(loc="upper right", ncol=2)
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------
print("\n=== NEXAH v7.3c Summary ===")
print("U min/max:", float(np.min(U_map)), float(np.max(U_map)))
print("I min/max:", float(np.min(I_map)), float(np.max(I_map)))
print("P min/max:", float(np.min(P_map)), float(np.max(P_map)))
print("Pressure min/max:", float(np.min(Q_map)), float(np.max(Q_map)))

print("\nState counts on grid:")
for st in range(4):
    print(f"{STATE_NAMES[st]}:", int(np.sum(S_map == st)))

print("\nTrajectory summaries:")
for idx, (traj, states) in enumerate(zip(trajectories, state_sequences)):
    if len(states) == 0:
        print(f"traj {idx}: empty")
        continue

    counts = {STATE_NAMES[s]: int(np.sum(states == s)) for s in range(4)}
    print(f"traj {idx}: len={len(states)}, counts={counts}")
