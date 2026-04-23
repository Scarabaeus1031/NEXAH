import os
import numpy as np
import matplotlib.pyplot as plt

print("⚡ NEXAH Gate Steering")

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
    # larger away from center -> more unstable / costly
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

    # reward alignment, penalize boundary
    score = alignment * np.exp(-0.3 * b)
    return score

# --------------------------------------------------
# 3. Find Best Gate
# --------------------------------------------------

def find_best_gate(target):
    xs = np.linspace(-2, 2, 140)
    ys = np.linspace(-2, 2, 140)

    best_score = -1e9
    best_gate = None

    for x in xs:
        for y in ys:
            s = gate_score(x, y, target)
            if s > best_score:
                best_score = s
                best_gate = np.array([x, y])

    return best_gate, best_score

# --------------------------------------------------
# 4. Steering Law
# --------------------------------------------------

def steering_step(pos, anchor, mode="gate"):
    x, y = pos

    flow = unit(flow_field(x, y))
    to_anchor = unit(anchor - pos)

    b = boundary_field(x, y)
    boundary_push = -0.05 * b * np.array([x, y])

    if mode == "gate":
        # more tolerant: use flow more
        w_flow = 0.65
        w_anchor = 0.45
    else:
        # after gate: stronger pull to target
        w_flow = 0.45
        w_anchor = 0.75

    direction = w_flow * flow + w_anchor * to_anchor + boundary_push
    return unit(direction)

# --------------------------------------------------
# 5. Simulation
# --------------------------------------------------

start = np.array([-1.5, 0.5])
target = np.array([1.5, 0.5])

gate, gscore = find_best_gate(target)

trajectory = [start.copy()]
phase_labels = []

pos = start.copy()
step_size = 0.035

reached_gate = False
gate_radius = 0.12
target_radius = 0.10

for _ in range(800):
    if not reached_gate:
        direction = steering_step(pos, gate, mode="gate")
        phase_labels.append(0)

        if np.linalg.norm(pos - gate) < gate_radius:
            reached_gate = True
    else:
        direction = steering_step(pos, target, mode="target")
        phase_labels.append(1)

        if np.linalg.norm(pos - target) < target_radius:
            break

    pos = pos + step_size * direction
    trajectory.append(pos.copy())

trajectory = np.array(trajectory)
phase_labels = np.array(phase_labels)

# --------------------------------------------------
# 6. Background Field for Plot
# --------------------------------------------------

x = np.linspace(-2, 2, 120)
y = np.linspace(-2, 2, 120)
X, Y = np.meshgrid(x, y)

U = np.zeros_like(X)
V = np.zeros_like(Y)
S = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        vec = flow_field(X[i, j], Y[i, j])
        U[i, j] = vec[0]
        V[i, j] = vec[1]
        S[i, j] = gate_score(X[i, j], Y[i, j], target)

# --------------------------------------------------
# 7. Plot
# --------------------------------------------------

plt.figure(figsize=(9, 8))

plt.contourf(X, Y, S, levels=30, alpha=0.55)
plt.streamplot(X, Y, U, V, color="black", density=1)

# trajectory split by phase
if len(trajectory) > 1:
    split_idx = np.where(phase_labels == 1)[0]
    if len(split_idx) > 0:
        k = split_idx[0]
        plt.plot(trajectory[:k+1, 0], trajectory[:k+1, 1],
                 color="red", linewidth=2, label="to gate")
        plt.plot(trajectory[k:, 0], trajectory[k:, 1],
                 color="orange", linewidth=2, label="to target")
    else:
        plt.plot(trajectory[:, 0], trajectory[:, 1],
                 color="red", linewidth=2, label="to gate")
else:
    plt.plot(trajectory[:, 0], trajectory[:, 1],
             color="red", linewidth=2)

# markers
plt.scatter(start[0], start[1], color="green", s=120, label="start")
plt.scatter(target[0], target[1], color="blue", s=120, label="target")
plt.scatter(gate[0], gate[1], color="magenta", s=120, label="gate")

plt.title("NEXAH Gate Steering")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()

out_path = os.path.join(OUT_DIR, "nexah_gate_steering.png")
plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")
print(f"✔ Best gate: {gate}, score={gscore:.4f}")

print("""
🧠 Interpretation:

Red path    = steering toward gate
Orange path = steering from gate to target
Magenta     = detected gate

→ control first aligns with a valid entry region
→ then approaches the target through the field
→ reduces unstable direct approaches
""")
