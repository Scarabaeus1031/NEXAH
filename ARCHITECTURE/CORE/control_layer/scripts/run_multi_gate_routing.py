import os
import numpy as np
import matplotlib.pyplot as plt

print("⚡ NEXAH Multi-Gate Routing")

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

    score = alignment * np.exp(-0.3 * b)
    return score

# --------------------------------------------------
# 3. Find Multiple Gates
# --------------------------------------------------

def find_candidate_gates(target, top_percent=99):
    xs = np.linspace(-2, 2, 180)
    ys = np.linspace(-2, 2, 180)

    X, Y = np.meshgrid(xs, ys)
    S = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            S[i, j] = gate_score(X[i, j], Y[i, j], target)

    threshold = np.percentile(S, top_percent)
    mask = S >= threshold

    candidates = np.column_stack([X[mask], Y[mask], S[mask]])
    return X, Y, S, candidates

def prune_gates(candidates, min_dist=0.18, max_keep=6):
    # greedy non-maximum-style selection
    if len(candidates) == 0:
        return np.empty((0, 3))

    # sort by score descending
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
# 4. Steering Law
# --------------------------------------------------

def steering_step(pos, anchor, mode="gate"):
    x, y = pos

    flow = unit(flow_field(x, y))
    to_anchor = unit(anchor - pos)

    b = boundary_field(x, y)
    boundary_push = -0.05 * b * np.array([x, y])

    if mode == "gate":
        w_flow = 0.65
        w_anchor = 0.45
    else:
        w_flow = 0.45
        w_anchor = 0.75

    direction = w_flow * flow + w_anchor * to_anchor + boundary_push
    return unit(direction)

# --------------------------------------------------
# 5. Simulate via One Gate
# --------------------------------------------------

def simulate_via_gate(start, gate, target, step_size=0.035, max_steps=800):
    pos = start.copy()
    traj = [pos.copy()]
    reached_gate = False
    gate_radius = 0.12
    target_radius = 0.10

    total_length = 0.0
    total_boundary_cost = 0.0

    for _ in range(max_steps):
        if not reached_gate:
            direction = steering_step(pos, gate, mode="gate")
            if np.linalg.norm(pos - gate) < gate_radius:
                reached_gate = True
        else:
            direction = steering_step(pos, target, mode="target")
            if np.linalg.norm(pos - target) < target_radius:
                break

        new_pos = pos + step_size * direction
        total_length += np.linalg.norm(new_pos - pos)
        total_boundary_cost += boundary_field(pos[0], pos[1])

        pos = new_pos
        traj.append(pos.copy())

    traj = np.array(traj)
    final_dist = np.linalg.norm(pos - target)

    return {
        "trajectory": traj,
        "final_dist": final_dist,
        "path_length": total_length,
        "boundary_cost": total_boundary_cost / max(1, len(traj)),
        "gate": gate
    }

# --------------------------------------------------
# 6. Routing: choose best gate
# --------------------------------------------------

start = np.array([-1.5, 0.5])
target = np.array([1.5, 0.5])

X, Y, S, raw_candidates = find_candidate_gates(target, top_percent=99)
gates = prune_gates(raw_candidates, min_dist=0.18, max_keep=6)

results = []
for g in gates:
    gate_xy = g[:2]
    sim = simulate_via_gate(start, gate_xy, target)
    sim["gate_score"] = g[2]
    # combined routing score: prefer reaching target, shorter path, lower boundary cost
    sim["routing_score"] = (
        - 3.0 * sim["final_dist"]
        - 0.15 * sim["path_length"]
        - 0.5 * sim["boundary_cost"]
        + 1.5 * sim["gate_score"]
    )
    results.append(sim)

best = max(results, key=lambda r: r["routing_score"]) if results else None

# --------------------------------------------------
# 7. Plot
# --------------------------------------------------

plt.figure(figsize=(10, 8))

plt.contourf(X, Y, S, levels=30, alpha=0.55)

U = np.zeros_like(X)
V = np.zeros_like(Y)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        vec = flow_field(X[i, j], Y[i, j])
        U[i, j] = vec[0]
        V[i, j] = vec[1]

plt.streamplot(X, Y, U, V, color="black", density=1)

# all candidate gates
if len(gates) > 0:
    plt.scatter(gates[:, 0], gates[:, 1], color="magenta", s=80, label="candidate gates")

# plot all trajectories lightly
for r in results:
    tr = r["trajectory"]
    plt.plot(tr[:, 0], tr[:, 1], color="gray", alpha=0.35, linewidth=1)

# best route
if best is not None:
    tr = best["trajectory"]
    gate = best["gate"]
    plt.plot(tr[:, 0], tr[:, 1], color="red", linewidth=2.5, label="best route")
    plt.scatter(gate[0], gate[1], color="yellow", edgecolor="black", s=140, label="selected gate")

plt.scatter(start[0], start[1], color="green", s=120, label="start")
plt.scatter(target[0], target[1], color="blue", s=120, label="target")

plt.title("NEXAH Multi-Gate Routing")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()

out_path = os.path.join(OUT_DIR, "nexah_multi_gate_routing.png")
plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

if best is not None:
    print("\n🧠 Best Route Summary:\n")
    print(f"Selected gate      : {best['gate']}")
    print(f"Gate score         : {best['gate_score']:.4f}")
    print(f"Final target dist  : {best['final_dist']:.4f}")
    print(f"Path length        : {best['path_length']:.4f}")
    print(f"Boundary cost      : {best['boundary_cost']:.4f}")
    print(f"Routing score      : {best['routing_score']:.4f}")
    print("\nInterpretation:")
    print("→ multiple valid gates exist")
    print("→ NEXAH can compare them")
    print("→ best route is selected by structure + cost")
else:
    print("No valid gates found.")
