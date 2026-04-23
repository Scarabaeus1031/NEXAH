import os
import numpy as np
import matplotlib.pyplot as plt

print("⚡ NEXAH Dynamic Multi-Agent Navigation")

# --------------------------------------------------
# Output Path
# --------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
OUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../outputs/demo"))
os.makedirs(OUT_DIR, exist_ok=True)

# --------------------------------------------------
# 1. Field Definition
# --------------------------------------------------

def flow_field(x, y):
    dx = y - x * (x**2 + y**2)
    dy = -x - y * (x**2 + y**2)
    return np.array([dx, dy])

def boundary_field(x, y):
    return np.exp(x**2 + y**2)

def target_field(x, y, tx, ty):
    return np.array([tx - x, ty - y])

def unit(v):
    n = np.linalg.norm(v)
    if n < 1e-12:
        return np.zeros_like(v)
    return v / n

# --------------------------------------------------
# 2. Gate Score
# --------------------------------------------------

def gate_score(x, y, target):
    flow = flow_field(x, y)
    tvec = target_field(x, y, target[0], target[1])

    flow_n = unit(flow)
    target_n = unit(tvec)

    alignment = np.dot(flow_n, target_n)
    b = boundary_field(x, y)

    return alignment * np.exp(-0.3 * b)

# --------------------------------------------------
# 3. Gate Detection
# --------------------------------------------------

def find_candidate_gates(target, top_percent=99.2):
    xs = np.linspace(-2, 2, 120)
    ys = np.linspace(-2, 2, 120)

    X, Y = np.meshgrid(xs, ys)
    S = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            S[i, j] = gate_score(X[i, j], Y[i, j], target)

    threshold = np.percentile(S, top_percent)
    mask = S >= threshold

    candidates = np.column_stack([X[mask], Y[mask], S[mask]])
    return candidates

def prune_gates(candidates, min_dist=0.2, max_keep=5):
    if len(candidates) == 0:
        return np.empty((0, 3))

    order = np.argsort(-candidates[:, 2])
    candidates = candidates[order]

    chosen = []
    for c in candidates:
        pt = c[:2]
        if all(np.linalg.norm(pt - np.array(ch[:2])) > min_dist for ch in chosen):
            chosen.append(c)
        if len(chosen) >= max_keep:
            break

    return np.array(chosen)

# --------------------------------------------------
# 4. Dynamic Target
# --------------------------------------------------

def moving_target(t):
    tx = 1.3 + 0.35 * np.cos(0.5 * t)
    ty = 0.3 + 0.35 * np.sin(0.8 * t)
    return np.array([tx, ty])

# --------------------------------------------------
# 5. Steering
# --------------------------------------------------

def steering_step(pos, anchor, target, mode="gate"):
    x, y = pos

    flow = unit(flow_field(x, y))
    to_anchor = unit(anchor - pos)
    to_target = unit(target - pos)

    b = boundary_field(x, y)
    boundary_push = -0.04 * b * np.array([x, y])

    if mode == "gate":
        direction = 0.6 * flow + 0.5 * to_anchor + boundary_push
    else:
        direction = 0.4 * flow + 0.7 * to_target + boundary_push

    return unit(direction)

# --------------------------------------------------
# 6. Multi-Agent Setup
# --------------------------------------------------

agents = np.array([
    [-1.6,  0.6],
    [-1.5,  0.2],
    [-1.4, -0.2],
    [-1.3, -0.6],
])

trajectories = [ [p.copy()] for p in agents ]

# --------------------------------------------------
# 7. Simulation
# --------------------------------------------------

dt = 0.04
steps = 300

for step in range(steps):

    t = step * 0.1
    target = moving_target(t)

    # gates updated every step
    raw = find_candidate_gates(target)
    gates = prune_gates(raw)

    if len(gates) == 0:
        continue

    selected_gate = gates[0, :2]

    for i in range(len(agents)):

        pos = agents[i]

        # check if agent reached gate
        if np.linalg.norm(pos - selected_gate) > 0.15:
            mode = "gate"
            anchor = selected_gate
        else:
            mode = "target"
            anchor = target

        direction = steering_step(pos, anchor, target, mode)
        agents[i] = pos + dt * direction

        trajectories[i].append(agents[i].copy())

# --------------------------------------------------
# 8. Plot
# --------------------------------------------------

# background field
x = np.linspace(-2, 2, 120)
y = np.linspace(-2, 2, 120)
X, Y = np.meshgrid(x, y)

U = np.zeros_like(X)
V = np.zeros_like(Y)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        vec = flow_field(X[i, j], Y[i, j])
        U[i, j] = vec[0]
        V[i, j] = vec[1]

plt.figure(figsize=(10, 8))

plt.streamplot(X, Y, U, V, color="black", density=1)

# plot trajectories
for tr in trajectories:
    tr = np.array(tr)
    plt.plot(tr[:, 0], tr[:, 1], linewidth=2)

# plot final target
final_target = moving_target(steps * 0.1)
plt.scatter(final_target[0], final_target[1], color="blue", s=120, label="final target")

# plot starts
for tr in trajectories:
    plt.scatter(tr[0][0], tr[0][1], color="green", s=60)

plt.title("NEXAH Dynamic Multi-Agent Navigation")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()

out_path = os.path.join(OUT_DIR, "nexah_dynamic_multi_agent.png")
plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

print("""
🧠 Interpretation:

Multiple agents move through a changing field

→ gates shift over time
→ agents continuously adapt
→ trajectories reorganize dynamically

This is emergent collective navigation
""")
