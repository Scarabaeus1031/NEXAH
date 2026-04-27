# ============================================================
# NEXAH — Policy Gradient (Halvorsen)
# ============================================================
#
# Purpose:
# Learn transition preferences over the adaptive Halvorsen
# transition system.
#
# Concept:
# - states = coarse clusters
# - actions = possible next clusters
# - reward = reaching target
# - policy learns which transitions improve navigation
#
# Input:
# - latest adaptive_matrix_*.npy
#   fallback: latest connected_matrix_*.npy
#   fallback: latest coarse_matrix_*.npy
#
# Output:
# - policy_gradient_*.txt
# - policy_gradient_*.png
#
# ============================================================

import os
import glob
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# LOAD MATRIX
# ============================================================

def load_latest_matrix():
    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"

    patterns = [
        "adaptive_matrix_*.npy",
        "connected_matrix_*.npy",
        "coarse_matrix_*.npy",
    ]

    for pattern in patterns:
        files = sorted(glob.glob(os.path.join(base, pattern)))
        if files:
            path = files[-1]
            print(f"→ loading matrix: {path}")
            return np.load(path), path

    raise RuntimeError("No matrix found. Run coarse / connect / adaptive bridge first.")


# ============================================================
# POLICY INITIALIZATION
# ============================================================

def initialize_policy(M, epsilon=1e-9):
    P = M.copy()
    P[P < epsilon] = 0.0

    for i in range(P.shape[0]):
        s = P[i].sum()
        if s > 0:
            P[i] /= s

    return P


# ============================================================
# SAMPLE EPISODE
# ============================================================

def sample_episode(policy, start, target, max_steps=50):
    state = start
    path = [state]
    log_probs = []
    rewards = []

    for _ in range(max_steps):
        probs = policy[state]

        if probs.sum() <= 0:
            rewards.append(-1.0)
            break

        action = np.random.choice(len(probs), p=probs)
        prob = probs[action]

        log_probs.append((state, action, prob))

        state = action
        path.append(state)

        if state == target:
            rewards.append(10.0)
            break
        else:
            rewards.append(-0.05)

    return path, log_probs, rewards


# ============================================================
# RETURNS
# ============================================================

def discounted_returns(rewards, gamma=0.95):
    G = 0.0
    returns = []

    for r in reversed(rewards):
        G = r + gamma * G
        returns.insert(0, G)

    returns = np.array(returns)

    if returns.std() > 1e-9:
        returns = (returns - returns.mean()) / returns.std()

    return returns


# ============================================================
# TRAIN POLICY
# ============================================================

def train_policy(M, target=15, episodes=3000, lr=0.03, gamma=0.95):
    policy = initialize_policy(M)
    n = policy.shape[0]

    success_count = 0
    history = []

    for ep in range(episodes):
        start = np.random.randint(0, n)

        path, log_probs, rewards = sample_episode(
            policy,
            start=start,
            target=target,
            max_steps=50
        )

        if path[-1] == target:
            success_count += 1

        returns = discounted_returns(rewards, gamma=gamma)

        for idx, (state, action, prob) in enumerate(log_probs):
            advantage = returns[idx]

            # reinforce selected action
            policy[state, action] += lr * advantage * prob

            # keep nonnegative
            policy[state] = np.clip(policy[state], 0.0, None)

            # preserve support from original matrix
            support = M[state] > 0
            policy[state, ~support] = 0.0

            # normalize row
            s = policy[state].sum()
            if s > 0:
                policy[state] /= s

        if (ep + 1) % 100 == 0:
            success_rate = success_count / 100
            history.append(success_rate)
            success_count = 0

    return policy, history


# ============================================================
# EXTRACT GREEDY POLICY
# ============================================================

def greedy_policy(policy):
    result = {}

    for i in range(policy.shape[0]):
        if policy[i].sum() <= 0:
            result[i] = None
        else:
            result[i] = int(np.argmax(policy[i]))

    return result


# ============================================================
# SAVE OUTPUTS
# ============================================================

def save_outputs(policy, greedy, history, source_matrix, target):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base, exist_ok=True)

    txt_path = f"{base}/policy_gradient_{timestamp}.txt"
    with open(txt_path, "w") as f:
        f.write("NEXAH — Halvorsen Policy Gradient\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Source matrix: {source_matrix}\n")
        f.write(f"Target cluster: {target}\n\n")

        f.write("GREEDY POLICY\n")
        f.write("-" * 60 + "\n")
        for state, action in greedy.items():
            f.write(f"{state} -> {action}\n")

        f.write("\nSUCCESS HISTORY\n")
        f.write("-" * 60 + "\n")
        for i, value in enumerate(history):
            f.write(f"{i * 100:05d}: {value:.4f}\n")

    png_matrix = f"{base}/policy_gradient_matrix_{timestamp}.png"
    plt.figure(figsize=(6, 5))
    plt.imshow(policy)
    plt.colorbar()
    plt.title("Learned Policy Matrix")
    plt.xlabel("action / next cluster")
    plt.ylabel("state / current cluster")
    plt.tight_layout()
    plt.savefig(png_matrix, dpi=300)
    plt.close()

    png_history = f"{base}/policy_gradient_success_{timestamp}.png"
    plt.figure(figsize=(7, 4))
    plt.plot(np.arange(len(history)) * 100, history)
    plt.title("Policy Gradient Success Rate")
    plt.xlabel("episode")
    plt.ylabel("success rate per 100 episodes")
    plt.tight_layout()
    plt.savefig(png_history, dpi=300)
    plt.close()

    npy_path = f"{base}/policy_gradient_matrix_{timestamp}.npy"
    np.save(npy_path, policy)

    print(f"[✓] TXT saved: {txt_path}")
    print(f"[✓] Policy PNG saved: {png_matrix}")
    print(f"[✓] Success PNG saved: {png_history}")
    print(f"[✓] NPY saved: {npy_path}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    np.random.seed(42)

    print("→ load matrix")
    M, source_matrix = load_latest_matrix()

    target = 15

    print("→ train policy gradient")
    policy, history = train_policy(
        M,
        target=target,
        episodes=3000,
        lr=0.03,
        gamma=0.95
    )

    print("→ extract greedy policy")
    greedy = greedy_policy(policy)

    for k in sorted(greedy):
        print(f"{k} -> {greedy[k]}")

    print("→ save")
    save_outputs(policy, greedy, history, source_matrix, target)

    print("✔ DONE")
