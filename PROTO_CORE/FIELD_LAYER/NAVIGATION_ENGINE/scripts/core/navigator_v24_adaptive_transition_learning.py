import numpy as np
import random
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "FIELD_LAYER/outputs/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

clusters = [0,1,2,3]
target = 2

# Initial matrix (start neutral-ish)
W = {
    (0,0):5,(0,1):5,(0,2):5,
    (1,0):5,(1,2):5,(1,3):5,
    (2,1):5,(2,2):5,
    (3,0):5,(3,1):5,(3,3):5
}

def normalize(W):
    prob = {}
    adj = defaultdict(list)
    for (s,d),w in W.items():
        adj[s].append((d,w))
    for s,edges in adj.items():
        total = sum(w for _,w in edges)
        prob[s] = [(d,w/total) for d,w in edges]
    return prob

def sample(prob_adj, current):
    dsts = [d for d,_ in prob_adj[current]]
    probs = [p for _,p in prob_adj[current]]
    return random.choices(dsts, weights=probs)[0]

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

def simulate(steps=500, lr=0.15):
    global W

    current = 0
    path = [current]

    instability_trace = []
    boundary_trace = []

    for step in range(steps):

        prob_adj = normalize(W)
        nxt = sample(prob_adj, current)

        # fake observer signals (simple proxy)
        instability = np.random.uniform(0.2,0.8)
        boundary = np.random.uniform(0.1,0.3)

        r = reward(current, nxt, instability, boundary)

        # update weight
        W[(current,nxt)] = max(0.1, W.get((current,nxt),0.1) + lr*r)

        # slight decay on others (stability pressure)
        for (s,d) in list(W.keys()):
            if s == current and d != nxt:
                W[(s,d)] *= 0.995

        current = nxt
        path.append(current)

        instability_trace.append(instability)
        boundary_trace.append(boundary)

    return path, instability_trace, boundary_trace


def plot(path, inst, bound):

    fig, axes = plt.subplots(2,2, figsize=(12,10))
    ax1,ax2,ax3,ax4 = axes.flatten()

    # Q1 trajectory
    ax1.plot(path)
    ax1.set_title("Q1 — Adaptive Trajectory")

    # Q2 signals
    ax2.plot(inst, label="instability")
    ax2.plot(bound, label="boundary")
    ax2.legend()
    ax2.set_title("Q2 — Observer Signals")

    # Q3 counts
    counts = Counter(path)
    ax3.bar(counts.keys(), counts.values())
    ax3.set_title("Q3 — Visit Counts")

    # Q4 learned matrix
    M = np.zeros((4,4))
    for (s,d),w in W.items():
        M[s,d] = w

    im = ax4.imshow(M, cmap="magma")
    for i in range(4):
        for j in range(4):
            if M[i,j] > 0:
                ax4.text(j,i,f"{M[i,j]:.1f}",ha="center",va="center",color="white")

    ax4.set_title("Q4 — Learned Transition Matrix")
    plt.colorbar(im, ax=ax4)

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "v24_adaptive_learning.png")
    plt.savefig(out, dpi=200)
    plt.close()

    print(f"Saved: {out}")


def main():
    print("Running V24 Adaptive Transition Learning...")

    path, inst, bound = simulate()

    counts = Counter(path)
    print("\nVisit Counts:")
    for k in sorted(counts):
        print(f"C{k}: {counts[k]}")

    print("\nLearned Weights:")
    for k,v in sorted(W.items()):
        print(f"{k}: {v:.2f}")

    plot(path, inst, bound)


if __name__ == "__main__":
    main()
