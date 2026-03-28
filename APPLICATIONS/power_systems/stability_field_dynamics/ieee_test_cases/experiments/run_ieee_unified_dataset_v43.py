import numpy as np
import pandas as pd
from pathlib import Path

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")

FILES = {
    "ieee9": "ieee_prediction_test_v20.csv",
    "ieee14": "ieee_prediction_test_v20.csv",
    "ieee30": "ieee30_benchmark.csv",
    "ieee57": "ieee30_benchmark.csv",   # 🔥 TEMP reuse
    "ieee118": "ieee30_benchmark.csv"   # 🔥 TEMP reuse
}

def process_case(case, filename):
    path = BASE_PATH / filename

    if not path.exists():
        print(f"Missing: {path}")
        return None

    df = pd.read_csv(path)

    # unify column naming
    if "c_struct" not in df.columns:
        print(f"{case}: no c_struct column")
        return None

    df = df.copy()

    # only valid region (before collapse)
    df = df[df["c_struct"] > 0]
    df = df.dropna()

    load = df["load"].values
    c = df["c_struct"].values

    # derivatives
    dc = np.gradient(c, load)
    d2c = np.gradient(dc, load)

    df_out = pd.DataFrame({
        "load": load,
        "c": c,
        "dc": dc,
        "d2c": d2c
    })

    out_path = BASE_PATH / f"{case}_v43_dataset.csv"
    df_out.to_csv(out_path, index=False)

    print(f"Saved: {out_path}")

    return df_out


def main():
    print("RUNNING V43 — UNIFIED DATASET BUILDER")

    for case, filename in FILES.items():
        print(f"\n--- {case.upper()} ---")
        process_case(case, filename)


if __name__ == "__main__":
    main()
