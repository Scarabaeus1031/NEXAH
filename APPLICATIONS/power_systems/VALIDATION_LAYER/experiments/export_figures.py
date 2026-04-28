# APPLICATIONS/power_systems/VALIDATION_LAYER/experiments/export_figures.py

import os
import shutil
from pathlib import Path


# ============================================================
# FIND PROJECT ROOT (VALIDATION_LAYER)
# ============================================================

BASE_DIR = Path(__file__).resolve()

while BASE_DIR.name != "VALIDATION_LAYER":
    BASE_DIR = BASE_DIR.parent

OUTPUT_DIR = BASE_DIR / "outputs"
FIGURE_DIR = BASE_DIR / "figures"


# ============================================================
# CONFIG
# ============================================================

FIGURE_MAP = {
    "overlay.png": "fig_01_overlay.png",
    "shape_space.png": "fig_02_shape_space.png",
    "clusters.png": "fig_03_clusters.png",
    "trajectory.png": "fig_04_trajectory.png",
    "motion_metrics.png": "fig_05_motion_metrics.png",
    "ieee_flow.png": "fig_06_ieee_flow.png",
}


# ============================================================
# HELPERS
# ============================================================

def get_latest_run():
    if not OUTPUT_DIR.exists():
        print(f"❌ Output directory not found: {OUTPUT_DIR}")
        return None

    runs = [
        d for d in OUTPUT_DIR.iterdir()
        if d.is_dir() and d.name.startswith("run_")
    ]

    if not runs:
        print("❌ No run folders found")
        return None

    runs_sorted = sorted(runs, key=lambda x: x.name, reverse=True)

    return runs_sorted[0]


def ensure_figure_dir():
    FIGURE_DIR.mkdir(exist_ok=True)


# ============================================================
# EXPORT
# ============================================================

def export_from_run(run_path):
    print(f"\n📦 Exporting from: {run_path.name}")

    ensure_figure_dir()

    exported = 0

    for src_name, dst_name in FIGURE_MAP.items():
        src_file = run_path / src_name

        if src_file.exists():
            dst_file = FIGURE_DIR / dst_name
            shutil.copy(src_file, dst_file)
            print(f"  ✔ {src_name} → {dst_name}")
            exported += 1
        else:
            print(f"  ⚠ missing: {src_name}")

    print(f"\n✅ Exported {exported} figures")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print(f"📁 Base dir: {BASE_DIR}")
    print(f"📁 Output dir: {OUTPUT_DIR}")
    print(f"📁 Figure dir: {FIGURE_DIR}")

    latest_run = get_latest_run()

    if latest_run:
        export_from_run(latest_run)
