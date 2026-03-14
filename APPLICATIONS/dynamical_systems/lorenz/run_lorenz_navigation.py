"""
NEXAH Chaos Navigator
Lorenz Reference System
"""

import argparse
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).parent


PIPELINE = [

    "analysis/lorenz_ftle_map.py",
    "analysis/lorenz_switch_map.py",
    "analysis/lorenz_symbolic_dynamics.py",
    "regimes/lorenz_regime_map.py",
]


def run_script(script):

    path = BASE_DIR / script

    print("Running:", script)
    subprocess.run(["python", str(path)], check=True)


def run_all():

    print("Running full Lorenz navigation pipeline...\n")

    for step in PIPELINE:
        run_script(step)

    print("\nPipeline complete.")


def run_single(name):

    for step in PIPELINE:
        if name in step:
            run_script(step)
            return

    print("Module not found:", name)


def list_modules():

    print("\nAvailable modules:\n")

    for step in PIPELINE:
        print(" ", Path(step).stem)

    print()


def main():

    parser = argparse.ArgumentParser(
        description="NEXAH Chaos Navigator"
    )

    parser.add_argument("--mode", choices=["all", "run", "list"], default="all")
    parser.add_argument("--module", help="module name")

    args = parser.parse_args()

    print("\n=== NEXAH Chaos Navigator ===")
    print("Lorenz Reference System\n")

    if args.mode == "all":
        run_all()

    elif args.mode == "list":
        list_modules()

    elif args.mode == "run":

        if args.module is None:
            print("Please specify --module")
        else:
            run_single(args.module)


if __name__ == "__main__":
    main()
