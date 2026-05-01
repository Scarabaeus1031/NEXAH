import numpy as np
import matplotlib.pyplot as plt

from run_cross_system_transition_comparison import run

def matrix_distance(A, B):
    return np.mean(np.abs(A - B))


def main():

    matrices = run()

    names = list(matrices.keys())
    n = len(names)

    D = np.zeros((n,n))

    for i in range(n):
        for j in range(n):
            D[i,j] = matrix_distance(
                matrices[names[i]],
                matrices[names[j]]
            )

    print("\n=== CROSS-SYSTEM DISTANCE MATRIX ===")
    for i in range(n):
        for j in range(n):
            print(f"{names[i]} vs {names[j]}: {D[i,j]:.4f}")

    # Heatmap
    plt.imshow(D, cmap="viridis")
    plt.xticks(range(n), names)
    plt.yticks(range(n), names)
    plt.colorbar(label="distance")
    plt.title("Cross-System Transition Distance")
    plt.savefig("RESEARCH/validation/cross_system_distance_matrix.png")
    plt.close()

    print("✅ Saved: cross_system_distance_matrix.png")


if __name__ == "__main__":
    main()
