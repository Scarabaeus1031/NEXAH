# ============================================================
# NEXAH — Flow / Residue Alignment (Halvorsen)
# ============================================================
#
# Purpose:
# Compare Halvorsen gate / flow structure with modular residue
# structure (mod 7 and mod 17).
#
# Idea:
# For every transition i -> j:
# - measure flow strength
# - compute residue jump mod 7
# - compute residue jump mod 17
# - visualize whether strong gates align with residue structure
#
# Outputs:
# - flow_residue_alignment_*.txt
# - flow_residue_scatter_mod7_*.png
# - flow_residue_scatter_mod17_*.png
# - flow_residue_heatmap_mod7_*.png
# - flow_residue_heatmap_mod17_*.png
# - flow_residue_summary_*.png
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
        "gate_aware_policy_matrix_*.npy",
        "policy_gradient_matrix_*.npy",
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

    raise RuntimeError("No matrix found.")


# ============================================================
# RESIDUE TOOLS
# ============================================================

def residue_jump(i, j, mod):
    return (j - i) % mod


def circular_distance(i, j, mod):
    d = abs((j - i) % mod)
    return min(d, mod - d)


# ============================================================
# EXTRACT TRANSITIONS
# ============================================================

def extract_transitions(M, threshold=0.02):
    transitions = []

    n = M.shape[0]
    diag = np.diag(M)

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            p = M[i, j]

            if p >= threshold:
                stability = diag[i]
                rel = p / (stability + 1e-9)

                transitions.append({
                    "from": i,
                    "to": j,
                    "p": float(p),
                    "rel": float(rel),
                    "jump7": residue_jump(i, j, 7),
                    "jump17": residue_jump(i, j, 17),
                    "dist7": circular_distance(i, j, 7),
                    "dist17": circular_distance(i, j, 17),
                })

    return transitions


# ============================================================
# AGGREGATE HEATMAPS
# ============================================================

def residue_heatmap(transitions, mod):
    H = np.zeros((mod, mod))

    for t in transitions:
        a = t["from"] % mod
        b = t["to"] % mod
        H[a, b] += t["p"]

    return H


def jump_profile(transitions, mod):
    profile = np.zeros(mod)

    key = f"jump{mod}"

    for t in transitions:
        profile[t[key]] += t["p"]

    return profile


# ============================================================
# SAVE REPORT
# ============================================================

def save_report(transitions, source, timestamp, base):
    path = f"{base}/flow_residue_alignment_{timestamp}.txt"

    p_values = np.array([t["p"] for t in transitions])
    dist7 = np.array([t["dist7"] for t in transitions])
    dist17 = np.array([t["dist17"] for t in transitions])

    corr7 = np.corrcoef(p_values, dist7)[0, 1] if len(p_values) > 1 else np.nan
    corr17 = np.corrcoef(p_values, dist17)[0, 1] if len(p_values) > 1 else np.nan

    with open(path, "w") as f:
        f.write("NEXAH — Halvorsen Flow / Residue Alignment\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Source matrix: {source}\n\n")

        f.write("GLOBAL SUMMARY\n")
        f.write("-" * 70 + "\n")
        f.write(f"number of transitions: {len(transitions)}\n")
        f.write(f"mean transition strength: {p_values.mean():.6f}\n")
        f.write(f"max transition strength: {p_values.max():.6f}\n")
        f.write(f"corr(p, residue distance mod 7): {corr7:.6f}\n")
        f.write(f"corr(p, residue distance mod 17): {corr17:.6f}\n\n")

        f.write("TRANSITIONS\n")
        f.write("-" * 70 + "\n")
        for t in transitions:
            f.write(
                f"{t['from']} -> {t['to']} | "
                f"p={t['p']:.4f} | rel={t['rel']:.3f} | "
                f"jump7={t['jump7']} dist7={t['dist7']} | "
                f"jump17={t['jump17']} dist17={t['dist17']}\n"
            )

    print(f"[✓] Report saved: {path}")


# ============================================================
# VISUAL 1 — SCATTER MOD 7
# ============================================================

def plot_scatter(transitions, mod, timestamp, base):
    jumps = np.array([t[f"jump{mod}"] for t in transitions])
    dists = np.array([t[f"dist{mod}"] for t in transitions])
    p = np.array([t["p"] for t in transitions])
    rel = np.array([t["rel"] for t in transitions])

    fig, ax = plt.subplots(figsize=(8, 5))

    sc = ax.scatter(
        jumps,
        p,
        s=80 + 220 * rel,
        c=dists,
        alpha=0.8
    )

    ax.set_title(f"Flow / Residue Alignment — mod {mod}")
    ax.set_xlabel(f"residue jump mod {mod}")
    ax.set_ylabel("transition strength p")
    ax.grid(alpha=0.25)

    plt.colorbar(sc, label="circular residue distance")

    plt.tight_layout()
    path = f"{base}/flow_residue_scatter_mod{mod}_{timestamp}.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)

    print(f"[✓] Scatter mod {mod} saved: {path}")


# ============================================================
# VISUAL 2 — RESIDUE HEATMAP
# ============================================================

def plot_heatmap(transitions, mod, timestamp, base):
    H = residue_heatmap(transitions, mod)

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(H)

    ax.set_title(f"Residue Transition Heatmap — mod {mod}")
    ax.set_xlabel(f"to residue mod {mod}")
    ax.set_ylabel(f"from residue mod {mod}")

    plt.colorbar(im, label="summed transition strength")

    plt.tight_layout()
    path = f"{base}/flow_residue_heatmap_mod{mod}_{timestamp}.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)

    print(f"[✓] Heatmap mod {mod} saved: {path}")


# ============================================================
# VISUAL 3 — JUMP PROFILE
# ============================================================

def plot_jump_profile(transitions, mod, timestamp, base):
    profile = jump_profile(transitions, mod)

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(np.arange(mod), profile)
    ax.set_title(f"Residue Jump Profile — mod {mod}")
    ax.set_xlabel(f"jump mod {mod}")
    ax.set_ylabel("summed flow strength")
    ax.grid(axis="y", alpha=0.25)

    plt.tight_layout()
    path = f"{base}/flow_residue_jump_profile_mod{mod}_{timestamp}.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)

    print(f"[✓] Jump profile mod {mod} saved: {path}")


# ============================================================
# VISUAL 4 — SUMMARY PANEL
# ============================================================

def plot_summary(transitions, timestamp, base):
    H7 = residue_heatmap(transitions, 7)
    H17 = residue_heatmap(transitions, 17)

    profile7 = jump_profile(transitions, 7)
    profile17 = jump_profile(transitions, 17)

    p = np.array([t["p"] for t in transitions])
    dist7 = np.array([t["dist7"] for t in transitions])
    dist17 = np.array([t["dist17"] for t in transitions])

    fig, axes = plt.subplots(2, 3, figsize=(16, 9))

    im0 = axes[0, 0].imshow(H7)
    axes[0, 0].set_title("Residue Heatmap mod 7")
    plt.colorbar(im0, ax=axes[0, 0])

    im1 = axes[0, 1].imshow(H17)
    axes[0, 1].set_title("Residue Heatmap mod 17")
    plt.colorbar(im1, ax=axes[0, 1])

    axes[0, 2].scatter(dist7, p, label="mod 7", alpha=0.8)
    axes[0, 2].scatter(dist17, p, label="mod 17", alpha=0.8)
    axes[0, 2].set_title("Strength vs Residue Distance")
    axes[0, 2].set_xlabel("circular residue distance")
    axes[0, 2].set_ylabel("transition strength p")
    axes[0, 2].legend()
    axes[0, 2].grid(alpha=0.25)

    axes[1, 0].bar(np.arange(7), profile7)
    axes[1, 0].set_title("Jump Profile mod 7")
    axes[1, 0].set_xlabel("jump")

    axes[1, 1].bar(np.arange(17), profile17)
    axes[1, 1].set_title("Jump Profile mod 17")
    axes[1, 1].set_xlabel("jump")

    axes[1, 2].hist(p, bins=10)
    axes[1, 2].set_title("Transition Strength Distribution")
    axes[1, 2].set_xlabel("p")
    axes[1, 2].set_ylabel("count")

    plt.tight_layout()
    path = f"{base}/flow_residue_summary_{timestamp}.png"
    fig.savefig(path, dpi=300)
    plt.close(fig)

    print(f"[✓] Summary saved: {path}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    base = "APPLICATIONS/dynamical_systems/halvorsen/outputs"
    os.makedirs(base, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("→ load matrix")
    M, source = load_latest_matrix()

    print("→ extract transitions")
    transitions = extract_transitions(M, threshold=0.02)

    print(f"transitions found: {len(transitions)}")

    print("→ save report")
    save_report(transitions, source, timestamp, base)

    print("→ create visuals")
    plot_scatter(transitions, 7, timestamp, base)
    plot_scatter(transitions, 17, timestamp, base)

    plot_heatmap(transitions, 7, timestamp, base)
    plot_heatmap(transitions, 17, timestamp, base)

    plot_jump_profile(transitions, 7, timestamp, base)
    plot_jump_profile(transitions, 17, timestamp, base)

    plot_summary(transitions, timestamp, base)

    print("✔ DONE")
