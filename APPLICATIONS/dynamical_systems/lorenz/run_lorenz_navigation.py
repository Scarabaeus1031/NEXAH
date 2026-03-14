"""
NEXAH Chaos Navigator
Lorenz Reference System
"""

import argparse
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).parent
OUTPUT_DIR = Path("../../outputs/lorenz_navigation")


def run_script(script_path):
    print("Running:", script_path)
    subprocess.run(["python", str(script_path)], check=True)


def run_all():

    print("Running full Lorenz navigation pipeline...")
    print("Outputs:", OUTPUT_DIR)
    print()

    run_script(BASE_DIR / "analysis/lorenz_ftle_map.py")
    run_script(BASE_DIR / "regimes/lorenz_regime_map.py")


def run_ftle():

    run_script(BASE_DIR / "analysis/lorenz_ftle_map.py")


def run_regime():

    run_script(BASE_DIR / "regimes/lorenz_regime_map.py")


def main():

    parser = argparse.ArgumentParser(
        description="NEXAH Chaos Navigator (Lorenz)"
    )

    parser.add_argument(
        "--mode",
        choices=["all", "ftle", "regime"],
        default="all"
    )

    args = parser.parse_args()

    print()
    print("=== NEXAH Chaos Navigator ===")
    print("Lorenz Reference System")
    print()

    if args.mode == "all":
        run_all()

    elif args.mode == "ftle":
        run_ftle()

    elif args.mode == "regime":
        run_regime()

    print()
    print("Done.")


if __name__ == "__main__":
    main()
