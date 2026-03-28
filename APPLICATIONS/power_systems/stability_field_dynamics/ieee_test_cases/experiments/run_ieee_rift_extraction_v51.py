# run_ieee_rift_extraction_v51.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import griddata

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee9", "ieee14", "ieee30"]
GRID_RES = 120
EPS = 0.03  # tolerance for residual ~ 0

# --------------------------------------------------
# LOAD FIT PARAMETERS
# --------------------------------------------------

fit_df = pd.read_csv(BASE_PATH / "ieee_v43_manifold_fit.csv")

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def normalize_safe(x):
    x = np.asarray(x, dtype=float)
    m = np.max(np.abs(x))
    if m == 0:
        return x
    return x / m


def power_model(c, dc, a, p, q):
    return a * (np.abs(c) ** p) * (np.abs(dc) ** q)


def load_case_dataset(case):
    file_path = BASE_PATH / f"{case}_v43_dataset.csv"
    if not file_path.exists():
        print(f"Missing file: {file_path}")
        return None
    return pd.read_csv(file_path).dropna()


def prepare_data(df):
    c = normalize_safe(df["c"].values)
    dc = normalize_safe(df["dc"].values)
    d2c = normalize_safe(df["d2c"].values)
    return c, dc, d2c


def build_grid(c, dc, z, grid_res=120):
    xi = np.linspace(0, 1, grid_res)
    yi = np.linspace(0, 1, grid_res)
    X, Y = np.meshgrid(xi, yi)

    Z = griddata(
        (c, dc),
        z,
        (X, Y),
        method="linear",
        fill_value=np.nan
    )

    return X, Y, Z


# --------------------------------------------------
# RIFT EXTRACTION
# --------------------------------------------------

def extract_rift_points(X, Y, R, eps=0.03):
    """
    Approximate residual-zero boundary:
    points where |residual| < eps on valid grid.
    """
    valid = np.isfinite(R)
    mask = valid & (np.abs(R) < eps)

    xr = X[mask]
    yr = Y[mask]
    rr = R[mask]

    if len(xr) == 0:
        return np.array([]), np.array([]), np.array([])

    order = np.argsort(xr)
    return xr[order], yr[order], rr[order]


def estimate_boundary_summary(xr, yr):
    if len(xr) == 0:
        return {
            "rift_count": 0,
            "rift_c_min": np.nan,
            "rift_c_max": np.nan,
            "rift_dc_min": np.nan,
            "rift_dc_max": np.nan,
        }

    return {
        "rift_count": int(len(xr)),
        "rift_c_min": float(np.min(xr)),
        "rift_c_max": float(np.max(xr)),
        "rift_dc_min": float(np.min(yr)),
        "rift_dc_max": float(np.max(yr)),
    }


# --------------------------------------------------
# MAIN CASE PROCESSING
# --------------------------------------------------

def process_case(case):
    print(f"\n--- {case.upper()} ---")

    df = load_case_dataset(case)
    if df is None:
        return None

    c, dc, d2c = prepare_data(df)

    params = fit_df[fit_df["case"] == case].iloc[0]
    a, p, q = params["power_a"], params["power_p"], params["power_q"]

    d2c_model = power_model(c, dc, a, p, q)
    residual = d2c - d2c_model

    X, Y, R = build_grid(c, dc, residual, GRID_RES)

    xr, yr, rr = extract_rift_points(X, Y, R, eps=EPS)
    summary = estimate_boundary_summary(xr, yr)

    # --------------------------------------------------
    # 1) Residual heatmap + extracted rift
    # --------------------------------------------------

    plt.figure(figsize=(8, 6))
    im = plt.imshow(
        R,
        extent=[0, 1, 0, 1],
        origin="lower",
        aspect="auto"
    )
    plt.colorbar(im, label="Residual (true - model)")

    plt.scatter(
        c, dc,
        c=np.linspace(0, 1, len(c)),
        cmap="viridis",
        s=18,
        alpha=0.8,
        label="Trajectory"
    )

    if len(xr) > 0:
        plt.scatter(
            xr, yr,
            s=10,
            c="white",
            alpha=0.9,
            label="Rift (residual≈0)"
        )

    plt.xlabel("c (norm)")
    plt.ylabel("dc (norm)")
    plt.title(f"{case.upper()} — Rift Extraction / Collapse Boundary (V51)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v51_rift_boundary.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # 2) Residual cross-section along c
    # --------------------------------------------------

    plt.figure(figsize=(8, 5))
    plt.scatter(c, residual, c=residual, cmap="coolwarm", s=30)
    plt.axhline(0, linestyle="--", linewidth=1, label="Residual = 0")

    if len(xr) > 0:
        plt.scatter(
            xr,
            np.zeros_like(xr),
            s=10,
            c="black",
            label="Rift projection"
        )

    plt.xlabel("c (norm)")
    plt.ylabel("Residual")
    plt.title(f"{case.upper()} — Rift Projection in Residual Space (V51)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v51_rift_projection.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # 3) Boundary line only
    # --------------------------------------------------

    plt.figure(figsize=(8, 6))
    plt.scatter(
        c, dc,
        c=np.linspace(0, 1, len(c)),
        cmap="viridis",
        s=20,
        alpha=0.35,
        label="Trajectory"
    )

    if len(xr) > 0:
        plt.plot(xr, yr, linewidth=2, label="Extracted rift")
        plt.scatter(xr, yr, s=8)

    plt.xlabel("c (norm)")
    plt.ylabel("dc (norm)")
    plt.title(f"{case.upper()} — Collapse Boundary Geometry (V51)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v51_boundary_geometry.png", dpi=150)
    plt.close()

    out = {"case": case}
    out.update(summary)
    return out


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V51 — RIFT EXTRACTION + COLLAPSE BOUNDARY")

    rows = []

    for case in CASES:
        try:
            res = process_case(case)
            if res:
                rows.append(res)
        except Exception as e:
            print(f"[{case}] ERROR: {e}")

    df_out = pd.DataFrame(rows)

    print("\n--- V51 SUMMARY ---")
    print(df_out)

    out_file = BASE_PATH / "ieee_v51_rift_summary.csv"
    df_out.to_csv(out_file, index=False)
    print("\nSaved:", out_file)


if __name__ == "__main__":
    main()
