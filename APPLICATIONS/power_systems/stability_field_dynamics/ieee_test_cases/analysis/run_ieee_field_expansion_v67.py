import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee30", "ieee57", "ieee118"]

EPS = 1e-6

# --------------------------------------------------
# LOAD
# --------------------------------------------------

def load_dataset(case):
    path = BASE_PATH / f"{case}_v43_dataset.csv"
    if not path.exists():
        print(f"Missing: {path}")
        return None
    return pd.read_csv(path).dropna()

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def normalize_safe(x):
    x = np.asarray(x, dtype=float)
    m = np.max(np.abs(x))
    if m == 0:
        return x
    return x / m


def compute_curvature(c, dc, d2c, eps=1e-6):
    """
    Curvature-like expansion dimension.
    This opens the manifold into a field.
    """
    return d2c / (np.abs(dc) + eps)


# --------------------------------------------------
# MAIN PER CASE
# --------------------------------------------------

def process_case(case):
    print(f"\n--- {case.upper()} ---")

    df = load_dataset(case)
    if df is None:
        return

    c = normalize_safe(df["c"].values)
    dc = normalize_safe(df["dc"].values)
    d2c = normalize_safe(df["d2c"].values)

    curvature = compute_curvature(c, dc, d2c, eps=EPS)
    curvature = normalize_safe(curvature)

    # --------------------------------------------------
    # 1) FIELD EXPANSION MAP (color = curvature)
    # --------------------------------------------------

    plt.figure(figsize=(8, 6))
    sc = plt.scatter(c, dc, c=curvature, cmap="coolwarm", s=40)
    plt.colorbar(sc, label="curvature")
    plt.xlabel("c")
    plt.ylabel("dc")
    plt.title(f"{case.upper()} — FIELD EXPANSION (V67)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v67_field_expansion.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # 2) TRUE 3D STRUCTURE (projection)
    # --------------------------------------------------

    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(c, dc, curvature, c=curvature, cmap="coolwarm", s=30)

    ax.set_xlabel("c")
    ax.set_ylabel("dc")
    ax.set_zlabel("curvature")

    ax.set_title(f"{case.upper()} — 3D FIELD (V67)")
    plt.tight_layout()

    plt.savefig(BASE_PATH / f"{case}_v67_3d_field.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # 3) CURVATURE VS DISTANCE STRUCTURE
    # --------------------------------------------------

    distance = np.sqrt(c**2 + dc**2)

    plt.figure(figsize=(8, 5))
    plt.scatter(distance, curvature, c=curvature, cmap="coolwarm", s=35)
    plt.xlabel("distance (approx)")
    plt.ylabel("curvature")
    plt.title(f"{case.upper()} — Curvature Structure (V67)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v67_curvature_structure.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # SAVE DATA
    # --------------------------------------------------

    df_out = pd.DataFrame({
        "c": c,
        "dc": dc,
        "d2c": d2c,
        "curvature": curvature
    })

    df_out.to_csv(BASE_PATH / f"{case}_v67_field_data.csv", index=False)
    print(f"Saved: {case}_v67_field_data.csv")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V67 — FIELD EXPANSION")

    for case in CASES:
        process_case(case)


if __name__ == "__main__":
    main()
