import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee30", "ieee57", "ieee118"]

N_OFFSETS = 15   # kleiner → stabiler + schneller
OFFSET_SCALE_C = 0.08
OFFSET_SCALE_DC = 0.08
EPS = 1e-8

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


def compute_curvature(dc, d2c):
    kappa = np.abs(d2c) / np.power(1.0 + dc**2, 1.5)
    return np.nan_to_num(kappa)


def classify_zone(curv, q1, q2):
    if curv <= q1:
        return 0   # core
    elif curv <= q2:
        return 1   # transition
    else:
        return 2   # expansion


# --------------------------------------------------
# OFF-MANIFOLD SAMPLING
# --------------------------------------------------

def build_off_manifold_cloud(c, dc, d2c):

    points = []

    c_scale = np.max(np.abs(c)) if np.max(np.abs(c)) > 0 else 1.0
    dc_scale = np.max(np.abs(dc)) if np.max(np.abs(dc)) > 0 else 1.0

    offsets = np.linspace(-1.0, 1.0, N_OFFSETS)

    for i in range(len(c)):
        for oc in offsets:
            for odc in offsets:

                c_new = c[i] + oc * OFFSET_SCALE_C * c_scale
                dc_new = dc[i] + odc * OFFSET_SCALE_DC * dc_scale
                d2c_new = d2c[i]

                points.append((c_new, dc_new, d2c_new))

    return pd.DataFrame(points, columns=["c", "dc", "d2c"])


# --------------------------------------------------
# MAIN PER CASE
# --------------------------------------------------

def process_case(case):

    print(f"\n--- {case.upper()} ---")

    df = load_dataset(case)
    if df is None:
        return

    # normalize
    c = normalize_safe(df["c"].values)
    dc = normalize_safe(df["dc"].values)
    d2c = normalize_safe(df["d2c"].values)

    # --------------------------------------------------
    # 1) Build OFF-MANIFOLD FIELD
    # --------------------------------------------------

    cloud = build_off_manifold_cloud(c, dc, d2c)

    # curvature
    cloud["curvature"] = compute_curvature(cloud["dc"].values, cloud["d2c"].values)

    # quantiles → adaptive zones
    q1 = np.quantile(cloud["curvature"], 0.33)
    q2 = np.quantile(cloud["curvature"], 0.66)

    cloud["zone"] = [classify_zone(k, q1, q2) for k in cloud["curvature"]]

    # --------------------------------------------------
    # SAVE DATA
    # --------------------------------------------------

    out_csv = BASE_PATH / f"{case}_v68_off_manifold_cloud.csv"
    cloud.to_csv(out_csv, index=False)
    print("Saved:", out_csv)

    # --------------------------------------------------
    # 2) VISUAL — FIELD EXPANSION
    # --------------------------------------------------

    plt.figure(figsize=(8,6))

    colors = {0: "green", 1: "orange", 2: "red"}

    for z in [0,1,2]:
        mask = cloud["zone"] == z
        plt.scatter(
            cloud.loc[mask, "c"],
            cloud.loc[mask, "dc"],
            s=8,
            alpha=0.5,
            color=colors[z],
            label=["core","transition","expansion"][z]
        )

    # original trajectory
    plt.plot(c, dc, color="black", linewidth=1.5, label="trajectory")

    plt.title(f"{case.upper()} — OFF-MANIFOLD FIELD (V68)")
    plt.xlabel("c")
    plt.ylabel("dc")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    out_img = BASE_PATH / f"{case}_v68_off_manifold_field.png"
    plt.savefig(out_img, dpi=150)
    plt.close()

    print("Saved:", out_img)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V68 — OFF-MANIFOLD FIELD")

    for case in CASES:
        process_case(case)


if __name__ == "__main__":
    main()
