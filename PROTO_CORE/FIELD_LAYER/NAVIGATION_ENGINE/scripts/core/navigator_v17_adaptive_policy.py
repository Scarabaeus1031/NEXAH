import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import random

print("Running V17 Adaptive Policy...\n")

# ---- Setup ----

clusters = ["C0", "C1", "C2", "C3"]
target = "C2"

# Base transition probabilities (aus V14)
P = {
    "C0": {"C0":0.286, "C1":0.333, "C2":0.381},
    "C1": {"C0":0.417, "C2":0.333, "C3":0.250},
    "C2": {"C1":1.000},
    "C3": {"C0":0.682, "C3":0.318}
}

# Base energy (aus V14)
E = {
    ("C0","C0"):1.98, ("C0","C1"):1.64, ("C0","C2"):0.97,
    ("C1","C0"):2.35, ("C1","C2"):1.10, ("C1","C3"):3.20,
    ("C2","C1"):2.72,
    ("C3","C0"):1.11, ("C3","C3"):1.94
}

# Memory
memory = defaultdict(lambda: {"success":1, "fail":1})

# Parameters
penalty_weight = 2.0
steps = 200
adapt_interval = 20

# ---- Helpers ----

def adaptive_cost(i, j):
    base = E[(i,j)]
    m = memory[(i,j)]
    fail_rate = m["fail"] / (m["fail"] + m["success"])
    return base + penalty_weight * fail_rate

def compute_policy():
    # simple greedy: best outgoing edge per node
    policy = {}
    for c in clusters:
        if c not in P:
            continue
        best = None
        best_cost = np.inf
        for j in P[c]:
            if (c,j) not in E:
                continue
            cost = adaptive_cost(c, j)
            if cost < best_cost:
                best_cost = cost
                best = j
        policy[c] = best
    return policy

def sample_transition(c):
    probs = P[c]
    keys = list(probs.keys())
    vals = list(probs.values())
    return random.choices(keys, weights=vals)[0]

# ---- Simulation ----

current = "C0"
trajectory = [current]
policy = compute_policy()

visit_counts = defaultdict(int)

for t in range(steps):

    visit_counts[current] += 1

    # Policy action
    if current in policy:
        action = policy[current]
    else:
        action = sample_transition(current)

    # Stochastic outcome
    next_state = sample_transition(current)

    # success if policy matched actual transition
    if next_state == action:
        memory[(current, action)]["success"] += 1
    else:
        memory[(current, action)]["fail"] += 1

    current = next_state
    trajectory.append(current)

    # adapt policy
    if t % adapt_interval == 0:
        policy = compute_policy()

# ---- Results ----

print("Final Policy:")
for k,v in policy.items():
    print(f"  {k} -> {v}")

print("\nVisit Counts:")
for c in clusters:
    print(f"  {c}: {visit_counts[c]}")

# ---- Plot ----

mapping = {c:i for i,c in enumerate(clusters)}
traj_numeric = [mapping[c] for c in trajectory]

plt.figure(figsize=(10,4))
plt.plot(traj_numeric, linewidth=1)
plt.yticks(range(len(clusters)), clusters)
plt.title("V17 Adaptive Policy Trajectory")
plt.xlabel("step")
plt.ylabel("cluster")
plt.grid(True)

plt.savefig("FIELD_LAYER/outputs/plots/v17_adaptive_policy.png")
plt.show()

print("\nSaved: FIELD_LAYER/outputs/plots/v17_adaptive_policy.png")
