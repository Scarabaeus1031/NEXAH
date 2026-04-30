# ============================================================
# NEXAH v6.7 — Symbolic Dynamics
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


# ------------------------------------------------------------
# Dummy trajectory (replace later)
# ------------------------------------------------------------
def generate_dummy_traj(n=5000):
    traj = []

    for t in range(n):
        v = 0.7 + 0.2 * np.sin(t * 0.03)
        dv = 0.05 * np.cos(t * 0.03)

        # structured switching
        mode = (t // 350) % 4

        energy = dv**2
        traj.append((v, dv, mode, energy))

    return traj


# ------------------------------------------------------------
# Extract mode sequence
# ------------------------------------------------------------
def extract_mode_sequence(traj):
    return np.array([int(p[2]) for p in traj])


# ------------------------------------------------------------
# Transition matrix (Markov)
# ------------------------------------------------------------
def compute_transition_matrix(mode_seq, n_modes=4):
    M = np.zeros((n_modes, n_modes))

    for i in range(len(mode_seq) - 1):
        a = mode_seq[i]
        b = mode_seq[i + 1]
        M[a, b] += 1

    # normalize rows
    for i in range(n_modes):
        if np.sum(M[i]) > 0:
            M[i] /= np.sum(M[i])

    return M


# ------------------------------------------------------------
# N-gram analysis
# ------------------------------------------------------------
def compute_ngrams(mode_seq, n=3):
    ngrams = []

    for i in range(len(mode_seq) - n + 1):
        ngrams.append(tuple(mode_seq[i:i+n]))

    counter = Counter(ngrams)
    return counter


# ------------------------------------------------------------
# Entropy
# ------------------------------------------------------------
def compute_entropy(mode_seq):
    counts = np.bincount(mode_seq)
    probs = counts / np.sum(counts)

    probs = probs[probs > 0]
    entropy = -np.sum(probs * np.log2(probs))

    return entropy


# ------------------------------------------------------------
# Plot transition matrix
# ------------------------------------------------------------
def plot_transition_matrix(M):
    plt.figure(figsize=(5, 4))
    plt.imshow(M)
    plt.colorbar(label="probability")

    plt.title("Transition Matrix")
    plt.xlabel("to state")
    plt.ylabel("from state")

    plt.xticks(range(4))
    plt.yticks(range(4))

    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Print top patterns
# ------------------------------------------------------------
def print_top_patterns(counter, top_k=10):
    print("\n=== Top Patterns ===")

    for seq, count in counter.most_common(top_k):
        print(f"{seq} → {count}")


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":

    traj = generate_dummy_traj()

    print("Trajectory size:", len(traj))

    # --------------------------------------------------------
    # 1. Mode sequence
    # --------------------------------------------------------
    mode_seq = extract_mode_sequence(traj)

    print("\nMode sequence sample:")
    print(mode_seq[:30])

    # --------------------------------------------------------
    # 2. Transition matrix
    # --------------------------------------------------------
    M = compute_transition_matrix(mode_seq)

    print("\n=== Transition Matrix ===")
    print(M)

    plot_transition_matrix(M)

    # --------------------------------------------------------
    # 3. N-grams
    # --------------------------------------------------------
    ngram_counter = compute_ngrams(mode_seq, n=3)

    print_top_patterns(ngram_counter)

    # --------------------------------------------------------
    # 4. Entropy
    # --------------------------------------------------------
    H = compute_entropy(mode_seq)

    print("\n=== Entropy ===")
    print(f"Entropy: {H:.4f} bits")
