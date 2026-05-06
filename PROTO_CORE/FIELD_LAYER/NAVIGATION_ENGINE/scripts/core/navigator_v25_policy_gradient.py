import numpy as np
import random
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

clusters = [0,1,2,3]
target = 2

# Q-table (state, action)
Q = defaultdict(lambda: 0.0)

actions = {
    0: [0,1,2],
    1: [0,2,3],
    2: [1,2],
    3: [0,1,3]
}

alpha = 0.2
gamma = 0.9
epsilon = 0.1  # exploration


def choose_action(state):
    if random.random() < epsilon:
        return random.choice(actions[state])
    else:
        qs = [(a, Q[(state,a)]) for a in actions[state]]
        return max(qs, key=lambda x: x[1])[0]


def reward(prev, new, instability, boundary):
    r = 0.0

    if new == target:
        r += 1.0
    if prev != target and new == target:
        r += 0.5

    if new == 3:
        r -= 1.0

    r -= 0.3 * instability
    r -= 0.3 * boundary

    return r


def simulate(steps=600):
    state = 0
    path = [state]

    inst_trace = []
    bound_trace = []

    for step in range(steps):

        action = choose_action(state)

        # stochastic environment (same as before)
        next_state = action

        instability = np.random.uniform(0.2,0.8)
        boundary = np.random.uniform(0.1,0.3)

        r = reward(state, next_state, instability, boundary)

        # Q-learning update
        future = max([Q[(next_state,a)] for a in actions[next_state]])
        Q[(state,action)] += alpha * (r + gamma * future - Q[(state,action)])

        state = next_state
        path.append(state)

        inst_trace.append(instability)
        bound_trace.append(boundary)

    return path, inst_trace, bound_trace


def plot(path, inst, bound):

    fig, axes = plt.subplots(2,2, figsize=(12,10))
    ax1,ax2,ax3,ax4 = axes.flatten()

    # Q1 trajectory
    ax1.plot(path)
    ax1.set_title("Q1 — Policy Gradient Trajectory")

    # Q2 signals
    ax2.plot(inst, label="instability")
    ax2.plot(bound, label="boundary")
    ax2.legend()
    ax2.set_title("Q2 — Signals")

    # Q3 counts
    counts = Counter(path)
    ax3.bar(counts.keys(), counts.values())
    ax3.set_title("Q3 — Visit Counts")

    # Q4 Q-table
    M = np.zeros((4,4))
    for (s,a),v in Q.items():
        M[s,a] = v

    im = ax4.imshow(M, cmap="magma")
    for i in range(4):
        for j in range(4):
            if M[i,j] != 0:
                ax4.text(j,i,f"{M[i,j]:.2f}",ha="center",va="center",color="white")

    ax4.set_title("Q4 — Learned Q-values")
    plt.colorbar(im, ax=ax4)

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "v25_policy_learning.png")
    plt.savefig(out, dpi=200)
    plt.close()

    print(f"Saved: {out}")


def main():
    print("Running V25 Policy Gradient Learning...")

    path, inst, bound = simulate()

    counts = Counter(path)
    print("\nVisit Counts:")
    for k in sorted(counts):
        print(f"C{k}: {counts[k]}")

    print("\nLearned Policy:")
    for s in clusters:
        best = max(actions[s], key=lambda a: Q[(s,a)])
        print(f"C{s} -> C{best}")

    plot(path, inst, bound)


if __name__ == "__main__":
    main()
