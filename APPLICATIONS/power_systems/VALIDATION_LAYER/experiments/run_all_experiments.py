import os
import sys
import json
import runpy
import datetime
import traceback
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ============================================================
# ROOT
# ============================================================

def find_validation_root():
    path = Path(__file__).resolve()
    while path.name != "VALIDATION_LAYER":
        path = path.parent
    return path


ROOT = find_validation_root()
EXPERIMENTS_DIR = ROOT / "experiments"
OUTPUTS_DIR = ROOT / "outputs"


# ============================================================
# CONFIG
# ============================================================

EXPERIMENTS = [
    "run_001_shape_validation.py",
    "run_002_shape_geometry.py",
    "run_003_shape_dynamics.py",
    "run_004_pre_collapse_dynamics.py",
    "run_005_motion_instability_metric.py",
    "run_006_continuous_shape_flow.py",
    "run_007_statistical_validation.py",
    "run_008_ieee_bridge.py",
    "run_009_ieee_collapse_sweep.py",
]


# ============================================================
# OUTPUT
# ============================================================

def create_pipeline_dir():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = OUTPUTS_DIR / f"pipeline_{timestamp}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def make_experiment_dir(pipeline_dir, script_name):
    name = script_name.replace(".py", "")
    path = pipeline_dir / name
    path.mkdir(parents=True, exist_ok=True)
    return path


# ============================================================
# AUTO FIGURE CAPTURE
# ============================================================

class FigureCapture:
    def __init__(self, out_dir):
        self.out_dir = Path(out_dir)
        self.counter = 1
        self.original_show = plt.show

    def save_all_open_figures(self):
        fig_nums = plt.get_fignums()

        for fig_num in fig_nums:
            fig = plt.figure(fig_num)
            filename = f"figure_{self.counter:02d}.png"
            path = self.out_dir / filename
            fig.savefig(path, dpi=200, bbox_inches="tight")
            print(f"[saved figure] {path}")
            self.counter += 1

        plt.close("all")

    def patched_show(self, *args, **kwargs):
        self.save_all_open_figures()

    def __enter__(self):
        plt.show = self.patched_show
        return self

    def __exit__(self, exc_type, exc, tb):
        self.save_all_open_figures()
        plt.show = self.original_show


# ============================================================
# RUNNER
# ============================================================

def run_experiment(script_path, out_dir):
    status = {
        "script": script_path.name,
        "status": "success",
        "error": None,
        "figures_saved": 0,
    }

    stdout_path = out_dir / "stdout.txt"
    stderr_path = out_dir / "stderr.txt"

    old_cwd = os.getcwd()
    os.chdir(ROOT)

    try:
        with open(stdout_path, "w") as stdout_file, open(stderr_path, "w") as stderr_file:
            with redirect_stdout(stdout_file), redirect_stderr(stderr_file):
                with FigureCapture(out_dir) as capture:
                    runpy.run_path(str(script_path), run_name="__main__")
                    status["figures_saved"] = capture.counter - 1

    except Exception:
        status["status"] = "failed"
        status["error"] = traceback.format_exc()

        with open(stderr_path, "a") as f:
            f.write("\n\n=== PIPELINE ERROR ===\n")
            f.write(status["error"])

    finally:
        os.chdir(old_cwd)

    with open(out_dir / "meta.json", "w") as f:
        json.dump(status, f, indent=2)

    return status


# ============================================================
# MAIN
# ============================================================

def main():
    pipeline_dir = create_pipeline_dir()

    print(f"\n=== NEXAH VALIDATION PIPELINE ===")
    print(f"Output: {pipeline_dir}\n")

    summary = []

    for script_name in EXPERIMENTS:
        script_path = EXPERIMENTS_DIR / script_name
        out_dir = make_experiment_dir(pipeline_dir, script_name)

        print(f"Running: {script_name}")

        if not script_path.exists():
            status = {
                "script": script_name,
                "status": "missing",
                "error": "script not found",
                "figures_saved": 0,
            }
            with open(out_dir / "meta.json", "w") as f:
                json.dump(status, f, indent=2)
            summary.append(status)
            print("  missing")
            continue

        status = run_experiment(script_path, out_dir)
        summary.append(status)

        print(f"  status: {status['status']}")
        print(f"  figures: {status['figures_saved']}")

    with open(pipeline_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\n=== PIPELINE DONE ===")
    print(f"Saved to: {pipeline_dir}")


if __name__ == "__main__":
    main()
